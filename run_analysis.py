#!/usr/bin/env python3
"""
run_analysis.py — SupeRR Selector Season 2 Main Runner
=======================================================
Orchestrates the full pipeline:
  1. Load & enrich ball-by-ball data
  2. Compute Dynamic Pressure Index (DPI)
  3. Rank batters & bowlers under pressure
  4. Generate all visualisations
"""

import os
import sys
import time

# Ensure project root is on the path
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from src.data_loader import load_enriched_data
from src.pressure_model import calculate_dpi
from src.player_ranker import get_top_batters, get_top_bowlers
from src.visualizations import (
    plot_pressure_distribution,
    plot_top_batters_clutch,
    plot_top_bowlers_clutch,
    plot_player_pressure_profile,
    plot_pressure_heatmap,
    plot_performance_comparison,
    plot_innings_pressure_curve,
    generate_summary_table,
)


def main():
    t0 = time.time()

    # ------------------------------------------------------------------
    # 1. Load & enrich data
    # ------------------------------------------------------------------
    print("=" * 60)
    print("  SupeRR Selector Season 2 — Pressure Analysis Pipeline")
    print("=" * 60)
    print("\n[1/6] Loading and enriching data...")
    df = load_enriched_data()
    print(f"      Loaded {len(df):,} deliveries across "
          f"{df['match_id'].nunique():,} matches.")

    # ------------------------------------------------------------------
    # 2. Calculate Dynamic Pressure Index
    # ------------------------------------------------------------------
    print("\n[2/6] Calculating Dynamic Pressure Index (DPI)...")
    df = calculate_dpi(df)
    print(f"      Pressure distribution:")
    for cat in ["low", "moderate", "high", "extreme"]:
        n = (df["pressure_category"] == cat).sum()
        pct = n / len(df) * 100
        print(f"        {cat:>10s}: {n:>7,} balls ({pct:5.1f}%)")

    # ------------------------------------------------------------------
    # 3. Get rankings
    # ------------------------------------------------------------------
    print("\n[3/6] Computing player rankings...")
    top_batters = get_top_batters(df, n=10)
    top_bowlers = get_top_bowlers(df, n=10)

    # ------------------------------------------------------------------
    # 4. Print results
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("  TOP 10 BATTERS UNDER PRESSURE")
    print("=" * 60)
    batter_cols = ["rank", "player_name", "clutch_factor",
                   "pressure_sr", "baseline_sr", "pressure_balls"]
    print(top_batters[batter_cols].to_string(index=False))

    print("\n" + "=" * 60)
    print("  TOP 10 BOWLERS UNDER PRESSURE")
    print("=" * 60)
    bowler_cols = ["rank", "player_name", "clutch_factor",
                   "pressure_economy", "baseline_economy", "pressure_balls"]
    print(top_bowlers[bowler_cols].to_string(index=False))

    # ------------------------------------------------------------------
    # 5. Generate visualisations
    # ------------------------------------------------------------------
    print("\n[5/6] Generating visualisations...")
    os.makedirs("output", exist_ok=True)

    plot_pressure_distribution(df)
    plot_top_batters_clutch(top_batters)
    plot_top_bowlers_clutch(top_bowlers)
    plot_pressure_heatmap(df)
    generate_summary_table(top_batters, top_bowlers)

    # Scatter comparison
    plot_performance_comparison(
        top_batters,
        metric_baseline="baseline_sr",
        metric_pressure="pressure_sr",
        title="Batter Strike Rate — Baseline vs Pressure",
    )

    # Pressure curve for the most pressure-volatile match
    match_volatility = (
        df.groupby("match_id")["pressure_index"]
        .agg(["std", "max"])
        .sort_values("std", ascending=False)
    )
    if not match_volatility.empty:
        exciting_match = match_volatility.index[0]
        print(f"\n      Most volatile match: {exciting_match}")
        plot_innings_pressure_curve(df, exciting_match)

    # Radar profile for the top-ranked batter
    if not top_batters.empty:
        star = top_batters.iloc[0]["player_name"]
        print(f"      Generating radar profile for {star}...")
        plot_player_pressure_profile(star, df)

    # ------------------------------------------------------------------
    # 6. Done
    # ------------------------------------------------------------------
    elapsed = time.time() - t0
    print(f"\n{'=' * 60}")
    print(f"  ✅ Done in {elapsed:.1f}s — check the output/ folder for charts.")
    print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
