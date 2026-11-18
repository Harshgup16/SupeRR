"""
visualizations.py — Chart generation for SupeRR Selector Season 2
=================================================================
Generates professional cricket pressure-analysis charts and saves
them to the ``output/`` directory.
"""

import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.patches import FancyBboxPatch
from math import pi

try:
    import seaborn as sns
    HAS_SEABORN = True
except ImportError:
    HAS_SEABORN = False

# ---------------------------------------------------------------------------
# Style constants
# ---------------------------------------------------------------------------
RR_PINK = "#EA1A85"
RR_DARK = "#2D1446"
RR_GOLD = "#F5A623"
IMPROVE_GREEN = "#27AE60"
DECLINE_RED = "#E74C3C"
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "output")

PRESSURE_COLORS = {
    "low": "#3498DB",
    "moderate": "#F39C12",
    "high": "#E67E22",
    "extreme": "#E74C3C",
}
PRESSURE_ORDER = ["low", "moderate", "high", "extreme"]

# Apply a clean style once at import time
try:
    plt.style.use("seaborn-v0_8-whitegrid")
except OSError:
    try:
        plt.style.use("seaborn-whitegrid")
    except OSError:
        pass  # fall back to default


def _ensure_output_dir():
    os.makedirs(OUTPUT_DIR, exist_ok=True)


