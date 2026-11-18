"""
generate_themed_presentation.py — Generates presentation slides in the EXACT
visual theme requested by the user:
- Clean white background (#FFFFFF)
- Title in a rounded box with thin amber/gold border (#D97706) and royal blue text (#1D4ED8)
- Subheading in burnt orange / terracotta (#C2410C)
- Body text in clean charcoal slate (#334155)
- Numbered lists, indented paragraphs, clean metric tables
- Both 9:16 vertical ratio and 16:9 widescreen ratio
- PDF and PNG exports
"""

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import fitz  # PyMuPDF
from pptx import Presentation
from pptx.util import Inches as PptxInches

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
SLIDES_9X16_THEMED = os.path.join(PROJECT_ROOT, "presentation_themed_9x16")
SLIDES_16X9_THEMED = os.path.join(PROJECT_ROOT, "presentation_themed_16x9")
os.makedirs(SLIDES_9X16_THEMED, exist_ok=True)
os.makedirs(SLIDES_16X9_THEMED, exist_ok=True)

# Exact Colors from Reference Image
BG_WHITE = "#FFFFFF"
PAGE_BG = "#F8FAFC"
BORDER_AMBER = "#D97706"
TITLE_BLUE = "#1D4ED8"
SUB_TERRACOTTA = "#C2410C"
TEXT_CHARCOAL = "#334155"
TEXT_MUTED = "#64748B"
LINE_GRAY = "#E2E8F0"
HIGHLIGHT_BG = "#FEF3C7"

def draw_title_box(ax, x, y, w, h, text):
    """Draws the distinct amber-bordered box with royal blue text matching the user image."""
    box = patches.FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0,rounding_size=0.08",
        facecolor="#FFFFFF", edgecolor=BORDER_AMBER, linewidth=1.4, zorder=2
    )
    ax.add_patch(box)
    ax.text(x + 0.2, y + h/2.0, text, color=TITLE_BLUE,
            fontsize=15, fontweight='bold', va='center', zorder=3)

# ==============================================================================
# 16:9 WIDESCREEN THEMED SLIDES
# ==============================================================================

