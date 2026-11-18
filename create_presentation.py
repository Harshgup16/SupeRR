"""
create_presentation.py — Generates ultra-high-resolution, professional
presentation decks in BOTH 9:16 (vertical mobile/story) and 16:9 (widescreen)
formats for SupeRR Selector Season 2.
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image
import fitz  # PyMuPDF
from pptx import Presentation
from pptx.util import Inches as PptxInches, Pt as PptxPt

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
SLIDES_9X16_DIR = os.path.join(PROJECT_ROOT, "presentation_slides_9x16")
SLIDES_16X9_DIR = os.path.join(PROJECT_ROOT, "presentation_slides_16x9")
os.makedirs(SLIDES_9X16_DIR, exist_ok=True)
os.makedirs(SLIDES_16X9_DIR, exist_ok=True)

# Colors
BG_COLOR = "#0A0316"
CARD_BG = "#16092C"
CARD_BORDER = "#35165E"
RR_PINK = "#EA1A85"
RR_MAGENTA = "#FF3399"
GOLD = "#F59E0B"
EMERALD = "#10B981"
CYAN = "#38BDF8"
WHITE = "#FFFFFF"
PURPLE_LIGHT = "#D8B4FE"
PURPLE_MUTED = "#8B5CF6"
GRAY = "#94A3B8"

def draw_rounded_card(ax, x, y, w, h, bg=CARD_BG, border=CARD_BORDER, lw=1.2, radius=0.03):
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=bg, edgecolor=border, linewidth=lw, zorder=2
    )
    ax.add_patch(box)
    return box

# ==============================================================================
# 9:16 VERTICAL SLIDES GENERATION
# ==============================================================================
def create_vertical_slide_1():
    fig, ax = plt.subplots(figsize=(9, 16), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 16)
    ax.axis('off')

    # Accent glow top
    glow = patches.Circle((4.5, 14.5), 3.5, facecolor="#EA1A85", alpha=0.15, zorder=1)
    ax.add_patch(glow)

    # Top Tag
    draw_rounded_card(ax, 2.0, 14.7, 5.0, 0.6, bg="#2A0F45", border=RR_PINK, radius=0.08)
    ax.text(4.5, 15.0, "RAJASTHAN ROYALS  •  SUPERR SELECTOR S2", color=WHITE,
            fontsize=11, fontweight='black', ha='center', va='center', zorder=3)

    # Main Title
    ax.text(4.5, 13.5, "CRACKING\nCRICKET'S\nCRUCIBLE", color=WHITE,
            fontsize=36, fontweight='black', ha='center', va='center', linespacing=0.9, zorder=3)
    ax.text(4.5, 11.5, "Identifying The Most Reliable Players Under Pressure", color=RR_PINK,
            fontsize=15, fontweight='bold', ha='center', va='center', zorder=3)
    ax.text(4.5, 10.9, "Dynamic Win-Probability & Bayesian Clutch Modeling", color=PURPLE_LIGHT,
            fontsize=11, ha='center', va='center', zorder=3)

    # Big Divider
    ax.plot([1.5, 7.5], [10.4, 10.4], color=RR_PINK, lw=2, zorder=3)

    # 4 Key Metrics Cards
    kpis = [
        ("200,999", "DELIVERIES ANALYZED", "2022–2026 IPL + T20I", WHITE),
        ("867", "MATCHES MODELLED", "371 IPL / 512 T20I", CYAN),
        ("60,311", "PRESSURE DELIVERIES", "30.0% WITH DPI > 0.60", RR_PINK),
        ("1,217", "SQUAD-MAPPED PLAYERS", "158 ELIGIBLE BATTERS", GOLD)
    ]
    for i, (val, lbl, sub, col) in enumerate(kpis):
        y_pos = 8.6 - (i * 1.5)
        draw_rounded_card(ax, 1.0, y_pos, 7.0, 1.25, radius=0.05)
        ax.text(1.5, y_pos + 0.65, val, color=col, fontsize=24, fontweight='black', va='center', zorder=3)
        ax.text(4.0, y_pos + 0.8, lbl, color=WHITE, fontsize=11, fontweight='bold', va='center', zorder=3)
        ax.text(4.0, y_pos + 0.45, sub, color=PURPLE_LIGHT, fontsize=9, va='center', zorder=3)

    # Bottom Submission Ready Pill
    draw_rounded_card(ax, 1.0, 1.0, 7.0, 1.2, bg="#1E0E38", border=EMERALD, radius=0.06)
    ax.text(4.5, 1.75, "✓ OFFICIAL ROUND 1 SUBMISSION READY", color=EMERALD,
            fontsize=12, fontweight='black', ha='center', va='center', zorder=3)
    ax.text(4.5, 1.35, "Full Dropdown Picks  •  PDF Report  •  Live Streamlit App", color=WHITE,
            fontsize=9.5, ha='center', va='center', zorder=3)

    plt.tight_layout()
    path = os.path.join(SLIDES_9X16_DIR, "slide_01_cover.png")
    fig.savefig(path, dpi=200, facecolor=BG_COLOR)
    plt.close(fig)
    return path

def create_vertical_slide_2():
    fig, ax = plt.subplots(figsize=(9, 16), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 16)
    ax.axis('off')

    # Header
    ax.text(0.8, 15.0, "02  •  THE PHILOSOPHY", color=RR_PINK, fontsize=11, fontweight='bold')
    ax.text(0.8, 14.3, "Rethinking Pressure in T20", color=WHITE, fontsize=24, fontweight='black')
    ax.text(0.8, 13.7, "Why 'Death Overs = Pressure' is fundamentally broken", color=GRAY, fontsize=11)

    # Comparison 1: The Flaw
    draw_rounded_card(ax, 0.8, 10.6, 7.4, 2.6, bg="#1B0C2E", border="#EF4444", radius=0.04)
    ax.text(1.2, 12.7, "❌ THE BLUNT APPROACH", color="#EF4444", fontsize=11, fontweight='black', zorder=3)
    ax.text(1.2, 12.0, "• Labels all overs 16–20 as 'pressure' by default.", color=WHITE, fontsize=10.5, zorder=3)
    ax.text(1.2, 11.4, "• Flaw: 160/2 needing 15 off 18 balls has ZERO pressure.", color=GRAY, fontsize=10, zorder=3)
    ax.text(1.2, 10.9, "• Ignores early collapses (e.g. 28/4 in over 5 chasing 190).", color=GRAY, fontsize=10, zorder=3)

    # Comparison 2: Our Innovation
    draw_rounded_card(ax, 0.8, 6.8, 7.4, 3.4, bg="#131B2E", border=CYAN, radius=0.04)
    ax.text(1.2, 9.7, "✓ OUR SOLUTION: THE DYNAMIC PRESSURE INDEX", color=CYAN, fontsize=11, fontweight='black', zorder=3)
    ax.text(1.2, 9.0, "1. Knife-Edge Maximum (2nd Innings):", color=WHITE, fontsize=10.5, fontweight='bold', zorder=3)
    ax.text(1.4, 8.5, "Tension peaks at 50/50 win prob:  1.0 - 2|P(Win) - 0.50|", color=PURPLE_LIGHT, fontsize=9.5, zorder=3)
    ax.text(1.2, 7.9, "2. Par-Score Deviations (1st Innings):", color=WHITE, fontsize=10.5, fontweight='bold', zorder=3)
    ax.text(1.4, 7.4, "Departure from state-dependent par matrix (overs × wickets)", color=PURPLE_LIGHT, fontsize=9.5, zorder=3)

    # 3 Multipliers Box
    draw_rounded_card(ax, 0.8, 2.6, 7.4, 3.8, radius=0.04)
    ax.text(1.2, 5.9, "CONTEXTUAL LEVERAGE MULTIPLIERS", color=GOLD, fontsize=11, fontweight='black', zorder=3)

    mults = [
        ("Phase Multiplier (1.30x)", "Death overs (16–20) amplify tension when stakes are close.", RR_PINK),
        ("Knockout Stakes (1.30x)", "Playoffs, Semi-Finals, and Finals carry mental leverage.", CYAN),
        ("Momentum Shock (up to 1.35x)", "Wicket clusters (+0.08 per wkt) or scoring stalls in last 6 balls.", EMERALD)
    ]
    for i, (title, desc, col) in enumerate(mults):
        yp = 5.2 - (i * 0.95)
        ax.text(1.2, yp, f"• {title}", color=col, fontsize=10.5, fontweight='bold', zorder=3)
        ax.text(1.4, yp - 0.35, desc, color=WHITE, fontsize=9, zorder=3)

    # Footer note
    draw_rounded_card(ax, 0.8, 1.0, 7.4, 1.2, bg="#1E0E38", border=RR_PINK, radius=0.04)
    ax.text(4.5, 1.6, "DPI is continuous (0.0 to 1.0) on all 200,999 balls", color=WHITE, fontsize=10.5, fontweight='bold', ha='center', zorder=3)

    plt.tight_layout()
    path = os.path.join(SLIDES_9X16_DIR, "slide_02_philosophy.png")
    fig.savefig(path, dpi=200, facecolor=BG_COLOR)
    plt.close(fig)
    return path

def create_vertical_slide_3():
    fig, ax = plt.subplots(figsize=(9, 16), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 16)
    ax.axis('off')

    # Header
    ax.text(0.8, 15.0, "03  •  UNSTOP SUBMISSION", color=RR_PINK, fontsize=11, fontweight='bold')
    ax.text(0.8, 14.3, "Top 10 Batters Under Pressure", color=WHITE, fontsize=23, fontweight='black')
    ax.text(0.8, 13.7, "Rank-ordered selections for Unstop dropdowns", color=GRAY, fontsize=11)

    # Highlight Card #1
    draw_rounded_card(ax, 0.8, 11.8, 7.4, 1.65, bg="#260C38", border=RR_PINK, radius=0.04)
    ax.text(1.2, 13.0, "#1 PICK  •  MAHEDI HASAN", color=GOLD, fontsize=12, fontweight='black', zorder=3)
    ax.text(1.2, 12.4, "Strike Rate: 81.5 → 131.4 (+61%)  |  Avg: 10.0 → 22.1 (+121%)", color=WHITE, fontsize=9.5, fontweight='bold', zorder=3)
    ax.text(1.2, 12.0, "Fearless lower-order finisher. Rises exponentially when team is behind par.", color=PURPLE_LIGHT, fontsize=8.5, zorder=3)

    # Batters List (2 to 10)
    batters = [
        ("2", "Washington Sundar", "1.304", "142.9 (vs 139.0)", "55.0 (vs 21.5)", "154"),
        ("3", "Rajat Patidar", "1.216", "149.0 (vs 172.9)", "96.3 (vs 30.5)", "194"),
        ("4", "Rahul Tewatia", "1.203", "152.1 (vs 148.4)", "44.5 (vs 21.5)", "117"),
        ("5", "Ayush Badoni", "1.188", "123.0 (vs 145.6)", "93.5 (vs 23.1)", "152"),
        ("6", "Abishek Porel", "1.126", "124.1 (vs 153.5)", "45.0 (vs 21.0)", "145"),
        ("7", "Vaibhav Sooryavanshi", "1.124", "227.5 (vs 221.4)", "57.1 (vs 36.7)", "276"),
        ("8", "Devdutt Padikkal", "1.069", "128.7 (vs 142.9)", "34.5 (vs 22.1)", "268"),
        ("9", "David Warner", "1.067", "132.0 (vs 151.9)", "62.4 (vs 36.1)", "378"),
        ("10", "Towhid Hridoy", "1.042", "108.9 (vs 131.1)", "49.0 (vs 28.0)", "225")
    ]

    for i, (rk, name, cf, sr, avg, balls) in enumerate(batters):
        yp = 10.6 - (i * 1.05)
        draw_rounded_card(ax, 0.8, yp, 7.4, 0.95, radius=0.03)
        ax.text(1.2, yp + 0.48, f"#{rk}", color=RR_PINK, fontsize=12, fontweight='black', zorder=3)
        ax.text(1.8, yp + 0.48, name, color=WHITE, fontsize=11, fontweight='bold', zorder=3)
        ax.text(5.5, yp + 0.58, f"SR: {sr}", color=PURPLE_LIGHT, fontsize=8.5, zorder=3)
        ax.text(5.5, yp + 0.28, f"Avg: {avg}", color=GRAY, fontsize=8, zorder=3)
        ax.text(7.6, yp + 0.48, f"CF {cf}", color=EMERALD, fontsize=10, fontweight='bold', zorder=3)

    plt.tight_layout()
    path = os.path.join(SLIDES_9X16_DIR, "slide_03_top_batters.png")
    fig.savefig(path, dpi=200, facecolor=BG_COLOR)
    plt.close(fig)
    return path

def create_vertical_slide_4():
    fig, ax = plt.subplots(figsize=(9, 16), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 16)
    ax.axis('off')

    # Header
    ax.text(0.8, 15.0, "04  •  UNSTOP SUBMISSION", color=RR_PINK, fontsize=11, fontweight='bold')
    ax.text(0.8, 14.3, "Top 10 Bowlers Under Pressure", color=WHITE, fontsize=23, fontweight='black')
    ax.text(0.8, 13.7, "Rank-ordered selections for Unstop dropdowns", color=GRAY, fontsize=11)

    # Highlight Card #1
    draw_rounded_card(ax, 0.8, 11.8, 7.4, 1.65, bg="#260C38", border=CYAN, radius=0.04)
    ax.text(1.2, 13.0, "#1 PICK  •  RIPON MONDOL", color=CYAN, fontsize=12, fontweight='black', zorder=3)
    ax.text(1.2, 12.4, "Economy: 11.51 → 5.48 (-52%)  |  Strike Rate: 14.2 → 8.3", color=WHITE, fontsize=9.5, fontweight='bold', zorder=3)
    ax.text(1.2, 12.0, "Elite death execution: 51.3% dot balls under pressure across 150 balls.", color=PURPLE_LIGHT, fontsize=8.5, zorder=3)

    # Bowlers List (2 to 10)
    bowlers = [
        ("2", "Wellington Masakadza", "1.614", "5.43 (vs 8.86)", "17.8 (vs 60.4)", "178"),
        ("3", "Salman Mirza", "1.569", "5.29 (vs 9.87)", "12.0 (vs 24.8)", "204"),
        ("4", "Arshad Khan", "1.482", "6.15 (vs 13.47)", "20.0 (vs 18.4)", "120"),
        ("5", "Jimmy Neesham", "1.481", "6.62 (vs 9.71)", "6.6 (vs 20.0)", "106"),
        ("6", "Dunith Wellalage", "1.449", "6.09 (vs 9.74)", "10.7 (vs 22.7)", "128"),
        ("7", "Daniel Sams", "1.430", "6.71 (vs 11.31)", "16.2 (vs 28.8)", "178"),
        ("8", "Patrick Cummins", "1.411", "6.80 (vs 10.40)", "15.3 (vs 21.5)", "336"),
        ("9", "Shaheen Afridi", "1.373", "5.99 (vs 10.01)", "12.8 (vs 16.4)", "434"),
        ("10", "Richard Ngarava", "1.367", "6.44 (vs 9.44)", "15.8 (vs 24.1)", "316")
    ]

    for i, (rk, name, cf, econ, sr, balls) in enumerate(bowlers):
        yp = 10.6 - (i * 1.05)
        draw_rounded_card(ax, 0.8, yp, 7.4, 0.95, radius=0.03)
        ax.text(1.2, yp + 0.48, f"#{rk}", color=CYAN, fontsize=12, fontweight='black', zorder=3)
        ax.text(1.8, yp + 0.48, name, color=WHITE, fontsize=11, fontweight='bold', zorder=3)
        ax.text(5.5, yp + 0.58, f"Econ: {econ}", color=PURPLE_LIGHT, fontsize=8.5, zorder=3)
        ax.text(5.5, yp + 0.28, f"Bowl SR: {sr}", color=GRAY, fontsize=8, zorder=3)
        ax.text(7.6, yp + 0.48, f"CF {cf}", color=EMERALD, fontsize=10, fontweight='bold', zorder=3)

    plt.tight_layout()
    path = os.path.join(SLIDES_9X16_DIR, "slide_04_top_bowlers.png")
    fig.savefig(path, dpi=200, facecolor=BG_COLOR)
    plt.close(fig)
    return path

def create_vertical_slide_5():
    fig, ax = plt.subplots(figsize=(9, 16), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 16)
    ax.axis('off')

    # Header
    ax.text(0.8, 15.0, "05  •  THE MATHEMATICS", color=RR_PINK, fontsize=11, fontweight='bold')
    ax.text(0.8, 14.3, "The 4D Clutch Factor", color=WHITE, fontsize=24, fontweight='black')
    ax.text(0.8, 13.7, "Normalized rating equations & Bayesian Shrinkage", color=GRAY, fontsize=11)

    # Batting Formula Card
    draw_rounded_card(ax, 0.8, 9.8, 7.4, 3.5, radius=0.04)
    ax.text(1.2, 12.7, "🏏 BATTING CLUTCH FORMULA", color=RR_PINK, fontsize=11, fontweight='black', zorder=3)
    ax.text(1.2, 12.0, "CF_bat = 0.35 × (SR_press / SR_base) +", color=WHITE, fontsize=10, fontweight='bold', zorder=3)
    ax.text(2.0, 11.5, "0.25 × (Avg_press / Avg_base) +", color=WHITE, fontsize=10, fontweight='bold', zorder=3)
    ax.text(2.0, 11.0, "0.20 × (Bnd%_press / Bnd%_base) +", color=WHITE, fontsize=10, fontweight='bold', zorder=3)
    ax.text(2.0, 10.5, "0.20 × ((1 - Dot%_press) / (1 - Dot%_base))", color=WHITE, fontsize=10, fontweight='bold', zorder=3)
    ax.text(1.2, 10.0, "• Identical baseline produces CF ≡ 1.000 exactly.", color=EMERALD, fontsize=9, zorder=3)

    # Bowling Formula Card
    draw_rounded_card(ax, 0.8, 5.8, 7.4, 3.5, radius=0.04)
    ax.text(1.2, 8.7, "🎳 BOWLING CLUTCH FORMULA", color=CYAN, fontsize=11, fontweight='black', zorder=3)
    ax.text(1.2, 8.0, "CF_bowl = 0.30 × (Econ_base / Econ_press) +", color=WHITE, fontsize=10, fontweight='bold', zorder=3)
    ax.text(2.1, 7.5, "0.25 × (SR_base / SR_press) +", color=WHITE, fontsize=10, fontweight='bold', zorder=3)
    ax.text(2.1, 7.0, "0.25 × (Dot%_press / Dot%_base) +", color=WHITE, fontsize=10, fontweight='bold', zorder=3)
    ax.text(2.1, 6.5, "0.20 × ((1 - Bnd_press) / (1 - Bnd_base))", color=WHITE, fontsize=10, fontweight='bold', zorder=3)
    ax.text(1.2, 6.0, "• Inverted ratios: lower runs conceded = higher rating.", color=EMERALD, fontsize=9, zorder=3)

    # Empirical Bayes Shrinkage Card
    draw_rounded_card(ax, 0.8, 1.2, 7.4, 4.2, bg="#1D0E36", border=GOLD, radius=0.04)
    ax.text(1.2, 4.8, "🔬 EMPIRICAL BAYES SHRINKAGE", color=GOLD, fontsize=11, fontweight='black', zorder=3)
    ax.text(1.2, 4.1, "Weighted_CF = 1.0 + (CF - 1.0) × Weight", color=WHITE, fontsize=10.5, fontweight='bold', zorder=3)
    ax.text(1.2, 3.5, "Weight = Pressure_Balls / (Pressure_Balls + 50)", color=CYAN, fontsize=10, fontweight='bold', zorder=3)
    ax.text(1.2, 2.9, "Why this matters:", color=WHITE, fontsize=9.5, fontweight='bold', zorder=3)
    ax.text(1.2, 2.4, "• Pulls small-sample volatility (e.g. 2 lucky sixes) to 1.0.", color=GRAY, fontsize=9, zorder=3)
    ax.text(1.2, 1.9, "• Sustained performers over 100+ balls dominate cleanly.", color=GRAY, fontsize=9, zorder=3)
    ax.text(1.2, 1.4, "• Filter: Min 100 pressure balls & 200 total balls.", color=EMERALD, fontsize=9, zorder=3)

    plt.tight_layout()
    path = os.path.join(SLIDES_9X16_DIR, "slide_05_math.png")
    fig.savefig(path, dpi=200, facecolor=BG_COLOR)
    plt.close(fig)
    return path

def create_vertical_slide_6():
    fig, ax = plt.subplots(figsize=(9, 16), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 16)
    ax.axis('off')

    # Header
    ax.text(0.8, 15.0, "06  •  EMPIRICAL EVIDENCE", color=RR_PINK, fontsize=11, fontweight='bold')
    ax.text(0.8, 14.3, "Visual Proof & Case Studies", color=WHITE, fontsize=24, fontweight='black')
    ax.text(0.8, 13.7, "Match tension dynamics & distribution charts", color=GRAY, fontsize=11)

    # Embed match curve image if available
    img_curve_path = os.path.join(OUTPUT_DIR, "pressure_curve_match_39808.png")
    if os.path.exists(img_curve_path):
        img_c = Image.open(img_curve_path)
        ax.imshow(img_c, extent=(0.8, 8.2, 8.5, 13.2), zorder=2)
        ax.text(4.5, 8.2, "Match 39808: Tension Curve Across Legal Deliveries", color=PURPLE_LIGHT, fontsize=9, ha='center', zorder=3)

    # Embed summary table or radar
    img_radar_path = os.path.join(OUTPUT_DIR, "player_profile_mahedi_hasan.png")
    if os.path.exists(img_radar_path):
        img_r = Image.open(img_radar_path)
        ax.imshow(img_r, extent=(1.2, 7.8, 2.5, 7.8), zorder=2)
        ax.text(4.5, 2.2, "Mahedi Hasan (Rank 1): Multi-Metric Resilience Radar", color=PURPLE_LIGHT, fontsize=9, ha='center', zorder=3)

    # Bottom Callout
    draw_rounded_card(ax, 0.8, 0.8, 7.4, 1.1, bg="#1E0E38", border=RR_PINK, radius=0.04)
    ax.text(4.5, 1.35, "All visualizations live on Streamlit Cloud & GitHub", color=WHITE, fontsize=10, fontweight='bold', ha='center', zorder=3)

    plt.tight_layout()
    path = os.path.join(SLIDES_9X16_DIR, "slide_06_evidence.png")
    fig.savefig(path, dpi=200, facecolor=BG_COLOR)
    plt.close(fig)
    return path

def create_vertical_slide_7():
    fig, ax = plt.subplots(figsize=(9, 16), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 16)
    ax.axis('off')

    # Header
    ax.text(0.8, 15.0, "07  •  TOURNAMENT CONTEXT", color=RR_PINK, fontsize=11, fontweight='bold')
    ax.text(0.8, 14.3, "IPL Sub-Cohort Analysis", color=WHITE, fontsize=24, fontweight='black')
    ax.text(0.8, 13.7, "Cross-validation across 87,687 IPL deliveries", color=GRAY, fontsize=11)

    # Royals Heroes Card
    draw_rounded_card(ax, 0.8, 10.6, 7.4, 2.7, bg="#260C38", border=RR_PINK, radius=0.04)
    ax.text(1.2, 12.8, "👑 RAJASTHAN ROYALS STARS IN TOP TIERS", color=RR_PINK, fontsize=11, fontweight='black', zorder=3)
    ax.text(1.2, 12.1, "• Rovman Powell: Ranked #4 in IPL Batters (143.9 SR under pressure).", color=WHITE, fontsize=9.5, zorder=3)
    ax.text(1.2, 11.5, "• Trent Boult: Ranked #9 in IPL Bowlers (6.62 Econ across 601 balls).", color=WHITE, fontsize=9.5, zorder=3)
    ax.text(1.2, 10.9, "• Rahul Tewatia: Ranked #6 in IPL Batters (152.1 SR, ice in veins).", color=WHITE, fontsize=9.5, zorder=3)

    # Top IPL Batters Box
    draw_rounded_card(ax, 0.8, 6.0, 7.4, 4.2, radius=0.04)
    ax.text(1.2, 9.7, "TOP IPL-ONLY BATTERS", color=GOLD, fontsize=11, fontweight='black', zorder=3)
    ipl_bats = [
        "1. Sameer Rizvi (1.574 CF, 163.9 SR)",
        "2. Karun Nair (1.521 CF, 173.5 SR)",
        "3. Washington Sundar (1.394 CF, 147.5 SR)",
        "4. Rovman Powell (1.390 CF, 143.9 SR) — RR",
        "5. Rajat Patidar (1.272 CF, 149.0 SR)",
        "6. Rahul Tewatia (1.289 CF, 152.1 SR)"
    ]
    for i, b in enumerate(ipl_bats):
        ax.text(1.2, 9.0 - (i * 0.55), b, color=WHITE, fontsize=9.5, zorder=3)

    # Top IPL Bowlers Box
    draw_rounded_card(ax, 0.8, 1.4, 7.4, 4.2, radius=0.04)
    ax.text(1.2, 5.1, "TOP IPL-ONLY BOWLERS", color=CYAN, fontsize=11, fontweight='black', zorder=3)
    ipl_bowls = [
        "1. Daniel Sams (1.846 CF, 6.35 Econ)",
        "2. Arshad Khan (1.683 CF, 6.15 Econ)",
        "3. Cameron Green (1.565 CF, 6.71 Econ)",
        "4. Patrick Cummins (1.479 CF, 6.80 Econ)",
        "5. Mayank Yadav (1.628 CF, 7.77 Econ, 156 km/h)",
        "6. Trent Boult (1.337 CF, 6.63 Econ) — RR"
    ]
    for i, b in enumerate(ipl_bowls):
        ax.text(1.2, 4.4 - (i * 0.55), b, color=WHITE, fontsize=9.5, zorder=3)

    plt.tight_layout()
    path = os.path.join(SLIDES_9X16_DIR, "slide_07_ipl.png")
    fig.savefig(path, dpi=200, facecolor=BG_COLOR)
    plt.close(fig)
    return path

def create_vertical_slide_8():
    fig, ax = plt.subplots(figsize=(9, 16), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 16)
    ax.axis('off')

    # Header
    ax.text(0.8, 15.0, "08  •  SUMMARY & VERIFICATION", color=RR_PINK, fontsize=11, fontweight='bold')
    ax.text(0.8, 14.3, "Ready for Submission", color=WHITE, fontsize=24, fontweight='black')
    ax.text(0.8, 13.7, "Everything aligned for Unstop Round 1 evaluation", color=GRAY, fontsize=11)

    # Checklist Card
    draw_rounded_card(ax, 0.8, 9.0, 7.4, 4.3, bg="#180C30", border=EMERALD, radius=0.04)
    ax.text(1.2, 12.8, "SUBMISSION CHECKLIST STATUS", color=EMERALD, fontsize=11, fontweight='black', zorder=3)

    checks = [
        ("✓ 10 Batters Selected", "Ranked 1 to 10 in Unstop dropdowns"),
        ("✓ 10 Bowlers Selected", "Ranked 1 to 10 in Unstop dropdowns"),
        ("✓ Methodology Report", "PDF (854 KB) & Word DOCX (766 KB)"),
        ("✓ Dashboard Link", "https://superr.streamlit.app"),
        ("✓ GitHub Code Repository", "https://github.com/Harshgup16/SupeRR")
    ]
    for i, (title, sub) in enumerate(checks):
        yp = 12.0 - (i * 0.68)
        ax.text(1.2, yp, title, color=WHITE, fontsize=10.5, fontweight='bold', zorder=3)
        ax.text(4.2, yp, sub, color=PURPLE_LIGHT, fontsize=9, zorder=3)

    # QR Code placeholder / Direct Link Card
    draw_rounded_card(ax, 0.8, 4.2, 7.4, 4.4, radius=0.04)
    ax.text(1.2, 8.0, "LIVE DASHBOARD & CODE REPO", color=GOLD, fontsize=11, fontweight='black', zorder=3)
    ax.text(1.2, 7.2, "Streamlit Cloud URL:", color=WHITE, fontsize=10, fontweight='bold', zorder=3)
    ax.text(1.2, 6.7, "https://superr.streamlit.app", color=RR_PINK, fontsize=11, fontweight='black', zorder=3)

    ax.text(1.2, 5.8, "GitHub Repository:", color=WHITE, fontsize=10, fontweight='bold', zorder=3)
    ax.text(1.2, 5.3, "https://github.com/Harshgup16/SupeRR", color=CYAN, fontsize=11, fontweight='black', zorder=3)

    ax.text(1.2, 4.6, "Standalone Local App:  d:\\Hackathon\\rr\\index.html", color=GRAY, fontsize=9, zorder=3)

    # Thank you footer
    draw_rounded_card(ax, 0.8, 1.2, 7.4, 2.6, bg="#260C38", border=RR_PINK, radius=0.04)
    ax.text(4.5, 3.2, "HALLA BOL! 🏏", color=RR_PINK, fontsize=20, fontweight='black', ha='center', zorder=3)
    ax.text(4.5, 2.5, "SupeRR Selector Season 2 • Round 1 Solution", color=WHITE, fontsize=11, fontweight='bold', ha='center', zorder=3)
    ax.text(4.5, 1.8, "Built with data rigor for Rajasthan Royals Analytics", color=PURPLE_LIGHT, fontsize=9.5, ha='center', zorder=3)

    plt.tight_layout()
    path = os.path.join(SLIDES_9X16_DIR, "slide_08_summary.png")
    fig.savefig(path, dpi=200, facecolor=BG_COLOR)
    plt.close(fig)
    return path

# ==============================================================================
# COMPILE 9:16 VERTICAL PDF
# ==============================================================================
def compile_vertical_pdf():
    print("Compiling 9:16 Vertical Slides into PDF...")
    pdf_path = os.path.join(PROJECT_ROOT, "SupeRR_Selector_Presentation_9x16.pdf")
    doc = fitz.open()

    slide_images = [
        create_vertical_slide_1(),
        create_vertical_slide_2(),
        create_vertical_slide_3(),
        create_vertical_slide_4(),
        create_vertical_slide_5(),
        create_vertical_slide_6(),
        create_vertical_slide_7(),
        create_vertical_slide_8(),
    ]

    for img_path in slide_images:
        # A4 proportioned or exact 9:16 ratio (width: 540, height: 960)
        page = doc.new_page(width=540, height=960)
        page.insert_image(fitz.Rect(0, 0, 540, 960), filename=img_path)

    doc.save(pdf_path, deflate=True, garbage=4)
    doc.close()
    print(f"✔ Saved 9:16 Presentation PDF to {pdf_path}")
    return pdf_path

# ==============================================================================
# 16:9 WIDESCREEN SLIDES GENERATION
# ==============================================================================
def create_16x9_slide_1():
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    glow = patches.Circle((8, 4.5), 4.5, facecolor="#EA1A85", alpha=0.12, zorder=1)
    ax.add_patch(glow)

    draw_rounded_card(ax, 5.0, 7.8, 6.0, 0.5, bg="#2A0F45", border=RR_PINK, radius=0.08)
    ax.text(8.0, 8.05, "RAJASTHAN ROYALS  •  SUPERR SELECTOR S2", color=WHITE,
            fontsize=11, fontweight='black', ha='center', va='center', zorder=3)

    ax.text(8.0, 6.6, "CRACKING CRICKET'S CRUCIBLE", color=WHITE,
            fontsize=34, fontweight='black', ha='center', va='center', zorder=3)
    ax.text(8.0, 5.8, "Identifying The Most Reliable Players Under Pressure", color=RR_PINK,
            fontsize=17, fontweight='bold', ha='center', va='center', zorder=3)
    ax.text(8.0, 5.2, "Dynamic Win-Probability & Bayesian Clutch Modeling | Round 1 Submission", color=PURPLE_LIGHT,
            fontsize=12, ha='center', va='center', zorder=3)

    # 4 Key Metrics Row
    kpis = [
        ("200,999", "DELIVERIES ANALYZED", "2022–2026 IPL + T20I", WHITE),
        ("867", "MATCHES MODELLED", "371 IPL / 512 T20I", CYAN),
        ("60,311", "PRESSURE BALLS", "30.0% WITH DPI > 0.60", RR_PINK),
        ("1,217", "TRACKED PLAYERS", "158 ELIGIBLE BATTERS", GOLD)
    ]
    for i, (val, lbl, sub, col) in enumerate(kpis):
        x_pos = 1.0 + (i * 3.6)
        draw_rounded_card(ax, x_pos, 2.5, 3.2, 1.8, radius=0.05)
        ax.text(x_pos + 1.6, 3.65, val, color=col, fontsize=24, fontweight='black', ha='center', zorder=3)
        ax.text(x_pos + 1.6, 3.05, lbl, color=WHITE, fontsize=10, fontweight='bold', ha='center', zorder=3)
        ax.text(x_pos + 1.6, 2.75, sub, color=PURPLE_LIGHT, fontsize=8.5, ha='center', zorder=3)

    draw_rounded_card(ax, 3.0, 0.8, 10.0, 0.9, bg="#1E0E38", border=EMERALD, radius=0.06)
    ax.text(8.0, 1.25, "✓ OFFICIAL ROUND 1 SUBMISSION READY  •  UNSTOP DROPDOWNS  •  PDF & DOCX  •  STREAMLIT CLOUD",
            color=EMERALD, fontsize=10.5, fontweight='bold', ha='center', va='center', zorder=3)

    plt.tight_layout()
    path = os.path.join(SLIDES_16X9_DIR, "slide_16x9_01_cover.png")
    fig.savefig(path, dpi=200, facecolor=BG_COLOR)
    plt.close(fig)
    return path

def create_16x9_slide_2():
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    ax.text(1.0, 8.2, "02  •  THE PHILOSOPHY", color=RR_PINK, fontsize=12, fontweight='bold')
    ax.text(1.0, 7.5, "Rethinking Pressure in T20 Cricket", color=WHITE, fontsize=26, fontweight='black')

    # Left: The Flaw
    draw_rounded_card(ax, 1.0, 1.8, 6.6, 5.0, bg="#1B0C2E", border="#EF4444", radius=0.04)
    ax.text(1.5, 6.2, "❌ THE BLUNT APPROACH", color="#EF4444", fontsize=13, fontweight='black', zorder=3)
    ax.text(1.5, 5.4, "• Labels all overs 16–20 as 'pressure' uniformly.", color=WHITE, fontsize=11, zorder=3)
    ax.text(1.5, 4.6, "• Flaw: 160/2 needing 15 off 18 balls has ZERO pressure.", color=GRAY, fontsize=10.5, zorder=3)
    ax.text(1.5, 3.8, "• Fails to detect early collapses (e.g. 28/4 in over 5).", color=GRAY, fontsize=10.5, zorder=3)
    ax.text(1.5, 3.0, "• Evaluates outcomes, not context-adjusted leverage.", color=GRAY, fontsize=10.5, zorder=3)

    # Right: Our Innovation
    draw_rounded_card(ax, 8.4, 1.8, 6.6, 5.0, bg="#131B2E", border=CYAN, radius=0.04)
    ax.text(8.9, 6.2, "✓ DYNAMIC PRESSURE INDEX (DPI)", color=CYAN, fontsize=13, fontweight='black', zorder=3)
    ax.text(8.9, 5.4, "1. Knife-Edge Maximum (2nd Innings):", color=WHITE, fontsize=11, fontweight='bold', zorder=3)
    ax.text(9.2, 4.8, "Tension peaks at 50/50 win prob: 1.0 - 2|P(Win) - 0.50|", color=PURPLE_LIGHT, fontsize=10, zorder=3)
    ax.text(8.9, 4.0, "2. Par-Score Expectancy Deviations (1st Innings):", color=WHITE, fontsize=11, fontweight='bold', zorder=3)
    ax.text(9.2, 3.4, "State-dependent matrix across overs × wickets fallen.", color=PURPLE_LIGHT, fontsize=10, zorder=3)
    ax.text(8.9, 2.6, "3. Multipliers: Death (1.30x), Knockouts (1.30x), Momentum Shocks", color=GOLD, fontsize=10, fontweight='bold', zorder=3)

    draw_rounded_card(ax, 1.0, 0.6, 14.0, 0.8, bg="#1E0E38", border=RR_PINK, radius=0.04)
    ax.text(8.0, 1.0, "DPI evaluated on every single ball (0.0 to 1.0) • 30.0% of all deliveries qualify as High/Extreme Pressure",
            color=WHITE, fontsize=10.5, fontweight='bold', ha='center', zorder=3)

    plt.tight_layout()
    path = os.path.join(SLIDES_16X9_DIR, "slide_16x9_02_philosophy.png")
    fig.savefig(path, dpi=200, facecolor=BG_COLOR)
    plt.close(fig)
    return path

def create_16x9_slide_3():
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    ax.text(1.0, 8.2, "03  •  UNSTOP SUBMISSION", color=RR_PINK, fontsize=12, fontweight='bold')
    ax.text(1.0, 7.5, "Official Top 10 Batters Under Pressure", color=WHITE, fontsize=26, fontweight='black')

    # Two columns of 5 batters each
    batters = [
        ("1", "Mahedi Hasan", "1.592", "131.4 (vs 81.5)", "22.1 (vs 10.0)", "118"),
        ("2", "Washington Sundar", "1.304", "142.9 (vs 139.0)", "55.0 (vs 21.5)", "154"),
        ("3", "Rajat Patidar", "1.216", "149.0 (vs 172.9)", "96.3 (vs 30.5)", "194"),
        ("4", "Rahul Tewatia", "1.203", "152.1 (vs 148.4)", "44.5 (vs 21.5)", "117"),
        ("5", "Ayush Badoni", "1.188", "123.0 (vs 145.6)", "93.5 (vs 23.1)", "152"),
        ("6", "Abishek Porel", "1.126", "124.1 (vs 153.5)", "45.0 (vs 21.0)", "145"),
        ("7", "Vaibhav Sooryavanshi", "1.124", "227.5 (vs 221.4)", "57.1 (vs 36.7)", "276"),
        ("8", "Devdutt Padikkal", "1.069", "128.7 (vs 142.9)", "34.5 (vs 22.1)", "268"),
        ("9", "David Warner", "1.067", "132.0 (vs 151.9)", "62.4 (vs 36.1)", "378"),
        ("10", "Towhid Hridoy", "1.042", "108.9 (vs 131.1)", "49.0 (vs 28.0)", "225")
    ]

    for i in range(5):
        # Col 1
        rk, name, cf, sr, avg, balls = batters[i]
        yp = 5.9 - (i * 1.1)
        draw_rounded_card(ax, 1.0, yp, 6.8, 0.95, radius=0.03)
        ax.text(1.3, yp + 0.48, f"#{rk}", color=GOLD if rk=='1' else RR_PINK, fontsize=13, fontweight='black', zorder=3)
        ax.text(1.9, yp + 0.48, name, color=WHITE, fontsize=11.5, fontweight='bold', zorder=3)
        ax.text(4.8, yp + 0.58, f"SR: {sr}", color=PURPLE_LIGHT, fontsize=9, zorder=3)
        ax.text(4.8, yp + 0.28, f"Avg: {avg}", color=GRAY, fontsize=8.5, zorder=3)
        ax.text(7.2, yp + 0.48, f"CF {cf}", color=EMERALD, fontsize=11, fontweight='bold', zorder=3)

        # Col 2
        rk2, name2, cf2, sr2, avg2, balls2 = batters[i+5]
        draw_rounded_card(ax, 8.2, yp, 6.8, 0.95, radius=0.03)
        ax.text(8.5, yp + 0.48, f"#{rk2}", color=RR_PINK, fontsize=13, fontweight='black', zorder=3)
        ax.text(9.1, yp + 0.48, name2, color=WHITE, fontsize=11.5, fontweight='bold', zorder=3)
        ax.text(12.0, yp + 0.58, f"SR: {sr2}", color=PURPLE_LIGHT, fontsize=9, zorder=3)
        ax.text(12.0, yp + 0.28, f"Avg: {avg2}", color=GRAY, fontsize=8.5, zorder=3)
        ax.text(14.4, yp + 0.48, f"CF {cf2}", color=EMERALD, fontsize=11, fontweight='bold', zorder=3)

    plt.tight_layout()
    path = os.path.join(SLIDES_16X9_DIR, "slide_16x9_03_top_batters.png")
    fig.savefig(path, dpi=200, facecolor=BG_COLOR)
    plt.close(fig)
    return path

def create_16x9_slide_4():
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    ax.text(1.0, 8.2, "04  •  UNSTOP SUBMISSION", color=RR_PINK, fontsize=12, fontweight='bold')
    ax.text(1.0, 7.5, "Official Top 10 Bowlers Under Pressure", color=WHITE, fontsize=26, fontweight='black')

    bowlers = [
        ("1", "Ripon Mondol", "1.689", "5.48 (vs 11.51)", "8.3 (vs 14.2)", "150"),
        ("2", "Wellington Masakadza", "1.614", "5.43 (vs 8.86)", "17.8 (vs 60.4)", "178"),
        ("3", "Salman Mirza", "1.569", "5.29 (vs 9.87)", "12.0 (vs 24.8)", "204"),
        ("4", "Arshad Khan", "1.482", "6.15 (vs 13.47)", "20.0 (vs 18.4)", "120"),
        ("5", "Jimmy Neesham", "1.481", "6.62 (vs 9.71)", "6.6 (vs 20.0)", "106"),
        ("6", "Dunith Wellalage", "1.449", "6.09 (vs 9.74)", "10.7 (vs 22.7)", "128"),
        ("7", "Daniel Sams", "1.430", "6.71 (vs 11.31)", "16.2 (vs 28.8)", "178"),
        ("8", "Patrick Cummins", "1.411", "6.80 (vs 10.40)", "15.3 (vs 21.5)", "336"),
        ("9", "Shaheen Afridi", "1.373", "5.99 (vs 10.01)", "12.8 (vs 16.4)", "434"),
        ("10", "Richard Ngarava", "1.367", "6.44 (vs 9.44)", "15.8 (vs 24.1)", "316")
    ]

    for i in range(5):
        rk, name, cf, econ, sr, balls = bowlers[i]
        yp = 5.9 - (i * 1.1)
        draw_rounded_card(ax, 1.0, yp, 6.8, 0.95, radius=0.03)
        ax.text(1.3, yp + 0.48, f"#{rk}", color=GOLD if rk=='1' else CYAN, fontsize=13, fontweight='black', zorder=3)
        ax.text(1.9, yp + 0.48, name, color=WHITE, fontsize=11.5, fontweight='bold', zorder=3)
        ax.text(4.8, yp + 0.58, f"Econ: {econ}", color=PURPLE_LIGHT, fontsize=9, zorder=3)
        ax.text(4.8, yp + 0.28, f"Bowl SR: {sr}", color=GRAY, fontsize=8.5, zorder=3)
        ax.text(7.2, yp + 0.48, f"CF {cf}", color=EMERALD, fontsize=11, fontweight='bold', zorder=3)

        rk2, name2, cf2, econ2, sr2, balls2 = bowlers[i+5]
        draw_rounded_card(ax, 8.2, yp, 6.8, 0.95, radius=0.03)
        ax.text(8.5, yp + 0.48, f"#{rk2}", color=CYAN, fontsize=13, fontweight='black', zorder=3)
        ax.text(9.1, yp + 0.48, name2, color=WHITE, fontsize=11.5, fontweight='bold', zorder=3)
        ax.text(12.0, yp + 0.58, f"Econ: {econ2}", color=PURPLE_LIGHT, fontsize=9, zorder=3)
        ax.text(12.0, yp + 0.28, f"Bowl SR: {sr2}", color=GRAY, fontsize=8.5, zorder=3)
        ax.text(14.4, yp + 0.48, f"CF {cf2}", color=EMERALD, fontsize=11, fontweight='bold', zorder=3)

    plt.tight_layout()
    path = os.path.join(SLIDES_16X9_DIR, "slide_16x9_04_top_bowlers.png")
    fig.savefig(path, dpi=200, facecolor=BG_COLOR)
    plt.close(fig)
    return path

def create_16x9_slide_5():
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    ax.text(1.0, 8.2, "05  •  THE MATHEMATICS", color=RR_PINK, fontsize=12, fontweight='bold')
    ax.text(1.0, 7.5, "The 4D Clutch Factor & Empirical Bayes Shrinkage", color=WHITE, fontsize=26, fontweight='black')

    # Left: Batting & Bowling Formulations
    draw_rounded_card(ax, 1.0, 1.4, 6.8, 5.5, radius=0.04)
    ax.text(1.4, 6.3, "🏏 BATTING FORMULA (Weights sum to 1.0)", color=RR_PINK, fontsize=11.5, fontweight='black', zorder=3)
    ax.text(1.4, 5.6, "CF_bat = 0.35 × (SR_p / SR_b) + 0.25 × (Avg_p / Avg_b) +", color=WHITE, fontsize=10, zorder=3)
    ax.text(2.2, 5.1, "0.20 × (Bnd_p / Bnd_b) + 0.20 × ((1-Dot_p)/(1-Dot_b))", color=WHITE, fontsize=10, zorder=3)

    ax.text(1.4, 4.0, "🎳 BOWLING FORMULA (Lower runs = Higher)", color=CYAN, fontsize=11.5, fontweight='black', zorder=3)
    ax.text(1.4, 3.3, "CF_bowl = 0.30 × (Econ_b / Econ_p) + 0.25 × (SR_b / SR_p) +", color=WHITE, fontsize=10, zorder=3)
    ax.text(2.3, 2.8, "0.25 × (Dot_p / Dot_b) + 0.20 × ((1-Bnd_p)/(1-Bnd_b))", color=WHITE, fontsize=10, zorder=3)

    ax.text(1.4, 1.8, "• Baseline Neutrality: Unchanged performance ≡ 1.000 identically.", color=EMERALD, fontsize=9.5, fontweight='bold', zorder=3)

    # Right: Empirical Bayes Shrinkage
    draw_rounded_card(ax, 8.2, 1.4, 6.8, 5.5, bg="#1D0E36", border=GOLD, radius=0.04)
    ax.text(8.6, 6.3, "🔬 EMPIRICAL BAYES SAMPLE SIZE REGULARIZATION", color=GOLD, fontsize=11.5, fontweight='black', zorder=3)
    ax.text(8.6, 5.5, "Weighted_CF = 1.0 + (CF - 1.0) × Weight", color=WHITE, fontsize=11, fontweight='bold', zorder=3)
    ax.text(8.6, 4.8, "Weight = Pressure_Balls / (Pressure_Balls + 50)", color=CYAN, fontsize=11, fontweight='bold', zorder=3)
    ax.text(8.6, 4.0, "Why this eliminates the 'Small-Sample Trap':", color=WHITE, fontsize=10.5, fontweight='bold', zorder=3)
    ax.text(8.6, 3.4, "• Low sample sizes (e.g. 30 balls) naturally suffer from high variance.", color=GRAY, fontsize=10, zorder=3)
    ax.text(8.6, 2.8, "• Formula mathematically shrinks unproven spikes toward 1.0.", color=GRAY, fontsize=10, zorder=3)
    ax.text(8.6, 2.2, "• Performers over 100+ pressure balls dominate the top tiers.", color=PURPLE_LIGHT, fontsize=10, zorder=3)
    ax.text(8.6, 1.7, "• Eligibility Rule: Min 100 pressure balls & 200 total balls.", color=EMERALD, fontsize=10, fontweight='bold', zorder=3)

    plt.tight_layout()
    path = os.path.join(SLIDES_16X9_DIR, "slide_16x9_05_math.png")
    fig.savefig(path, dpi=200, facecolor=BG_COLOR)
    plt.close(fig)
    return path

def create_16x9_slide_6():
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    ax.text(1.0, 8.2, "06  •  VISUAL EVIDENCE", color=RR_PINK, fontsize=12, fontweight='bold')
    ax.text(1.0, 7.5, "Empirical Match Dynamics & Radar Profiles", color=WHITE, fontsize=26, fontweight='black')

    img_curve_path = os.path.join(OUTPUT_DIR, "pressure_curve_match_39808.png")
    if os.path.exists(img_curve_path):
        img_c = Image.open(img_curve_path)
        ax.imshow(img_c, extent=(1.0, 8.2, 1.5, 6.8), zorder=2)
        ax.text(4.6, 1.1, "Match 39808: Ball-by-Ball Tension Curve Across Innings", color=PURPLE_LIGHT, fontsize=10, ha='center', zorder=3)

    img_radar_path = os.path.join(OUTPUT_DIR, "player_profile_mahedi_hasan.png")
    if os.path.exists(img_radar_path):
        img_r = Image.open(img_radar_path)
        ax.imshow(img_r, extent=(8.6, 15.0, 1.5, 6.8), zorder=2)
        ax.text(11.8, 1.1, "Mahedi Hasan (Rank 1): Multi-Metric Resilience Radar", color=PURPLE_LIGHT, fontsize=10, ha='center', zorder=3)

    plt.tight_layout()
    path = os.path.join(SLIDES_16X9_DIR, "slide_16x9_06_evidence.png")
    fig.savefig(path, dpi=200, facecolor=BG_COLOR)
    plt.close(fig)
    return path

def create_16x9_slide_7():
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    ax.text(1.0, 8.2, "07  •  TOURNAMENT CONTEXT", color=RR_PINK, fontsize=12, fontweight='bold')
    ax.text(1.0, 7.5, "IPL Sub-Cohort Analysis (87,687 Deliveries)", color=WHITE, fontsize=26, fontweight='black')

    # Royals Callout Top
    draw_rounded_card(ax, 1.0, 5.0, 14.0, 1.8, bg="#260C38", border=RR_PINK, radius=0.04)
    ax.text(1.5, 6.2, "👑 RAJASTHAN ROYALS STARS IN HIGH-PRESSURE TIERS", color=RR_PINK, fontsize=12, fontweight='black', zorder=3)
    ax.text(1.5, 5.5, "• Rovman Powell: Ranked #4 in IPL Batters (143.9 SR under pressure across 66 balls).", color=WHITE, fontsize=10.5, zorder=3)
    ax.text(8.5, 5.5, "• Trent Boult: Ranked #9 in IPL Bowlers (6.63 Economy under pressure across 601 balls).", color=WHITE, fontsize=10.5, zorder=3)

    # Left: Top IPL Batters
    draw_rounded_card(ax, 1.0, 0.8, 6.8, 3.8, radius=0.04)
    ax.text(1.4, 4.0, "TOP IPL-ONLY BATTERS", color=GOLD, fontsize=11, fontweight='black', zorder=3)
    ipl_b = [
        "1. Sameer Rizvi (1.574 CF, 163.9 SR)",
        "2. Karun Nair (1.521 CF, 173.5 SR)",
        "3. Washington Sundar (1.394 CF, 147.5 SR)",
        "4. Rovman Powell (1.390 CF, 143.9 SR) — RR",
        "5. Rajat Patidar (1.272 CF, 149.0 SR)"
    ]
    for i, t in enumerate(ipl_b):
        ax.text(1.4, 3.4 - (i * 0.55), t, color=WHITE, fontsize=10, zorder=3)

    # Right: Top IPL Bowlers
    draw_rounded_card(ax, 8.2, 0.8, 6.8, 3.8, radius=0.04)
    ax.text(8.6, 4.0, "TOP IPL-ONLY BOWLERS", color=CYAN, fontsize=11, fontweight='black', zorder=3)
    ipl_bw = [
        "1. Daniel Sams (1.846 CF, 6.35 Econ)",
        "2. Arshad Khan (1.683 CF, 6.15 Econ)",
        "3. Cameron Green (1.565 CF, 6.71 Econ)",
        "4. Patrick Cummins (1.479 CF, 6.80 Econ)",
        "5. Trent Boult (1.337 CF, 6.63 Econ) — RR"
    ]
    for i, t in enumerate(ipl_bw):
        ax.text(8.6, 3.4 - (i * 0.55), t, color=WHITE, fontsize=10, zorder=3)

    plt.tight_layout()
    path = os.path.join(SLIDES_16X9_DIR, "slide_16x9_07_ipl.png")
    fig.savefig(path, dpi=200, facecolor=BG_COLOR)
    plt.close(fig)
    return path

def create_16x9_slide_8():
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_COLOR)
    ax.set_facecolor(BG_COLOR)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    ax.text(1.0, 8.2, "08  •  SUBMISSION SUMMARY", color=RR_PINK, fontsize=12, fontweight='bold')
    ax.text(1.0, 7.5, "Round 1 Verification & Final Deliverables", color=WHITE, fontsize=26, fontweight='black')

    # Left: Checklist
    draw_rounded_card(ax, 1.0, 1.2, 6.8, 5.8, bg="#180C30", border=EMERALD, radius=0.04)
    ax.text(1.4, 6.3, "OFFICIAL SUBMISSION ASSETS", color=EMERALD, fontsize=12, fontweight='black', zorder=3)
    assets = [
        ("✓ 10 Batters Selected", "Ranked 1 to 10 in Unstop dropdowns"),
        ("✓ 10 Bowlers Selected", "Ranked 1 to 10 in Unstop dropdowns"),
        ("✓ Methodology PDF Report", "854 KB uploadable document"),
        ("✓ Methodology Word Report", "766 KB styled DOCX document"),
        ("✓ Live Streamlit App", "https://superr.streamlit.app"),
        ("✓ GitHub Repository", "https://github.com/Harshgup16/SupeRR")
    ]
    for i, (head, sub) in enumerate(assets):
        yp = 5.5 - (i * 0.72)
        ax.text(1.4, yp, head, color=WHITE, fontsize=11, fontweight='bold', zorder=3)
        ax.text(1.7, yp - 0.28, sub, color=PURPLE_LIGHT, fontsize=9.5, zorder=3)

    # Right: Halla Bol Box
    draw_rounded_card(ax, 8.2, 1.2, 6.8, 5.8, bg="#260C38", border=RR_PINK, radius=0.04)
    ax.text(11.6, 5.8, "HALLA BOL! 🏏", color=RR_PINK, fontsize=24, fontweight='black', ha='center', zorder=3)
    ax.text(11.6, 5.0, "Rajasthan Royals SupeRR Selector Season 2", color=WHITE, fontsize=13, fontweight='bold', ha='center', zorder=3)
    ax.text(11.6, 4.4, "Round 1 Complete Data Science Solution", color=PURPLE_LIGHT, fontsize=11, ha='center', zorder=3)

    ax.plot([9.5, 13.7], [3.8, 3.8], color=RR_PINK, lw=1.5, zorder=3)

    ax.text(11.6, 3.2, "Streamlit Cloud Live Dashboard Link:", color=GRAY, fontsize=9.5, ha='center', zorder=3)
    ax.text(11.6, 2.7, "https://superr.streamlit.app", color=CYAN, fontsize=13, fontweight='black', ha='center', zorder=3)

    ax.text(11.6, 1.9, "GitHub Repository:", color=GRAY, fontsize=9.5, ha='center', zorder=3)
    ax.text(11.6, 1.5, "https://github.com/Harshgup16/SupeRR", color=GOLD, fontsize=11, fontweight='bold', ha='center', zorder=3)

    plt.tight_layout()
    path = os.path.join(SLIDES_16X9_DIR, "slide_16x9_08_summary.png")
    fig.savefig(path, dpi=200, facecolor=BG_COLOR)
    plt.close(fig)
    return path

# ==============================================================================
# COMPILE 16:9 WIDESCREEN PDF & PPTX
# ==============================================================================
def compile_16x9_pdf_and_pptx():
    print("Compiling 16:9 Widescreen Slides into PDF & PPTX...")
    pdf_path = os.path.join(PROJECT_ROOT, "SupeRR_Selector_Presentation_16x9.pdf")
    pptx_path = os.path.join(PROJECT_ROOT, "SupeRR_Selector_Presentation_16x9.pptx")

    slide_images = [
        create_16x9_slide_1(),
        create_16x9_slide_2(),
        create_16x9_slide_3(),
        create_16x9_slide_4(),
        create_16x9_slide_5(),
        create_16x9_slide_6(),
        create_16x9_slide_7(),
        create_16x9_slide_8(),
    ]

    # 1. Compile PDF (16:9 ratio: 960 x 540)
    doc = fitz.open()
    for img_path in slide_images:
        page = doc.new_page(width=960, height=540)
        page.insert_image(fitz.Rect(0, 0, 960, 540), filename=img_path)
    doc.save(pdf_path, deflate=True, garbage=4)
    doc.close()
    print(f"✔ Saved 16:9 Presentation PDF to {pdf_path}")

    # 2. Compile PPTX (16:9 ratio: 13.333 x 7.5 inches)
    prs = Presentation()
    prs.slide_width = PptxInches(13.333)
    prs.slide_height = PptxInches(7.5)
    blank_slide_layout = prs.slide_layouts[6]

    for img_path in slide_images:
        slide = prs.slides.add_slide(blank_slide_layout)
        slide.shapes.add_picture(img_path, 0, 0, width=prs.slide_width, height=prs.slide_height)

    prs.save(pptx_path)
    print(f"✔ Saved 16:9 Presentation PPTX to {pptx_path}")

    return pdf_path, pptx_path

if __name__ == "__main__":
    compile_vertical_pdf()
    compile_16x9_pdf_and_pptx()
    print("✨ All presentations generated successfully!")
