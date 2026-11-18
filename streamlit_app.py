"""
SupeRR Selector Season 2 — Streamlit Community Cloud Analytics App
===================================================================
Rajasthan Royals Hackathon: Identify the Most Reliable Players Under Pressure
"""

import os
import json
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Set Streamlit Page Config
st.set_page_config(
    page_title="SupeRR Selector | Rajasthan Royals Analytics",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom High-End Rajasthan Royals CSS
st.markdown("""
<style>
    /* Dark Theme with RR Accents */
    .stApp {
        background-color: #0D051B;
        color: #F8FAFC;
    }
    
    /* Header & Titles */
    h1, h2, h3 {
        color: #EA1A85 !important;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        font-weight: 800 !important;
    }
    
    /* KPI Card Component */
    .kpi-container {
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        background: linear-gradient(135deg, #1C0C35 0%, #2A1245 100%);
        border: 1px solid rgba(234, 26, 133, 0.35);
        border-radius: 18px;
        padding: 16px 12px;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        text-align: center;
        transition: transform 0.2s ease;
    }
    .kpi-container:hover {
        transform: translateY(-2px);
        border-color: #EA1A85;
    }
    .kpi-label {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #D8B4FE;
    }
    .kpi-val {
        font-size: 1.7rem;
        font-weight: 900;
        color: #FFFFFF;
        margin: 4px 0;
    }
    .kpi-desc {
        font-size: 0.7rem;
        color: #34D399;
        font-weight: 600;
    }

    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid rgba(234, 26, 133, 0.2);
    }
    .stTabs [data-baseweb="tab"] {
        padding: 10px 16px;
        font-weight: 700;
        color: #C084FC;
        border-radius: 8px 8px 0 0;
    }
    .stTabs [aria-selected="true"] {
        color: #EA1A85 !important;
        border-bottom: 3px solid #EA1A85 !important;
        background-color: rgba(234, 26, 133, 0.1) !important;
    }
</style>
""", unsafe_allow_html=True)

# Path resolution for local & Streamlit Cloud
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(ROOT_DIR, "dashboard", "data")
if not os.path.exists(DATA_DIR):
    DATA_DIR = os.path.join(ROOT_DIR, "data")

@st.cache_data
def load_all_data():
    rankings_file = os.path.join(DATA_DIR, "rankings.json")
    extras_file = os.path.join(DATA_DIR, "extras.json")
    
    with open(rankings_file, "r", encoding="utf-8") as f:
        rankings = json.load(f)
    with open(extras_file, "r", encoding="utf-8") as f:
        extras = json.load(f)
    return rankings, extras

rankings, extras = load_all_data()

# ==================== SIDEBAR ====================
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:12px;">
        <div style="background:linear-gradient(135deg, #EA1A85, #FF53A5); width:40px; height:40px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-weight:900; color:white; font-size:1.2rem; box-shadow:0 4px 12px rgba(234,26,133,0.4);">
            RR
        </div>
        <div>
            <h3 style="margin:0; font-size:1.1rem; color:white !important;">SupeRR Selector</h3>
            <p style="margin:0; font-size:0.75rem; color:#D8B4FE;">Rajasthan Royals Hackathon</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tournament Scope Filter
    cohort = st.radio(
        "🏆 Tournament Scope:",
        ["Combined (IPL + T20I)", "IPL Only", "T20I Only"],
        index=0,
        help="Select whether to evaluate player clutch performance across all data or specific tournament subsets."
    )
    cohort_key = "overall" if "Combined" in cohort else ("ipl" if "IPL" in cohort else "t20i")
    
    st.markdown("---")
    
    st.markdown("### 📥 Download Submissions")
    pptx_path = os.path.join(ROOT_DIR, "SupeRR_Selector_Season2_Presentation.pptx")
    pdf_path = os.path.join(ROOT_DIR, "SupeRR_Selector_Season2_Presentation.pdf")
    
    if os.path.exists(pptx_path):
        with open(pptx_path, "rb") as f:
            st.download_button(
                label="📊 Download Presentation (.pptx)",
                data=f,
                file_name="SupeRR_Selector_Season2_Presentation.pptx",
                mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                use_container_width=True
            )
            
    if os.path.exists(pdf_path):
        with open(pdf_path, "rb") as f:
            st.download_button(
                label="📄 Download Deck & Report (.pdf)",
                data=f,
                file_name="SupeRR_Selector_Season2_Presentation.pdf",
                mime="application/pdf",
                use_container_width=True
            )
            
    st.markdown("---")
    st.caption("SupeRR Selector Season 2 • Round 1\nVerified against 200,999 deliveries.")

# ==================== MAIN BANNER & KPIS ====================
st.markdown("""
<div style="margin-bottom: 20px;">
    <h1 style="margin: 0; font-size: 2.3rem;">🏏 SupeRR Selector: Pressure Analytics Hub</h1>
    <p style="color: #C084FC; font-size: 0.95rem; margin-top: 4px;">
        Identifying the Most Reliable Batters & Bowlers Under Pressure via Dynamic Win-Probability & Bayesian Clutch Modeling
    </p>
</div>
""", unsafe_allow_html=True)

# 6 Executive KPI Cards
top_bat = rankings[f"{cohort_key}_batters"][0]
top_bowl = rankings[f"{cohort_key}_bowlers"][0]

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

with kpi1:
    st.markdown('<div class="kpi-container"><div class="kpi-label">Deliveries</div><div class="kpi-val">201K</div><div class="kpi-desc">2022–2026 Seasons</div></div>', unsafe_allow_html=True)
with kpi2:
    st.markdown('<div class="kpi-container"><div class="kpi-label">Total Matches</div><div class="kpi-val">867</div><div class="kpi-desc">371 IPL / 512 T20I</div></div>', unsafe_allow_html=True)
with kpi3:
    st.markdown('<div class="kpi-container"><div class="kpi-label">Pressure Deliveries</div><div class="kpi-val">60.3K</div><div class="kpi-desc">30.0% with DPI > 0.60</div></div>', unsafe_allow_html=True)
with kpi4:
    st.markdown('<div class="kpi-container"><div class="kpi-label">Tracked Players</div><div class="kpi-val">1,217</div><div class="kpi-desc">Squad Verified</div></div>', unsafe_allow_html=True)
with kpi5:
    st.markdown(f'<div class="kpi-container"><div class="kpi-label">#1 Clutch Batter</div><div class="kpi-val" style="font-size:1.15rem; color:#EA1A85;">{top_bat["player_name"]}</div><div class="kpi-desc">{top_bat["weighted_clutch"]:.3f} Weighted CF</div></div>', unsafe_allow_html=True)
with kpi6:
    st.markdown(f'<div class="kpi-container"><div class="kpi-label">#1 Clutch Bowler</div><div class="kpi-val" style="font-size:1.15rem; color:#EA1A85;">{top_bowl["player_name"]}</div><div class="kpi-desc">{top_bowl["weighted_clutch"]:.3f} Weighted CF</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==================== MAIN TABS ====================
tab_official, tab_deck, tab_radar, tab_scatter, tab_tension, tab_calculator, tab_about = st.tabs([
    "🏆 Top 10 Official Rankings",
    "📽️ Official Submission Deck",
    "🕸️ Player Radar Comparison",
    "📊 Baseline vs Pressure Metrics",
    "📈 Ball-by-Ball Match Tension",
    "🎛️ Live DPI Calculator",
    "📖 Scientific Methodology"
])

# ----------------- TAB 1: OFFICIAL TOP 10 RANKINGS -----------------
with tab_official:
    st.subheader(f"Official Submission Rankings ({cohort})")
    st.caption("Exact rank order for the Unstop dropdown fields. Filtered with sample-size thresholds and Bayesian shrinkage.")
    
    role = st.radio("Select Role Category:", ["🏏 Top 10 Batters", "🎳 Top 10 Bowlers"], horizontal=True)
    
    search_q = st.text_input("🔍 Search Player in Candidates:", "", placeholder="Type player name...")
    
    if "Batters" in role:
        bat_list = rankings[f"{cohort_key}_batters"]
        if search_q:
            bat_list = [b for b in bat_list if search_q.lower() in b["player_name"].lower()]
        
        df_bat = pd.DataFrame(bat_list[:10])
        
        col_table, col_chart = st.columns([13, 7])
        
        with col_table:
            display_df = df_bat[[
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
            
        with col_chart:
            fig_sr = go.Figure()
            fig_sr.add_trace(go.Bar(
                y=df_bat["player_name"][::-1],
                x=df_bat["pressure_sr"][::-1],
                name="Pressure SR",
                orientation="h",
                marker=dict(color="#EA1A85")
            ))
            fig_sr.add_trace(go.Bar(
                y=df_bat["player_name"][::-1],
                x=df_bat["baseline_sr"][::-1],
                name="Baseline SR",
                orientation="h",
                marker=dict(color="rgba(168, 85, 247, 0.4)")
            ))
            fig_sr.update_layout(
                title="Strike Rate Shift (Pressure vs Baseline)",
                barmode="group",
                height=380,
                margin=dict(l=0, r=0, t=35, b=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E2E8F0", size=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_sr, use_container_width=True)

    else:
        bowl_list = rankings[f"{cohort_key}_bowlers"]
        if search_q:
            bowl_list = [b for b in bowl_list if search_q.lower() in b["player_name"].lower()]
            
        df_bowl = pd.DataFrame(bowl_list[:10])
        
        col_table, col_chart = st.columns([13, 7])
        
        with col_table:
            display_df = df_bowl[[
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
            
        with col_chart:
            fig_econ = go.Figure()
            fig_econ.add_trace(go.Bar(
                y=df_bowl["player_name"][::-1],
                x=df_bowl["pressure_economy"][::-1],
                name="Pressure Economy",
                orientation="h",
                marker=dict(color="#EA1A85")
            ))
            fig_econ.add_trace(go.Bar(
                y=df_bowl["player_name"][::-1],
                x=df_bowl["baseline_economy"][::-1],
                name="Baseline Economy",
                orientation="h",
                marker=dict(color="rgba(168, 85, 247, 0.4)")
            ))
            fig_econ.update_layout(
                title="Economy Shift (Lower is Better)",
                barmode="group",
                height=380,
                margin=dict(l=0, r=0, t=35, b=0),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#E2E8F0", size=10),
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_econ, use_container_width=True)


# ----------------- TAB 2: OFFICIAL PRESENTATION DECK -----------------
with tab_deck:
    st.subheader("📽️ Official Submission Presentation Deck (14 Slides)")
    st.caption("SupeRR Selector Season 2 — Dynamic Win-Probability & Bayesian Clutch Modeling (Rajasthan Royals Round 1)")
    
    # Download header buttons
    d_col1, d_col2, d_col3 = st.columns([1, 1, 2])
    with d_col1:
        if os.path.exists(pptx_path):
            with open(pptx_path, "rb") as f:
                st.download_button(
                    label="📊 Download Deck (.pptx)",
                    data=f,
                    file_name="SupeRR_Selector_Season2_Presentation.pptx",
                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation",
                    use_container_width=True,
                    key="deck_tab_pptx"
                )
    with d_col2:
        if os.path.exists(pdf_path):
            with open(pdf_path, "rb") as f:
                st.download_button(
                    label="📄 Download Submission (.pdf)",
                    data=f,
                    file_name="SupeRR_Selector_Season2_Presentation.pdf",
                    mime="application/pdf",
                    use_container_width=True,
                    key="deck_tab_pdf"
                )
    with d_col3:
        st.markdown(
            '<div style="text-align:right; font-size:0.85rem; color:#A7F3D0; padding-top:8px;">'
            '✅ Verified against 200,999 deliveries • 867 matches (IPL & T20I)'
            '</div>',
            unsafe_allow_html=True
        )
    
    st.markdown("---")
    
    slide_metadata = {
        1: {
            "title": "Slide 1: Executive Cover & Scope",
            "desc": "Problem Statement Title: Dynamic Win-Probability & Bayesian Clutch Modeling for Pressure-Performance Analytics in T20 Cricket. Data scope: 200,999 deliveries, 867 matches (IPL & T20I, 2022–2026)."
        },
        2: {
            "title": "Slide 2: Proposed Solution — Problem Statement & Challenges",
            "desc": "Cricket analytics proxies pressure with static heuristics (e.g. overs 16–20 = death overs). A team on 160/2 needing 15 off 18 balls faces negligible pressure, whereas 28/4 in over 5 chasing 190 faces extreme leverage. Static rules cannot tell them apart."
        },
        3: {
            "title": "Slide 3: Proposed Solution — Detailed Architectural Framework",
            "desc": "Dynamic Pressure Index (DPI 0.0–1.0) with win-probability knife-edge peak at 50/50 balance, par-score matrix for 1st innings, and multipliers for phase (1.30x), knockouts (1.30x), and momentum shocks (1.18x)."
        },
        4: {
            "title": "Slide 4: Innovation & Uniqueness of the Solution",
            "desc": "Symmetric pressure scoring both batting burden and bowling containment, ball-by-ball recalibration, 4D Clutch Factor, and Empirical Bayes shrinkage to prevent small-sample anomalies."
        },
        5: {
            "title": "Slide 5: Technical Strategy — Tools & Stack",
            "desc": "Vectorized Python 3 data pipeline with pandas & NumPy on 200,999 deliveries. Statistical modeling via SciPy, scikit-learn logistic regression, and Empirical Bayes shrinkage."
        },
        6: {
            "title": "Slide 6: Technical Strategy — End-to-End Methodology",
            "desc": "Three-phase execution pipeline: (1) Data Ingestion & Legal Ball Filtering, (2) Dynamic Win-Probability & DPI Calculation, (3) 4D Clutch Factor with Empirical Bayes Weighting."
        },
        7: {
            "title": "Slide 7: Mathematical Framework — DPI & Clutch Factor Formulas",
            "desc": "DPI = min(1.0, Base × M_phase × M_stakes × M_mom). Batting CF = 0.35·SR + 0.25·Avg + 0.20·Bnd% + 0.20·(1 - Dot%). Bowling CF = 0.30·Econ + 0.25·BowlSR + 0.25·Dot% + 0.20·(1 - Bnd%). Shrinkage Weight = N / (N + 50)."
        },
        8: {
            "title": "Slide 8: Results — Top 10 Batters Under Pressure",
            "desc": "Mahedi Hasan (1.592), Washington Sundar (1.304), Rajat Patidar (1.216), Rahul Tewatia (1.203), Ayush Badoni (1.188), Abishek Porel (1.126), Vaibhav Sooryavanshi (1.124), Devdutt Padikkal (1.069), David Warner (1.067), Towhid Hridoy (1.042)."
        },
        9: {
            "title": "Slide 9: Results — Top 10 Bowlers Under Pressure",
            "desc": "Ripon Mondol (1.689), Wellington Masakadza (1.614), Salman Mirza (1.569), Arshad Khan (1.482), Jimmy Neesham (1.481), Dunith Wellalage (1.449), Daniel Sams (1.430), Patrick Cummins (1.411), Shaheen Afridi (1.373), Richard Ngarava (1.367)."
        },
        10: {
            "title": "Slide 10: Results — Player Pressure Profile & Uplift Matrix",
            "desc": "Mahedi Hasan high-pressure zone strike rate and non-dot % uplift. Scatter plot displaying players above the diagonal who elevate performance under extreme tension."
        },
        11: {
            "title": "Slide 11: Official Submission — Official Top 10 Batters & Bowlers Table",
            "desc": "Final submission rankings for the Unstop form dropdowns. Contains exact Rank, Player Name, Weighted Clutch Factor, and Pressure Balls faced/bowled."
        },
        12: {
            "title": "Slide 12: Feasibility & Viability — Edge Cases & Mitigations",
            "desc": "Robustness verified across 50, 100, 150, 200 ball thresholds. Addresses Impact Player rule dynamics, attack strength weighting, and small-sample variance."
        },
        13: {
            "title": "Slide 13: Impact & Strategic Benefits for Rajasthan Royals",
            "desc": "Actionable scouting & auction intelligence: identifies true ice-in-the-veins finishers and death bowlers who peak when match win probability is on a knife edge."
        },
        14: {
            "title": "Slide 14: Academic References & Deliverables",
            "desc": "Duckworth & Lewis (1998), Carter & Guthrie (2004), Efron & Morris (1975) Stein estimator, Gelman et al. (2013) Bayesian Data Analysis."
        }
    }
    
    if "current_slide" not in st.session_state:
        st.session_state.current_slide = 11
        
    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([2, 5, 2, 2])
    
    with nav_col1:
        if st.button("◀ Previous Slide", use_container_width=True):
            st.session_state.current_slide = max(1, st.session_state.current_slide - 1)
            st.rerun()
            
    with nav_col2:
        slide_options = [f"Slide {i}: {slide_metadata[i]['title'].split(':', 1)[1].strip()}" for i in range(1, 15)]
        selected_option = st.selectbox(
            "Go to Slide:",
            slide_options,
            index=st.session_state.current_slide - 1,
            label_visibility="collapsed"
        )
        selected_num = int(selected_option.split(":")[0].replace("Slide", "").strip())
        if selected_num != st.session_state.current_slide:
            st.session_state.current_slide = selected_num
            st.rerun()
            
    with nav_col3:
        if st.button("Next Slide ▶", use_container_width=True):
            st.session_state.current_slide = min(14, st.session_state.current_slide + 1)
            st.rerun()
            
    with nav_col4:
        if st.button("🎯 Jump to Slide 11", use_container_width=True):
            st.session_state.current_slide = 11
            st.rerun()
            
    current_idx = st.session_state.current_slide
    slide_file = f"slide_{current_idx:02d}.png"
    slide_img_path = os.path.join(ROOT_DIR, "dashboard", "slides", slide_file)
    if not os.path.exists(slide_img_path):
        slide_img_path = os.path.join(ROOT_DIR, "slides", slide_file)
        
    if os.path.exists(slide_img_path):
        st.image(slide_img_path, use_container_width=True)
    else:
        st.warning(f"Slide image {slide_file} not found.")
        
    st.markdown(f'''
    <div style="background: linear-gradient(135deg, #1C0C35 0%, #2A1245 100%); border-left: 4px solid #EA1A85; border-radius: 8px; padding: 14px 18px; margin-top: 14px; box-shadow: 0 4px 16px rgba(0,0,0,0.3);">
        <h4 style="margin: 0 0 6px 0; color: #EA1A85 !important; font-size: 1.05rem;">{slide_metadata[current_idx]['title']}</h4>
        <p style="margin: 0; color: #E2E8F0; font-size: 0.9rem; line-height: 1.5;">{slide_metadata[current_idx]['desc']}</p>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.expander("📑 View All 14 Slide Thumbnails & Jump Directly", expanded=False):
        for row_start in range(1, 15, 4):
            cols = st.columns(4)
            for c_i, s_num in enumerate(range(row_start, min(row_start + 4, 15))):
                with cols[c_i]:
                    thumb_path = os.path.join(ROOT_DIR, "dashboard", "slides", f"slide_{s_num:02d}.png")
                    if not os.path.exists(thumb_path):
                        thumb_path = os.path.join(ROOT_DIR, "slides", f"slide_{s_num:02d}.png")
                    if os.path.exists(thumb_path):
                        st.image(thumb_path, caption=f"Slide {s_num}", use_container_width=True)
                    if st.button(f"Open Slide {s_num}", key=f"thumb_{s_num}", use_container_width=True):
                        st.session_state.current_slide = s_num
                        st.rerun()

# ----------------- TAB 2: PLAYER RADAR COMPARISON -----------------
with tab_radar:
    st.subheader("Interactive Multi-Dimensional Radar Comparison")
    st.caption("Select two players to compare how their skill profiles adapt to high-pressure situations.")
    
    radar_role = st.selectbox("Role Category:", ["Batters", "Bowlers"])
    
    if radar_role == "Batters":
        batters_data = rankings[f"{cohort_key}_batters"]
        b_names = [b["player_name"] for b in batters_data[:20]]
        
        c1, c2 = st.columns(2)
        with c1:
            p1_name = st.selectbox("Player 1:", b_names, index=0)
        with c2:
            p2_name = st.selectbox("Player 2:", b_names, index=min(1, len(b_names)-1))
            
        p1 = next(b for b in batters_data if b["player_name"] == p1_name)
        p2 = next(b for b in batters_data if b["player_name"] == p2_name)
        
        categories = ['Strike Rate Uplift', 'Average Preserved', 'Boundary Hitting', 'Strike Rotation', 'Experience / Volume']
        
        v1 = [
            min(100, max(20, (p1["pressure_sr"] / (p1["baseline_sr"] or 1)) * 50)),
            min(100, max(20, (p1["pressure_batting_avg"] / (p1["baseline_batting_avg"] or 1)) * 50)),
            min(100, max(20, (p1["pressure_boundary_pct"] / (p1["baseline_boundary_pct"] or 0.1)) * 50)),
            min(100, max(20, ((1 - p1["pressure_dot_ball_pct"]) / (1 - (p1["baseline_dot_ball_pct"] or 0.5))) * 50)),
            min(95, 50 + (p1["pressure_balls"] / 8))
        ]
        
        v2 = [
            min(100, max(20, (p2["pressure_sr"] / (p2["baseline_sr"] or 1)) * 50)),
            min(100, max(20, (p2["pressure_batting_avg"] / (p2["baseline_batting_avg"] or 1)) * 50)),
            min(100, max(20, (p2["pressure_boundary_pct"] / (p2["baseline_boundary_pct"] or 0.1)) * 50)),
            min(100, max(20, ((1 - p2["pressure_dot_ball_pct"]) / (1 - (p2["baseline_dot_ball_pct"] or 0.5))) * 50)),
            min(95, 50 + (p2["pressure_balls"] / 8))
        ]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=v1, theta=categories, fill='toself', name=p1_name, line_color="#EA1A85"))
        fig_radar.add_trace(go.Scatterpolar(r=v2, theta=categories, fill='toself', name=p2_name, line_color="#38BDF8"))
        fig_radar.add_trace(go.Scatterpolar(r=[50]*5, theta=categories, name='Neutral Baseline (1.0)', line=dict(color='rgba(255,255,255,0.3)', dash='dot')))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=False, range=[0, 100]),
                bgcolor="rgba(0,0,0,0)"
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E2E8F0"),
            height=450
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        
    else:
        bowlers_data = rankings[f"{cohort_key}_bowlers"]
        b_names = [b["player_name"] for b in bowlers_data[:20]]
        
        c1, c2 = st.columns(2)
        with c1:
            p1_name = st.selectbox("Bowler 1:", b_names, index=0)
        with c2:
            p2_name = st.selectbox("Bowler 2:", b_names, index=min(1, len(b_names)-1))
            
        p1 = next(b for b in bowlers_data if b["player_name"] == p1_name)
        p2 = next(b for b in bowlers_data if b["player_name"] == p2_name)
        
        categories = ['Economy Slashed', 'Wicket Frequency (SR)', 'Dot Ball Building', 'Boundary Suppression', 'Sample Volume']
        
        v1 = [
            min(100, max(20, (p1["baseline_economy"] / (p1["pressure_economy"] or 1)) * 50)),
            min(100, max(20, (p1["baseline_bowling_strike_rate"] / (p1["pressure_bowling_strike_rate"] or 1)) * 50)),
            min(100, max(20, (p1["pressure_dot_ball_pct"] / (p1["baseline_dot_ball_pct"] or 0.2)) * 50)),
            min(100, max(20, ((1 - p1["pressure_boundaries_conceded_pct"]) / (1 - (p1["baseline_boundaries_conceded_pct"] or 0.2))) * 50)),
            min(95, 50 + (p1["pressure_balls"] / 8))
        ]
        
        v2 = [
            min(100, max(20, (p2["baseline_economy"] / (p2["pressure_economy"] or 1)) * 50)),
            min(100, max(20, (p2["baseline_bowling_strike_rate"] / (p2["pressure_bowling_strike_rate"] or 1)) * 50)),
            min(100, max(20, (p2["pressure_dot_ball_pct"] / (p2["baseline_dot_ball_pct"] or 0.2)) * 50)),
            min(100, max(20, ((1 - p2["pressure_boundaries_conceded_pct"]) / (1 - (p2["baseline_boundaries_conceded_pct"] or 0.2))) * 50)),
            min(95, 50 + (p2["pressure_balls"] / 8))
        ]
        
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=v1, theta=categories, fill='toself', name=p1_name, line_color="#EA1A85"))
        fig_radar.add_trace(go.Scatterpolar(r=v2, theta=categories, fill='toself', name=p2_name, line_color="#38BDF8"))
        fig_radar.add_trace(go.Scatterpolar(r=[50]*5, theta=categories, name='Neutral Baseline (1.0)', line=dict(color='rgba(255,255,255,0.3)', dash='dot')))
        
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(visible=False, range=[0, 100]),
                bgcolor="rgba(0,0,0,0)"
            ),
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E2E8F0"),
            height=450
        )
        st.plotly_chart(fig_radar, use_container_width=True)

# ----------------- TAB 3: SCATTER PLOTS -----------------
with tab_scatter:
    st.subheader("Baseline vs Pressure Scatter Analysis")
    st.caption("Points above the diagonal line indicate players whose performance ELEVATES under pressure.")
    
    bat_all = pd.DataFrame(rankings[f"{cohort_key}_batters"])
    
    fig_scat = px.scatter(
        bat_all,
        x="baseline_sr",
        y="pressure_sr",
        size="pressure_balls",
        hover_name="player_name",
        hover_data=["weighted_clutch", "clutch_factor", "pressure_batting_avg"],
        text="player_name",
        labels={"baseline_sr": "Normal Baseline Strike Rate", "pressure_sr": "High Pressure Strike Rate"},
        title="Batter Strike Rate Elevation (Bubble Size = Pressure Deliveries)",
        color="weighted_clutch",
        color_continuous_scale="Purples"
    )
    # Add diagonal line x = y
    fig_scat.add_shape(
        type="line", line=dict(dash='dash', color='rgba(234, 26, 133, 0.7)', width=2),
        x0=80, y0=80, x1=230, y1=230
    )
    fig_scat.update_traces(textposition='top center')
    fig_scat.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E2E8F0"),
        height=500
    )
    st.plotly_chart(fig_scat, use_container_width=True)

# ----------------- TAB 4: MATCH TENSION -----------------
with tab_tension:
    st.subheader("Match Tension Curve Simulator (Match 39808)")
    st.caption("Ball-by-ball Dynamic Pressure Index (DPI) evolution in a high-volatility T20 thriller.")
    
    curve_df = pd.DataFrame(extras["match_39808"])
    
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=curve_df["cum_balls"],
        y=curve_df["dpi"],
        mode="lines",
        line=dict(color="#EA1A85", width=2.5),
        fill='tozeroy',
        fillcolor="rgba(234, 26, 133, 0.15)",
        text=[f"Over {r['over']}.{r['ball']} ({r['score']})<br>{r['striker']} vs {r['bowler']}<br>Outcome: {'WICKET' if r['is_wicket'] else str(r['runs'])+' runs'}" for _, r in curve_df.iterrows()],
        hoverinfo="text+y"
    ))
    
    # Pressure threshold markers
    fig_line.add_hline(y=0.80, line_dash="dash", line_color="#EF4444", annotation_text="Extreme Pressure Zone (>0.80)")
    fig_line.add_hline(y=0.60, line_dash="dash", line_color="#F97316", annotation_text="High Pressure Threshold (0.60)")
    
    fig_line.update_layout(
        title="Match 39808: Tension Curve Across Legal Deliveries",
        xaxis_title="Cumulative Legal Deliveries",
        yaxis_title="Dynamic Pressure Index (DPI)",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#E2E8F0"),
        height=450
    )
    st.plotly_chart(fig_line, use_container_width=True)

# ----------------- TAB 5: LIVE DPI CALCULATOR -----------------
with tab_calculator:
    st.subheader("Interactive Dynamic Pressure Index (DPI) Engine")
    st.caption("Adjust match parameters to see how the mathematical win-probability engine calculates tension.")
    
    c_left, c_right = st.columns([12, 8])
    
    with c_left:
        c_rrr = st.slider("Required Run Rate (RPO)", 4.0, 24.0, 11.5, 0.5)
        c_balls = st.slider("Legal Balls Remaining", 1, 120, 18, 1)
        c_wkts = st.slider("Wickets in Hand (Chasing Team)", 1, 10, 4, 1)
        c_ko = st.checkbox("Knockout / Playoff Fixture (1.30x Multiplier)", value=True)
        c_cluster = st.checkbox("Wicket Fallen or Scoring Freeze in Last 6 Balls", value=True)
        
    with c_right:
        rpb = c_rrr / 6.0
        z = 0.5 + 3.5 * rpb - 0.35 * c_wkts
        win_prob = 1.0 / (1.0 + np.exp(z))
        base_press = 1.0 - 2.0 * abs(win_prob - 0.5)
        phase_m = 1.30 if c_balls <= 30 else 1.0
        stakes_m = 1.30 if c_ko else 1.0
        mom_m = 1.18 if c_cluster else 1.0
        dpi = min(1.0, max(0.0, base_press * phase_m * stakes_m * mom_m))
        
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = dpi,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Calculated DPI", 'font': {'size': 20, 'color': '#EA1A85'}},
            gauge = {
                'axis': {'range': [0, 1], 'tickwidth': 1, 'tickcolor': "white"},
                'bar': {'color': "#EA1A85"},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "gray",
                'steps': [
                    {'range': [0, 0.40], 'color': 'rgba(56, 189, 248, 0.3)'},
                    {'range': [0.40, 0.60], 'color': 'rgba(251, 191, 36, 0.3)'},
                    {'range': [0.60, 0.80], 'color': 'rgba(249, 115, 22, 0.3)'},
                    {'range': [0.80, 1.0], 'color': 'rgba(239, 68, 68, 0.3)'}
                ]
            }
        ))
        fig_gauge.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#E2E8F0"),
            height=280,
            margin=dict(l=20, r=20, t=30, b=20)
        )
        st.plotly_chart(fig_gauge, use_container_width=True)
        
        if dpi > 0.80:
            st.error(f"🔥 Zone: EXTREME PRESSURE ({dpi:.3f})\nGame on a knife-edge; maximum stakes.")
        elif dpi > 0.60:
            st.warning(f"⚡ Zone: HIGH PRESSURE ({dpi:.3f})\nOutcome unresolved; high leverage on every delivery.")
        elif dpi > 0.40:
            st.info(f"⚖️ Zone: MODERATE PRESSURE ({dpi:.3f})\nStandard chase situation.")
        else:
            st.success(f"🍃 Zone: LOW PRESSURE ({dpi:.3f})\nOne-sided match; minimal tension.")

# ----------------- TAB 6: SCIENTIFIC METHODOLOGY -----------------
with tab_about:
    st.markdown("""
    ### 🔬 Architectural Framework
    
    #### 1. Dynamic Pressure Index (DPI)
    - **Knife-Edge Principle:** Pressure is maximum when match win probability is closest to 50/50: $\\text{Balance} = 1.0 - 2.0 \\times |P(\\text{Win}) - 0.50|$.
    - **1st Innings Par-Score Matrix:** Tracks state-dependent deviations from projected scores based on overs and wickets fallen.
    - **Multipliers:** Death overs ($1.30\\times$), Playoffs/Knockouts ($1.30\\times$), and Wicket shocks ($1.18\\times$).
    
    #### 2. Multi-Dimensional Clutch Factor (CF)
    $$\\text{CF}_{\\text{bat}} = 0.35 \\left(\\frac{\\text{SR}_p}{\\text{SR}_b}\\right) + 0.25 \\left(\\frac{\\text{Avg}_p}{\\text{Avg}_b}\\right) + 0.20 \\left(\\frac{\\text{Bnd\\%}_p}{\\text{Bnd\\%}_b}\\right) + 0.20 \\left(\\frac{1 - \\text{Dot\\%}_p}{1 - \\text{Dot\\%}_b}\\right)$$
    - Baseline performance produces $\\text{CF} \\equiv 1.000$ identically.
    - Scoring efficiency $(1 - \\text{Dot\\%})$ measures ability to rotate strike and avoid dot-ball pressure.
    
    #### 3. Empirical Bayes Regularization
    $$\\text{Weight} = \\frac{N_p}{N_p + 50}, \\quad \\text{Weighted CF} = 1.0 + (\\text{CF} - 1.0) \\times \\text{Weight}$$
    - Pulls small-sample volatility toward the neutral baseline to prevent flash-in-the-pan anomalies.
    - Eligibility threshold: $\\ge 100$ pressure balls and $\\ge 200$ total balls logged.
    """)

st.markdown("---")
st.caption("Rajasthan Royals SupeRR Selector Season 2 • Round 1 Submission Dashboard")