def make_16x9_themed_card(slide_num, title, subtitle, content_fn):
    fig, ax = plt.subplots(figsize=(16, 9), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    ax.axis('off')

    outer_card = patches.FancyBboxPatch(
        (0.5, 0.4), 15.0, 8.2,
        boxstyle="round,pad=0,rounding_size=0.12",
        facecolor=BG_WHITE, edgecolor="#CBD5E1", linewidth=1.2, zorder=1
    )
    ax.add_patch(outer_card)

    draw_title_box(ax, 0.9, 7.3, 14.2, 0.9, title)

    ax.text(0.95, 6.9, subtitle, color=SUB_TERRACOTTA,
            fontsize=13, fontweight='bold', va='top', zorder=3)

    content_fn(ax)

    ax.plot([0.9, 15.1], [0.95, 0.95], color=LINE_GRAY, lw=1, zorder=2)
    ax.text(0.95, 0.65, f"Rajasthan Royals • SupeRR Selector S2  |  Slide {slide_num} of 8",
            color=TEXT_MUTED, fontsize=9.5, va='center', zorder=3)
    ax.text(15.05, 0.65, "Round 1 Official Submission", color=TITLE_BLUE,
            fontsize=9.5, fontweight='bold', ha='right', va='center', zorder=3)

    plt.tight_layout()
    path = os.path.join(SLIDES_16X9_THEMED, f"themed_slide_16x9_{slide_num:02d}.png")
    fig.savefig(path, dpi=200, facecolor=BG_WHITE)
    plt.close(fig)
    return path

def content_16x9_slide_1(ax):
    desc = (
        "Accessing true pressure performance in T20 cricket is challenging for franchise analysts due to over-simplified\n"
        "heuristics and lack of context-aware modeling. Traditional metrics fail to capture when performance elevates.\n\n"
        "The Rajasthan Royals SupeRR Selector challenge requires building an objective, data-driven system to identify and\n"
        "rank the 10 most reliable batters and 10 most reliable bowlers under pressure from 2022 onwards across 200,999 delivery-\n"
        "level records in IPL and T20 Internationals."
    )
    ax.text(0.95, 6.4, desc, color=TEXT_CHARCOAL, fontsize=11, va='top', linespacing=1.45, zorder=3)

    kpis = [
        ("200,999", "DELIVERIES ANALYZED", "2022–2026 IPL + T20I"),
        ("867", "MATCHES MODELLED", "371 IPL / 512 T20I"),
        ("60,311", "PRESSURE BALLS", "30.0% WITH DPI > 0.60"),
        ("1,217", "SQUAD-MAPPED PLAYERS", "158 ELIGIBLE BATTERS")
    ]
    for i, (val, lbl, sub) in enumerate(kpis):
        x = 0.95 + (i * 3.55)
        p = patches.FancyBboxPatch((x, 1.8), 3.3, 1.8, boxstyle="round,pad=0,rounding_size=0.08",
                                   facecolor="#F1F5F9", edgecolor=BORDER_AMBER, linewidth=1.2, zorder=2)
        ax.add_patch(p)
        ax.text(x + 1.65, 2.9, val, color=TITLE_BLUE, fontsize=20, fontweight='black', ha='center', zorder=3)
        ax.text(x + 1.65, 2.35, lbl, color=TEXT_CHARCOAL, fontsize=9.5, fontweight='bold', ha='center', zorder=3)
        ax.text(x + 1.65, 2.05, sub, color=TEXT_MUTED, fontsize=8.5, ha='center', zorder=3)

def content_16x9_slide_2(ax):
    box_l = patches.FancyBboxPatch((0.95, 1.4), 6.9, 5.0, boxstyle="round,pad=0,rounding_size=0.06",
                                   facecolor="#FFF5F5", edgecolor="#F87171", linewidth=1.2, zorder=2)
    ax.add_patch(box_l)
    ax.text(1.2, 5.9, "❌ The Traditional Flaw (Static Overs):", color="#DC2626", fontsize=11.5, fontweight='bold', zorder=3)
    flaw_text = (
        "• Labels all overs 16–20 as 'pressure' uniformly.\n"
        "• Flaw: 160/2 needing 15 off 18 balls has ZERO pressure.\n"
        "• Fails to capture early collapses (e.g. 28/4 in over 5).\n"
        "• Ignores required run rate and wickets in hand dynamics."
    )
    ax.text(1.2, 5.3, flaw_text, color=TEXT_CHARCOAL, fontsize=10, linespacing=1.45, zorder=3)

    box_r = patches.FancyBboxPatch((8.15, 1.4), 6.9, 5.0, boxstyle="round,pad=0,rounding_size=0.06",
                                   facecolor="#EFF6FF", edgecolor="#60A5FA", linewidth=1.2, zorder=2)
    ax.add_patch(box_r)
    ax.text(8.4, 5.9, "✓ Our Solution: Dynamic Pressure Index (DPI):", color=TITLE_BLUE, fontsize=11.5, fontweight='bold', zorder=3)
    sol_text = (
        "• Continuous metric (0.0 to 1.0) calculated for every ball.\n"
        "• 2nd Innings: Knife-edge tension peaks at 50/50 win probability:\n"
        "  Match_Balance = 1.0 - 2.0 * |P(Win) - 0.50|.\n"
        "• 1st Innings: Par-Score Expectancy deviation matrix.\n"
        "• Context Multipliers: Death (1.30x), Knockouts (1.30x), Momentum Shocks."
    )
    ax.text(8.4, 5.3, sol_text, color=TEXT_CHARCOAL, fontsize=9.8, linespacing=1.4, zorder=3)

def content_16x9_slide_3(ax):
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
        rk, name, cf, sr, avg, balls = batters[i]
        yp = 5.2 - (i * 0.95)
        p1 = patches.FancyBboxPatch((0.95, yp), 6.9, 0.85, boxstyle="round,pad=0,rounding_size=0.04",
                                   facecolor=HIGHLIGHT_BG if rk=="1" else "#F8FAFC", edgecolor=BORDER_AMBER if rk=="1" else "#E2E8F0", linewidth=1, zorder=2)
        ax.add_patch(p1)
        ax.text(1.2, yp + 0.42, f"#{rk}  {name}", color=TITLE_BLUE if rk=="1" else TEXT_CHARCOAL, fontsize=10.5, fontweight='bold', zorder=3)
        ax.text(4.7, yp + 0.42, f"SR: {sr} | Avg: {avg}", color=TEXT_MUTED, fontsize=8.5, zorder=3)
        ax.text(7.6, yp + 0.42, f"CF {cf}", color="#059669", fontsize=10, fontweight='bold', ha='right', zorder=3)

        rk2, name2, cf2, sr2, avg2, balls2 = batters[i+5]
        p2 = patches.FancyBboxPatch((8.15, yp), 6.9, 0.85, boxstyle="round,pad=0,rounding_size=0.04",
                                   facecolor="#F8FAFC", edgecolor="#E2E8F0", linewidth=1, zorder=2)
        ax.add_patch(p2)
        ax.text(8.4, yp + 0.42, f"#{rk2}  {name2}", color=TEXT_CHARCOAL, fontsize=10.5, fontweight='bold', zorder=3)
        ax.text(11.9, yp + 0.42, f"SR: {sr2} | Avg: {avg2}", color=TEXT_MUTED, fontsize=8.5, zorder=3)
        ax.text(14.8, yp + 0.42, f"CF {cf2}", color="#059669", fontsize=10, fontweight='bold', ha='right', zorder=3)

def content_16x9_slide_4(ax):
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
        yp = 5.2 - (i * 0.95)
        p1 = patches.FancyBboxPatch((0.95, yp), 6.9, 0.85, boxstyle="round,pad=0,rounding_size=0.04",
                                   facecolor=HIGHLIGHT_BG if rk=="1" else "#F8FAFC", edgecolor=BORDER_AMBER if rk=="1" else "#E2E8F0", linewidth=1, zorder=2)
        ax.add_patch(p1)
        ax.text(1.2, yp + 0.42, f"#{rk}  {name}", color=TITLE_BLUE if rk=="1" else TEXT_CHARCOAL, fontsize=10.5, fontweight='bold', zorder=3)
        ax.text(4.7, yp + 0.42, f"Econ: {econ} | SR: {sr}", color=TEXT_MUTED, fontsize=8.5, zorder=3)
        ax.text(7.6, yp + 0.42, f"CF {cf}", color="#059669", fontsize=10, fontweight='bold', ha='right', zorder=3)

        rk2, name2, cf2, econ2, sr2, balls2 = bowlers[i+5]
        p2 = patches.FancyBboxPatch((8.15, yp), 6.9, 0.85, boxstyle="round,pad=0,rounding_size=0.04",
                                   facecolor="#F8FAFC", edgecolor="#E2E8F0", linewidth=1, zorder=2)
        ax.add_patch(p2)
        ax.text(8.4, yp + 0.42, f"#{rk2}  {name2}", color=TEXT_CHARCOAL, fontsize=10.5, fontweight='bold', zorder=3)
        ax.text(11.9, yp + 0.42, f"Econ: {econ2} | SR: {sr2}", color=TEXT_MUTED, fontsize=8.5, zorder=3)
        ax.text(14.8, yp + 0.42, f"CF {cf2}", color="#059669", fontsize=10, fontweight='bold', ha='right', zorder=3)

def content_16x9_slide_5(ax):
    b1 = patches.FancyBboxPatch((0.95, 3.8), 6.9, 2.6, boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor="#FFFFFF", edgecolor=BORDER_AMBER, linewidth=1.2, zorder=2)
    ax.add_patch(b1)
    ax.text(1.2, 6.0, "🏏 Batting Clutch Factor Formulation:", color=TITLE_BLUE, fontsize=11, fontweight='bold', zorder=3)
    t_bat = (
        "CF_bat = 0.35 * (SR_p / SR_b) + 0.25 * (Avg_p / Avg_b) +\n"
        "         0.20 * (Bnd_p / Bnd_b) + 0.20 * ((1-Dot_p)/(1-Dot_b))\n"
        "• Unchanged performance identically equals 1.000."
    )
    ax.text(1.2, 5.3, t_bat, color=TEXT_CHARCOAL, fontsize=9.2, linespacing=1.35, zorder=3)

    b2 = patches.FancyBboxPatch((8.15, 3.8), 6.9, 2.6, boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor="#FFFFFF", edgecolor=BORDER_AMBER, linewidth=1.2, zorder=2)
    ax.add_patch(b2)
    ax.text(8.4, 6.0, "🎳 Bowling Clutch Factor Formulation:", color=TITLE_BLUE, fontsize=11, fontweight='bold', zorder=3)
    t_bowl = (
        "CF_bowl = 0.30 * (Econ_b / Econ_p) + 0.25 * (SR_b / SR_p) +\n"
        "          0.25 * (Dot_p / Dot_b) + 0.20 * ((1-Bnd_p)/(1-Bnd_b))\n"
        "• Inverted ratios: lower runs conceded = higher score."
    )
    ax.text(8.4, 5.3, t_bowl, color=TEXT_CHARCOAL, fontsize=9.2, linespacing=1.35, zorder=3)

    b3 = patches.FancyBboxPatch((0.95, 1.2), 14.1, 2.2, boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor="#EFF6FF", edgecolor="#93C5FD", linewidth=1.2, zorder=2)
    ax.add_patch(b3)
    ax.text(1.2, 3.0, "🔬 Empirical Bayes Sample Size Regularization:", color=SUB_TERRACOTTA, fontsize=11, fontweight='bold', zorder=3)
    t_sh = (
        "Weighted_CF = 1.0 + (CF - 1.0) * (Pressure_Balls / (Pressure_Balls + 50))\n"
        "• Shrinks low-sample volatility toward the population mean (1.000), eliminating small-sample noise.\n"
        "• Rigorous eligibility filter: Minimum 100 pressure balls and 200 total balls faced/bowled."
    )
    ax.text(1.2, 2.4, t_sh, color=TEXT_CHARCOAL, fontsize=9.5, linespacing=1.35, zorder=3)

def content_16x9_slide_6(ax):
    img_curve_path = os.path.join(OUTPUT_DIR, "pressure_curve_match_39808.png")
    if os.path.exists(img_curve_path):
        img_c = Image.open(img_curve_path)
        ax.imshow(img_c, extent=(0.95, 7.8, 1.5, 6.4), zorder=2)
        ax.text(4.35, 1.2, "Match 39808: Ball-by-ball tension curve across legal deliveries",
                color=TEXT_MUTED, fontsize=9, ha='center', zorder=3)

    img_radar_path = os.path.join(OUTPUT_DIR, "player_profile_mahedi_hasan.png")
    if os.path.exists(img_radar_path):
        img_r = Image.open(img_radar_path)
        ax.imshow(img_r, extent=(8.25, 15.05, 1.5, 6.4), zorder=2)
        ax.text(11.65, 1.2, "Mahedi Hasan (Rank 1): 5-Axis Resilience Radar Profile",
                color=TEXT_MUTED, fontsize=9, ha='center', zorder=3)

def content_16x9_slide_7(ax):
    b1 = patches.FancyBboxPatch((0.95, 4.2), 14.1, 2.2, boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor=HIGHLIGHT_BG, edgecolor=BORDER_AMBER, linewidth=1.2, zorder=2)
    ax.add_patch(b1)
    ax.text(1.2, 6.0, "👑 Rajasthan Royals Franchise Core in High-Pressure Tiers:", color=SUB_TERRACOTTA, fontsize=11.5, fontweight='bold', zorder=3)
    t_rr = (
        "• Rovman Powell: Ranked #4 among all IPL Batters under pressure (143.9 SR across 66 pressure balls).\n"
        "• Trent Boult: Ranked #9 among all IPL Bowlers under pressure (6.63 economy across 601 pressure balls; elite new-ball & death control).\n"
        "• Rahul Tewatia: Ranked #6 among IPL Batters (152.1 SR, quintessential ice-in-veins match winner)."
    )
    ax.text(1.2, 5.4, t_rr, color=TEXT_CHARCOAL, fontsize=9.5, linespacing=1.35, zorder=3)

    b2 = patches.FancyBboxPatch((0.95, 1.2), 6.9, 2.6, boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor="#FFFFFF", edgecolor=BORDER_AMBER, linewidth=1.2, zorder=2)
    ax.add_patch(b2)
    ax.text(1.2, 3.4, "Top IPL-Only Batters:", color=TITLE_BLUE, fontsize=10.5, fontweight='bold', zorder=3)
    ax.text(1.2, 2.9, "1. Sameer Rizvi (1.574 CF)    2. Karun Nair (1.521 CF)\n3. Washington Sundar (1.394) 4. Rovman Powell (1.390) - RR\n5. Rajat Patidar (1.272 CF)   6. Rahul Tewatia (1.289 CF)",
            color=TEXT_CHARCOAL, fontsize=9, linespacing=1.35, zorder=3)

    b3 = patches.FancyBboxPatch((8.15, 1.2), 6.9, 2.6, boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor="#FFFFFF", edgecolor=BORDER_AMBER, linewidth=1.2, zorder=2)
    ax.add_patch(b3)
    ax.text(8.4, 3.4, "Top IPL-Only Bowlers:", color=TITLE_BLUE, fontsize=10.5, fontweight='bold', zorder=3)
    ax.text(8.4, 2.9, "1. Daniel Sams (1.846 CF)      2. Arshad Khan (1.683 CF)\n3. Cameron Green (1.565 CF) 4. Patrick Cummins (1.479)\n5. Mayank Yadav (1.628 CF)    6. Trent Boult (1.337 CF) - RR",
            color=TEXT_CHARCOAL, fontsize=9, linespacing=1.35, zorder=3)

def content_16x9_slide_8(ax):
    b1 = patches.FancyBboxPatch((0.95, 1.2), 6.9, 5.2, boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor="#F0FDF4", edgecolor="#86EFAC", linewidth=1.2, zorder=2)
    ax.add_patch(b1)
    ax.text(1.2, 5.9, "✓ Official Submission Checklist:", color="#15803D", fontsize=11.5, fontweight='bold', zorder=3)
    t_chk = (
        "1. Dropdown Batters: 10 batters ranked (Mahedi Hasan to Hridoy).\n"
        "2. Dropdown Bowlers: 10 bowlers ranked (Ripon Mondol to Ngarava).\n"
        "3. Methodology Document: Methodology_Report_SupeRR_Selector.pdf (854 KB).\n"
        "4. Live Dashboard URL: https://superr.streamlit.app\n"
        "5. Open-Source Code: https://github.com/Harshgup16/SupeRR\n\n"
        "All players verified against official squad mappings."
    )
    ax.text(1.2, 5.2, t_chk, color=TEXT_CHARCOAL, fontsize=9.2, linespacing=1.45, zorder=3)

    b2 = patches.FancyBboxPatch((8.15, 1.2), 6.9, 5.2, boxstyle="round,pad=0,rounding_size=0.06",
                                facecolor="#FFFFFF", edgecolor=BORDER_AMBER, linewidth=1.2, zorder=2)
    ax.add_patch(b2)
    ax.text(8.4, 5.9, "Official Submission Links:", color=SUB_TERRACOTTA, fontsize=11.5, fontweight='bold', zorder=3)
    ax.text(8.4, 5.1, "Dashboard URL (for 'Please upload your dashboard link'):", color=TITLE_BLUE, fontsize=9.5, fontweight='bold', zorder=3)
    ax.text(8.4, 4.6, "https://superr.streamlit.app", color=SUB_TERRACOTTA, fontsize=12, fontweight='bold', zorder=3)

    ax.text(8.4, 3.8, "GitHub Code Repository:", color=TITLE_BLUE, fontsize=9.5, fontweight='bold', zorder=3)
    ax.text(8.4, 3.3, "https://github.com/Harshgup16/SupeRR", color=TEXT_CHARCOAL, fontsize=10.5, fontweight='bold', zorder=3)

    ax.text(8.4, 2.5, "HALLA BOL! 🏏", color=SUB_TERRACOTTA, fontsize=16, fontweight='bold', zorder=3)
    ax.text(8.4, 2.0, "Rajasthan Royals SupeRR Selector Season 2 • Round 1 Solution", color=TEXT_MUTED, fontsize=9, zorder=3)

def generate_16x9_themed_slides():
    print("Generating Themed 16:9 Widescreen Slides matching user reference image...")
    slides_16x9 = [
        make_16x9_themed_card(1, "Proposed Solution & Overview", "Description of problem statement:", content_16x9_slide_1),
        make_16x9_themed_card(2, "Proposed Solution & Innovation", "Detailed Explanation of the Proposed Solution:", content_16x9_slide_2),
        make_16x9_themed_card(3, "Official Dropdown: Top 10 Batters", "Rank-ordered selections for Unstop dropdowns:", content_16x9_slide_3),
        make_16x9_themed_card(4, "Official Dropdown: Top 10 Bowlers", "Rank-ordered selections for Unstop dropdowns:", content_16x9_slide_4),
        make_16x9_themed_card(5, "Mathematical Formulation & Metrics", "Detailed scoring logic and rating formulation:", content_16x9_slide_5),
        make_16x9_themed_card(6, "Empirical Results & Visual Proof", "Statistical validation and match case studies:", content_16x9_slide_6),
        make_16x9_themed_card(7, "Tournament Context (IPL vs T20I)", "Cross-competition robustness and franchise alignment:", content_16x9_slide_7),
        make_16x9_themed_card(8, "Submission Summary & Deliverables", "Round 1 checklist and access points:", content_16x9_slide_8),
    ]

    pdf_16x9_path = os.path.join(PROJECT_ROOT, "SupeRR_Selector_Themed_Presentation_16x9.pdf")
    doc = fitz.open()
    for s_path in slides_16x9:
        page = doc.new_page(width=960, height=540) # 16:9 ratio
        page.insert_image(fitz.Rect(0, 0, 960, 540), filename=s_path)
    doc.save(pdf_16x9_path, deflate=True, garbage=4)
    doc.close()
    print(f"✔ Saved Themed 16:9 Presentation PDF to {pdf_16x9_path}")

    # Also build PPTX
    pptx_path = os.path.join(PROJECT_ROOT, "SupeRR_Selector_Themed_Presentation_16x9.pptx")
    prs = Presentation()
    prs.slide_width = PptxInches(13.333)
    prs.slide_height = PptxInches(7.5)
    blank_layout = prs.slide_layouts[6]
    for s_path in slides_16x9:
        slide = prs.slides.add_slide(blank_layout)
        slide.shapes.add_picture(s_path, 0, 0, width=prs.slide_width, height=prs.slide_height)
    prs.save(pptx_path)
    print(f"✔ Saved Themed 16:9 Presentation PPTX to {pptx_path}")

    return pdf_16x9_path, pptx_path

def make_vertical_card(slide_num, title, subtitle, content_fn):
    fig, ax = plt.subplots(figsize=(9, 16), facecolor=BG_WHITE)
    ax.set_facecolor(BG_WHITE)
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 16)
    ax.axis('off')

    # Outer subtle card frame
    outer_card = patches.FancyBboxPatch(
        (0.3, 0.4), 8.4, 15.2,
        boxstyle="round,pad=0,rounding_size=0.15",
        facecolor=BG_WHITE, edgecolor="#CBD5E1", linewidth=1.2, zorder=1
    )
    ax.add_patch(outer_card)

    # Top Title Box (Matches Image exactly)
    draw_title_box(ax, 0.7, 14.1, 7.6, 1.0, title)

    # Subheading (Burnt orange / terracotta)
    ax.text(0.75, 13.5, subtitle, color=SUB_TERRACOTTA,
            fontsize=13, fontweight='bold', va='top', zorder=3)

    # Dynamic Content
    content_fn(ax)

    # Bottom footer metadata
    ax.plot([0.7, 8.3], [1.2, 1.2], color=LINE_GRAY, lw=1, zorder=2)
    ax.text(0.75, 0.8, f"Rajasthan Royals • SupeRR Selector S2  |  Slide {slide_num} of 8",
            color=TEXT_MUTED, fontsize=8.5, va='center', zorder=3)
    ax.text(8.25, 0.8, "Round 1 Submission", color=TITLE_BLUE,
            fontsize=8.5, fontweight='bold', ha='right', va='center', zorder=3)

    plt.tight_layout()
    path = os.path.join(SLIDES_9X16_THEMED, f"themed_slide_9x16_{slide_num:02d}.png")
    fig.savefig(path, dpi=200, facecolor=BG_WHITE)
    plt.close(fig)
    return path

