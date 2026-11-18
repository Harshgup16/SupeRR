"""
data_loader.py — Data engineering foundation for SupeRR Selector Season 2.

Loads all CSVs from the Data Pack, enriches the ball-by-ball DataFrame with
cumulative stats, rolling momentum windows, 2nd-innings chase fields,
match format, knockout flag, and match phase.
"""

import os
import pandas as pd
import numpy as np
from pathlib import Path

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
DATA_DIR = Path(r"d:\Hackathon\rr\Data Pack")
T20_TOTAL_BALLS = 120  # 20 overs × 6 legal balls

# Extras that do NOT count as legal deliveries
_ILLEGAL_EXTRAS = {"wide", "Overstep"}

# Stage keywords that indicate a knockout match
_KNOCKOUT_KEYWORDS = ("Final", "Semi", "Eliminator", "Qualifier")


# ---------------------------------------------------------------------------
# 1. Raw CSV loaders
# ---------------------------------------------------------------------------

def load_ball_by_ball() -> pd.DataFrame:
    """Load delivery-level data (201K rows, 33 cols)."""
    return pd.read_csv(DATA_DIR / "ball_by_ball.csv")


def load_matches() -> pd.DataFrame:
    """Load match metadata (883 rows)."""
    df = pd.read_csv(DATA_DIR / "matches.csv")
    # Ensure knock_out is boolean
    df["knock_out"] = df["knock_out"].astype(bool)
    return df


def load_playing_eleven() -> pd.DataFrame:
    """Load playing-eleven data (28K rows)."""
    return pd.read_csv(DATA_DIR / "playing_eleven.csv")


def load_competitions() -> pd.DataFrame:
    """Load competition metadata (141 rows)."""
    return pd.read_csv(DATA_DIR / "competitions.csv")


def load_teams() -> pd.DataFrame:
    """Load comp-team mapping (353 rows)."""
    return pd.read_csv(DATA_DIR / "teams.csv")


def load_player_mapping() -> pd.DataFrame:
    """Load competition-team-player squad mapping (6.4K rows)."""
    return pd.read_csv(DATA_DIR / "competition_team_player_mapping.csv")


def load_all_raw() -> dict[str, pd.DataFrame]:
    """Load every CSV and return them as a dict keyed by logical name."""
    return {
        "ball_by_ball": load_ball_by_ball(),
        "matches": load_matches(),
        "playing_eleven": load_playing_eleven(),
        "competitions": load_competitions(),
        "teams": load_teams(),
        "player_mapping": load_player_mapping(),
    }


# ---------------------------------------------------------------------------
# 2. First-innings totals helper
# ---------------------------------------------------------------------------

def get_first_innings_totals(df: pd.DataFrame) -> pd.DataFrame:
    """
    Given the ball-by-ball DataFrame (raw or enriched), return a DataFrame
    with columns [match_id, first_innings_total] — the total runs scored in
    innings 1 for every match.

    Total runs = bat runs + extras1_runs + extras_2_runs.
    """
    inn1 = df[df["innings"] == 1].copy()
    inn1["total_ball_runs"] = inn1["runs"] + inn1["extras1_runs"] + inn1["extras_2_runs"]
    totals = (
        inn1.groupby("match_id")["total_ball_runs"]
        .sum()
        .reset_index()
        .rename(columns={"total_ball_runs": "first_innings_total"})
    )
    return totals


# ---------------------------------------------------------------------------
# 3. Enrichment pipeline
# ---------------------------------------------------------------------------

def _add_total_runs_col(df: pd.DataFrame) -> pd.DataFrame:
    """Add total_runs (bat runs + all extras) for each delivery."""
    df["total_runs"] = df["runs"] + df["extras1_runs"] + df["extras_2_runs"]
    return df


def _add_legal_ball_flag(df: pd.DataFrame) -> pd.DataFrame:
    """
    Flag each delivery as a legal ball or not.
    Wides and no-balls (Overstep) are not legal deliveries.
    """
    df["is_legal_ball"] = ~df["extras_type"].isin(_ILLEGAL_EXTRAS)
    return df


def _add_cumulative_stats(df: pd.DataFrame) -> pd.DataFrame:
    """
    Within each (match_id, innings), compute running totals:
      - cum_runs:    cumulative total runs up to this ball
      - cum_wickets: cumulative wickets fallen up to this ball
      - cum_balls:   cumulative *legal* balls bowled up to this ball
    """
    grp = df.groupby(["match_id", "innings"])

    df["cum_runs"] = grp["total_runs"].cumsum()
    df["cum_wickets"] = grp["is_wicket"].cumsum().astype(int)
    df["cum_balls"] = grp["is_legal_ball"].cumsum().astype(int)
    return df


def _add_balls_remaining(df: pd.DataFrame) -> pd.DataFrame:
    """balls_remaining = 120 - cum_balls (T20 = 120 legal deliveries)."""
    df["balls_remaining"] = T20_TOTAL_BALLS - df["cum_balls"]
    return df


