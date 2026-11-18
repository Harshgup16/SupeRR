"""
SupeRR Selector Season 2 — Streamlit Analytics Dashboard
=========================================================
Interactive dashboard for Rajasthan Royals Hackathon:
Identify the Most Reliable Players Under Pressure.
"""

import os
import json
import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="SupeRR Selector | Pressure Analytics Hub",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Rajasthan Royals Pink & Royal Purple)
st.markdown("""
<style>
    .main { background-color: #0E061C; color: #F8FAFC; }
    h1, h2, h3 { color: #EA1A85; font-weight: 800; }
    .kpi-card {
        background: linear-gradient(135deg, #1E1035, #2D1446);
        border: 1px solid rgba(234, 26, 133, 0.3);
        border-radius: 16px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .kpi-title { font-size: 0.8rem; color: #D8B4FE; font-weight: 600; text-transform: uppercase; }
    .kpi-value { font-size: 1.8rem; color: #FFFFFF; font-weight: 900; margin: 4px 0; }
    .kpi-sub { font-size: 0.75rem; color: #34D399; }
</style>
""", unsafe_allow_html=True)

# Load data
DASHBOARD_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(DASHBOARD_DIR, "data")

@st.cache_data
def load_data():
    with open(os.path.join(DATA_DIR, "rankings.json"), "r") as f:
        rankings = json.load(f)
    with open(os.path.join(DATA_DIR, "extras.json"), "r") as f:
        extras = json.load(f)
    return rankings, extras

rankings, extras = load_data()

# Sidebar
st.sidebar.image("https://raw.githubusercontent.com/feathericons/feather/master/icons/award.svg", width=50)
st.sidebar.title("SupeRR Selector")
st.sidebar.caption("Season 2 • Rajasthan Royals Analytics")
st.sidebar.markdown("---")

cohort = st.sidebar.radio(
    "Select Tournament Scope:",
    ["Combined (IPL + T20I)", "IPL Only", "T20I Only"],
    index=0
)
cohort_key = "overall" if "Combined" in cohort else ("ipl" if "IPL" in cohort else "t20i")

st.sidebar.markdown("---")
st.sidebar.info("""
**Round 1 Objective:**
Identify batters and bowlers who rise to the occasion under pressure compared to normal baseline.
""")

# Header Banner
st.title("🏏 SupeRR Selector Season 2: Pressure Analytics Hub")
st.markdown("##### Dynamic Win-Probability & Bayesian Clutch Modeling across 200,999 Deliveries")

