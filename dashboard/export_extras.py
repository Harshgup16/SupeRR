import os
import sys
import json
import pandas as pd
import numpy as np

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import src.data_loader as dl
import src.pressure_model as pm

df = dl.load_enriched_data()
df = pm.calculate_dpi(df)

# Match tension curve for Match 39808
m_df = df[df['match_id'] == 39808].sort_values(['innings', 'overid', 'over_ball_num'])
curve_data = []
for _, r in m_df.iterrows():
    curve_data.append({
        'innings': int(r['innings']),
        'over': int(r['overid']),
        'ball': int(r['over_ball_num']),
        'cum_balls': int(r['cum_balls']),
        'score': f"{int(r['cum_runs'])}/{int(r['cum_wickets'])}",
        'dpi': round(float(r['pressure_index']), 3),
        'cat': str(r['pressure_category']),
        'striker': str(r['striker_name']),
        'bowler': str(r['bowler_name']),
        'runs': int(r['total_runs']),
        'is_wicket': bool(r['is_wicket'])
    })

# Pressure distribution
dist = {str(k): int(v) for k, v in df['pressure_category'].value_counts().items()}

# Distribution across overs (1-20)
over_group = df.groupby(['overid', 'pressure_category'], observed=False)['total_runs'].count().unstack(fill_value=0)
over_dist = {int(k): {str(cat): int(val) for cat, val in row.items()} for k, row in over_group.iterrows()}

with open('dashboard/data/extras.json', 'w') as f:
    json.dump({
        'match_39808': curve_data,
        'category_counts': dist,
        'over_distribution': over_dist
    }, f, indent=2)

print('Saved extras.json successfully!')
