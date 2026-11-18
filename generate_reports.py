"""
generate_reports.py — Generates DOCX, PDF, and Markdown Methodology Reports
for SupeRR Selector Season 2.
"""

import os
import sys
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn
import fitz  # PyMuPDF

PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# RR Colors
RR_PINK_HEX = "EA1A85"
RR_DARK_HEX = "2D1446"
RR_PINK = RGBColor(234, 26, 133)
RR_DARK = RGBColor(45, 20, 70)
GRAY_TEXT = RGBColor(100, 100, 100)

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'''<w:tcMar {nsdecls("w")}>
        <w:top w:w="{top}" w:type="dxa"/>
        <w:bottom w:w="{bottom}" w:type="dxa"/>
        <w:left w:w="{left}" w:type="dxa"/>
        <w:right w:w="{right}" w:type="dxa"/>
    </w:tcMar>''')
    tcPr.append(tcMar)

def generate_docx():
    print("Generating Methodology_Report.docx...")
    doc = docx.Document()

    # Page setup - 0.75 in margins
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # Document Title
    p_title = doc.add_paragraph()
    r_title = p_title.add_run("SupeRR Selector Season 2: Round 1 Methodology Report")
    r_title.font.name = "Arial"
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = RR_PINK

    p_sub = doc.add_paragraph()
    r_sub = p_sub.add_run("Identifying the Most Reliable Batters and Bowlers Under Pressure via Dynamic Win-Probability & Bayesian Clutch Modeling")
    r_sub.font.name = "Arial"
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RR_DARK

    p_meta = doc.add_paragraph()
    r_meta = p_meta.add_run("Dataset: IPL & T20I (2022–2026) | 200,999 Deliveries | 867 Matches | Evaluation: Rajasthan Royals Analytics")
    r_meta.font.name = "Arial"
    r_meta.font.size = Pt(9.5)
    r_meta.font.color.rgb = GRAY_TEXT

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # --- Section 1: Executive Summary ---
    h1 = doc.add_heading(level=1)
    r1 = h1.add_run("1. Executive Summary & Top-10 Submission Lists")
    r1.font.color.rgb = RR_PINK

    p = doc.add_paragraph(
        "Cricket analysis often falls back on blunt heuristics like 'death overs = pressure'. In reality, batting at 160/2 requiring 15 off 18 balls carries almost zero pressure, while batting at 30/4 in the 5th over chasing 190 carries monumental pressure. "
        "This project introduces a principled, data-driven framework: the Dynamic Pressure Index (DPI), a continuous metric (0.0 to 1.0) calculated for every single delivery. "
        "We then evaluate player resilience using the Clutch Factor (CF)—a mathematically normalized multi-dimensional index that compares high-pressure performance against player baseline, stabilized through Empirical Bayes shrinkage to ensure fairness across sample sizes."
    )
    p.runs[0].font.size = Pt(10.5)

    # Tables of Top 10
    doc.add_heading(level=2).add_run("Top 10 Batters Under Pressure (Unstop Dropdown Selections)").font.color.rgb = RR_DARK

    bat_data = [
        ["Rank", "Player Name", "Weighted Clutch", "Clutch Factor", "Press. SR", "Base. SR", "Press. Avg", "Base. Avg", "Press. Balls"],
        ["1", "Mahedi Hasan", "1.592", "1.844", "131.4", "81.5", "22.1", "10.0", "118"],
        ["2", "Washington Sundar", "1.304", "1.402", "142.9", "139.0", "55.0", "21.5", "154"],
        ["3", "Rajat Patidar", "1.216", "1.272", "149.0", "172.9", "96.3", "30.5", "194"],
        ["4", "Rahul Tewatia", "1.203", "1.290", "152.1", "148.4", "44.5", "21.5", "117"],
        ["5", "Ayush Badoni", "1.188", "1.250", "123.0", "145.6", "93.5", "23.1", "152"],
        ["6", "Abishek Porel", "1.126", "1.169", "124.1", "153.5", "45.0", "21.0", "145"],
        ["7", "Vaibhav Sooryavanshi", "1.124", "1.146", "227.5", "221.4", "57.1", "36.7", "276"],
        ["8", "Devdutt Padikkal", "1.069", "1.082", "128.7", "142.9", "34.5", "22.1", "268"],
        ["9", "David Warner", "1.067", "1.076", "132.0", "151.9", "62.4", "36.1", "378"],
        ["10", "Towhid Hridoy", "1.042", "1.051", "108.9", "131.1", "49.0", "28.0", "225"]
    ]

    t_bat = doc.add_table(rows=len(bat_data), cols=9)
    t_bat.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(bat_data):
        for c_idx, val in enumerate(row):
            cell = t_bat.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)
            if r_idx == 0:
                set_cell_background(cell, RR_PINK_HEX)
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            else:
                if r_idx % 2 == 1:
                    set_cell_background(cell, "FBF0F6")
                cell.paragraphs[0].runs[0].font.color.rgb = RR_DARK
            set_cell_margins(cell, 60, 60, 80, 80)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    doc.add_heading(level=2).add_run("Top 10 Bowlers Under Pressure (Unstop Dropdown Selections)").font.color.rgb = RR_DARK

    bowl_data = [
        ["Rank", "Player Name", "Weighted Clutch", "Clutch Factor", "Press. Econ", "Base. Econ", "Press. SR", "Base. SR", "Press. Balls"],
        ["1", "Ripon Mondol", "1.689", "1.919", "5.48", "11.51", "8.3", "14.2", "150"],
        ["2", "Wellington Masakadza", "1.614", "1.787", "5.43", "8.86", "17.8", "60.4", "178"],
        ["3", "Salman Mirza", "1.569", "1.709", "5.29", "9.87", "12.0", "24.8", "204"],
        ["4", "Arshad Khan", "1.482", "1.683", "6.15", "13.47", "20.0", "18.4", "120"],
        ["5", "Jimmy Neesham", "1.481", "1.707", "6.62", "9.71", "6.6", "20.0", "106"],
        ["6", "Dunith Wellalage", "1.449", "1.625", "6.09", "9.74", "10.7", "22.7", "128"],
        ["7", "Daniel Sams", "1.430", "1.550", "6.71", "11.31", "16.2", "28.8", "178"],
        ["8", "Patrick Cummins", "1.411", "1.472", "6.80", "10.40", "15.3", "21.5", "336"],
        ["9", "Shaheen Afridi", "1.373", "1.416", "5.99", "10.01", "12.8", "16.4", "434"],
        ["10", "Richard Ngarava", "1.367", "1.425", "6.44", "9.44", "15.8", "24.1", "316"]
    ]

    t_bowl = doc.add_table(rows=len(bowl_data), cols=9)
    t_bowl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for r_idx, row in enumerate(bowl_data):
        for c_idx, val in enumerate(row):
            cell = t_bowl.cell(r_idx, c_idx)
            cell.text = val
            cell.paragraphs[0].runs[0].font.size = Pt(8.5)
            if r_idx == 0:
                set_cell_background(cell, RR_PINK_HEX)
                cell.paragraphs[0].runs[0].font.bold = True
                cell.paragraphs[0].runs[0].font.color.rgb = RGBColor(255, 255, 255)
            else:
                if r_idx % 2 == 1:
                    set_cell_background(cell, "FBF0F6")
                cell.paragraphs[0].runs[0].font.color.rgb = RR_DARK
            set_cell_margins(cell, 60, 60, 80, 80)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # Summary Table image
    img_summary = os.path.join(OUTPUT_DIR, "summary_table.png")
    if os.path.exists(img_summary):
        doc.add_picture(img_summary, width=Inches(6.8))
        doc.add_paragraph("Figure 1: Visual comparison of Top 10 Batters and Bowlers under Pressure with key statistical shifts.").runs[0].font.size = Pt(8.5)

    # --- Section 2: Pressure Definition & Mathematical Modeling ---
    doc.add_page_break()
    h2 = doc.add_heading(level=1)
    r2 = h2.add_run("2. Pressure Definition & Dynamic Win-Probability Modeling")
    r2.font.color.rgb = RR_PINK

    doc.add_paragraph(
        "A rigorous definition of pressure must satisfy three fundamental principles:\n"
        "1. Symmetry: Pressure exists for both batting and bowling sides simultaneously; when one team is desperate, the match stakes are maximized.\n"
        "2. Knife-Edge Maximum: Pressure reaches its absolute peak when win probability is closest to 50/50 (P = 0.50). One-sided games have low pressure.\n"
        "3. Dynamic State Evolution: Match context evolves delivery-by-delivery based on score relative to par, wickets lost, and momentum shifts."
    )

    doc.add_heading(level=2).add_run("Mathematical Architecture: The Dynamic Pressure Index (DPI)").font.color.rgb = RR_DARK
    doc.add_paragraph(
        "For Second Innings Chases:\n"
        "We model Chase Win Probability P(Win) from historical empirical outcomes across (Balls_Remaining, Wickets_in_Hand, Required_Runs_per_Ball). "
        "Match balance is then formulated as:\n"
        "    Match_Balance = 1.0 - 2.0 * |P(Win) - 0.50|\n"
        "When P(Win) = 0.50, Match_Balance = 1.0 (maximum tension). When P(Win) = 0.95 or 0.05, Match_Balance = 0.10 (minimal pressure).\n\n"
        "For First Innings Setting Target:\n"
        "We construct a multi-dimensional Par-Score Expectancy Matrix based on overs completed and wickets fallen. "
        "Deviation from par indicates whether a batting collapse is underway or a bowling side is hemorrhaging runs:\n"
        "    Deviation = (Par_Total * (Balls/120)^0.85 - Cumulative_Runs) / Par_Total\n"
        "    First_Inn_Pressure = 1 / (1 + exp(-6.0 * (|Deviation| - 0.30)))"
    )

    doc.add_paragraph(
        "Contextual Leverage Multipliers:\n"
        "• Phase Multiplier (M_phase): Powerplay = 1.0, Middle = 1.0, Death Overs (Overs 16–20) = 1.30 (higher leverage).\n"
        "• Tournament Stakes Multiplier (M_stakes): Playoff/Knockout Matches (Finals, Qualifiers, Eliminators) = 1.30.\n"
        "• Momentum Shock Multiplier (M_mom): Cluster of wickets in last 6 balls (+0.08 per wicket) or scoring stalls (+0.10 for <=3 runs in last 6 balls), capped at 1.35.\n\n"
        "Final Delivery DPI:\n"
        "    DPI = min(1.0, Base_Pressure * M_phase * M_stakes * M_mom)"
    )

    img_dist = os.path.join(OUTPUT_DIR, "pressure_distribution.png")
    img_heat = os.path.join(OUTPUT_DIR, "pressure_heatmap.png")
    if os.path.exists(img_dist):
        doc.add_picture(img_dist, width=Inches(6.0))
        doc.add_paragraph("Figure 2: Empirical distribution of DPI across 200,999 deliveries. Pressure deliveries (DPI > 0.6) comprise ~30% of all balls.").runs[0].font.size = Pt(8.5)
    if os.path.exists(img_heat):
        doc.add_picture(img_heat, width=Inches(6.0))
        doc.add_paragraph("Figure 3: Pressure heatmap across Overs (1–20) vs Wickets Fallen (0–9), identifying high-density tension zones.").runs[0].font.size = Pt(8.5)

    # --- Section 3: Performance Measurement & Clutch Factor ---
    doc.add_page_break()
    h3 = doc.add_heading(level=1)
    r3 = h3.add_run("3. Performance Measurement & The Clutch Factor (CF)")
    r3.font.color.rgb = RR_PINK

    doc.add_paragraph(
        "A player's true 'clutch' ability is not just their absolute strike rate or average; it is how their performance changes when the game is on the line compared to their own baseline. "
        "We divide every player's deliveries into Pressure Deliveries (DPI > 0.60) and Baseline Deliveries (DPI <= 0.60)."
    )

    doc.add_heading(level=2).add_run("Batting Clutch Factor Formula").font.color.rgb = RR_DARK
    doc.add_paragraph(
        "    CF_bat = 0.35 * (SR_press / SR_base) + \n"
        "             0.25 * (Avg_press / Avg_base) + \n"
        "             0.20 * (Boundary%_press / Boundary%_base) + \n"
        "             0.20 * ((1 - Dot%_press) / (1 - Dot%_base))\n\n"
        "Properties:\n"
        "• A player whose pressure performance equals their baseline achieves CF = 1.000 identically.\n"
        "• Ratios are clipped to 2.5 to prevent outliers from single not-out innings.\n"
        "• (1 - Dot%) represents Scoring Efficiency (percentage of deliveries generating runs)."
    )

    doc.add_heading(level=2).add_run("Bowling Clutch Factor Formula").font.color.rgb = RR_DARK
    doc.add_paragraph(
        "    CF_bowl = 0.30 * (Econ_base / Econ_press) + \n"
        "              0.25 * (Bowl_SR_base / Bowl_SR_press) + \n"
        "              0.25 * (Dot%_press / Dot%_base) + \n"
        "              0.20 * ((1 - Bnd_press) / (1 - Bnd_base))\n\n"
        "Properties:\n"
        "• Economy and bowling SR are inverted (lower runs conceded and fewer balls per wicket = higher ratio).\n"
        "• A bowler who maintains exact baseline under pressure receives CF = 1.000 identically."
    )

    doc.add_heading(level=2).add_run("Empirical Bayes Shrinkage for Sample Size Fairness").font.color.rgb = RR_DARK
    doc.add_paragraph(
        "Small sample sizes in cricket introduce massive variance (e.g., a batter who hit 2 sixes in 40 balls would appear to have an insane CF of 2.8). "
        "To enforce statistical rigor and fair comparisons across player roles, we apply Empirical Bayes Shrinkage:\n"
        "    Weight = Pressure_Balls / (Pressure_Balls + 50)\n"
        "    Weighted_Clutch = 1.0 + (CF - 1.0) * Weight\n\n"
        "Eligibility Filter: Minimum 100 pressure balls faced/bowled AND minimum 200 total balls faced/bowled. "
        "This ensures every ranked player has proven, repeatable resilience across multiple tournaments and seasons."
    )

    img_bat = os.path.join(OUTPUT_DIR, "top_batters_clutch.png")
    img_bowl = os.path.join(OUTPUT_DIR, "top_bowlers_clutch.png")
    if os.path.exists(img_bat):
        doc.add_picture(img_bat, width=Inches(6.0))
        doc.add_paragraph("Figure 4: Top 10 Batters ranked by Clutch Factor with baseline to pressure strike rate transitions.").runs[0].font.size = Pt(8.5)
    if os.path.exists(img_bowl):
        doc.add_picture(img_bowl, width=Inches(6.0))
        doc.add_paragraph("Figure 5: Top 10 Bowlers ranked by Clutch Factor with baseline to pressure economy transitions.").runs[0].font.size = Pt(8.5)

    # --- Section 4: Deep Evidence & Match Case Studies ---
    doc.add_page_break()
    h4 = doc.add_heading(level=1)
    r4 = h4.add_run("4. Empirical Evidence, Player Insights & Tournament Context")
    r4.font.color.rgb = RR_PINK

    doc.add_paragraph(
        "Why our Top 10 lists reflect genuine cricket reality:\n\n"
        "Batting Insights:\n"
        "• Mahedi Hasan (Rank 1): Elevates his strike rate from 81.5 in routine phases to 131.4 under intense pressure, with average doubling from 10.0 to 22.1. A fearless lower-order counter-attacker.\n"
        "• Washington Sundar (Rank 2): Calm under fire. Average surges from 21.5 to 55.0 under pressure with dot ball % dropping from 32.1% to 27.9% across 154 pressure balls.\n"
        "• Rajat Patidar (Rank 3): The undisputed playoff specialist. In high-pressure situations, Patidar averages an astonishing 96.3 across 194 deliveries with a 149.0 strike rate.\n"
        "• Rahul Tewatia (Rank 4): The ultimate IPL finisher. Under pressure, Tewatia's average jumps from 21.5 to 44.5 with a 152.1 strike rate across 117 pressure deliveries.\n"
        "• Vaibhav Sooryavanshi (Rank 7): High-octane phenomenon. Maintains an unreal 227.5 strike rate under pressure with nearly 40% boundary percentage over 276 deliveries.\n\n"
        "Bowling Insights:\n"
        "• Ripon Mondol (Rank 1): Slashes his economy from 11.51 to 5.48, bowling 51.3% dot balls under pressure with a wicket every 8.3 balls.\n"
        "• Patrick Cummins (Rank 8): World-class champion temperament. Across 336 pressure balls, Cummins drops his economy from 10.40 to 6.80, bowling 51.5% dot balls.\n"
        "• Shaheen Shah Afridi (Rank 9): Tested across 434 pressure balls (the highest among elite pacers), drops his economy from 10.01 to 5.99 with a lethal 12.8 strike rate.\n"
        "• Trent Boult (IPL Top 10 / #11 overall): Rajasthan Royals spearhead with 686 pressure balls, dropping economy from 10.24 to 6.54 under high pressure."
    )

    img_curve = os.path.join(OUTPUT_DIR, "pressure_curve_match_39808.png")
    img_radar = os.path.join(OUTPUT_DIR, "player_profile_mahedi_hasan.png")
    if os.path.exists(img_curve):
        doc.add_picture(img_curve, width=Inches(5.8))
        doc.add_paragraph("Figure 6: Ball-by-ball Pressure Curve for high-volatility thriller (Match 39808), demonstrating pressure spikes and release points.").runs[0].font.size = Pt(8.5)
    if os.path.exists(img_radar):
        doc.add_picture(img_radar, width=Inches(5.0))
        doc.add_paragraph("Figure 7: Multi-metric Pressure Profile Radar for Rank 1 Batter Mahedi Hasan across Low, Moderate, High, and Extreme pressure.").runs[0].font.size = Pt(8.5)

    # --- Section 5: Reliability, Limitations & IPL Sub-Analysis ---
    doc.add_page_break()
    h5 = doc.add_heading(level=1)
    r5 = h5.add_run("5. Fair Comparisons, IPL Sub-Analysis & Model Limitations")
    r5.font.color.rgb = RR_PINK

    doc.add_paragraph(
        "Treatment of IPL vs T20I Data:\n"
        "The supplied dataset contains 87,687 IPL deliveries (371 matches) and 113,312 T20I deliveries (512 matches). "
        "While our primary submission evaluates the full combined dataset as requested, we also evaluated an IPL-Only cohort:\n"
        "• Top IPL Batters: Sameer Rizvi, Karun Nair, Washington Sundar, Rovman Powell (Rajasthan Royals), Rajat Patidar, Rahul Tewatia, Ayush Badoni, Matthew Short, Josh Inglis, Abishek Porel.\n"
        "• Top IPL Bowlers: Daniel Sams, Arshad Khan, Cameron Green, Patrick Cummins, Allah Ghazanfar, Mayank Yadav, Romario Shepherd, Xavier Bartlett, Trent Boult (Rajasthan Royals), Lockie Ferguson.\n\n"
        "Model Reliability & Sensitivity Analysis:\n"
        "1. Stability Across Thresholds: We tested threshold bounds from 50 to 200 pressure balls. Core performers (Sundar, Patidar, Tewatia, Cummins, Afridi, Sams) remained firmly in the top tier throughout.\n"
        "2. Wicket Value Asymmetry: In death overs, a boundary may be worth more than preserving an average. Our formula balances SR (35%) and Scoring Efficiency (20%) with average (25%) to reflect modern T20 dynamics.\n\n"
        "Known Limitations:\n"
        "1. Associate Opponent Quality: Some T20I matches feature associate nations where bowling attack strength varies. Future iterations can incorporate opponent Elo rating adjustments.\n"
        "2. Dropped Catches & Field Placements: Ball-by-ball CSV does not record dropped catches or field placements, which can influence bowler economy variance.\n"
        "3. Impact Player Rule: Introduced in IPL 2023, the Impact Player lengthens batting line-ups and alters death over baseline risk tolerance."
    )

    doc_path = os.path.join(PROJECT_ROOT, "Methodology_Report_SupeRR_Selector.docx")
    doc.save(doc_path)
    print(f"✔ Saved DOCX to {doc_path}")

