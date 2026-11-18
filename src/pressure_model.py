"""
pressure_model.py — Dynamic Pressure Index (DPI) for T20 Cricket
=================================================================

Core algorithm for the SupeRR Selector hackathon.

Pressure is defined by how close a match is to a 50/50 outcome.
When one team is cruising, pressure is low.  When the match hangs
on a knife-edge, pressure is at its peak.

Exports
-------
- build_chase_win_prob_lookup(df, matches_df)  → lookup dict
- build_par_score_table(df)                    → par-score dict
- calc_chase_win_prob(...)                     → float  (0–1)
- calc_first_innings_pressure(...)             → float  (0–1)
- calculate_dpi(enriched_df)                   → DataFrame with
      pressure_index (float 0–1) and pressure_category columns
"""

from __future__ import annotations

import sys, os
import numpy as np
import pandas as pd

# ---------------------------------------------------------------------------
# Ensure the src directory is importable so `from data_loader import …` works
# when this module is executed or imported from the project root.
# ---------------------------------------------------------------------------
_SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if _SRC_DIR not in sys.path:
    sys.path.insert(0, _SRC_DIR)

from data_loader import load_enriched_data  # noqa: E402

# ===================================================================
# 1. SECOND INNINGS — Chase Win-Probability Lookup
# ===================================================================

