import src.data_loader as dl
import src.pressure_model as pm
import src.player_ranker as pr
import pandas as pd

df = dl.load_enriched_data()
df = pm.calculate_dpi(df)

top_b = pr.get_top_batters(df, n=10)
top_bw = pr.get_top_bowlers(df, n=10)

print("=== DETAILED TOP 10 BATTERS ===")
for _, r in top_b.iterrows():
    print(f"Rank {int(r['rank'])}: {r['player_name']} (Clutch: {r['clutch_factor']:.3f}, Weighted: {r['weighted_clutch']:.3f})")
    print(f"   Pressure: SR={r['pressure_strike_rate']:.1f}, Avg={r['pressure_batting_avg']:.1f}, Bnd%={r['pressure_boundary_pct']*100:.1f}%, Dot%={r['pressure_dot_ball_pct']*100:.1f}%, Balls={int(r['pressure_balls_faced'])}")
    print(f"   Baseline: SR={r['baseline_strike_rate']:.1f}, Avg={r['baseline_batting_avg']:.1f}, Bnd%={r['baseline_boundary_pct']*100:.1f}%, Dot%={r['baseline_dot_ball_pct']*100:.1f}%, Balls={int(r['baseline_balls_faced'])}")

print("\n=== DETAILED TOP 10 BOWLERS ===")
for _, r in top_bw.iterrows():
    print(f"Rank {int(r['rank'])}: {r['player_name']} (Clutch: {r['clutch_factor']:.3f}, Weighted: {r['weighted_clutch']:.3f})")
    print(f"   Pressure: Econ={r['pressure_economy_rate']:.2f}, SR={r['pressure_bowling_strike_rate']:.1f}, Dot%={r['pressure_dot_ball_pct']*100:.1f}%, Bnd%={r['pressure_boundaries_conceded_pct']*100:.1f}%, Balls={int(r['pressure_balls_bowled'])}")
    print(f"   Baseline: Econ={r['baseline_economy_rate']:.2f}, SR={r['baseline_bowling_strike_rate']:.1f}, Dot%={r['baseline_dot_ball_pct']*100:.1f}%, Bnd%={r['baseline_boundaries_conceded_pct']*100:.1f}%, Balls={int(r['baseline_balls_bowled'])}")