def _save(fig, name: str, dpi: int = 180):
    """Save figure and close it."""
    _ensure_output_dir()
    path = os.path.join(OUTPUT_DIR, name)
    fig.savefig(path, dpi=dpi, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  ✔ Saved {name}")


# ===================================================================
# 1. Pressure Distribution Histogram
# ===================================================================
def plot_pressure_distribution(df: pd.DataFrame) -> None:
    """Histogram of pressure_index coloured by pressure_category."""
    fig, ax = plt.subplots(figsize=(10, 5))

    for cat in PRESSURE_ORDER:
        subset = df.loc[df["pressure_category"] == cat, "pressure_index"]
        if subset.empty:
            continue
        ax.hist(
            subset,
            bins=30,
            alpha=0.7,
            label=cat.title(),
            color=PRESSURE_COLORS[cat],
            edgecolor="white",
            linewidth=0.5,
        )

    # Overlay percentages
    total = len(df)
    for cat in PRESSURE_ORDER:
        count = (df["pressure_category"] == cat).sum()
        pct = count / total * 100 if total else 0
        ax.annotate(
            f"{pct:.1f}%",
            xy=(0.5, 0.95 - PRESSURE_ORDER.index(cat) * 0.07),
            xycoords="axes fraction",
            fontsize=9,
            color=PRESSURE_COLORS[cat],
            fontweight="bold",
            ha="right",
        )

    ax.set_xlabel("Pressure Index", fontsize=11)
    ax.set_ylabel("Number of Deliveries", fontsize=11)
    ax.set_title("Distribution of Pressure Index Across All Deliveries",
                 fontsize=13, fontweight="bold", color=RR_DARK)
    ax.legend(title="Pressure Zone", fontsize=9)
    _save(fig, "pressure_distribution.png")


# ===================================================================
# 2. Top Batters Clutch Factor — Horizontal Bar
# ===================================================================
def plot_top_batters_clutch(top_batters_df: pd.DataFrame) -> None:
    """Horizontal bar chart of top 10 batters by clutch factor."""
    df = top_batters_df.head(10).copy().sort_values("clutch_factor")

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = [IMPROVE_GREEN if cf > 1 else DECLINE_RED for cf in df["clutch_factor"]]
    bars = ax.barh(df["player_name"], df["clutch_factor"], color=colors,
                   edgecolor="white", height=0.6)

    # Baseline line at 1.0
    ax.axvline(x=1.0, color=RR_DARK, linewidth=1.2, linestyle="--", alpha=0.6)

    # Annotations
    for bar, (_, row) in zip(bars, df.iterrows()):
        baseline = row.get("baseline_sr", 0)
        pressure = row.get("pressure_sr", 0)
        ax.text(
            bar.get_width() + 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"SR: {baseline:.0f} → {pressure:.0f}",
            va="center", fontsize=8, color="#555",
        )

    ax.set_xlabel("Clutch Factor  (>1 = improves under pressure)", fontsize=10)
    ax.set_title("Top 10 Batters — Clutch Performance Under Pressure",
                 fontsize=13, fontweight="bold", color=RR_DARK)
    ax.tick_params(axis="y", labelsize=9)
    _save(fig, "top_batters_clutch.png")


# ===================================================================
# 3. Top Bowlers Clutch Factor — Horizontal Bar
# ===================================================================
def plot_top_bowlers_clutch(top_bowlers_df: pd.DataFrame) -> None:
    """Horizontal bar chart of top 10 bowlers by clutch factor."""
    df = top_bowlers_df.head(10).copy().sort_values("clutch_factor")

    fig, ax = plt.subplots(figsize=(10, 6))
    colors = [IMPROVE_GREEN if cf > 1 else DECLINE_RED for cf in df["clutch_factor"]]
    bars = ax.barh(df["player_name"], df["clutch_factor"], color=colors,
                   edgecolor="white", height=0.6)

    ax.axvline(x=1.0, color=RR_DARK, linewidth=1.2, linestyle="--", alpha=0.6)

    for bar, (_, row) in zip(bars, df.iterrows()):
        baseline = row.get("baseline_economy", 0)
        pressure = row.get("pressure_economy", 0)
        ax.text(
            bar.get_width() + 0.01,
            bar.get_y() + bar.get_height() / 2,
            f"Econ: {baseline:.1f} → {pressure:.1f}",
            va="center", fontsize=8, color="#555",
        )

    ax.set_xlabel("Clutch Factor  (>1 = improves under pressure)", fontsize=10)
    ax.set_title("Top 10 Bowlers — Clutch Performance Under Pressure",
                 fontsize=13, fontweight="bold", color=RR_DARK)
    ax.tick_params(axis="y", labelsize=9)
    _save(fig, "top_bowlers_clutch.png")


# ===================================================================
# 4. Player Pressure Profile — Radar / Spider Chart
# ===================================================================
def plot_player_pressure_profile(player_name: str, df: pd.DataFrame) -> None:
    """Radar chart of a player's performance across pressure levels."""

    # Filter to this batter
    pdf = df[df["striker_name"] == player_name].copy()
    if pdf.empty:
        print(f"  ⚠ No data for {player_name}")
        return

    metrics = {}
    for cat in PRESSURE_ORDER:
        sub = pdf[pdf["pressure_category"] == cat]
        if sub.empty:
            metrics[cat] = {"SR": 0, "Avg": 0, "Boundary%": 0, "Dot%": 0}
            continue

        balls = len(sub)
        runs = sub["runs"].sum()
        wickets = sub["is_wicket"].sum()
        boundaries = (sub["is_four"].sum() + sub["is_six"].sum())
        dots = (sub["runs"] == 0).sum()

        sr = (runs / balls * 100) if balls else 0
        avg = (runs / wickets) if wickets > 0 else runs
        boundary_pct = (boundaries / balls * 100) if balls else 0
        dot_pct = (dots / balls * 100) if balls else 0
        metrics[cat] = {"SR": sr, "Avg": avg, "Boundary%": boundary_pct, "Dot%": 100 - dot_pct}

    categories_labels = ["Strike Rate", "Average", "Boundary %", "Non-Dot %"]
    N = len(categories_labels)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]  # close the polygon

    fig, ax = plt.subplots(figsize=(7, 7), subplot_kw=dict(polar=True))

    for cat in PRESSURE_ORDER:
        vals = [metrics[cat]["SR"] / 2,  # scale SR to ~same range
                metrics[cat]["Avg"] / 2,
                metrics[cat]["Boundary%"],
                metrics[cat]["Dot%"]]
        vals += vals[:1]
        ax.plot(angles, vals, "o-", linewidth=1.8, label=cat.title(),
                color=PRESSURE_COLORS[cat])
        ax.fill(angles, vals, alpha=0.08, color=PRESSURE_COLORS[cat])

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories_labels, fontsize=9)
    ax.set_title(f"Pressure Profile — {player_name}",
                 fontsize=13, fontweight="bold", color=RR_DARK, pad=20)
    ax.legend(loc="upper right", bbox_to_anchor=(1.25, 1.1), fontsize=8)
    _save(fig, f"player_profile_{player_name.replace(' ', '_').lower()}.png")