# Slide 1: Problem Statement
def content_slide_1(ax):
    desc = (
        "Accessing true pressure performance in T20 cricket is challenging\n"
        "for franchise analysts due to over-simplified heuristics and lack of\n"
        "context-aware modeling. Analysts struggle to:\n\n"
        "• Distinguish genuine clutch match-winners from volume accumulators.\n"
        "• Accurately account for game state, required run rate, and wickets in hand.\n"
        "• Measure whether death overs actually carry pressure in lopsided games.\n"
        "• Compare players fairly across varying sample sizes and league contexts.\n\n"
        "Furthermore, traditional statistics (raw average and strike rate) fail to\n"
        "capture player performance shifts between routine passages and high-\n"
        "leverage match-deciding situations.\n\n"
        "The Rajasthan Royals SupeRR Selector challenge requires building an\n"
        "objective, data-driven system to identify and rank the 10 most reliable\n"
        "batters and 10 most reliable bowlers under pressure from 2022 onwards\n"
        "across 200,999 delivery-level records in IPL and T20 Internationals."
    )
    ax.text(0.75, 12.9, desc, color=TEXT_CHARCOAL, fontsize=10.5,
            va='top', linespacing=1.45, zorder=3)

    # 4 Key Stat Pills
    kpis = [
        ("200,999", "Deliveries"),
        ("867", "Matches"),
        ("60,311", "Pressure Balls"),
        ("1,217", "Players")
    ]
    for i, (val, lbl) in enumerate(kpis):
        x = 0.75 + (i * 1.9)
        p = patches.FancyBboxPatch((x, 1.8), 1.7, 1.1, boxstyle="round,pad=0,rounding_size=0.08",
                                   facecolor="#F1F5F9", edgecolor=BORDER_AMBER, linewidth=1, zorder=2)
        ax.add_patch(p)
        ax.text(x + 0.85, 2.45, val, color=TITLE_BLUE, fontsize=13, fontweight='bold', ha='center', zorder=3)
        ax.text(x + 0.85, 2.1, lbl, color=TEXT_CHARCOAL, fontsize=8.5, ha='center', zorder=3)

