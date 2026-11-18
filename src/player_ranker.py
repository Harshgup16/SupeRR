"""
player_ranker.py — Clutch Factor ranking engine for cricket batters and bowlers.

Compares each player's performance in high-pressure (DPI > 0.6) vs normal
(DPI ≤ 0.6) situations.  Players who *elevate* their game under pressure
rank highest.

Expects a ball-by-ball DataFrame already enriched with:
    - pressure_index  (float 0–1, from pressure_model.py)
    - pressure_category (str, from pressure_model.py)
    - All columns produced by data_loader.py (runs, is_four, is_six,
      is_wicket, extras_type, extras1_runs, striker_id, striker_name,
      bowler_id, bowler_name, etc.)
"""

from __future__ import annotations

import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
PRESSURE_THRESHOLD = 0.6          # DPI above this → "pressure"
MIN_PRESSURE_BALLS_BAT = 100      # Minimum pressure balls faced (batting)
MIN_TOTAL_BALLS_BAT = 200         # Minimum total balls faced (batting)
MIN_PRESSURE_BALLS_BOWL = 100     # Minimum pressure balls bowled
MIN_TOTAL_BALLS_BOWL = 200        # Minimum total balls bowled
BOWLING_SR_CAP = 300              # Cap bowling SR when 0 wickets taken
BOWLING_AVG_CAP = 200             # Cap batting avg when 0 dismissals
SHRINKAGE_K = 50                  # Prior strength for Bayesian shrinkage

# Extras that do NOT count as a legal delivery for the batter
_BATTER_ILLEGAL_EXTRAS = {"wide", "Overstep"}


# ═══════════════════════════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════════════════════════

def _is_legal_delivery(extras_type: pd.Series) -> pd.Series:
    """True when the delivery counts as a ball faced by the batter."""
    return ~extras_type.isin(_BATTER_ILLEGAL_EXTRAS)


def _is_dot_ball(row_runs: pd.Series, extras_type: pd.Series,
                 extras1_runs: pd.Series) -> pd.Series:
    """
    A dot ball: 0 runs scored by the batter AND no extras on a legal delivery.
    """
    legal = _is_legal_delivery(extras_type)
    no_runs = row_runs == 0
    no_extras = extras1_runs == 0
    return legal & no_runs & no_extras


def _safe_divide(numerator, denominator, fill=0.0):
    """Element-wise division with zero-safe fill."""
    if isinstance(numerator, (pd.Series, pd.DataFrame)):
        return numerator.div(denominator).replace([np.inf, -np.inf], fill).fillna(fill)
    if denominator == 0:
        return fill
    return numerator / denominator


# ═══════════════════════════════════════════════════════════════════════════
# 1. Batting Metrics
# ═══════════════════════════════════════════════════════════════════════════