# ===================================================================
# 5. Pressure Heatmap — Over × Wickets Fallen
# ===================================================================
def plot_pressure_heatmap(df: pd.DataFrame) -> None:
    """Heatmap of average pressure_index by over (1-20) × wickets fallen (0-9)."""

    pivot = (
        df.assign(over=df["overid"].clip(upper=20))
        .assign(wickets=df["cum_wickets"].clip(upper=9))
        .groupby(["over", "wickets"])["pressure_index"]
        .mean()
        .unstack(fill_value=np.nan)
    )

    fig, ax = plt.subplots(figsize=(12, 6))

    if HAS_SEABORN:
        sns.heatmap(
            pivot.T,
            cmap="YlOrRd",
            linewidths=0.3,
            linecolor="white",
            ax=ax,
            cbar_kws={"label": "Avg Pressure Index"},
            vmin=0,
            vmax=1,
        )
    else:
        im = ax.imshow(pivot.T.values, aspect="auto", cmap="YlOrRd",
                       vmin=0, vmax=1, origin="lower")
        fig.colorbar(im, ax=ax, label="Avg Pressure Index")
        ax.set_xticks(range(len(pivot.index)))
        ax.set_xticklabels(pivot.index)
        ax.set_yticks(range(len(pivot.columns)))
        ax.set_yticklabels(pivot.columns)

    ax.set_xlabel("Over", fontsize=11)
    ax.set_ylabel("Wickets Fallen", fontsize=11)
    ax.set_title("Pressure Heatmap — Where Pressure Concentrates in a Match",
                 fontsize=13, fontweight="bold", color=RR_DARK)
    _save(fig, "pressure_heatmap.png")


# ===================================================================
# 6. Performance Comparison — Scatter (Baseline vs Pressure)
# ===================================================================
def plot_performance_comparison(
    top_df: pd.DataFrame,
    metric_baseline: str,
    metric_pressure: str,
    title: str,
) -> None:
    """Scatter plot: baseline metric on X, pressure metric on Y.
    Points above the diagonal = players who improve under pressure.
    """
    fig, ax = plt.subplots(figsize=(8, 8))

    ax.scatter(
        top_df[metric_baseline],
        top_df[metric_pressure],
        s=70,
        c=RR_PINK,
        edgecolors="white",
        linewidths=0.6,
        zorder=3,
    )

    # Diagonal reference line
    lo = min(top_df[metric_baseline].min(), top_df[metric_pressure].min()) * 0.9
    hi = max(top_df[metric_baseline].max(), top_df[metric_pressure].max()) * 1.1
    ax.plot([lo, hi], [lo, hi], "--", color="#999", linewidth=1, zorder=1)
    ax.fill_between([lo, hi], [lo, hi], hi, alpha=0.04, color=IMPROVE_GREEN, zorder=0)
    ax.fill_between([lo, hi], lo, [lo, hi], alpha=0.04, color=DECLINE_RED, zorder=0)

    # Label top 10
    for _, row in top_df.head(10).iterrows():
        ax.annotate(
            row["player_name"],
            (row[metric_baseline], row[metric_pressure]),
            fontsize=7,
            textcoords="offset points",
            xytext=(5, 5),
            color=RR_DARK,
        )

    ax.set_xlabel(f"Baseline {metric_baseline.replace('_', ' ').title()}", fontsize=10)
    ax.set_ylabel(f"Pressure {metric_pressure.replace('_', ' ').title()}", fontsize=10)
    ax.set_title(title, fontsize=13, fontweight="bold", color=RR_DARK)
    ax.text(
        0.02, 0.98, "▲ Improves under pressure",
        transform=ax.transAxes, fontsize=8, va="top", color=IMPROVE_GREEN,
    )
    ax.text(
        0.98, 0.02, "▼ Declines under pressure",
        transform=ax.transAxes, fontsize=8, va="bottom", ha="right", color=DECLINE_RED,
    )
    _save(fig, f"comparison_{metric_baseline}_vs_{metric_pressure}.png")