def _add_rolling_momentum(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rolling 6-ball windows for momentum:
      - runs_in_last_6_balls:    sum of total_runs over the last 6 deliveries
      - wickets_in_last_6_balls: sum of is_wicket over the last 6 deliveries

    The window is applied within each (match_id, innings) group.
    Partial windows at the start are filled with the available sum.
    """
    grp = df.groupby(["match_id", "innings"])
    df["runs_in_last_6_balls"] = (
        grp["total_runs"]
        .transform(lambda s: s.rolling(6, min_periods=1).sum())
        .fillna(0)
        .astype(int)
    )
    df["wickets_in_last_6_balls"] = (
        grp["is_wicket"]
        .transform(lambda s: s.astype(int).rolling(6, min_periods=1).sum())
        .fillna(0)
        .astype(int)
    )
    return df


def _add_second_innings_chase_fields(df: pd.DataFrame) -> pd.DataFrame:
    """
    For 2nd-innings rows, add:
      - target:             first_innings_total + 1
      - runs_needed:        target - cum_runs
      - required_run_rate:  runs_needed / (balls_remaining / 6)
                            (NaN when balls_remaining == 0)
    1st-innings rows get NaN for these columns.
    """
    # Compute first-innings totals
    fi_totals = get_first_innings_totals(df)
    fi_totals = fi_totals.rename(columns={"first_innings_total": "_fi_total"})

    df = df.merge(fi_totals, on="match_id", how="left")

    # Only populate for innings == 2
    is_inn2 = df["innings"] == 2
    df["target"] = np.where(is_inn2, df["_fi_total"] + 1, np.nan)
    df["runs_needed"] = np.where(is_inn2, df["target"] - df["cum_runs"], np.nan)

    # Required run rate: runs_needed per over remaining
    overs_remaining = df["balls_remaining"] / 6.0
    df["required_run_rate"] = np.where(
        is_inn2 & (df["balls_remaining"] > 0),
        df["runs_needed"] / overs_remaining,
        np.nan,
    )

    df.drop(columns=["_fi_total"], inplace=True)

    # Cast target to nullable int for cleanliness (NaN in 1st innings)
    df["target"] = df["target"].astype("Int64")
    df["runs_needed"] = df["runs_needed"].astype("Int64")

    return df


def _add_match_format(df: pd.DataFrame, matches: pd.DataFrame,
                      competitions: pd.DataFrame) -> pd.DataFrame:
    """
    Add match_format (T20I or IPL) by joining:
      ball_by_ball → matches (on match_id) → competitions (on comp_id).
    """
    comp_fmt = competitions[["comp_id", "match_format"]].drop_duplicates()
    match_comp = matches[["match_id", "comp_id"]].drop_duplicates()
    fmt_map = match_comp.merge(comp_fmt, on="comp_id", how="left")
    df = df.merge(fmt_map[["match_id", "match_format"]], on="match_id", how="left")
    return df


def _add_is_knockout(df: pd.DataFrame, matches: pd.DataFrame) -> pd.DataFrame:
    """
    is_knockout is True when:
      - matches.knock_out == 1 (True), OR
      - matches.stage contains any of: Final, Semi, Eliminator, Qualifier
    """
    m = matches[["match_id", "knock_out", "stage"]].copy()
    m["_stage_ko"] = m["stage"].str.contains(
        "|".join(_KNOCKOUT_KEYWORDS), case=False, na=False
    )
    m["is_knockout"] = m["knock_out"] | m["_stage_ko"]
    df = df.merge(m[["match_id", "is_knockout"]], on="match_id", how="left")
    df["is_knockout"] = df["is_knockout"].astype(bool)
    return df


def _add_phase(df: pd.DataFrame) -> pd.DataFrame:
    """
    Match phase based on the over number (overid):
      - powerplay: overs 1–6
      - middle:    overs 7–15
      - death:     overs 16–20
    """
    conditions = [
        df["overid"] <= 6,
        df["overid"] <= 15,
        df["overid"] <= 20,
    ]
    choices = ["powerplay", "middle", "death"]
    df["phase"] = np.select(conditions, choices, default="death")
    return df


# ---------------------------------------------------------------------------
# 4. Main enrichment function
# ---------------------------------------------------------------------------

def build_enriched_ball_by_ball() -> pd.DataFrame:
    """
    Load all data and return a fully enriched ball-by-ball DataFrame with
    all computed columns.

    Returns
    -------
    pd.DataFrame
        The enriched ball-by-ball DataFrame.
    """
    # Load raw data
    bbb = load_ball_by_ball()
    matches = load_matches()
    competitions = load_competitions()

    # Sort to ensure correct cumulative / rolling computations
    bbb = bbb.sort_values(
        ["match_id", "innings", "overid", "over_ball_num"]
    ).reset_index(drop=True)

    # --- Enrichment pipeline ---
    bbb = _add_total_runs_col(bbb)
    bbb = _add_legal_ball_flag(bbb)
    bbb = _add_cumulative_stats(bbb)
    bbb = _add_balls_remaining(bbb)
    bbb = _add_rolling_momentum(bbb)
    bbb = _add_second_innings_chase_fields(bbb)
    bbb = _add_match_format(bbb, matches, competitions)
    bbb = _add_is_knockout(bbb, matches)
    bbb = _add_phase(bbb)

    # --- Final dtype enforcement ---
    bool_cols = ["is_four", "is_six", "is_wicket", "is_legal_ball", "is_knockout"]
    for col in bool_cols:
        bbb[col] = bbb[col].astype(bool)

    int_cols = ["cum_runs", "cum_wickets", "cum_balls", "balls_remaining",
                "runs_in_last_6_balls", "wickets_in_last_6_balls"]
    for col in int_cols:
        bbb[col] = bbb[col].astype(int)

    return bbb


# Alias for backward/forward compatibility
load_enriched_data = build_enriched_ball_by_ball


# ---------------------------------------------------------------------------
# 5. Quick-test entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    print("Loading and enriching ball-by-ball data...")
    df = build_enriched_ball_by_ball()
    print(f"Shape: {df.shape}")
    print(f"\nColumns ({len(df.columns)}):")
    for c in df.columns:
        print(f"  {c:40s}  {df[c].dtype}")
    print(f"\nSample (first 5 rows):")
    print(df.head().to_string())
    print(f"\n2nd innings chase sample:")
    inn2 = df[df.innings == 2]
    print(inn2[["match_id", "overid", "over_ball_num", "cum_runs",
                "target", "runs_needed", "required_run_rate"]].head(10).to_string())