# Slide 2: Proposed Solution
def content_slide_2(ax):
    intro = (
        "We propose an end-to-end framework combining the Dynamic Pressure\n"
        "Index (DPI) with a Bayesian 4D Clutch Factor rating engine:\n"
    )
    ax.text(0.75, 12.9, intro, color=TEXT_CHARCOAL, fontsize=10.5, va='top', zorder=3)

    points = [
        ("1. Dynamic Pressure Index (DPI):",
         "Measures tension continuously (0.0 to 1.0) for every ball.\n"
         "• 2nd Innings: Knife-edge tension peaks at 50/50 win prob:\n"
         "  Match_Balance = 1.0 - 2.0 * |P(Win) - 0.50|.\n"
         "• 1st Innings: Par-Score Expectancy deviation matrix (overs × wickets)."),

        ("2. Contextual Leverage Multipliers:",
         "• Phase Multiplier: Death overs (overs 16–20) receive 1.30x.\n"
         "• Knockout Multiplier: Finals and playoffs receive 1.30x.\n"
         "• Momentum Shock: Wicket clusters or dot freezes in last 6 balls."),

        ("3. 4-Dimensional Clutch Factor (CF):",
         "Evaluates Strike Rate/Economy, Average, Boundary %, and Non-Dot\n"
         "scoring efficiency. Neutral baseline produces CF ≡ 1.000 identically."),

        ("4. Empirical Bayes Sample Size Shrinkage:",
         "Pulls low-sample volatility toward the neutral baseline (1.000)\n"
         "using Weight = N / (N + 50) to prevent small-sample anomalies.")
    ]

    y = 12.1
    for title, body in points:
        ax.text(0.75, y, title, color=TITLE_BLUE, fontsize=10, fontweight='bold', va='top', zorder=3)
        ax.text(0.95, y - 0.35, body, color=TEXT_CHARCOAL, fontsize=9.2, va='top', linespacing=1.35, zorder=3)
        y -= 2.4