# ===================================================================
# 7. Innings Pressure Curve — Ball-by-Ball
# ===================================================================
def plot_innings_pressure_curve(df: pd.DataFrame, match_id) -> None:
    """Line chart of pressure_index ball-by-ball for a given match."""

    mdf = df[df["match_id"] == match_id].sort_values(["innings", "overid", "over_ball_num"])
    if mdf.empty:
        print(f"  ⚠ No data for match {match_id}")
        return

    fig, ax = plt.subplots(figsize=(14, 5))

    for inn in sorted(mdf["innings"].unique()):
        sub = mdf[mdf["innings"] == inn].reset_index(drop=True)
        label = f"Innings {inn}"
        color = RR_PINK if inn == 1 else RR_DARK
        ax.plot(sub.index, sub["pressure_index"], color=color, linewidth=1.4,
                alpha=0.85, label=label)
        ax.fill_between(sub.index, 0, sub["pressure_index"], alpha=0.08, color=color)

        # Mark wickets
        wk = sub[sub["is_wicket"] == 1]
        ax.scatter(wk.index, wk["pressure_index"], marker="v", s=40,
                   color=DECLINE_RED, zorder=4, label=f"Wicket (Inn {inn})" if not wk.empty else "")

    ax.set_ylim(0, 1.05)
    ax.set_xlabel("Ball Number (sequential)", fontsize=10)
    ax.set_ylabel("Pressure Index", fontsize=10)
    ax.set_title(f"Pressure Curve — Match {match_id}",
                 fontsize=13, fontweight="bold", color=RR_DARK)
    ax.legend(fontsize=9)
    _save(fig, f"pressure_curve_match_{match_id}.png")


# ===================================================================
# 8. Summary Table as Figure
# ===================================================================
def generate_summary_table(top_batters: pd.DataFrame, top_bowlers: pd.DataFrame) -> None:
    """Create a formatted summary table as a saved figure."""

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))

    for ax in (ax1, ax2):
        ax.axis("off")

    # --- Batters table ---
    bat_cols = ["rank", "player_name", "clutch_factor", "pressure_sr", "baseline_sr", "pressure_balls"]
    bat_display = top_batters[bat_cols].head(10).copy()
    bat_display.columns = ["#", "Batter", "Clutch", "Pressure SR", "Baseline SR", "Press. Balls"]
    bat_display["Clutch"] = bat_display["Clutch"].map(lambda x: f"{x:.2f}")
    bat_display["Pressure SR"] = bat_display["Pressure SR"].map(lambda x: f"{x:.1f}")
    bat_display["Baseline SR"] = bat_display["Baseline SR"].map(lambda x: f"{x:.1f}")

    table1 = ax1.table(
        cellText=bat_display.values,
        colLabels=bat_display.columns,
        loc="center",
        cellLoc="center",
    )
    table1.auto_set_font_size(False)
    table1.set_fontsize(9)
    table1.scale(1, 1.5)
    # Style header
    for (row, col), cell in table1.get_celld().items():
        if row == 0:
            cell.set_facecolor(RR_PINK)
            cell.set_text_props(color="white", fontweight="bold")
        else:
            cell.set_facecolor("#FFF0F6" if row % 2 == 0 else "white")
        cell.set_edgecolor("#DDD")

    ax1.set_title("Top 10 Batters Under Pressure", fontsize=14,
                   fontweight="bold", color=RR_DARK, pad=15)

    # --- Bowlers table ---
    bowl_cols = ["rank", "player_name", "clutch_factor", "pressure_economy", "baseline_economy", "pressure_balls"]
    bowl_display = top_bowlers[bowl_cols].head(10).copy()
    bowl_display.columns = ["#", "Bowler", "Clutch", "Press. Econ", "Base. Econ", "Press. Balls"]
    bowl_display["Clutch"] = bowl_display["Clutch"].map(lambda x: f"{x:.2f}")
    bowl_display["Press. Econ"] = bowl_display["Press. Econ"].map(lambda x: f"{x:.2f}")
    bowl_display["Base. Econ"] = bowl_display["Base. Econ"].map(lambda x: f"{x:.2f}")

    table2 = ax2.table(
        cellText=bowl_display.values,
        colLabels=bowl_display.columns,
        loc="center",
        cellLoc="center",
    )
    table2.auto_set_font_size(False)
    table2.set_fontsize(9)
    table2.scale(1, 1.5)
    for (row, col), cell in table2.get_celld().items():
        if row == 0:
            cell.set_facecolor(RR_PINK)
            cell.set_text_props(color="white", fontweight="bold")
        else:
            cell.set_facecolor("#FFF0F6" if row % 2 == 0 else "white")
        cell.set_edgecolor("#DDD")

    ax2.set_title("Top 10 Bowlers Under Pressure", fontsize=14,
                   fontweight="bold", color=RR_DARK, pad=15)

    fig.suptitle("SupeRR Selector Season 2 — Pressure Performance Summary",
                 fontsize=16, fontweight="bold", color=RR_PINK, y=0.98)
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    _save(fig, "summary_table.png")