def generate_pdf():
    print("Generating Methodology_Report.pdf via PyMuPDF...")
    pdf_path = os.path.join(PROJECT_ROOT, "Methodology_Report_SupeRR_Selector.pdf")
    doc = fitz.open()

    # Helper to create a new page
    def add_page():
        return doc.new_page(width=595, height=842) # A4

    # Page 1: Title & Executive Summary & Top 10 Tables
    p1 = add_page()
    # Header bar
    p1.draw_rect(fitz.Rect(0, 0, 595, 45), color=None, fill=(0.92, 0.10, 0.52))
    p1.insert_text((40, 28), "SupeRR Selector Season 2 — Round 1 Methodology Report", fontsize=14, color=(1, 1, 1), fontname="helv")

    p1.insert_text((40, 75), "Identifying the Most Reliable Players Under Pressure", fontsize=18, color=(0.18, 0.08, 0.28), fontname="helv")
    p1.insert_text((40, 95), "Dynamic Win-Probability & Bayesian Clutch Modeling | Rajasthan Royals Analytics", fontsize=10, color=(0.4, 0.4, 0.4), fontname="helv")

    p1.draw_line(fitz.Point(40, 105), fitz.Point(555, 105), color=(0.92, 0.10, 0.52), width=1.5)

    summary_text = (
        "1. Executive Summary & Dropdown Selection Lists\n"
        "We introduce the Dynamic Pressure Index (DPI), a continuous metric (0.0 to 1.0) calculated for all 200,999\n"
        "deliveries across 867 IPL & T20I matches (2022-2026). Player resilience is evaluated using the Clutch Factor (CF)\n"
        "with Empirical Bayes shrinkage across 4 key dimensions: Strike Rate / Economy, Average, Boundary %, and Dot %."
    )
    p1.insert_textbox(fitz.Rect(40, 115, 555, 175), summary_text, fontsize=9, color=(0.2, 0.2, 0.2), fontname="helv")

    # Embed summary_table.png on page 1
    img_summary = os.path.join(OUTPUT_DIR, "summary_table.png")
    if os.path.exists(img_summary):
        p1.insert_image(fitz.Rect(40, 185, 555, 510), filename=img_summary)

    p1.insert_text((40, 525), "Top 10 Batters Selection (Unstop Dropdown):", fontsize=11, color=(0.92, 0.10, 0.52), fontname="helv")
    bat_summary = (
        "1. Mahedi Hasan (1.59)  2. Washington Sundar (1.30)  3. Rajat Patidar (1.22)  4. Rahul Tewatia (1.20)  5. Ayush Badoni (1.19)\n"
        "6. Abishek Porel (1.13)  7. Vaibhav Sooryavanshi (1.12)  8. Devdutt Padikkal (1.07)  9. David Warner (1.07)  10. Towhid Hridoy (1.04)"
    )
    p1.insert_textbox(fitz.Rect(40, 540, 555, 575), bat_summary, fontsize=8.5, color=(0.18, 0.08, 0.28), fontname="helv")

    p1.insert_text((40, 585), "Top 10 Bowlers Selection (Unstop Dropdown):", fontsize=11, color=(0.92, 0.10, 0.52), fontname="helv")
    bowl_summary = (
        "1. Ripon Mondol (1.69)  2. Wellington Masakadza (1.61)  3. Salman Mirza (1.57)  4. Arshad Khan (1.48)  5. Jimmy Neesham (1.48)\n"
        "6. Dunith Wellalage (1.45)  7. Daniel Sams (1.43)  8. Patrick Cummins (1.41)  9. Shaheen Afridi (1.37)  10. Richard Ngarava (1.37)"
    )
    p1.insert_textbox(fitz.Rect(40, 600, 555, 635), bowl_summary, fontsize=8.5, color=(0.18, 0.08, 0.28), fontname="helv")

    # Embed pressure_distribution.png on page 1 bottom
    img_dist = os.path.join(OUTPUT_DIR, "pressure_distribution.png")
    if os.path.exists(img_dist):
        p1.insert_image(fitz.Rect(140, 645, 455, 815), filename=img_dist)

    # Page 2: Mathematical Formulation & Pressure Heatmap
    p2 = add_page()
    p2.draw_rect(fitz.Rect(0, 0, 595, 45), color=None, fill=(0.18, 0.08, 0.28))
    p2.insert_text((40, 28), "Section 2: Dynamic Pressure Modeling Architecture", fontsize=14, color=(1, 1, 1), fontname="helv")

    sec2_text = (
        "Pressure Definition & Formulations:\n"
        "1. Second Innings Chases (Win-Probability Knife Edge):\n"
        "   P(Win) is modeled using required runs/ball, balls remaining, and wickets in hand. Pressure is maximized when\n"
        "   the contest hangs on a knife-edge: Match_Balance = 1.0 - 2.0 * |P(Win) - 0.50|.\n\n"
        "2. First Innings Par Score Expectations:\n"
        "   Par total is projected based on (Overs, Wickets). Deviation triggers sigmoid pressure scaling:\n"
        "   Deviation = (Par_Total * (Balls/120)^0.85 - Runs) / Par_Total\n"
        "   First_Inn_Pressure = 1 / (1 + exp(-6.0 * (|Deviation| - 0.30))).\n\n"
        "3. Multipliers: Phase (Death overs = 1.30x), Tournament Stakes (Knockout = 1.30x), Momentum (+0.08 per recent wicket)."
    )
    p2.insert_textbox(fitz.Rect(40, 60, 555, 205), sec2_text, fontsize=9, color=(0.15, 0.15, 0.15), fontname="helv")

    img_heat = os.path.join(OUTPUT_DIR, "pressure_heatmap.png")
    if os.path.exists(img_heat):
        p2.insert_image(fitz.Rect(75, 215, 520, 515), filename=img_heat)

    img_curve = os.path.join(OUTPUT_DIR, "pressure_curve_match_39808.png")
    if os.path.exists(img_curve):
        p2.insert_image(fitz.Rect(75, 530, 520, 815), filename=img_curve)

    # Page 3: Clutch Factor & Charts
    p3 = add_page()
    p3.draw_rect(fitz.Rect(0, 0, 595, 45), color=None, fill=(0.92, 0.10, 0.52))
    p3.insert_text((40, 28), "Section 3 & 4: Clutch Factor Evidence & Top 10 Visuals", fontsize=14, color=(1, 1, 1), fontname="helv")

    sec3_text = (
        "Clutch Factor (CF) Formulations:\n"
        "• Batting: CF = 0.35*(SR_p/SR_b) + 0.25*(Avg_p/Avg_b) + 0.20*(Bnd%_p/Bnd%_b) + 0.20*((1-Dot%_p)/(1-Dot%_b))\n"
        "• Bowling: CF = 0.30*(Econ_b/Econ_p) + 0.25*(SR_b/SR_p) + 0.25*(Dot%_p/Dot%_b) + 0.20*((1-Bnd_p)/(1-Bnd_b))\n"
        "• Empirical Bayes Shrinkage: Weighted_CF = 1.0 + (CF - 1.0) * (Pressure_Balls / (Pressure_Balls + 50))\n"
        "  Thresholds: Minimum 100 pressure balls and 200 total balls to eliminate small-sample noise."
    )
    p3.insert_textbox(fitz.Rect(40, 55, 555, 135), sec3_text, fontsize=8.5, color=(0.15, 0.15, 0.15), fontname="helv")

    img_bat = os.path.join(OUTPUT_DIR, "top_batters_clutch.png")
    if os.path.exists(img_bat):
        p3.insert_image(fitz.Rect(40, 140, 555, 465), filename=img_bat)

    img_bowl = os.path.join(OUTPUT_DIR, "top_bowlers_clutch.png")
    if os.path.exists(img_bowl):
        p3.insert_image(fitz.Rect(40, 480, 555, 805), filename=img_bowl)

    # Page 4: Radar, Comparison & Limitations
    p4 = add_page()
    p4.draw_rect(fitz.Rect(0, 0, 595, 45), color=None, fill=(0.18, 0.08, 0.28))
    p4.insert_text((40, 28), "Section 5: Player Profiles, IPL Context & Reliability", fontsize=14, color=(1, 1, 1), fontname="helv")

    img_radar = os.path.join(OUTPUT_DIR, "player_profile_mahedi_hasan.png")
    if os.path.exists(img_radar):
        p4.insert_image(fitz.Rect(40, 60, 310, 340), filename=img_radar)

    img_comp = os.path.join(OUTPUT_DIR, "comparison_baseline_sr_vs_pressure_sr.png")
    if os.path.exists(img_comp):
        p4.insert_image(fitz.Rect(320, 60, 555, 340), filename=img_comp)

    sec5_text = (
        "Tournament Context & Fair Comparisons (IPL vs T20I):\n"
        "• IPL Sub-Cohort Analysis: Evaluated separately across 87,687 deliveries.\n"
        "  Top IPL Batters: Sameer Rizvi, Karun Nair, Washington Sundar, Rovman Powell (RR), Rajat Patidar, Rahul Tewatia.\n"
        "  Top IPL Bowlers: Daniel Sams, Arshad Khan, Cameron Green, Patrick Cummins, Mayank Yadav, Trent Boult (RR).\n\n"
        "Reliability & Sensitivity Analysis:\n"
        "• Stability: Cross-checked across 50, 100, 150, and 200 pressure ball thresholds; elite names remained persistent.\n"
        "• Empirical Bayes Shrinkage ensures sustained performers over hundreds of deliveries dominate flash-in-the-pan anomalies.\n\n"
        "Limitations & Future Extensions:\n"
        "1. Opponent Quality: Incorporating Elo ratings for bowling attacks across associate series.\n"
        "2. Impact Player Rule: Adjusting for the extended batting depth in IPL 2023-2026.\n"
        "3. Field Placements & Missed Chances: Beyond standard ball-by-ball logging."
    )
    p4.insert_textbox(fitz.Rect(40, 355, 555, 800), sec5_text, fontsize=9, color=(0.15, 0.15, 0.15), fontname="helv")

    doc.save(pdf_path)
    doc.close()
    print(f"✔ Saved PDF to {pdf_path}")

if __name__ == "__main__":
    generate_docx()
    generate_pdf()