# Slide 3: Top 10 Batters
def content_slide_3(ax):
    intro = "Official rank-ordered submissions for Unstop dropdown selections:"
    ax.text(0.75, 12.9, intro, color=TEXT_MUTED, fontsize=9.5, va='top', zorder=3)

    batters = [
        ("1", "Mahedi Hasan", "1.592", "131.4", "81.5", "22.1", "10.0", "118"),
        ("2", "Washington Sundar", "1.304", "142.9", "139.0", "55.0", "21.5", "154"),
        ("3", "Rajat Patidar", "1.216", "149.0", "172.9", "96.3", "30.5", "194"),
        ("4", "Rahul Tewatia", "1.203", "152.1", "148.4", "44.5", "21.5", "117"),
        ("5", "Ayush Badoni", "1.188", "123.0", "145.6", "93.5", "23.1", "152"),
        ("6", "Abishek Porel", "1.126", "124.1", "153.5", "45.0", "21.0", "145"),
        ("7", "Vaibhav Sooryavanshi", "1.124", "227.5", "221.4", "57.1", "36.7", "276"),
        ("8", "Devdutt Padikkal", "1.069", "128.7", "142.9", "34.5", "22.1", "268"),
        ("9", "David Warner", "1.067", "132.0", "151.9", "62.4", "36.1", "378"),
        ("10", "Towhid Hridoy", "1.042", "108.9", "131.1", "49.0", "28.0", "225")
    ]

    # Table Header
    y = 12.3
    p_head = patches.FancyBboxPatch((0.75, y - 0.4), 7.5, 0.5, boxstyle="round,pad=0,rounding_size=0.04",
                                    facecolor="#EFF6FF", edgecolor=BORDER_AMBER, linewidth=1, zorder=2)
    ax.add_patch(p_head)
    ax.text(0.9, y - 0.15, "#", color=TITLE_BLUE, fontsize=8.5, fontweight='bold', zorder=3)
    ax.text(1.3, y - 0.15, "Player Name", color=TITLE_BLUE, fontsize=8.5, fontweight='bold', zorder=3)
    ax.text(3.9, y - 0.15, "Weighted CF", color=TITLE_BLUE, fontsize=8.5, fontweight='bold', zorder=3)
    ax.text(5.2, y - 0.15, "Press. SR", color=TITLE_BLUE, fontsize=8.5, fontweight='bold', zorder=3)
    ax.text(6.3, y - 0.15, "Base. SR", color=TITLE_BLUE, fontsize=8.5, fontweight='bold', zorder=3)
    ax.text(7.4, y - 0.15, "Balls", color=TITLE_BLUE, fontsize=8.5, fontweight='bold', zorder=3)

    # Table Rows
    y -= 0.55
    for rk, name, wcf, psr, bsr, pavg, bavg, balls in batters:
        bg = HIGHLIGHT_BG if rk == "1" else ("#FFFFFF" if int(rk) % 2 == 1 else "#F8FAFC")
        row_box = patches.Rectangle((0.75, y - 0.45), 7.5, 0.45, facecolor=bg, edgecolor="#E2E8F0", linewidth=0.6, zorder=2)
        ax.add_patch(row_box)

        ax.text(0.9, y - 0.22, f"#{rk}", color=SUB_TERRACOTTA if rk=="1" else TEXT_CHARCOAL, fontsize=8.5, fontweight='bold', zorder=3)
        ax.text(1.3, y - 0.22, name, color=TITLE_BLUE if rk=="1" else TEXT_CHARCOAL, fontsize=8.5, fontweight='bold' if rk=="1" else 'normal', zorder=3)
        ax.text(4.1, y - 0.22, wcf, color="#059669", fontsize=8.5, fontweight='bold', zorder=3)
        ax.text(5.4, y - 0.22, psr, color=TEXT_CHARCOAL, fontsize=8.2, zorder=3)
        ax.text(6.5, y - 0.22, bsr, color=TEXT_MUTED, fontsize=8.2, zorder=3)
        ax.text(7.6, y - 0.22, balls, color=TEXT_CHARCOAL, fontsize=8.2, zorder=3)
        y -= 0.5

    # Key Takeaway Box
    p_bot = patches.FancyBboxPatch((0.75, 4.6), 7.5, 2.2, boxstyle="round,pad=0,rounding_size=0.08",
                                   facecolor="#EFF6FF", edgecolor="#BFDBFE", linewidth=1, zorder=2)
    ax.add_patch(p_bot)
    ax.text(0.95, 6.5, "Key Analytical Insights (Batting):", color=TITLE_BLUE, fontsize=9.5, fontweight='bold', zorder=3)
    takeaway = (
        "• Mahedi Hasan (#1): Elevates SR from 81.5 to 131.4 (+61%) and average from\n"
        "  10.0 to 22.1 (+121%) under pressure. Outstanding counter-attacker.\n"
        "• Washington Sundar (#2): Exceptional composure; average surges to 55.0.\n"
        "• Rajat Patidar (#3) & Rahul Tewatia (#4): Proven IPL playoff finishers.\n"
        "• Filter: Enforced min 100 pressure balls and 200 total balls."
    )
    ax.text(0.95, 6.1, takeaway, color=TEXT_CHARCOAL, fontsize=8.5, linespacing=1.35, zorder=3)

