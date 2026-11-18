"""
build_html_dashboard.py — Inlines data into a self-contained, responsive,
Rajasthan Royals-branded interactive web dashboard.
"""

import os
import json

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DASHBOARD_DIR = os.path.join(PROJECT_ROOT, "dashboard")
DATA_DIR = os.path.join(DASHBOARD_DIR, "data")

with open(os.path.join(DATA_DIR, "rankings.json"), "r") as f:
    rankings_data = json.load(f)

with open(os.path.join(DATA_DIR, "extras.json"), "r") as f:
    extras_data = json.load(f)

html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SupeRR Selector Season 2 | Pressure Analytics Hub</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js CDN -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --rr-pink: #EA1A85;
            --rr-dark: #1E1035;
            --rr-blue: #0A1931;
            --rr-gold: #F5A623;
        }
        .bg-rr-pink { background-color: var(--rr-pink); }
        .text-rr-pink { color: var(--rr-pink); }
        .border-rr-pink { border-color: var(--rr-pink); }
        .bg-rr-dark { background-color: var(--rr-dark); }
        .bg-rr-card { background-color: #261642; }
        .tab-active {
            border-bottom: 3px solid #EA1A85;
            color: #EA1A85;
            font-weight: 700;
        }
    </style>
</head>
<body class="bg-[#120824] text-slate-100 font-sans min-h-screen">

    <!-- Top Navigation -->
    <header class="sticky top-0 z-50 bg-[#1A0C33]/90 backdrop-blur-md border-b border-purple-900/50 px-6 py-4 shadow-xl">
        <div class="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-pink-600 to-[#EA1A85] flex items-center justify-center font-black text-xl shadow-lg shadow-pink-500/30">
                    RR
                </div>
                <div>
                    <h1 class="text-xl font-bold tracking-tight text-white flex items-center gap-2">
                        SupeRR Selector <span class="text-xs bg-pink-500/20 text-pink-300 border border-pink-500/40 px-2 py-0.5 rounded-full font-semibold">Season 2</span>
                    </h1>
                    <p class="text-xs text-purple-300">Pressure Performance Hub • Rajasthan Royals Analytics</p>
                </div>
            </div>
            <nav class="flex items-center space-x-2 text-sm">
                <a href="#overview" class="px-3 py-1.5 rounded-lg hover:bg-purple-800/40 transition">Overview</a>
                <a href="#rankings" class="px-3 py-1.5 rounded-lg hover:bg-purple-800/40 transition">Top 10 Rankings</a>
                <a href="#deep-dive" class="px-3 py-1.5 rounded-lg hover:bg-purple-800/40 transition">Player Radar</a>
                <a href="#tension-curve" class="px-3 py-1.5 rounded-lg hover:bg-purple-800/40 transition">Match Tension</a>
                <a href="#simulator" class="px-3 py-1.5 rounded-lg hover:bg-purple-800/40 transition">DPI Simulator</a>
                <a href="#methodology" class="px-3 py-1.5 rounded-lg bg-pink-600/30 text-pink-300 hover:bg-pink-600/50 transition border border-pink-500/30 font-medium">Methodology</a>
            </nav>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-4 md:px-6 py-8 space-y-12">

        <!-- Hero & KPI Banner -->
        <section id="overview" class="relative rounded-3xl overflow-hidden bg-gradient-to-br from-[#2D1446] via-[#200F36] to-[#120824] border border-pink-500/20 p-8 shadow-2xl">
            <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-8">
                <div class="max-w-2xl space-y-3">
                    <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                        <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> Round 1 Verified Submission Ready
                    </span>
                    <h2 class="text-3xl md:text-4xl font-extrabold tracking-tight text-white">
                        Identifying Players Who <span class="text-transparent bg-clip-text bg-gradient-to-r from-pink-400 to-rose-400">Rise Under Pressure</span>
                    </h2>
                    <p class="text-sm md:text-base text-purple-200/80 leading-relaxed">
                        Rather than treating death overs as uniform pressure, our system models dynamic win-probability knife-edge tension at every single delivery. We rank batters and bowlers by how much they elevate over their baseline when the game is on the line.
                    </p>
                </div>
                <div class="flex flex-wrap lg:flex-nowrap gap-3">
                    <a href="../Methodology_Report_SupeRR_Selector.pdf" target="_blank" class="px-5 py-3 rounded-xl bg-pink-600 hover:bg-pink-500 text-white font-semibold text-sm shadow-lg shadow-pink-600/30 flex items-center gap-2 transition">
                        <i class="fa-solid fa-file-pdf"></i> Download PDF Report
                    </a>
                    <a href="../Methodology_Report_SupeRR_Selector.docx" target="_blank" class="px-5 py-3 rounded-xl bg-purple-900/60 hover:bg-purple-800 text-purple-200 border border-purple-700/50 font-semibold text-sm flex items-center gap-2 transition">
                        <i class="fa-solid fa-file-word"></i> Download Word Doc
                    </a>
                </div>
            </div>

            <!-- KPI Cards Grid -->
            <div class="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4 mt-8 pt-6 border-t border-purple-900/40">
                <div class="bg-purple-950/40 rounded-2xl p-4 border border-purple-800/30">
                    <p class="text-xs text-purple-300 font-medium">Deliveries Analyzed</p>
                    <p class="text-2xl font-black text-white mt-1">200,999</p>
                    <p class="text-[10px] text-emerald-400 mt-0.5">IPL + T20I (2022-26)</p>
                </div>
                <div class="bg-purple-950/40 rounded-2xl p-4 border border-purple-800/30">
                    <p class="text-xs text-purple-300 font-medium">Total Matches</p>
                    <p class="text-2xl font-black text-white mt-1">867</p>
                    <p class="text-[10px] text-purple-300 mt-0.5">371 IPL / 512 T20I</p>
                </div>
                <div class="bg-purple-950/40 rounded-2xl p-4 border border-purple-800/30">
                    <p class="text-xs text-purple-300 font-medium">Pressure Deliveries</p>
                    <p class="text-2xl font-black text-pink-400 mt-1">60,311</p>
                    <p class="text-[10px] text-pink-300 mt-0.5">30.0% with DPI > 0.60</p>
                </div>
                <div class="bg-purple-950/40 rounded-2xl p-4 border border-purple-800/30">
                    <p class="text-xs text-purple-300 font-medium">Candidate Pool</p>
                    <p class="text-2xl font-black text-white mt-1">1,217</p>
                    <p class="text-[10px] text-purple-300 mt-0.5">158 eligible batters</p>
                </div>
                <div class="bg-purple-950/40 rounded-2xl p-4 border border-purple-800/30">
                    <p class="text-xs text-purple-300 font-medium">Top Clutch Batter</p>
                    <p class="text-lg font-black text-white mt-1 truncate">Mahedi Hasan</p>
                    <p class="text-[10px] text-pink-400 font-bold mt-0.5">1.592 Weighted CF</p>
                </div>
                <div class="bg-purple-950/40 rounded-2xl p-4 border border-purple-800/30">
                    <p class="text-xs text-purple-300 font-medium">Top Clutch Bowler</p>
                    <p class="text-lg font-black text-white mt-1 truncate">Ripon Mondol</p>
                    <p class="text-[10px] text-pink-400 font-bold mt-0.5">1.689 Weighted CF</p>
                </div>
            </div>
        </section>

        <!-- Player Rankings Section -->
        <section id="rankings" class="space-y-6">
            <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
                <div>
                    <h2 class="text-2xl font-extrabold text-white flex items-center gap-2">
                        <i class="fa-solid fa-trophy text-amber-400"></i> Top 10 Player Rankings Under Pressure
                    </h2>
                    <p class="text-sm text-purple-300">Official rank-ordered submissions for Unstop dropdown selections</p>
                </div>

                <!-- Controls: Filter & Cohort -->
                <div class="flex flex-wrap items-center gap-3">
                    <div class="bg-[#1F103A] p-1 rounded-xl border border-purple-800/50 flex">
                        <button onclick="setCohort('overall')" id="cohort-overall" class="px-3 py-1.5 rounded-lg text-xs font-semibold bg-pink-600 text-white transition">Combined (IPL+T20I)</button>
                        <button onclick="setCohort('ipl')" id="cohort-ipl" class="px-3 py-1.5 rounded-lg text-xs font-semibold text-purple-300 hover:text-white transition">IPL Only</button>
                        <button onclick="setCohort('t20i')" id="cohort-t20i" class="px-3 py-1.5 rounded-lg text-xs font-semibold text-purple-300 hover:text-white transition">T20I Only</button>
                    </div>
                    <div class="relative">
                        <i class="fa-solid fa-magnifying-glass absolute left-3 top-2.5 text-xs text-purple-400"></i>
                        <input type="text" id="player-search" oninput="filterPlayers()" placeholder="Search player..." class="bg-[#1F103A] border border-purple-800/50 rounded-xl pl-8 pr-3 py-1.5 text-xs text-white focus:outline-none focus:border-pink-500 w-44">
                    </div>
                </div>
            </div>

            <!-- Tab Switcher: Batters vs Bowlers -->
            <div class="border-b border-purple-900/60 flex space-x-8 text-sm">
                <button onclick="switchRole('batters')" id="tab-batters" class="pb-3 tab-active flex items-center gap-2 transition">
                    <i class="fa-solid fa-baseball-bat-ball"></i> Top Batters Under Pressure (Dropdown List)
                </button>
                <button onclick="switchRole('bowlers')" id="tab-bowlers" class="pb-3 text-purple-400 hover:text-white flex items-center gap-2 transition">
                    <i class="fa-solid fa-bowling-ball"></i> Top Bowlers Under Pressure (Dropdown List)
                </button>
            </div>

            <!-- Batters Table Container -->
            <div id="batters-view" class="overflow-x-auto rounded-2xl border border-purple-900/40 bg-[#1A0C33] shadow-xl">
                <table class="w-full text-left text-xs">
                    <thead class="bg-[#241244] text-purple-300 font-semibold uppercase tracking-wider text-[11px] border-b border-purple-800/50">
                        <tr>
                            <th class="py-3 px-4">#</th>
                            <th class="py-3 px-4">Player</th>
                            <th class="py-3 px-4 text-center">Weighted Clutch</th>
                            <th class="py-3 px-4 text-center">Raw Clutch</th>
                            <th class="py-3 px-4 text-center">Strike Rate (Press / Base)</th>
                            <th class="py-3 px-4 text-center">Average (Press / Base)</th>
                            <th class="py-3 px-4 text-center">Boundary %</th>
                            <th class="py-3 px-4 text-center">Dot %</th>
                            <th class="py-3 px-4 text-center">Pressure Balls</th>
                            <th class="py-3 px-4 text-center">Action</th>
                        </tr>
                    </thead>
                    <tbody id="batters-table-body" class="divide-y divide-purple-900/30">
                        <!-- Populated by JS -->
                    </tbody>
                </table>
            </div>

            <!-- Bowlers Table Container -->
            <div id="bowlers-view" class="hidden overflow-x-auto rounded-2xl border border-purple-900/40 bg-[#1A0C33] shadow-xl">
                <table class="w-full text-left text-xs">
                    <thead class="bg-[#241244] text-purple-300 font-semibold uppercase tracking-wider text-[11px] border-b border-purple-800/50">
                        <tr>
                            <th class="py-3 px-4">#</th>
                            <th class="py-3 px-4">Player</th>
                            <th class="py-3 px-4 text-center">Weighted Clutch</th>
                            <th class="py-3 px-4 text-center">Raw Clutch</th>
                            <th class="py-3 px-4 text-center">Economy (Press / Base)</th>
                            <th class="py-3 px-4 text-center">Bowling SR (Press / Base)</th>
                            <th class="py-3 px-4 text-center">Dot % (Press / Base)</th>
                            <th class="py-3 px-4 text-center">Boundaries Conceded %</th>
                            <th class="py-3 px-4 text-center">Pressure Balls</th>
                            <th class="py-3 px-4 text-center">Action</th>
                        </tr>
                    </thead>
                    <tbody id="bowlers-table-body" class="divide-y divide-purple-900/30">
                        <!-- Populated by JS -->
                    </tbody>
                </table>
            </div>
        </section>

        <!-- Player Deep Dive & Radar Chart -->
        <section id="deep-dive" class="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
            <!-- Radar Chart Card -->
            <div class="lg:col-span-7 bg-[#1A0C33] border border-purple-900/40 rounded-3xl p-6 shadow-xl space-y-4">
                <div class="flex items-center justify-between">
                    <div>
                        <h3 class="text-lg font-bold text-white flex items-center gap-2">
                            <i class="fa-solid fa-chart-pie text-pink-400"></i> Player Resilience Radar Profile
                        </h3>
                        <p class="text-xs text-purple-300">Multi-metric shift from routine baseline to high-pressure moments</p>
                    </div>
                    <span id="radar-player-badge" class="px-3 py-1 rounded-full text-xs font-bold bg-pink-500/20 text-pink-300 border border-pink-500/40">
                        Mahedi Hasan (Rank 1)
                    </span>
                </div>
                <div class="h-80 flex items-center justify-center">
                    <canvas id="radarChart"></canvas>
                </div>
            </div>

            <!-- Player Spotlight Card -->
            <div class="lg:col-span-5 bg-gradient-to-br from-[#261442] to-[#1A0C33] border border-purple-800/40 rounded-3xl p-6 shadow-xl space-y-4">
                <div class="flex items-center justify-between border-b border-purple-800/40 pb-4">
                    <div>
                        <h4 id="spotlight-name" class="text-2xl font-black text-white">Mahedi Hasan</h4>
                        <p id="spotlight-role" class="text-xs text-purple-300">All-Rounder • Bangladesh / T20</p>
                    </div>
                    <div class="text-right">
                        <span id="spotlight-rank" class="text-2xl font-black text-pink-400">#1</span>
                        <p class="text-[10px] text-purple-300 uppercase tracking-widest font-bold">Unstop Rank</p>
                    </div>
                </div>

                <div class="space-y-3 text-xs">
                    <div class="bg-purple-950/50 p-3 rounded-xl border border-purple-800/30 flex justify-between items-center">
                        <span class="text-purple-300">Weighted Clutch Factor</span>
                        <span id="spotlight-weighted" class="font-bold text-pink-400 text-sm">1.592</span>
                    </div>
                    <div class="bg-purple-950/50 p-3 rounded-xl border border-purple-800/30 flex justify-between items-center">
                        <span class="text-purple-300">Raw Elevation Factor</span>
                        <span id="spotlight-raw" class="font-bold text-emerald-400 text-sm">1.844 (Elevated)</span>
                    </div>
                    <div class="bg-purple-950/50 p-3 rounded-xl border border-purple-800/30 flex justify-between items-center">
                        <span class="text-purple-300">Strike Rate Shift</span>
                        <span id="spotlight-sr-shift" class="font-bold text-white">81.5 → 131.4 (+61.2%)</span>
                    </div>
                    <div class="bg-purple-950/50 p-3 rounded-xl border border-purple-800/30 flex justify-between items-center">
                        <span class="text-purple-300">Average Shift</span>
                        <span id="spotlight-avg-shift" class="font-bold text-white">10.0 → 22.1 (+121.0%)</span>
                    </div>
                    <div class="bg-purple-950/50 p-3 rounded-xl border border-purple-800/30 flex justify-between items-center">
                        <span class="text-purple-300">Pressure Balls Logged</span>
                        <span id="spotlight-balls" class="font-bold text-white">118 deliveries</span>
                    </div>
                </div>

                <p id="spotlight-desc" class="text-xs text-purple-200/80 leading-relaxed bg-[#190C30] p-3 rounded-xl border border-purple-800/20 italic">
                    "Elevates his strike rate from 81.5 in routine phases to 131.4 under intense pressure, with average doubling from 10.0 to 22.1. A fearless lower-order counter-attacker who consistently thrives when behind par."
                </p>
            </div>
        </section>

        <!-- Match Tension Curve & Heatmap -->
        <section id="tension-curve" class="space-y-6">
            <div class="flex flex-col md:flex-row md:items-end justify-between gap-4">
                <div>
                    <h2 class="text-2xl font-extrabold text-white flex items-center gap-2">
                        <i class="fa-solid fa-chart-line text-pink-400"></i> Match Tension Curve Simulator (Match 39808)
                    </h2>
                    <p class="text-sm text-purple-300">Ball-by-ball Dynamic Pressure Index (DPI) evolution in a high-volatility T20 thriller</p>
                </div>
            </div>

            <div class="bg-[#1A0C33] border border-purple-900/40 rounded-3xl p-6 shadow-xl space-y-4">
                <div class="h-80">
                    <canvas id="matchCurveChart"></canvas>
                </div>
                <div class="flex flex-wrap items-center justify-between text-xs text-purple-300 border-t border-purple-900/40 pt-4">
                    <div class="flex items-center gap-4">
                        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-blue-500"></span> Low (DPI &le; 0.40)</span>
                        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-amber-500"></span> Moderate (0.40-0.60)</span>
                        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-orange-500"></span> High (0.60-0.80)</span>
                        <span class="flex items-center gap-1.5"><span class="w-3 h-3 rounded-full bg-rose-500"></span> Extreme (> 0.80)</span>
                    </div>
                    <span class="text-purple-400 italic">Notice how tension surges above 0.85 during the 18th-20th over finish</span>
                </div>
            </div>
        </section>

        <!-- Interactive DPI Calculator Simulator -->
        <section id="simulator" class="bg-gradient-to-br from-[#23123D] to-[#16092C] border border-pink-500/20 rounded-3xl p-8 shadow-xl space-y-6">
            <div>
                <h2 class="text-2xl font-extrabold text-white flex items-center gap-2">
                    <i class="fa-solid fa-sliders text-pink-400"></i> Interactive Dynamic Pressure Calculator
                </h2>
                <p class="text-sm text-purple-300">Test the win-probability and par-score pressure engine in real time</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-12 gap-8 items-center">
                <!-- Sliders -->
                <div class="md:col-span-7 space-y-4">
                    <div>
                        <div class="flex justify-between text-xs font-semibold mb-1">
                            <span class="text-purple-300">Required Run Rate (2nd Innings)</span>
                            <span id="sim-rrr-val" class="text-pink-400 font-bold">10.5 RPO</span>
                        </div>
                        <input type="range" id="sim-rrr" min="4" max="24" step="0.5" value="10.5" oninput="runSim()" class="w-full accent-pink-500">
                    </div>

                    <div>
                        <div class="flex justify-between text-xs font-semibold mb-1">
                            <span class="text-purple-300">Balls Remaining in Innings</span>
                            <span id="sim-balls-val" class="text-pink-400 font-bold">18 balls (Over 17.0)</span>
                        </div>
                        <input type="range" id="sim-balls" min="1" max="120" step="1" value="18" oninput="runSim()" class="w-full accent-pink-500">
                    </div>

                    <div>
                        <div class="flex justify-between text-xs font-semibold mb-1">
                            <span class="text-purple-300">Wickets in Hand</span>
                            <span id="sim-wkts-val" class="text-pink-400 font-bold">4 wickets (Score: 6 down)</span>
                        </div>
                        <input type="range" id="sim-wkts" min="1" max="10" step="1" value="4" oninput="runSim()" class="w-full accent-pink-500">
                    </div>

                    <div class="grid grid-cols-2 gap-4 pt-2">
                        <label class="flex items-center space-x-2 text-xs text-purple-200 cursor-pointer">
                            <input type="checkbox" id="sim-ko" onchange="runSim()" checked class="accent-pink-500 rounded">
                            <span>Knockout / Playoff Game (1.30x)</span>
                        </label>
                        <label class="flex items-center space-x-2 text-xs text-purple-200 cursor-pointer">
                            <input type="checkbox" id="sim-cluster" onchange="runSim()" checked class="accent-pink-500 rounded">
                            <span>Wicket Fallen in Last 6 Balls</span>
                        </label>
                    </div>
                </div>

                <!-- Live Score Output Display -->
                <div class="md:col-span-5 bg-[#1A0C33] border border-purple-800/40 rounded-2xl p-6 text-center space-y-3">
                    <p class="text-xs uppercase tracking-widest font-bold text-purple-400">Calculated Dynamic Pressure (DPI)</p>
                    <div id="sim-dpi-display" class="text-5xl font-black text-rose-500 animate-pulse">0.892</div>
                    <span id="sim-cat-badge" class="inline-block px-4 py-1 rounded-full text-xs font-extrabold uppercase tracking-wide bg-rose-500/20 text-rose-300 border border-rose-500/40">
                        Extreme Pressure
                    </span>
                    <p id="sim-explanation" class="text-[11px] text-purple-300/80 leading-relaxed pt-2">
                        Match is on a knife edge (chase win probability ~48%). Death-over leverage and recent wicket cluster maximize bowling and batting tension.
                    </p>
                </div>
            </div>
        </section>

        <!-- Methodology Reference -->
        <section id="methodology" class="bg-[#1A0C33] border border-purple-900/40 rounded-3xl p-8 shadow-xl space-y-6">
            <div class="border-b border-purple-900/50 pb-4">
                <h2 class="text-2xl font-extrabold text-white flex items-center gap-2">
                    <i class="fa-solid fa-brain text-pink-400"></i> Methodology & Scientific Framework
                </h2>
                <p class="text-sm text-purple-300">Addressing all five requirements of the Rajasthan Royals SupeRR Selector brief</p>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 text-xs text-purple-200/80">
                <div class="bg-purple-950/30 p-5 rounded-2xl border border-purple-800/30 space-y-2">
                    <h4 class="font-bold text-white text-sm flex items-center gap-2">
                        <i class="fa-solid fa-scale-balanced text-pink-400"></i> 1. Knife-Edge Maximum
                    </h4>
                    <p>Pressure is non-linear and peaks when win probability is closest to 50/50. One-sided blowouts have low pressure even in over 19.</p>
                </div>
                <div class="bg-purple-950/30 p-5 rounded-2xl border border-purple-800/30 space-y-2">
                    <h4 class="font-bold text-white text-sm flex items-center gap-2">
                        <i class="fa-solid fa-chart-line text-emerald-400"></i> 2. Par-Score Deviations
                    </h4>
                    <p>In the first innings, pressure is dictated by dynamic departure from projected par score across over-by-wicket matrix states.</p>
                </div>
                <div class="bg-purple-950/30 p-5 rounded-2xl border border-purple-800/30 space-y-2">
                    <h4 class="font-bold text-white text-sm flex items-center gap-2">
                        <i class="fa-solid fa-calculator text-amber-400"></i> 3. 4D Clutch Factor
                    </h4>
                    <p>Batting and bowling metrics balance Strike Rate/Economy, Average, Boundary striking, and non-dot scoring efficiency with baseline = 1.000.</p>
                </div>
                <div class="bg-purple-950/30 p-5 rounded-2xl border border-purple-800/30 space-y-2">
                    <h4 class="font-bold text-white text-sm flex items-center gap-2">
                        <i class="fa-solid fa-filter text-sky-400"></i> 4. Empirical Bayes Shrinkage
                    </h4>
                    <p>Small-sample noise is mathematically pulled to neutral baseline via N/(N+50) weight, ensuring large-sample reliability.</p>
                </div>
                <div class="bg-purple-950/30 p-5 rounded-2xl border border-purple-800/30 space-y-2">
                    <h4 class="font-bold text-white text-sm flex items-center gap-2">
                        <i class="fa-solid fa-trophy text-rose-400"></i> 5. Tournament Context
                    </h4>
                    <p>Separate cross-validations for IPL (87K balls) and T20I (113K balls), featuring franchise icons like Tewatia, Patidar, Cummins & Boult.</p>
                </div>
                <div class="bg-purple-950/30 p-5 rounded-2xl border border-purple-800/30 space-y-2">
                    <h4 class="font-bold text-white text-sm flex items-center gap-2">
                        <i class="fa-solid fa-shield-halved text-purple-400"></i> 6. Dropdown Alignment
                    </h4>
                    <p>All 20 selected players are rigorously verified against official tournament squad lists for instant Unstop selection.</p>
                </div>
            </div>
        </section>

    </main>

    <!-- Footer -->
    <footer class="border-t border-purple-900/50 bg-[#0E061C] py-8 text-center text-xs text-purple-400">
        <p class="font-medium text-purple-300">Rajasthan Royals SupeRR Selector Season 2 • Round 1 Analysis</p>
        <p class="mt-1">Developed for Unstop Hackathon Submission • Data: 2022–2026 IPL & T20I</p>
    </footer>

    <!-- INLINED DATA AND LOGIC -->
    <script>
        const RANKINGS_DATA = """ + json.dumps(rankings_data) + """;
        const EXTRAS_DATA = """ + json.dumps(extras_data) + """;

        let currentCohort = 'overall';
        let currentRole = 'batters';
        let radarChartInstance = null;
        let matchCurveChartInstance = null;

        // Initialize on load
        document.addEventListener('DOMContentLoaded', () => {
            renderTables();
            initRadarChart();
            initMatchCurveChart();
            runSim();
        });

        function setCohort(cohort) {
            currentCohort = cohort;
            ['overall', 'ipl', 't20i'].forEach(c => {
                const btn = document.getElementById('cohort-' + c);
                if (c === cohort) {
                    btn.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold bg-pink-600 text-white transition';
                } else {
                    btn.className = 'px-3 py-1.5 rounded-lg text-xs font-semibold text-purple-300 hover:text-white transition';
                }
            });
            renderTables();
        }

        function switchRole(role) {
            currentRole = role;
            const batBtn = document.getElementById('tab-batters');
            const bowlBtn = document.getElementById('tab-bowlers');
            const batView = document.getElementById('batters-view');
            const bowlView = document.getElementById('bowlers-view');

            if (role === 'batters') {
                batBtn.className = 'pb-3 tab-active flex items-center gap-2 transition';
                bowlBtn.className = 'pb-3 text-purple-400 hover:text-white flex items-center gap-2 transition';
                batView.classList.remove('hidden');
                bowlView.classList.add('hidden');
            } else {
                bowlBtn.className = 'pb-3 tab-active flex items-center gap-2 transition';
                batBtn.className = 'pb-3 text-purple-400 hover:text-white flex items-center gap-2 transition';
                bowlView.classList.remove('hidden');
                batView.classList.add('hidden');
            }
        }

        function renderTables() {
            renderBattersTable();
            renderBowlersTable();
        }

        function renderBattersTable() {
            const listKey = currentCohort + '_batters';
            const batters = (RANKINGS_DATA[listKey] || []).slice(0, 10);
            const tbody = document.getElementById('batters-table-body');
            tbody.innerHTML = '';

            batters.forEach((b, idx) => {
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-purple-900/30 transition cursor-pointer';
                tr.onclick = () => selectPlayer('batter', b);

                tr.innerHTML = `
                    <td class="py-3 px-4 font-black text-pink-400">#${idx + 1}</td>
                    <td class="py-3 px-4 font-bold text-white">${b.player_name}</td>
                    <td class="py-3 px-4 text-center font-extrabold text-pink-400">${Number(b.weighted_clutch).toFixed(3)}</td>
                    <td class="py-3 px-4 text-center text-purple-300">${Number(b.clutch_factor).toFixed(3)}</td>
                    <td class="py-3 px-4 text-center">
                        <span class="font-bold text-emerald-400">${Number(b.pressure_sr).toFixed(1)}</span>
                        <span class="text-purple-400 text-[10px]"> / ${Number(b.baseline_sr).toFixed(1)}</span>
                    </td>
                    <td class="py-3 px-4 text-center">
                        <span class="font-bold text-emerald-400">${Number(b.pressure_batting_avg).toFixed(1)}</span>
                        <span class="text-purple-400 text-[10px]"> / ${Number(b.baseline_batting_avg).toFixed(1)}</span>
                    </td>
                    <td class="py-3 px-4 text-center font-medium">${(Number(b.pressure_boundary_pct)*100).toFixed(1)}%</td>
                    <td class="py-3 px-4 text-center font-medium text-purple-300">${(Number(b.pressure_dot_ball_pct)*100).toFixed(1)}%</td>
                    <td class="py-3 px-4 text-center font-bold text-purple-200">${b.pressure_balls}</td>
                    <td class="py-3 px-4 text-center">
                        <button class="px-2 py-1 rounded bg-purple-800/50 hover:bg-pink-600 text-[10px] text-white transition">View</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        function renderBowlersTable() {
            const listKey = currentCohort + '_bowlers';
            const bowlers = (RANKINGS_DATA[listKey] || []).slice(0, 10);
            const tbody = document.getElementById('bowlers-table-body');
            tbody.innerHTML = '';

            bowlers.forEach((b, idx) => {
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-purple-900/30 transition cursor-pointer';
                tr.onclick = () => selectPlayer('bowler', b);

                tr.innerHTML = `
                    <td class="py-3 px-4 font-black text-pink-400">#${idx + 1}</td>
                    <td class="py-3 px-4 font-bold text-white">${b.player_name}</td>
                    <td class="py-3 px-4 text-center font-extrabold text-pink-400">${Number(b.weighted_clutch).toFixed(3)}</td>
                    <td class="py-3 px-4 text-center text-purple-300">${Number(b.clutch_factor).toFixed(3)}</td>
                    <td class="py-3 px-4 text-center">
                        <span class="font-bold text-emerald-400">${Number(b.pressure_economy).toFixed(2)}</span>
                        <span class="text-purple-400 text-[10px]"> / ${Number(b.baseline_economy).toFixed(2)}</span>
                    </td>
                    <td class="py-3 px-4 text-center">
                        <span class="font-bold text-emerald-400">${Number(b.pressure_bowling_strike_rate).toFixed(1)}</span>
                        <span class="text-purple-400 text-[10px]"> / ${Number(b.baseline_bowling_strike_rate).toFixed(1)}</span>
                    </td>
                    <td class="py-3 px-4 text-center font-medium">${(Number(b.pressure_dot_ball_pct)*100).toFixed(1)}%</td>
                    <td class="py-3 px-4 text-center font-medium text-purple-300">${(Number(b.pressure_boundaries_conceded_pct)*100).toFixed(1)}%</td>
                    <td class="py-3 px-4 text-center font-bold text-purple-200">${b.pressure_balls}</td>
                    <td class="py-3 px-4 text-center">
                        <button class="px-2 py-1 rounded bg-purple-800/50 hover:bg-pink-600 text-[10px] text-white transition">View</button>
                    </td>
                `;
                tbody.appendChild(tr);
            });
        }

        function filterPlayers() {
            const query = document.getElementById('player-search').value.toLowerCase();
            const rows = document.querySelectorAll('#batters-table-body tr, #bowlers-table-body tr');
            rows.forEach(r => {
                const name = r.children[1].textContent.toLowerCase();
                r.style.display = name.includes(query) ? '' : 'none';
            });
        }

        function selectPlayer(type, p) {
            document.getElementById('radar-player-badge').textContent = p.player_name + ' (Rank ' + p.rank + ')';
            document.getElementById('spotlight-name').textContent = p.player_name;
            document.getElementById('spotlight-rank').textContent = '#' + p.rank;
            document.getElementById('spotlight-weighted').textContent = Number(p.weighted_clutch).toFixed(3);
            document.getElementById('spotlight-raw').textContent = Number(p.clutch_factor).toFixed(3) + ' (Elevated)';
            document.getElementById('spotlight-balls').textContent = p.pressure_balls + ' deliveries';

            if (type === 'batter') {
                document.getElementById('spotlight-role').textContent = 'Batter / Finisher';
                document.getElementById('spotlight-sr-shift').textContent = Number(p.baseline_sr).toFixed(1) + ' → ' + Number(p.pressure_sr).toFixed(1);
                document.getElementById('spotlight-avg-shift').textContent = Number(p.baseline_batting_avg).toFixed(1) + ' → ' + Number(p.pressure_batting_avg).toFixed(1);
                updateRadarBatter(p);
            } else {
                document.getElementById('spotlight-role').textContent = 'Bowler / Death Specialist';
                document.getElementById('spotlight-sr-shift').textContent = 'Econ: ' + Number(p.baseline_economy).toFixed(2) + ' → ' + Number(p.pressure_economy).toFixed(2);
                document.getElementById('spotlight-avg-shift').textContent = 'Bowl SR: ' + Number(p.baseline_bowling_strike_rate).toFixed(1) + ' → ' + Number(p.pressure_bowling_strike_rate).toFixed(1);
                updateRadarBowler(p);
            }
        }

        function initRadarChart() {
            const ctx = document.getElementById('radarChart').getContext('2d');
            radarChartInstance = new Chart(ctx, {
                type: 'radar',
                data: {
                    labels: ['Strike Rate Uplift', 'Average Preserved', 'Boundary Rate', 'Non-Dot Rotation', 'Sample Stability'],
                    datasets: [
                        {
                            label: 'Pressure Performance',
                            data: [85, 90, 80, 75, 88],
                            backgroundColor: 'rgba(234, 26, 133, 0.25)',
                            borderColor: '#EA1A85',
                            pointBackgroundColor: '#EA1A85',
                            borderWidth: 2
                        },
                        {
                            label: 'Player Normal Baseline',
                            data: [50, 50, 50, 50, 50],
                            backgroundColor: 'rgba(168, 85, 247, 0.1)',
                            borderColor: 'rgba(168, 85, 247, 0.6)',
                            borderDash: [4, 4],
                            borderWidth: 1.5
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        r: {
                            angleLines: { color: 'rgba(255, 255, 255, 0.1)' },
                            grid: { color: 'rgba(255, 255, 255, 0.1)' },
                            pointLabels: { color: '#D8B4FE', font: { size: 10 } },
                            ticks: { display: false, max: 100, min: 0 }
                        }
                    },
                    plugins: {
                        legend: { labels: { color: '#E2E8F0', font: { size: 11 } } }
                    }
                }
            });
        }

        function updateRadarBatter(p) {
            const srUplift = Math.min(100, Math.max(20, (p.pressure_sr / (p.baseline_sr || 1)) * 50));
            const avgUplift = Math.min(100, Math.max(20, (p.pressure_batting_avg / (p.baseline_batting_avg || 1)) * 50));
            const bndUplift = Math.min(100, Math.max(20, (p.pressure_boundary_pct / (p.baseline_boundary_pct || 0.1)) * 50));
            const rotUplift = Math.min(100, Math.max(20, ((1 - p.pressure_dot_ball_pct) / (1 - (p.baseline_dot_ball_pct || 0.5))) * 50));
            const stability = Math.min(95, 50 + (p.pressure_balls / 10));

            radarChartInstance.data.datasets[0].data = [srUplift, avgUplift, bndUplift, rotUplift, stability];
            radarChartInstance.update();
        }

        function updateRadarBowler(p) {
            const econUplift = Math.min(100, Math.max(20, (p.baseline_economy / (p.pressure_economy || 1)) * 50));
            const srUplift = Math.min(100, Math.max(20, (p.baseline_bowling_strike_rate / (p.pressure_bowling_strike_rate || 1)) * 50));
            const dotUplift = Math.min(100, Math.max(20, (p.pressure_dot_ball_pct / (p.baseline_dot_ball_pct || 0.2)) * 50));
            const bndSuppression = Math.min(100, Math.max(20, ((1 - p.pressure_boundaries_conceded_pct) / (1 - (p.baseline_boundaries_conceded_pct || 0.2))) * 50));
            const stability = Math.min(95, 50 + (p.pressure_balls / 10));

            radarChartInstance.data.datasets[0].data = [econUplift, srUplift, dotUplift, bndSuppression, stability];
            radarChartInstance.update();
        }

        function initMatchCurveChart() {
            const curve = EXTRAS_DATA.match_39808 || [];
            const ctx = document.getElementById('matchCurveChart').getContext('2d');

            const labels = curve.map(c => 'O' + c.over + '.' + c.ball);
            const dpis = curve.map(c => c.dpi);

            matchCurveChartInstance = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Dynamic Pressure Index (DPI)',
                        data: dpis,
                        borderColor: '#EA1A85',
                        backgroundColor: 'rgba(234, 26, 133, 0.1)',
                        fill: true,
                        tension: 0.3,
                        pointRadius: 2,
                        pointHoverRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        x: {
                            grid: { display: false },
                            ticks: { color: '#A855F7', maxTicksLimit: 20 }
                        },
                        y: {
                            min: 0,
                            max: 1.0,
                            grid: { color: 'rgba(255, 255, 255, 0.08)' },
                            ticks: { color: '#A855F7' }
                        }
                    },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                title: (items) => {
                                    const idx = items[0].dataIndex;
                                    const pt = curve[idx];
                                    return 'Inn ' + pt.innings + ' | Over ' + pt.over + '.' + pt.ball + ' (' + pt.score + ')';
                                },
                                label: (item) => {
                                    const pt = curve[item.dataIndex];
                                    return [
                                        'DPI: ' + pt.dpi + ' (' + pt.cat + ')',
                                        'Batter: ' + pt.striker + ' | Bowler: ' + pt.bowler,
                                        'Outcome: ' + (pt.is_wicket ? 'WICKET!' : pt.runs + ' runs')
                                    ];
                                }
                            }
                        }
                    }
                }
            });
        }

        function runSim() {
            const rrr = parseFloat(document.getElementById('sim-rrr').value);
            const balls = parseInt(document.getElementById('sim-balls').value);
            const wkts = parseInt(document.getElementById('sim-wkts').value);
            const isKnockout = document.getElementById('sim-ko').checked;
            const hasCluster = document.getElementById('sim-cluster').checked;

            document.getElementById('sim-rrr-val').textContent = rrr.toFixed(1) + ' RPO';
            document.getElementById('sim-balls-val').textContent = balls + ' balls (' + (balls/6).toFixed(1) + ' overs left)';
            document.getElementById('sim-wkts-val').textContent = wkts + ' wickets in hand (' + (10 - wkts) + ' down)';

            // Logistic win prob approximation
            const rpb = rrr / 6.0;
            const z = 0.5 + 3.5 * rpb - 0.35 * wkts;
            const winProb = 1.0 / (1.0 + Math.exp(z));

            // Knife-edge balance
            let basePressure = 1.0 - 2.0 * Math.abs(winProb - 0.5);

            // Phase multiplier
            const phaseMult = balls <= 30 ? 1.30 : 1.0;
            const stakesMult = isKnockout ? 1.30 : 1.0;
            const momMult = hasCluster ? 1.18 : 1.0;

            let dpi = Math.min(1.0, Math.max(0.0, basePressure * phaseMult * stakesMult * momMult));

            const dpiEl = document.getElementById('sim-dpi-display');
            const badgeEl = document.getElementById('sim-cat-badge');
            const expEl = document.getElementById('sim-explanation');

            dpiEl.textContent = dpi.toFixed(3);

            if (dpi > 0.80) {
                dpiEl.className = 'text-5xl font-black text-rose-500 animate-pulse';
                badgeEl.className = 'inline-block px-4 py-1 rounded-full text-xs font-extrabold uppercase tracking-wide bg-rose-500/20 text-rose-300 border border-rose-500/40';
                badgeEl.textContent = 'Extreme Pressure';
                expEl.textContent = 'Match is on a razor knife edge. Stakes and death leverage elevate pressure to maximum intensity.';
            } else if (dpi > 0.60) {
                dpiEl.className = 'text-5xl font-black text-orange-400';
                badgeEl.className = 'inline-block px-4 py-1 rounded-full text-xs font-extrabold uppercase tracking-wide bg-orange-500/20 text-orange-300 border border-orange-500/40';
                badgeEl.textContent = 'High Pressure';
                expEl.textContent = 'Game hanging in balance; one wicket or boundary will swing win probability decisively.';
            } else if (dpi > 0.40) {
                dpiEl.className = 'text-5xl font-black text-amber-400';
                badgeEl.className = 'inline-block px-4 py-1 rounded-full text-xs font-extrabold uppercase tracking-wide bg-amber-500/20 text-amber-300 border border-amber-500/40';
                badgeEl.textContent = 'Moderate Pressure';
                expEl.textContent = 'Standard match contest. Chase is manageable with moderate risk.';
            } else {
                dpiEl.className = 'text-5xl font-black text-blue-400';
                badgeEl.className = 'inline-block px-4 py-1 rounded-full text-xs font-extrabold uppercase tracking-wide bg-blue-500/20 text-blue-300 border border-blue-500/40';
                badgeEl.textContent = 'Low Pressure';
                expEl.textContent = 'One team is cruising or the contest is lopsided; minimal pressure on participants.';
            }
        }
    </script>
</body>
</html>
"""

output_html_path = os.path.join(DASHBOARD_DIR, "index.html")
with open(output_html_path, "w", encoding="utf-8") as f:
    f.write(html_template)

print(f"✔ Successfully generated standalone interactive HTML dashboard at: {output_html_path}")