def _compute_batting_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate batting metrics per (striker_id, striker_name, is_pressure).

    Returns one row per batter per condition with:
        balls_faced, total_runs, dismissals, fours, sixes,
        strike_rate, batting_avg, boundary_pct, dot_ball_pct, runs_per_ball
    """
    # Mark pressure and legal deliveries
    df = df.copy()
    df["is_pressure"] = df["pressure_index"] > PRESSURE_THRESHOLD
    df["_legal"] = _is_legal_delivery(df["extras_type"].fillna(""))
    df["_dot"] = _is_dot_ball(df["runs"], df["extras_type"].fillna(""),
                              df["extras1_runs"].fillna(0))

    # Keep only legal deliveries for batter metrics
    legal = df[df["_legal"]].copy()

    agg = legal.groupby(["striker_id", "striker_name", "is_pressure"]).agg(
        balls_faced=("runs", "size"),
        total_runs=("runs", "sum"),
        dismissals=("is_wicket", "sum"),
        fours=("is_four", "sum"),
        sixes=("is_six", "sum"),
        dot_balls=("_dot", "sum"),
    ).reset_index()

    # Derived metrics
    agg["strike_rate"] = _safe_divide(agg["total_runs"], agg["balls_faced"]) * 100
    agg["batting_avg"] = _safe_divide(
        agg["total_runs"],
        agg["dismissals"].replace(0, np.nan)
    ).fillna(BOWLING_AVG_CAP)
    agg["boundary_pct"] = _safe_divide(
        agg["fours"] + agg["sixes"], agg["balls_faced"]
    )
    agg["dot_ball_pct"] = _safe_divide(agg["dot_balls"], agg["balls_faced"])
    agg["runs_per_ball"] = _safe_divide(agg["total_runs"], agg["balls_faced"])

    return agg


# ═══════════════════════════════════════════════════════════════════════════
# 2. Bowling Metrics
# ═══════════════════════════════════════════════════════════════════════════

def _compute_bowling_metrics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate bowling metrics per (bowler_id, bowler_name, is_pressure).

    Runs conceded INCLUDE extras.  Legal deliveries only for ball counts
    (wides/no-balls don't count as legal balls bowled, but their runs do
    count against the bowler).
    """
    df = df.copy()
    df["is_pressure"] = df["pressure_index"] > PRESSURE_THRESHOLD
    df["_legal"] = _is_legal_delivery(df["extras_type"].fillna(""))
    # Total runs conceded on this delivery (batter runs + extras)
    df["_runs_conceded"] = df["runs"] + df["extras1_runs"].fillna(0).astype(int)
    df["_dot_bowl"] = (df["_runs_conceded"] == 0) & df["_legal"]

    # We aggregate on ALL deliveries for runs conceded, but balls bowled
    # counts only legal deliveries.
    agg_all = df.groupby(["bowler_id", "bowler_name", "is_pressure"]).agg(
        total_runs_conceded=("_runs_conceded", "sum"),
        total_wickets=("is_wicket", "sum"),
        fours_conceded=("is_four", "sum"),
        sixes_conceded=("is_six", "sum"),
    ).reset_index()

    legal = df[df["_legal"]]
    agg_legal = legal.groupby(["bowler_id", "bowler_name", "is_pressure"]).agg(
        balls_bowled=("runs", "size"),
        dot_balls=("_dot_bowl", "sum"),
    ).reset_index()

    agg = agg_all.merge(agg_legal, on=["bowler_id", "bowler_name", "is_pressure"],
                        how="left")
    agg["balls_bowled"] = agg["balls_bowled"].fillna(0).astype(int)
    agg["dot_balls"] = agg["dot_balls"].fillna(0).astype(int)

    # Derived metrics
    agg["economy_rate"] = _safe_divide(
        agg["total_runs_conceded"], agg["balls_bowled"]
    ) * 6
    # Bowling strike rate: lower is better; cap when 0 wickets
    agg["bowling_strike_rate"] = _safe_divide(
        agg["balls_bowled"],
        agg["total_wickets"].replace(0, np.nan)
    ).fillna(BOWLING_SR_CAP)
    agg["dot_ball_pct"] = _safe_divide(agg["dot_balls"], agg["balls_bowled"])
    agg["boundaries_conceded_pct"] = _safe_divide(
        agg["fours_conceded"] + agg["sixes_conceded"], agg["balls_bowled"]
    )
    agg["wickets_per_over"] = _safe_divide(
        agg["total_wickets"], agg["balls_bowled"]
    ) * 6

    return agg


# ═══════════════════════════════════════════════════════════════════════════
# 3 & 4. Clutch Factor + Confidence Weighting
# ═══════════════════════════════════════════════════════════════════════════

def _pivot_conditions(agg: pd.DataFrame, id_col: str, name_col: str,
                      balls_col: str) -> pd.DataFrame:
    """Pivot is_pressure (True/False) into pressure_ / baseline_ columns."""
    pressure = agg[agg["is_pressure"]].copy()
    baseline = agg[~agg["is_pressure"]].copy()

    pressure = pressure.rename(
        columns={c: f"pressure_{c}" for c in agg.columns
                 if c not in [id_col, name_col, "is_pressure"]}
    ).drop(columns=["is_pressure"])

    baseline = baseline.rename(
        columns={c: f"baseline_{c}" for c in agg.columns
                 if c not in [id_col, name_col, "is_pressure"]}
    ).drop(columns=["is_pressure"])

    merged = pressure.merge(baseline, on=[id_col, name_col], how="inner")
    return merged