# Slide 4: Top 10 Bowlers
def content_slide_4(ax):
    intro = "Official rank-ordered selections for Unstop dropdowns:"
    ax.text(0.75, 12.9, intro, color=TEXT_MUTED, fontsize=9.5, va='top', zorder=3)

    bowlers = [
        ("1", "Ripon Mondol", "1.689", "5.48", "11.51", "8.3", "14.2", "150"),
        ("2", "Wellington Masakadza", "1.614", "5.43", "8.86", "17.8", "60.4", "178"),
        ("3", "Salman Mirza", "1.569", "5.29", "9.87", "12.0", "24.8", "204"),
        ("4", "Arshad Khan", "1.482", "6.15", "13.47", "20.0", "18.4", "120"),
        ("5", "Jimmy Neesham", "1.481", "6.62", "9.71", "6.6", "20.0", "106"),
        ("6", "Dunith Wellalage", "1.449", "6.09", "9.74", "10.7", "22.7", "128"),
        ("7", "Daniel Sams", "1.430", "6.71", "11.31", "16.2", "28.8", "178"),
        ("8", "Patrick Cummins", "1.411", "6.80", "10.40", "15.3", "21.5", "336"),
        ("9", "Shaheen Afridi", "1.373", "5.99", "10.01", "12.8", "16.4", "434"),
        ("10", "Richard Ngarava", "1.367", "6.44", "9.44", "15.8", "24.1", "316")
    ]

    y = 12.3
    p_head = patches.FancyBboxPatch((0.75, y - 0.4), 7.5, 0.5, boxstyle="round,pad=0,rounding_size=0.04",
                                    facecolor="#EFF6FF", edgecolor=BORDER_AMBER, linewidth=1, zorder=2)
    ax.add_patch(p_head)
    ax.text(0.9, y - 0.15, "#", color=TITLE_BLUE, fontsize=8.5, fontweight='bold', zorder=3)
    ax.text(1.3, y - 0.15, "Player Name", color=TITLE_BLUE, fontsize=8.5, fontweight='bold', zorder=3)
    ax.text(3.9, y - 0.15, "Weighted CF", color=TITLE_BLUE, fontsize=8.5, fontweight='bold', zorder=3)
    ax.text(5.2, y - 0.15, "Press. Econ", color=TITLE_BLUE, fontsize=8.5, fontweight='bold', zorder=3)
    ax.text(6.3, y - 0.15, "Base. Econ", color=TITLE_BLUE, fontsize=8.5, fontweight='bold', zorder=3)
    ax.text(7.4, y - 0.15, "Balls", color=TITLE_BLUE, fontsize=8.5, fontweight='bold', zorder=3)

    y -= 0.55
    for rk, name, wcf, pecon, becon, psr, bsr, balls in bowlers:
        bg = HIGHLIGHT_BG if rk == "1" else ("#FFFFFF" if int(rk) % 2 == 1 else "#F8FAFC")
        row_box = patches.Rectangle((0.75, y - 0.45), 7.5, 0.45, facecolor=bg, edgecolor="#E2E8F0", linewidth=0.6, zorder=2)
        ax.add_patch(row_box)

        ax.text(0.9, y - 0.22, f"#{rk}", color=SUB_TERRACOTTA if rk=="1" else TEXT_CHARCOAL, fontsize=8.5, fontweight='bold', zorder=3)
        ax.text(1.3, y - 0.22, name, color=TITLE_BLUE if rk=="1" else TEXT_CHARCOAL, fontsize=8.5, fontweight='bold' if rk=="1" else 'normal', zorder=3)
        ax.text(4.1, y - 0.22, wcf, color="#059669", fontsize=8.5, fontweight='bold', zorder=3)
        ax.text(5.4, y - 0.22, pecon, color=TEXT_CHARCOAL, fontsize=8.2, zorder=3)
        ax.text(6.5, y - 0.22, becon, color=TEXT_MUTED, fontsize=8.2, zorder=3)
        ax.text(7.6, y - 0.22, balls, color=TEXT_CHARCOAL, fontsize=8.2, zorder=3)
        y -= 0.5

    p_bot = patches.FancyBboxPatch((0.75, 4.6), 7.5, 2.2, boxstyle="round,pad=0,rounding_size=0.08",
                                   facecolor="#EFF6FF", edgecolor="#BFDBFE", linewidth=1, zorder=2)
    ax.add_patch(p_bot)
    ax.text(0.95, 6.5, "Key Analytical Insights (Bowling):", color=TITLE_BLUE, fontsize=9.5, fontweight='bold', zorder=3)
    takeaway = (
        "• Ripon Mondol (#1): Drops economy from 11.51 to 5.48 (-52%) with 51.3% dots.\n"
        "• Patrick Cummins (#8): World-class champion pacer; drops economy to 6.80\n"
        "  across 336 high-pressure balls with 51.5% dot ball rate.\n"
        "• Shaheen Afridi (#9): Highest volume under pressure (434 balls) with 5.99 econ.\n"
        "• Trent Boult (RR Franchise): Maintained 6.63 economy across 601 pressure balls."
    )
    ax.text(0.95, 6.1, takeaway, color=TEXT_CHARCOAL, fontsize=8.5, linespacing=1.35, zorder=3)