# Top KPI Row
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.markdown('<div class="kpi-card"><div class="kpi-title">Deliveries Analyzed</div><div class="kpi-value">200,999</div><div class="kpi-sub">IPL & T20I (2022-26)</div></div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="kpi-card"><div class="kpi-title">Total Matches</div><div class="kpi-value">867</div><div class="kpi-sub">371 IPL / 512 T20I</div></div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="kpi-card"><div class="kpi-title">Pressure Balls</div><div class="kpi-value">60,311</div><div class="kpi-sub">30.0% with DPI > 0.60</div></div>', unsafe_allow_html=True)
with col4:
    top_bat = rankings[f"{cohort_key}_batters"][0]
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">#1 Clutch Batter</div><div class="kpi-value">{top_bat["player_name"]}</div><div class="kpi-sub">{top_bat["weighted_clutch"]:.3f} Weighted CF</div></div>', unsafe_allow_html=True)
with col5:
    top_bowl = rankings[f"{cohort_key}_bowlers"][0]
    st.markdown(f'<div class="kpi-card"><div class="kpi-title">#1 Clutch Bowler</div><div class="kpi-value">{top_bowl["player_name"]}</div><div class="kpi-sub">{top_bowl["weighted_clutch"]:.3f} Weighted CF</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Tabs: Rankings, Match Tension, Simulator, Methodology
tab_rank, tab_match, tab_sim, tab_doc = st.tabs([
    "🏆 Top 10 Official Rankings",
    "📈 Match Tension Simulator",
    "🎛️ Dynamic Pressure Calculator",
    "📖 Methodology & Documentation"
])

# ----------------- TAB 1: RANKINGS -----------------
with tab_rank:
    st.subheader(f"Top 10 Rankings Under Pressure ({cohort})")
    role_choice = st.radio("Select Role:", ["Batters (Dropdown Selections)", "Bowlers (Dropdown Selections)"], horizontal=True)

    if "Batters" in role_choice:
        bat_df = pd.DataFrame(rankings[f"{cohort_key}_batters"][:10])
        display_df = bat_df[[
            "rank", "player_name", "weighted_clutch", "clutch_factor",
            "pressure_sr", "baseline_sr", "pressure_batting_avg", "baseline_batting_avg",
            "pressure_balls"
        ]].copy()
        display_df.columns = [
            "Rank", "Player Name", "Weighted Clutch", "Raw Clutch",
            "Press. SR", "Base. SR", "Press. Avg", "Base. Avg", "Pressure Balls"
        ]
        st.dataframe(
            display_df.style.format({
                "Weighted Clutch": "{:.3f}",
                "Raw Clutch": "{:.3f}",
                "Press. SR": "{:.1f}",
                "Base. SR": "{:.1f}",
                "Press. Avg": "{:.1f}",
                "Base. Avg": "{:.1f}",
            }).background_gradient(subset=["Weighted Clutch"], cmap="PuRd"),
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            bat_df.set_index("player_name")[["pressure_sr", "baseline_sr"]],
            color=["#EA1A85", "#6B7280"]
        )

    else:
        bowl_df = pd.DataFrame(rankings[f"{cohort_key}_bowlers"][:10])
        display_df = bowl_df[[
            "rank", "player_name", "weighted_clutch", "clutch_factor",
            "pressure_economy", "baseline_economy", "pressure_bowling_strike_rate", "baseline_bowling_strike_rate",
            "pressure_balls"
        ]].copy()
        display_df.columns = [
            "Rank", "Player Name", "Weighted Clutch", "Raw Clutch",
            "Press. Econ", "Base. Econ", "Press. Bowl SR", "Base. Bowl SR", "Pressure Balls"
        ]
        st.dataframe(
            display_df.style.format({
                "Weighted Clutch": "{:.3f}",
                "Raw Clutch": "{:.3f}",
                "Press. Econ": "{:.2f}",
                "Base. Econ": "{:.2f}",
                "Press. Bowl SR": "{:.1f}",
                "Base. Bowl SR": "{:.1f}",
            }).background_gradient(subset=["Weighted Clutch"], cmap="PuRd"),
            use_container_width=True,
            hide_index=True
        )

        st.bar_chart(
            bowl_df.set_index("player_name")[["pressure_economy", "baseline_economy"]],
            color=["#EA1A85", "#6B7280"]
        )

# ----------------- TAB 2: MATCH TENSION -----------------
with tab_match:
    st.subheader("Match 39808: Ball-by-Ball Tension Evolution")
    curve_df = pd.DataFrame(extras["match_39808"])
    st.line_chart(
        curve_df.set_index("cum_balls")["dpi"],
        color="#EA1A85"
    )
    st.caption("Dynamic Pressure Index (DPI) tracks delivery-by-delivery swing. Peaks above 0.80 indicate extreme tension.")

# ----------------- TAB 3: SIMULATOR -----------------
with tab_sim:
    st.subheader("Dynamic Pressure Index (DPI) Live Engine")
    sim_col1, sim_col2 = st.columns([2, 1])

    with sim_col1:
        s_rrr = st.slider("Required Run Rate (RPO)", 4.0, 24.0, 11.5, 0.5)
        s_balls = st.slider("Legal Balls Remaining", 1, 120, 18, 1)
        s_wkts = st.slider("Wickets in Hand", 1, 10, 4, 1)
        s_ko = st.checkbox("Knockout / Playoff Match (1.30x)", value=True)
        s_mom = st.checkbox("Wicket Cluster in Last 6 Balls", value=True)

    with sim_col2:
        rpb = s_rrr / 6.0
        z = 0.5 + 3.5 * rpb - 0.35 * s_wkts
        win_prob = 1.0 / (1.0 + np.exp(z))
        base_press = 1.0 - 2.0 * abs(win_prob - 0.5)
        phase_m = 1.30 if s_balls <= 30 else 1.0
        stakes_m = 1.30 if s_ko else 1.0
        mom_m = 1.18 if s_mom else 1.0
        dpi = min(1.0, max(0.0, base_press * phase_m * stakes_m * mom_m))

        st.metric("Live Calculated DPI", f"{dpi:.3f}")
        if dpi > 0.80:
            st.error("Zone: EXTREME PRESSURE (> 0.80)")
        elif dpi > 0.60:
            st.warning("Zone: HIGH PRESSURE (0.60 - 0.80)")
        elif dpi > 0.40:
            st.info("Zone: MODERATE PRESSURE (0.40 - 0.60)")
        else:
            st.success("Zone: LOW PRESSURE (< 0.40)")

# ----------------- TAB 4: METHODOLOGY -----------------
with tab_doc:
    st.markdown("""
    ### 🔬 Scientific Methodology Summary
    1. **Knife-Edge Peak:** High pressure occurs when the game is unresolved ($P(Win) \\approx 0.50$).
    2. **Par-Score Matrix:** In the 1st innings, pressure tracks deviation from dynamic over-by-wicket par score expectations.
    3. **Multipliers:** Death overs (1.30x), Knockouts (1.30x), and recent momentum shocks.
    4. **4D Clutch Factor:** Strike Rate/Economy, Average, Boundary %, and Non-Dot scoring efficiency.
    5. **Empirical Bayes Shrinkage:** $N / (N + 50)$ sample-size prior ensures sustainable performance beats small-sample noise.
    """)

st.markdown("---")
st.caption("Rajasthan Royals SupeRR Selector Season 2 • Round 1 Analysis Pack")