def _bucket_balls(balls_remaining: int) -> int:
    """Round balls_remaining into coarser buckets for the lookup table.

    Buckets: 0-6, 7-12, 13-18, … up to 114-120.
    Returns the lower bound of each 6-ball (1-over) bucket.
    """
    return max(0, (balls_remaining // 6) * 6)


def _bucket_rpb(runs_per_ball: float) -> float:
    """Bucket the required runs-per-ball into 0.25-width bins.

    Caps at 3.0 (essentially impossible to chase above ~36 an over).
    """
    if runs_per_ball < 0:
        return 0.0
    rpb = min(runs_per_ball, 3.0)
    return round(round(rpb / 0.25) * 0.25, 2)


def build_chase_win_prob_lookup(
    enriched_df: pd.DataFrame,
    matches_df: pd.DataFrame,
) -> dict[tuple, float]:
    """Build a historical win-probability lookup table for 2nd-innings chases.

    Groups every 2nd-innings ball by
        (balls_remaining_bucket, wickets_in_hand, runs_per_ball_bucket)
    and computes the fraction of times the chasing team eventually won.

    Parameters
    ----------
    enriched_df : DataFrame
        Ball-by-ball with cum_runs, cum_wickets, cum_balls, balls_remaining,
        runs_needed, target, innings, match_id.
    matches_df : DataFrame
        Must contain match_id, win_team_id columns.

    Returns
    -------
    dict  — keyed by (balls_bucket, wkts_in_hand, rpb_bucket) → float win%
    """
    df2 = enriched_df[enriched_df["innings"] == 2].copy()
    if df2.empty:
        return {}

    # Determine chasing team and whether they won
    chase_team = (
        df2.groupby("match_id")["batting_team_id"]
        .first()
        .reset_index()
        .rename(columns={"batting_team_id": "chase_team_id"})
    )
    merged = df2.merge(matches_df[["match_id", "win_team_id"]], on="match_id", how="left")
    merged = merged.merge(chase_team, on="match_id", how="left")
    merged["chase_won"] = (merged["win_team_id"] == merged["chase_team_id"]).astype(int)

    # Compute bucketed features
    merged["wkts_in_hand"] = 10 - merged["cum_wickets"]
    merged["rpb"] = merged["runs_needed"] / merged["balls_remaining"].clip(lower=1)
    merged["balls_bucket"] = merged["balls_remaining"].apply(_bucket_balls)
    merged["rpb_bucket"] = merged["rpb"].apply(_bucket_rpb)

    # Group and compute win %
    grouped = (
        merged.groupby(["balls_bucket", "wkts_in_hand", "rpb_bucket"])["chase_won"]
        .agg(["mean", "count"])
        .reset_index()
    )

    # Only keep buckets with ≥3 observations for stability
    grouped = grouped[grouped["count"] >= 3]

    lookup: dict[tuple, float] = {}
    for _, row in grouped.iterrows():
        key = (int(row["balls_bucket"]), int(row["wkts_in_hand"]), float(row["rpb_bucket"]))
        lookup[key] = float(row["mean"])

    return lookup


# Module-level cache so the lookup is built once
_WIN_PROB_LOOKUP: dict[tuple, float] | None = None
_PAR_SCORE_TABLE: dict[tuple, float] | None = None


def calc_chase_win_prob(
    runs_needed: float,
    balls_remaining: int,
    wickets_in_hand: int,
    lookup: dict[tuple, float] | None = None,
) -> float:
    """Return probability (0–1) of the chasing team winning.

    Uses the historical lookup table when a matching bucket exists.
    Falls back to a logistic estimate calibrated to T20 norms when
    the exact bucket is missing.

    Parameters
    ----------
    runs_needed : float
        Runs still required to win.
    balls_remaining : int
        Legal deliveries left in the innings.
    wickets_in_hand : int
        Wickets remaining (10 − cum_wickets).
    lookup : dict, optional
        Pre-built lookup; uses module-level cache if None.
    """
    if lookup is None:
        lookup = _WIN_PROB_LOOKUP or {}

    # Edge cases
    if runs_needed <= 0:
        return 1.0
    if wickets_in_hand <= 0 or balls_remaining <= 0:
        return 0.0

    rpb = runs_needed / max(balls_remaining, 1)
    key = (_bucket_balls(balls_remaining), wickets_in_hand, _bucket_rpb(rpb))

    if key in lookup:
        return lookup[key]

    # ----- Logistic fallback (calibrated to T20 data) -----
    # Features that drive win probability:
    #   - runs_per_ball: higher → harder to chase → lower win prob
    #   - wickets_in_hand: more wickets → higher win prob
    # Logistic: P(win) = 1 / (1 + exp(z))
    # z = β0 + β1*rpb + β2*wkts
    # Coefficients hand-tuned from T20 averages:
    #   average T20 run rate ≈ 1.33 rpb (8 rpo), 50 % win at that rate with 5 wkts
    beta0 = 0.5
    beta1 = 3.5   # penalty per unit of rpb
    beta2 = -0.35  # reward per wicket in hand
    z = beta0 + beta1 * rpb + beta2 * wickets_in_hand
    win_prob = 1.0 / (1.0 + np.exp(z))

    return float(np.clip(win_prob, 0.0, 1.0))


# ===================================================================
# 2. FIRST INNINGS — Par Score Pressure
# ===================================================================

def build_par_score_table(enriched_df: pd.DataFrame) -> dict[tuple, float]:
    """Build a lookup of average first-innings projected total from each state.

    Groups by (overs_completed, wickets_fallen) and computes the mean
    final first-innings total for matches that passed through that state.

    Returns
    -------
    dict  — keyed by (overs_completed: int, wickets_fallen: int) → avg total
    """
    df1 = enriched_df[enriched_df["innings"] == 1].copy()
    if df1.empty:
        return {}

    # Compute first-innings total per match
    match_totals = (
        df1.groupby("match_id")["cum_runs"]
        .max()
        .reset_index()
        .rename(columns={"cum_runs": "first_inn_total"})
    )

    df1 = df1.merge(match_totals, on="match_id", how="left")

    # over completed = floor(cum_balls / 6), capped at 20
    df1["overs_completed"] = (df1["cum_balls"] // 6).clip(upper=20).astype(int)
    df1["wkts_fallen"] = df1["cum_wickets"].astype(int)

    # Take one row per match per state (last ball in that over/wicket combo)
    state_df = (
        df1.groupby(["match_id", "overs_completed", "wkts_fallen"])
        .agg(first_inn_total=("first_inn_total", "first"))
        .reset_index()
    )

    par_table = (
        state_df.groupby(["overs_completed", "wkts_fallen"])["first_inn_total"]
        .mean()
        .to_dict()
    )

    return par_table


def calc_first_innings_pressure(
    cum_runs: float,
    cum_wickets: int,
    cum_balls: int,
    par_table: dict[tuple, float] | None = None,
) -> float:
    """Return a base-pressure score (0–1) for a first-innings situation.

    Uses deviation from the par (average) first-innings total at this
    point in the innings.  Larger deviation from par → higher pressure
    for the under-performing side, mapped through a sigmoid.

    Parameters
    ----------
    cum_runs : float
        Runs scored so far in this innings.
    cum_wickets : int
        Wickets fallen so far.
    cum_balls : int
        Balls bowled so far.
    par_table : dict, optional
        Pre-built par-score table; uses module-level cache if None.
    """
    if par_table is None:
        par_table = _PAR_SCORE_TABLE or {}

    overs_completed = min(int(cum_balls // 6), 20)
    wkts_fallen = int(cum_wickets)

    # Lookup par total — search nearby states if exact key missing
    par_total = par_table.get((overs_completed, wkts_fallen))
    if par_total is None:
        # Try nearest wickets bucket
        for dw in range(0, 11):
            for sign in [0, -1, 1]:
                key = (overs_completed, max(0, min(10, wkts_fallen + sign * dw)))
                if key in par_table:
                    par_total = par_table[key]
                    break
            if par_total is not None:
                break
    if par_total is None or par_total == 0:
        # Default par total fallback (average T20 total ~155)
        par_total = 155.0

    # What proportion of the innings is done?
    innings_progress = cum_balls / 120.0  # fraction of T20 innings completed

    # Project what the par score SHOULD be at this point
    # Use a simple proportion: par_at_this_point ≈ par_total * progress_fraction
    # But T20 scoring accelerates, so apply a slight convex curve
    # Approximate: par_at_ball = par_total * (cum_balls/120) ^ 0.85
    if cum_balls <= 0:
        return 0.3  # start of innings, moderate baseline

    par_at_this_point = par_total * (innings_progress ** 0.85)

    # Deviation: positive means batting team is BEHIND par
    deviation = (par_at_this_point - cum_runs) / max(par_at_this_point, 1.0)

    # Map through sigmoid for smooth 0–1 scaling
    # abs(deviation) drives pressure; sign tells us who feels it
    # For DPI we care about MATCH pressure (either side feeling heat)
    abs_dev = abs(deviation)

    # Sigmoid: pressure = 1 / (1 + exp(-k*(x - x0)))
    # Tuned so ~0 deviation ≈ 0.3 pressure, large deviation ≈ 0.9+
    k = 6.0   # steepness
    x0 = 0.3  # midpoint — 30 % deviation from par → 0.5 pressure
    pressure = 1.0 / (1.0 + np.exp(-k * (abs_dev - x0)))

    # Wicket loss amplifies pressure (more wickets fallen → fewer resources)
    # Small wicket boost only when behind par AND wickets down
    if deviation > 0 and wkts_fallen >= 4:
        wicket_boost = 0.05 * (wkts_fallen - 3)  # +0.05 per extra wicket above 3
        pressure = min(pressure + wicket_boost, 1.0)

    return float(np.clip(pressure, 0.0, 1.0))


# ===================================================================
# 3. DYNAMIC PRESSURE INDEX (DPI) — Main Entry Point
# ===================================================================

def _momentum_multiplier(row: pd.Series) -> float:
    """Compute a momentum-based pressure multiplier (1.0–1.3).

    Clusters of recent wickets or dot balls spike pressure.
    Uses `wickets_in_last_6_balls` and `runs_in_last_6_balls`.
    """
    mult = 1.0

    wkts_6 = row.get("wickets_in_last_6_balls", 0) or 0
    runs_6 = row.get("runs_in_last_6_balls", 0) or 0

    # Recent wicket cluster: each wicket in last 6 balls adds 0.08
    if wkts_6 >= 1:
        mult += 0.08 * wkts_6  # e.g. 2 wkts → 1.16, 3 → 1.24

    # Dot-ball pressure: if fewer than 4 runs in last 6 balls → building pressure
    if runs_6 <= 3:
        mult += 0.10  # stalling adds 0.10

    return min(mult, 1.35)  # cap at 1.35


def calculate_dpi(
    enriched_df: pd.DataFrame,
    matches_df: pd.DataFrame | None = None,
) -> pd.DataFrame:
    """Add ``pressure_index`` and ``pressure_category`` columns to the DataFrame.

    Parameters
    ----------
    enriched_df : DataFrame
        Ball-by-ball enriched data (from data_loader.load_enriched_data).
    matches_df : DataFrame, optional
        Match-level data with win_team_id.  If None, loaded from disk.

    Returns
    -------
    DataFrame — same rows, with two new columns appended.
    """
    global _WIN_PROB_LOOKUP, _PAR_SCORE_TABLE

    df = enriched_df.copy()

    # Load matches if not provided (needed for win-prob lookup)
    if matches_df is None:
        _DATA_DIR = os.path.join(os.path.dirname(_SRC_DIR), "Data Pack")
        matches_df = pd.read_csv(os.path.join(_DATA_DIR, "matches.csv"))

    # --- Build lookup tables (cached) ---
    if _WIN_PROB_LOOKUP is None:
        _WIN_PROB_LOOKUP = build_chase_win_prob_lookup(df, matches_df)
    if _PAR_SCORE_TABLE is None:
        _PAR_SCORE_TABLE = build_par_score_table(df)

    # --- Phase multiplier ---
    phase_mult_map = {"powerplay": 1.0, "middle": 1.0, "death": 1.3}
    df["_phase_mult"] = df["phase"].map(phase_mult_map).fillna(1.0)

    # --- Stakes multiplier ---
    df["_stakes_mult"] = np.where(df["is_knockout"].astype(bool), 1.3, 1.0)

    # --- Momentum multiplier ---
    df["_momentum_mult"] = df.apply(_momentum_multiplier, axis=1)

    # --- Base pressure per ball ---
    base_pressure = np.zeros(len(df), dtype=float)

    # Second innings: win-probability-based
    mask_2nd = df["innings"] == 2
    if mask_2nd.any():
        df2 = df.loc[mask_2nd]
        wkts_in_hand = 10 - df2["cum_wickets"].values
        runs_needed = df2["runs_needed"].values
        balls_rem = df2["balls_remaining"].values

        win_probs = np.array([
            calc_chase_win_prob(rn, br, wih, _WIN_PROB_LOOKUP)
            for rn, br, wih in zip(runs_needed, balls_rem, wkts_in_hand)
        ])
        # Match balance peaks when win_prob ≈ 0.5
        match_balance = 1.0 - 2.0 * np.abs(win_probs - 0.5)
        base_pressure[mask_2nd.values] = match_balance

    # First innings: par-score deviation
    mask_1st = df["innings"] == 1
    if mask_1st.any():
        df1 = df.loc[mask_1st]
        first_pressures = np.array([
            calc_first_innings_pressure(cr, cw, cb, _PAR_SCORE_TABLE)
            for cr, cw, cb in zip(
                df1["cum_runs"].values,
                df1["cum_wickets"].values,
                df1["cum_balls"].values,
            )
        ])
        base_pressure[mask_1st.values] = first_pressures

    df["_base_pressure"] = base_pressure

    # --- Final DPI ---
    raw_dpi = (
        df["_base_pressure"]
        * df["_phase_mult"]
        * df["_stakes_mult"]
        * df["_momentum_mult"]
    )
    df["pressure_index"] = np.clip(raw_dpi, 0.0, 1.0)

    # --- Pressure categories ---
    df["pressure_category"] = pd.cut(
        df["pressure_index"],
        bins=[-0.01, 0.4, 0.6, 0.8, 1.01],
        labels=["low", "moderate", "high", "extreme"],
    )

    # Clean up temp columns
    df.drop(columns=["_phase_mult", "_stakes_mult", "_momentum_mult", "_base_pressure"],
            inplace=True)

    return df


# ===================================================================
# 4. CONVENIENCE — Run Standalone
# ===================================================================

def main() -> pd.DataFrame:
    """Load data, compute DPI, and return the enriched DataFrame."""
    enriched_df = load_enriched_data()
    result = calculate_dpi(enriched_df)
    return result


if __name__ == "__main__":
    result_df = main()
    print(f"Computed DPI for {len(result_df):,} deliveries")
    print("\nPressure category distribution:")
    print(result_df["pressure_category"].value_counts().sort_index())
    print("\nSample rows (2nd innings, death overs):")
    sample = result_df[
        (result_df["innings"] == 2) & (result_df["phase"] == "death")
    ].head(10)
    print(
        sample[
            ["match_id", "innings", "overid", "cum_runs", "runs_needed",
             "balls_remaining", "pressure_index", "pressure_category"]
        ].to_string(index=False)
    )