# Slide 5: Mathematical Formulation
def content_slide_5(ax):
    intro = "Normalized mathematical rating equations and shrinkage regularization:"
    ax.text(0.75, 12.9, intro, color=TEXT_CHARCOAL, fontsize=10, va='top', zorder=3)

    eq_box1 = patches.FancyBboxPatch((0.75, 9.4), 7.5, 3.2, boxstyle="round,pad=0,rounding_size=0.08",
                                    facecolor="#FFFFFF", edgecolor=BORDER_AMBER, linewidth=1.2, zorder=2)
    ax.add_patch(eq_box1)
    ax.text(0.95, 12.2, "1. Batting Clutch Factor Formulation:", color=TITLE_BLUE, fontsize=10.5, fontweight='bold', zorder=3)
    eq_bat = (
        "CF_bat = 0.35 * (SR_press / SR_base) +\n"
        "         0.25 * (Avg_press / Avg_base) +\n"
        "         0.20 * (Boundary%_press / Boundary%_base) +\n"
        "         0.20 * ((1 - Dot%_press) / (1 - Dot%_base))\n\n"
        "• (1 - Dot%) represents Scoring Efficiency (non-dot ball percentage).\n"
        "• Baseline Neutrality: Unchanged performance yields CF ≡ 1.000 identically."
    )
    ax.text(1.1, 11.8, eq_bat, color=TEXT_CHARCOAL, fontsize=8.8, linespacing=1.35, zorder=3)

    eq_box2 = patches.FancyBboxPatch((0.75, 5.8), 7.5, 3.2, boxstyle="round,pad=0,rounding_size=0.08",
                                    facecolor="#FFFFFF", edgecolor=BORDER_AMBER, linewidth=1.2, zorder=2)
    ax.add_patch(eq_box2)
    ax.text(0.95, 8.6, "2. Bowling Clutch Factor Formulation:", color=TITLE_BLUE, fontsize=10.5, fontweight='bold', zorder=3)
    eq_bowl = (
        "CF_bowl = 0.30 * (Econ_base / Econ_press) +\n"
        "          0.25 * (Bowl_SR_base / Bowl_SR_press) +\n"
        "          0.25 * (Dot%_press / Dot%_base) +\n"
        "          0.20 * ((1 - Bnd%_press) / (1 - Bnd%_base))\n\n"
        "• Inverted ratios: lower runs conceded and fewer balls per wicket = higher score.\n"
        "• Boundary suppression captures yorker and slower-ball execution under pressure."
    )
    ax.text(1.1, 8.2, eq_bowl, color=TEXT_CHARCOAL, fontsize=8.8, linespacing=1.35, zorder=3)

    eq_box3 = patches.FancyBboxPatch((0.75, 2.0), 7.5, 3.4, boxstyle="round,pad=0,rounding_size=0.08",
                                    facecolor="#EFF6FF", edgecolor="#93C5FD", linewidth=1.2, zorder=2)
    ax.add_patch(eq_box3)
    ax.text(0.95, 5.0, "3. Empirical Bayes Sample Size Shrinkage:", color=SUB_TERRACOTTA, fontsize=10.5, fontweight='bold', zorder=3)
    shrinkage = (
        "Weight = Pressure_Balls / (Pressure_Balls + 50)\n"
        "Weighted_CF = 1.0 + (CF - 1.0) * Weight\n\n"
        "Why this is essential:\n"
        "• Small sample sizes (e.g. 30 balls) naturally create artificial ratio spikes.\n"
        "• The shrinkage formula mathematically pulls low-sample outliers to 1.000.\n"
        "• Sustained performers over 100+ balls dominate the rankings with high confidence."
    )
    ax.text(1.1, 4.6, shrinkage, color=TEXT_CHARCOAL, fontsize=8.8, linespacing=1.35, zorder=3)

# Slide 6: Visual Evidence
def content_slide_6(ax):
    intro = "Empirical validation across match volatility and player profiles:"
    ax.text(0.75, 12.9, intro, color=TEXT_CHARCOAL, fontsize=10, va='top', zorder=3)

    img_curve_path = os.path.join(OUTPUT_DIR, "pressure_curve_match_39808.png")
    if os.path.exists(img_curve_path):
        img_c = Image.open(img_curve_path)
        ax.imshow(img_c, extent=(0.75, 8.25, 7.8, 12.5), zorder=2)
        ax.text(4.5, 7.5, "Figure 1: Match 39808 — Ball-by-ball tension evolution across innings",
                color=TEXT_MUTED, fontsize=8.5, ha='center', zorder=3)

    img_radar_path = os.path.join(OUTPUT_DIR, "player_profile_mahedi_hasan.png")
    if os.path.exists(img_radar_path):
        img_r = Image.open(img_radar_path)
        ax.imshow(img_r, extent=(1.2, 7.8, 2.0, 7.0), zorder=2)
        ax.text(4.5, 1.7, "Figure 2: Mahedi Hasan (Rank 1) — 5-Axis Resilience Radar Profile",
                color=TEXT_MUTED, fontsize=8.5, ha='center', zorder=3)

# Slide 7: Tournament Context
def content_slide_7(ax):
    intro = "Sub-cohort evaluations and Rajasthan Royals franchise alignment:"
    ax.text(0.75, 12.9, intro, color=TEXT_CHARCOAL, fontsize=10, va='top', zorder=3)

    box_rr = patches.FancyBboxPatch((0.75, 9.6), 7.5, 3.0, boxstyle="round,pad=0,rounding_size=0.08",
                                    facecolor=HIGHLIGHT_BG, edgecolor=BORDER_AMBER, linewidth=1.2, zorder=2)
    ax.add_patch(box_rr)
    ax.text(0.95, 12.2, "👑 Rajasthan Royals Franchise Core in Top Tiers:", color=SUB_TERRACOTTA, fontsize=10.5, fontweight='bold', zorder=3)
    rr_text = (
        "• Rovman Powell: Ranked #4 among all IPL Batters under pressure (143.9 SR).\n"
        "• Trent Boult: Ranked #9 among all IPL Bowlers under pressure (6.63 economy\n"
        "  across 601 pressure balls; elite new-ball and death control).\n"
        "• Rahul Tewatia: Ranked #6 among IPL Batters (152.1 SR, legendary ice in veins)."
    )
    ax.text(1.1, 11.7, rr_text, color=TEXT_CHARCOAL, fontsize=8.8, linespacing=1.35, zorder=3)

    box_ipl = patches.FancyBboxPatch((0.75, 5.2), 7.5, 4.0, boxstyle="round,pad=0,rounding_size=0.08",
                                     facecolor="#FFFFFF", edgecolor=BORDER_AMBER, linewidth=1.2, zorder=2)
    ax.add_patch(box_ipl)
    ax.text(0.95, 8.8, "IPL-Only Sub-Analysis (87,687 Deliveries):", color=TITLE_BLUE, fontsize=10.5, fontweight='bold', zorder=3)
    ipl_text = (
        "Top IPL Batters Under Pressure:\n"
        "1. Sameer Rizvi (1.574 CF, 163.9 SR)    2. Karun Nair (1.521 CF, 173.5 SR)\n"
        "3. Washington Sundar (1.394 CF, 147.5 SR) 4. Rovman Powell (1.390 CF) — RR\n"
        "5. Rajat Patidar (1.272 CF, 149.0 SR)   6. Rahul Tewatia (1.289 CF)\n\n"
        "Top IPL Bowlers Under Pressure:\n"
        "1. Daniel Sams (1.846 CF, 6.35 Econ)   2. Arshad Khan (1.683 CF, 6.15 Econ)\n"
        "3. Cameron Green (1.565 CF, 6.71 Econ) 4. Patrick Cummins (1.479 CF, 6.80 Econ)\n"
        "5. Mayank Yadav (1.628 CF, 156 km/h)  6. Trent Boult (1.337 CF, 6.63 Econ) — RR"
    )
    ax.text(1.1, 8.4, ipl_text, color=TEXT_CHARCOAL, fontsize=8.5, linespacing=1.3, zorder=3)

    box_lim = patches.FancyBboxPatch((0.75, 1.8), 7.5, 3.0, boxstyle="round,pad=0,rounding_size=0.08",
                                     facecolor="#EFF6FF", edgecolor="#93C5FD", linewidth=1.2, zorder=2)
    ax.add_patch(box_lim)
    ax.text(0.95, 4.4, "Model Sensitivity & Edge Cases:", color=TITLE_BLUE, fontsize=10.5, fontweight='bold', zorder=3)
    lim_text = (
        "• Stability: Rankings remain persistent across threshold shifts (50 to 200 balls).\n"
        "• Impact Player Effect: Accounts for extended batting depth in post-2023 IPL.\n"
        "• Quality Weighting: Eliminates associate league skew via sample thresholds."
    )
    ax.text(1.1, 4.0, lim_text, color=TEXT_CHARCOAL, fontsize=8.5, linespacing=1.35, zorder=3)