def compute_batting_clutch(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full pipeline: aggregate batting metrics → compute clutch factor →
    apply confidence weighting → filter by minimum thresholds → sort.

    Returns DataFrame sorted by weighted_clutch descending.
    """
    agg = _compute_batting_metrics(df)
    pivoted = _pivot_conditions(agg, "striker_id", "striker_name", "balls_faced")

    # --- Minimum-threshold filter ---
    pivoted = pivoted[
        (pivoted["pressure_balls_faced"] >= MIN_PRESSURE_BALLS_BAT)
        & ((pivoted["pressure_balls_faced"] + pivoted["baseline_balls_faced"])
           >= MIN_TOTAL_BALLS_BAT)
    ].copy()

    if pivoted.empty:
        return pivoted

    # --- Clutch factor ---
    sr_ratio = _safe_divide(pivoted["pressure_strike_rate"],
                            pivoted["baseline_strike_rate"], fill=1.0)
    avg_ratio = _safe_divide(pivoted["pressure_batting_avg"],
                             pivoted["baseline_batting_avg"], fill=1.0)
    if isinstance(avg_ratio, (pd.Series, pd.DataFrame)):
        avg_ratio = avg_ratio.clip(upper=2.5)
    bnd_ratio = _safe_divide(pivoted["pressure_boundary_pct"],
                             pivoted["baseline_boundary_pct"], fill=1.0)
    if isinstance(bnd_ratio, (pd.Series, pd.DataFrame)):
        bnd_ratio = bnd_ratio.clip(upper=2.5)
    # Scoring Efficiency (Non-dot ball percentage improvement)
    pressure_scoring = 1.0 - pivoted["pressure_dot_ball_pct"]
    baseline_scoring = 1.0 - pivoted["baseline_dot_ball_pct"]
    scoring_ratio = _safe_divide(pressure_scoring, baseline_scoring, fill=1.0)
    if isinstance(scoring_ratio, (pd.Series, pd.DataFrame)):
        scoring_ratio = scoring_ratio.clip(upper=2.0)

    pivoted["clutch_factor"] = (
        0.35 * sr_ratio
        + 0.25 * avg_ratio
        + 0.20 * bnd_ratio
        + 0.20 * scoring_ratio
    )

    # --- Bayesian Shrinkage Confidence Weight ---
    # Shrinks estimate toward neutral baseline (1.0) for smaller samples
    conf = pivoted["pressure_balls_faced"] / (pivoted["pressure_balls_faced"] + SHRINKAGE_K)
    pivoted["confidence"] = conf
    pivoted["weighted_clutch"] = 1.0 + (pivoted["clutch_factor"] - 1.0) * conf

    return pivoted.sort_values("weighted_clutch", ascending=False).reset_index(drop=True)


def compute_bowling_clutch(df: pd.DataFrame) -> pd.DataFrame:
    """
    Full pipeline: aggregate bowling metrics → compute clutch factor →
    apply confidence weighting → filter by minimum thresholds → sort.

    Returns DataFrame sorted by weighted_clutch descending.
    """
    agg = _compute_bowling_metrics(df)
    pivoted = _pivot_conditions(agg, "bowler_id", "bowler_name", "balls_bowled")

    # --- Minimum-threshold filter ---
    pivoted = pivoted[
        (pivoted["pressure_balls_bowled"] >= MIN_PRESSURE_BALLS_BOWL)
        & ((pivoted["pressure_balls_bowled"] + pivoted["baseline_balls_bowled"])
           >= MIN_TOTAL_BALLS_BOWL)
    ].copy()

    if pivoted.empty:
        return pivoted

    # --- Clutch factor ---
    econ_ratio = _safe_divide(pivoted["baseline_economy_rate"],
                              pivoted["pressure_economy_rate"], fill=1.0)
    if isinstance(econ_ratio, (pd.Series, pd.DataFrame)):
        econ_ratio = econ_ratio.clip(upper=2.5)
    sr_ratio = _safe_divide(pivoted["baseline_bowling_strike_rate"],
                            pivoted["pressure_bowling_strike_rate"], fill=1.0)
    if isinstance(sr_ratio, (pd.Series, pd.DataFrame)):
        sr_ratio = sr_ratio.clip(upper=2.5)
    dot_ratio = _safe_divide(pivoted["pressure_dot_ball_pct"],
                             pivoted["baseline_dot_ball_pct"], fill=1.0)
    if isinstance(dot_ratio, (pd.Series, pd.DataFrame)):
        dot_ratio = dot_ratio.clip(upper=2.5)
    # Non-boundary suppression ratio
    pressure_non_bnd = 1.0 - pivoted["pressure_boundaries_conceded_pct"]
    baseline_non_bnd = 1.0 - pivoted["baseline_boundaries_conceded_pct"]
    bnd_suppression = _safe_divide(pressure_non_bnd, baseline_non_bnd, fill=1.0)
    if isinstance(bnd_suppression, (pd.Series, pd.DataFrame)):
        bnd_suppression = bnd_suppression.clip(upper=2.0)

    pivoted["clutch_factor"] = (
        0.30 * econ_ratio
        + 0.25 * sr_ratio
        + 0.25 * dot_ratio
        + 0.20 * bnd_suppression
    )

    # --- Bayesian Shrinkage Confidence Weight ---
    conf = pivoted["pressure_balls_bowled"] / (pivoted["pressure_balls_bowled"] + SHRINKAGE_K)
    pivoted["confidence"] = conf
    pivoted["weighted_clutch"] = 1.0 + (pivoted["clutch_factor"] - 1.0) * conf

    return pivoted.sort_values("weighted_clutch", ascending=False).reset_index(drop=True)


# ═══════════════════════════════════════════════════════════════════════════
# 5. Output / Query Functions
# ═══════════════════════════════════════════════════════════════════════════

def get_top_batters(enriched_df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Return the top-*n* clutch batters.

    Parameters
    ----------
    enriched_df : pd.DataFrame
        Ball-by-ball data with pressure_index column.
    n : int
        Number of top batters to return.

    Returns
    -------
    pd.DataFrame with columns:
        rank, player_id, player_name, weighted_clutch, clutch_factor,
        confidence, pressure_strike_rate, baseline_strike_rate,
        pressure_batting_avg, baseline_batting_avg, pressure_boundary_pct,
        baseline_boundary_pct, pressure_dot_ball_pct, baseline_dot_ball_pct,
        pressure_balls_faced, baseline_balls_faced
    """
    result = compute_batting_clutch(enriched_df).head(n).copy()
    if result.empty:
        return result
    result.insert(0, "rank", range(1, len(result) + 1))
    result = result.rename(columns={
        "striker_id": "player_id",
        "striker_name": "player_name",
    })
    # Add convenient aliases for runners and visualizations
    result["pressure_sr"] = result["pressure_strike_rate"]
    result["baseline_sr"] = result["baseline_strike_rate"]
    result["pressure_balls"] = result["pressure_balls_faced"]
    display_cols = [
        "rank", "player_id", "player_name",
        "weighted_clutch", "clutch_factor", "confidence",
        "pressure_strike_rate", "baseline_strike_rate",
        "pressure_batting_avg", "baseline_batting_avg",
        "pressure_boundary_pct", "baseline_boundary_pct",
        "pressure_dot_ball_pct", "baseline_dot_ball_pct",
        "pressure_balls_faced", "baseline_balls_faced",
        "pressure_sr", "baseline_sr", "pressure_balls",
    ]
    return result[[c for c in display_cols if c in result.columns]]


def get_top_bowlers(enriched_df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    """
    Return the top-*n* clutch bowlers.

    Parameters
    ----------
    enriched_df : pd.DataFrame
        Ball-by-ball data with pressure_index column.
    n : int
        Number of top bowlers to return.

    Returns
    -------
    pd.DataFrame with columns:
        rank, player_id, player_name, weighted_clutch, clutch_factor,
        confidence, pressure_economy_rate, baseline_economy_rate,
        pressure_bowling_strike_rate, baseline_bowling_strike_rate,
        pressure_dot_ball_pct, baseline_dot_ball_pct,
        pressure_boundaries_conceded_pct, baseline_boundaries_conceded_pct,
        pressure_balls_bowled, baseline_balls_bowled
    """
    result = compute_bowling_clutch(enriched_df).head(n).copy()
    if result.empty:
        return result
    result.insert(0, "rank", range(1, len(result) + 1))
    result = result.rename(columns={
        "bowler_id": "player_id",
        "bowler_name": "player_name",
    })
    # Add convenient aliases for runners and visualizations
    result["pressure_economy"] = result["pressure_economy_rate"]
    result["baseline_economy"] = result["baseline_economy_rate"]
    result["pressure_balls"] = result["pressure_balls_bowled"]
    display_cols = [
        "rank", "player_id", "player_name",
        "weighted_clutch", "clutch_factor", "confidence",
        "pressure_economy_rate", "baseline_economy_rate",
        "pressure_bowling_strike_rate", "baseline_bowling_strike_rate",
        "pressure_dot_ball_pct", "baseline_dot_ball_pct",
        "pressure_boundaries_conceded_pct", "baseline_boundaries_conceded_pct",
        "pressure_balls_bowled", "baseline_balls_bowled",
        "pressure_economy", "baseline_economy", "pressure_balls",
    ]
    return result[[c for c in display_cols if c in result.columns]]


def get_player_profile(enriched_df: pd.DataFrame, player_id: int) -> dict:
    """
    Detailed pressure vs baseline breakdown for a single player (batting
    AND bowling if applicable).

    Parameters
    ----------
    enriched_df : pd.DataFrame
        Ball-by-ball data with pressure_index column.
    player_id : int
        The player's ID (matches striker_id or bowler_id).

    Returns
    -------
    dict with keys:
        - "player_id"
        - "player_name"
        - "batting" : dict or None  — pressure/baseline batting metrics + clutch
        - "bowling" : dict or None  — pressure/baseline bowling metrics + clutch
    """
    profile: dict = {"player_id": player_id, "player_name": None,
                     "batting": None, "bowling": None}

    # --- Batting ---
    bat_df = enriched_df[enriched_df["striker_id"] == player_id]
    if not bat_df.empty:
        profile["player_name"] = bat_df["striker_name"].iloc[0]
        bat_agg = _compute_batting_metrics(bat_df)
        bat_detail = {}
        for _, row in bat_agg.iterrows():
            label = "pressure" if row["is_pressure"] else "baseline"
            bat_detail[label] = {
                "balls_faced": int(row["balls_faced"]),
                "total_runs": int(row["total_runs"]),
                "dismissals": int(row["dismissals"]),
                "strike_rate": round(row["strike_rate"], 2),
                "batting_avg": round(row["batting_avg"], 2),
                "boundary_pct": round(row["boundary_pct"], 4),
                "dot_ball_pct": round(row["dot_ball_pct"], 4),
                "runs_per_ball": round(row["runs_per_ball"], 4),
            }
        # Compute clutch if both conditions exist
        if "pressure" in bat_detail and "baseline" in bat_detail:
            p, b = bat_detail["pressure"], bat_detail["baseline"]
            sr_r = _safe_divide(p["strike_rate"], b["strike_rate"], 1.0)
            avg_r = min(2.5, _safe_divide(p["batting_avg"], b["batting_avg"], 1.0))
            bnd_r = min(2.5, _safe_divide(p["boundary_pct"], b["boundary_pct"], 1.0))
            score_r = min(2.0, _safe_divide(1.0 - p["dot_ball_pct"], 1.0 - b["dot_ball_pct"], 1.0))
            clutch = 0.35 * sr_r + 0.25 * avg_r + 0.20 * bnd_r + 0.20 * score_r
            pressure_balls = p["balls_faced"]
            conf = pressure_balls / (pressure_balls + SHRINKAGE_K)
            bat_detail["clutch_factor"] = round(clutch, 4)
            bat_detail["confidence"] = round(conf, 4)
            bat_detail["weighted_clutch"] = round(1.0 + (clutch - 1.0) * conf, 4)
        profile["batting"] = bat_detail

    # --- Bowling ---
    bowl_df = enriched_df[enriched_df["bowler_id"] == player_id]
    if not bowl_df.empty:
        if profile["player_name"] is None:
            profile["player_name"] = bowl_df["bowler_name"].iloc[0]
        bowl_agg = _compute_bowling_metrics(bowl_df)
        bowl_detail = {}
        for _, row in bowl_agg.iterrows():
            label = "pressure" if row["is_pressure"] else "baseline"
            bowl_detail[label] = {
                "balls_bowled": int(row["balls_bowled"]),
                "total_runs_conceded": int(row["total_runs_conceded"]),
                "wickets": int(row["total_wickets"]),
                "economy_rate": round(row["economy_rate"], 2),
                "bowling_strike_rate": round(row["bowling_strike_rate"], 2),
                "dot_ball_pct": round(row["dot_ball_pct"], 4),
                "boundaries_conceded_pct": round(row["boundaries_conceded_pct"], 4),
                "wickets_per_over": round(row["wickets_per_over"], 4),
            }
        if "pressure" in bowl_detail and "baseline" in bowl_detail:
            p, b = bowl_detail["pressure"], bowl_detail["baseline"]
            econ_r = min(2.5, _safe_divide(b["economy_rate"], p["economy_rate"], 1.0))
            sr_r = min(2.5, _safe_divide(b["bowling_strike_rate"], p["bowling_strike_rate"], 1.0))
            dot_r = min(2.5, _safe_divide(p["dot_ball_pct"], b["dot_ball_pct"], 1.0))
            non_bnd_r = min(2.0, _safe_divide(1.0 - p["boundaries_conceded_pct"], 1.0 - b["boundaries_conceded_pct"], 1.0))
            clutch = 0.30 * econ_r + 0.25 * sr_r + 0.25 * dot_r + 0.20 * non_bnd_r
            pressure_balls = p["balls_bowled"]
            conf = pressure_balls / (pressure_balls + SHRINKAGE_K)
            bowl_detail["clutch_factor"] = round(clutch, 4)
            bowl_detail["confidence"] = round(conf, 4)
            bowl_detail["weighted_clutch"] = round(1.0 + (clutch - 1.0) * conf, 4)
        profile["bowling"] = bowl_detail

    return profile


# ═══════════════════════════════════════════════════════════════════════════
# Quick smoke-test when run directly
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Minimal synthetic test to verify formulas run without error
    np.random.seed(42)
    n = 2000
    test_df = pd.DataFrame({
        "striker_id": np.random.choice([1, 2, 3, 4, 5], n),
        "striker_name": "",
        "bowler_id": np.random.choice([10, 20, 30, 40, 50], n),
        "bowler_name": "",
        "runs": np.random.choice([0, 1, 2, 4, 6], n, p=[0.4, 0.3, 0.1, 0.12, 0.08]),
        "is_four": False,
        "is_six": False,
        "is_wicket": np.random.choice([True, False], n, p=[0.05, 0.95]),
        "extras_type": np.random.choice(["", "wide", "Overstep"], n, p=[0.9, 0.07, 0.03]),
        "extras1_runs": 0,
        "pressure_index": np.random.uniform(0, 1, n),
    })
    test_df.loc[test_df["runs"] == 4, "is_four"] = True
    test_df.loc[test_df["runs"] == 6, "is_six"] = True
    test_df["striker_name"] = test_df["striker_id"].map(
        {1: "A", 2: "B", 3: "C", 4: "D", 5: "E"})
    test_df["bowler_name"] = test_df["bowler_id"].map(
        {10: "X", 20: "Y", 30: "Z", 40: "W", 50: "V"})
    test_df.loc[test_df["extras_type"].isin(["wide", "Overstep"]), "extras1_runs"] = 1

    print("=== Top Clutch Batters ===")
    print(get_top_batters(test_df, n=5).to_string(index=False))
    print()
    print("=== Top Clutch Bowlers ===")
    print(get_top_bowlers(test_df, n=5).to_string(index=False))
    print()
    print("=== Player Profile (ID=1) ===")
    import json
    print(json.dumps(get_player_profile(test_df, 1), indent=2))