# Slide 8: Submission Summary
def content_slide_8(ax):
    intro = "Round 1 official requirements verified and ready for evaluation:"
    ax.text(0.75, 12.9, intro, color=TEXT_CHARCOAL, fontsize=10, va='top', zorder=3)

    box_check = patches.FancyBboxPatch((0.75, 7.8), 7.5, 4.8, boxstyle="round,pad=0,rounding_size=0.08",
                                       facecolor="#F0FDF4", edgecolor="#86EFAC", linewidth=1.2, zorder=2)
    ax.add_patch(box_check)
    ax.text(0.95, 12.2, "✓ Official Submission Checklist:", color="#15803D", fontsize=11, fontweight='bold', zorder=3)

    checks = [
        ("1. Dropdown Batter Selections:", "10 batters selected in rank order (Mahedi Hasan to Hridoy)."),
        ("2. Dropdown Bowler Selections:", "10 bowlers selected in rank order (Ripon Mondol to Ngarava)."),
        ("3. Methodology Report Document:", "Methodology_Report_SupeRR_Selector.pdf (854 KB) upload-ready."),
        ("4. Live Dashboard Link:", "https://superr.streamlit.app deployed on Streamlit Cloud."),
        ("5. Open-Source Code:", "https://github.com/Harshgup16/SupeRR verified on GitHub.")
    ]
    y = 11.5
    for title, desc in checks:
        ax.text(1.1, y, title, color=TITLE_BLUE, fontsize=9.2, fontweight='bold', zorder=3)
        ax.text(1.1, y - 0.35, desc, color=TEXT_CHARCOAL, fontsize=8.5, zorder=3)
        y -= 0.75

    box_link = patches.FancyBboxPatch((0.75, 2.0), 7.5, 5.4, boxstyle="round,pad=0,rounding_size=0.08",
                                      facecolor="#FFFFFF", edgecolor=BORDER_AMBER, linewidth=1.2, zorder=2)
    ax.add_patch(box_link)
    ax.text(0.95, 7.0, "Official Links for Unstop Submission:", color=SUB_TERRACOTTA, fontsize=11, fontweight='bold', zorder=3)

    ax.text(1.1, 6.3, "Dashboard URL (for 'Please upload your dashboard link'):", color=TITLE_BLUE, fontsize=9.5, fontweight='bold', zorder=3)
    ax.text(1.1, 5.8, "https://superr.streamlit.app", color=SUB_TERRACOTTA, fontsize=11, fontweight='bold', zorder=3)

    ax.text(1.1, 5.0, "GitHub Code Repository:", color=TITLE_BLUE, fontsize=9.5, fontweight='bold', zorder=3)
    ax.text(1.1, 4.5, "https://github.com/Harshgup16/SupeRR", color=TEXT_CHARCOAL, fontsize=10, fontweight='bold', zorder=3)

    ax.text(1.1, 3.7, "Local HTML App:", color=TITLE_BLUE, fontsize=9.5, fontweight='bold', zorder=3)
    ax.text(1.1, 3.2, "d:\\Hackathon\\rr\\index.html (Opens in any browser)", color=TEXT_MUTED, fontsize=9, zorder=3)

    ax.text(4.5, 2.4, "HALLA BOL! 🏏", color=SUB_TERRACOTTA, fontsize=13, fontweight='bold', ha='center', zorder=3)

def generate_all_themed_slides():
    print("Generating Themed 9:16 Vertical Slides matching user reference image...")
    slides_9x16 = [
        make_vertical_card(1, "Proposed Solution & Overview", "Description of problem statement:", content_slide_1),
        make_vertical_card(2, "Proposed Solution & Innovation", "Detailed Explanation of the Proposed Solution:", content_slide_2),
        make_vertical_card(3, "Official Dropdown: Top 10 Batters", "Rank-ordered selections for Unstop dropdowns:", content_slide_3),
        make_vertical_card(4, "Official Dropdown: Top 10 Bowlers", "Rank-ordered selections for Unstop dropdowns:", content_slide_4),
        make_vertical_card(5, "Mathematical Formulation & Metrics", "Detailed scoring logic and rating formulation:", content_slide_5),
        make_vertical_card(6, "Empirical Results & Visual Proof", "Statistical validation and match case studies:", content_slide_6),
        make_vertical_card(7, "Tournament Context (IPL vs T20I)", "Cross-competition robustness and franchise alignment:", content_slide_7),
        make_vertical_card(8, "Submission Summary & Deliverables", "Round 1 checklist and access points:", content_slide_8),
    ]

    pdf_9x16_path = os.path.join(PROJECT_ROOT, "SupeRR_Selector_Themed_Presentation_9x16.pdf")
    doc = fitz.open()
    for s_path in slides_9x16:
        page = doc.new_page(width=540, height=960) # 9:16 ratio
        page.insert_image(fitz.Rect(0, 0, 540, 960), filename=s_path)
    doc.save(pdf_9x16_path, deflate=True, garbage=4)
    doc.close()
    print(f"✔ Saved Themed 9:16 Presentation PDF to {pdf_9x16_path}")

    return pdf_9x16_path, slides_9x16

if __name__ == "__main__":
    generate_all_themed_slides()
    generate_16x9_themed_slides()
    print("✨ All themed presentations generated successfully!")
