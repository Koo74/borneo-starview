"""
Advanced GeoAI Agent - Borneo AstroView Site Selection
=======================================================
CYBERPUNK EDITION v3.2.2: Futuristic UI + OSM Up-to-Date + INSTANT Results

FOCUSED ON: BEST STARGAZING & GALAXY VIEWING SPOTS IN SABAH & SARAWAK, MALAYSIA (Borneo) 🌌

V3.2.2 NEW:
- 🌫️ High-Altitude Fog Detection (distinguishes mountain fog from smoke haze)
- ✅ Correctly labels cold high-altitude clouds as "FOG" not "HAZE"
- ✅ Clean-air health advisory for natural fog (no false N95 warnings)
- ✅ Better action advice for foggy summits (go to lower elevation)

V3.2.1 FIX (preserved):
- ✅ Coastal cloud risk classifier (elevation < 50m → "Coastal")

V3.2 FEATURES (preserved):
- 🌫️ Haze Detection (transboundary smoke alerts)
- 📊 Live Air Quality Index (AQI) from Open-Meteo
- 💨 PM2.5, PM10, aerosol data
- 🌬️ Wind direction analysis
- 💚 Health advisories for outdoor activity
- 📅 Seasonal haze calendar for Malaysia

V3.1 FIXES (preserved):
- ✅ Population-weighted light pollution
- ✅ Distance-weighted inverse-square model

V3.0 FEATURES (preserved):
- 🌙 Moon Phase Integration
- 🌌 Milky Way Visibility Calendar
- 📸 Astrophotography Score
- 📊 Export Reports
"""

import streamlit as st
import folium
from folium.plugins import Fullscreen, MiniMap, MousePosition
from streamlit_folium import st_folium
import pandas as pd
import numpy as np
import json
import time
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import requests
from pathlib import Path
import sqlite3
import pickle
import math

# ============================================================================
# CYBERPUNK STYLING
# ============================================================================

CYBERPUNK_CSS = """
<style>
    :root {
        --neon-cyan: #00f0ff;
        --neon-pink: #ff2d95;
        --neon-purple: #b026ff;
        --neon-green: #39ff14;
        --neon-yellow: #ffe84d;
    }
    .stApp {
        background: linear-gradient(135deg, #0a0a0f 0%, #1a0a2e 50%, #0a0a1f 100%);
    }
    .main-title {
        font-family: 'Courier New', monospace;
        font-size: 3.5rem;
        font-weight: 900;
        background: linear-gradient(90deg, #00f0ff, #b026ff, #ff2d95);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        letter-spacing: 4px;
        animation: glowPulse 3s ease-in-out infinite;
    }
    @keyframes glowPulse {
        0%, 100% { text-shadow: 0 0 40px rgba(0, 240, 255, 0.3); }
        50% { text-shadow: 0 0 60px rgba(0, 240, 255, 0.6), 0 0 80px rgba(176, 38, 255, 0.3); }
    }
    .subtitle {
        font-family: 'Courier New', monospace;
        color: #00f0ff;
        font-size: 1.2rem;
        letter-spacing: 8px;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.3);
        border-bottom: 1px solid rgba(0, 240, 255, 0.2);
        padding-bottom: 10px;
        margin-bottom: 20px;
    }
    .css-1d391kg, .css-1633s9g {
        background: rgba(10, 10, 20, 0.95) !important;
        border-right: 1px solid rgba(0, 240, 255, 0.2) !important;
        backdrop-filter: blur(10px);
    }
    .css-1d391kg p, .css-1633s9g p,
    .css-1d391kg label, .css-1633s9g label,
    .css-1d391kg div, .css-1633s9g div,
    .css-1d391kg span, .css-1633s9g span {
        color: #ffffff !important;
        font-weight: 400 !important;
    }
    .recommendation-container {
        background: rgba(15, 15, 35, 0.85);
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 12px;
        padding: 20px;
        margin: 15px 0;
        backdrop-filter: blur(10px);
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.05);
        transition: all 0.3s ease;
    }
    .recommendation-container:hover {
        border-color: #00f0ff;
        box-shadow: 0 0 40px rgba(0, 240, 255, 0.15);
        transform: translateY(-2px);
    }
    .recommendation-title {
        color: #00f0ff;
        font-family: 'Courier New', monospace;
        font-size: 1.2rem;
        font-weight: bold;
        letter-spacing: 2px;
        margin-bottom: 10px;
        text-shadow: 0 0 20px rgba(0, 240, 255, 0.3);
    }
    .recommendation-item {
        color: #ffffff;
        font-family: 'Courier New', monospace;
        font-size: 0.9rem;
        padding: 6px 0;
        border-bottom: 1px solid rgba(0, 240, 255, 0.05);
        line-height: 1.6;
    }
    .recommendation-item:last-child { border-bottom: none; }
    .recommendation-item .icon { margin-right: 8px; }
    .stButton > button {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.15), rgba(176, 38, 255, 0.15)) !important;
        border: 1px solid rgba(0, 240, 255, 0.4) !important;
        color: #00f0ff !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
        text-transform: uppercase !important;
        letter-spacing: 2px !important;
        transition: all 0.3s ease !important;
        backdrop-filter: blur(5px);
        text-shadow: 0 0 10px rgba(0, 240, 255, 0.2);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.3), rgba(176, 38, 255, 0.3)) !important;
        border-color: #00f0ff !important;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.3) !important;
        transform: scale(1.02);
        color: #ffffff !important;
    }
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, rgba(0, 240, 255, 0.25), rgba(176, 38, 255, 0.25)) !important;
        border: 1px solid #00f0ff !important;
        box-shadow: 0 0 30px rgba(0, 240, 255, 0.2) !important;
        color: #ffffff !important;
    }
    [data-testid="metric-container"] {
        background: rgba(15, 15, 35, 0.8);
        border: 1px solid rgba(0, 240, 255, 0.15);
        border-radius: 10px;
        padding: 15px;
        backdrop-filter: blur(5px);
    }
    [data-testid="metric-container"] label {
        color: #00f0ff !important;
        font-family: 'Courier New', monospace !important;
        letter-spacing: 2px;
        font-size: 0.8rem !important;
    }
    [data-testid="metric-container"] div {
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
    }
    .dataframe {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.15) !important;
        border-radius: 10px !important;
        font-family: 'Courier New', monospace !important;
    }
    .dataframe th {
        color: #00f0ff !important;
        background: rgba(0, 240, 255, 0.1) !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
        font-size: 0.9rem !important;
    }
    .dataframe td {
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.85rem !important;
    }
    .streamlit-expanderHeader {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.15) !important;
        border-radius: 8px !important;
        color: #00f0ff !important;
        font-family: 'Courier New', monospace !important;
        font-weight: bold !important;
    }
    .streamlit-expanderContent {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.1) !important;
        border-top: none !important;
    }
    .streamlit-expanderContent p, .streamlit-expanderContent div,
    .streamlit-expanderContent li, .streamlit-expanderContent span {
        color: #ffffff !important;
    }
    .stSelectbox [data-baseweb="select"] {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        color: #00f0ff !important;
    }
    .stTextInput input, .stTextArea textarea {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
    }
    .stAlert {
        background: rgba(15, 15, 35, 0.9) !important;
        border: 1px solid rgba(0, 240, 255, 0.2) !important;
        border-radius: 8px !important;
    }
    .stAlert p, .stAlert div, .stAlert li, .stAlert span { color: #ffffff !important; }
    .stProgress > div > div {
        background: linear-gradient(90deg, #00f0ff, #b026ff, #ff2d95) !important;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: rgba(15, 15, 35, 0.8) !important;
        border: 1px solid rgba(0, 240, 255, 0.15) !important;
        border-radius: 8px !important;
    }
    .stTabs [data-baseweb="tab"] {
        color: #a0a0c0 !important;
        font-family: 'Courier New', monospace !important;
        letter-spacing: 2px;
        text-transform: uppercase;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #00f0ff !important;
        border-bottom: 2px solid #00f0ff !important;
        font-weight: bold !important;
    }
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: rgba(10, 10, 20, 0.5); }
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(180deg, #00f0ff, #b026ff);
        border-radius: 3px;
    }
    .folium-map {
        border: 1px solid rgba(0, 240, 255, 0.2);
        border-radius: 12px;
        box-shadow: 0 0 40px rgba(0, 240, 255, 0.05);
    }
    .cyber-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #00f0ff, #b026ff, #ff2d95, transparent);
        margin: 20px 0;
        opacity: 0.5;
    }
    .stMarkdown p, .stMarkdown li {
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        line-height: 1.6 !important;
    }
    .stMarkdown h1 { color: #00f0ff !important; }
    .stMarkdown h2 { color: #b026ff !important; }
    .stMarkdown h3 { color: #ff2d95 !important; }
    .stMarkdown h4 { color: #39ff14 !important; }
    .stCaption {
        color: #a0a0c0 !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.8rem !important;
    }
    .stRadio label {
        color: #ffffff !important;
        font-family: 'Courier New', monospace !important;
        font-size: 0.9rem !important;
    }
    .stRadio [role="radiogroup"] {
        gap: 8px;
    }
    /* Haze alert animations */
    @keyframes hazePulse {
        0%, 100% { box-shadow: 0 0 20px rgba(255, 100, 0, 0.3); }
        50% { box-shadow: 0 0 40px rgba(255, 100, 0, 0.6); }
    }
    .haze-alert {
        animation: hazePulse 2s ease-in-out infinite;
    }
    /* Fog alert animation (blue) */
    @keyframes fogPulse {
        0%, 100% { box-shadow: 0 0 20px rgba(0, 240, 255, 0.3); }
        50% { box-shadow: 0 0 40px rgba(0, 240, 255, 0.6); }
    }
    .fog-alert {
        animation: fogPulse 2s ease-in-out infinite;
    }
</style>
"""

# ============================================================================
# PROTECTED DARK-SKY ZONES IN BORNEO
# ============================================================================

PROTECTED_DARK_SKY_ZONES = {
    'Mount Kinabalu': (6.0750, 116.5583, 15, 'UNESCO World Heritage', 
                       'High-altitude granite peak, above most cloud layers'),
    'Kinabalu National Park': (6.0100, 116.5400, 20, 'UNESCO World Heritage',
                                'Protected 754 km² park, minimal artificial light'),
    'Maliau Basin': (4.7200, 117.5200, 25, 'Conservation Area',
                     'Remote pristine rainforest, "Sabah\'s Lost World"'),
    'Danum Valley': (4.9500, 117.7800, 25, 'Conservation Area',
                     '438 km² protected primary rainforest'),
    'Bario Highlands': (3.7300, 115.4700, 15, 'Kelabit Highlands',
                        'Remote highland plateau, minimal light pollution'),
    'Ba Kelalan': (3.9700, 115.6200, 12, 'Kelabit Highlands',
                   'Highland valley, pristine dark skies'),
    'Gunung Mulu': (4.0500, 114.9300, 20, 'UNESCO World Heritage',
                    'Karst formations, protected park'),
    'Crocker Range': (5.8000, 116.3000, 30, 'National Park',
                      '1,399 km² protected mountain range'),
    'Tawau Hills Park': (4.3500, 117.9000, 15, 'National Park',
                         'Volcanic landscape, protected forest'),
    'Pulau Sipadan': (4.1140, 118.6250, 5, 'Marine Protected Area',
                      'Isolated island, zero light pollution'),
    'Pulau Bohey Dulang': (4.5800, 118.7800, 8, 'Marine Park',
                           'Volcanic island, remote dark skies'),
    'Pulau Tiga': (5.7200, 115.6300, 8, 'National Park',
                   'Volcanic island, minimal development'),
    'Tabin Wildlife Reserve': (5.2000, 118.6500, 20, 'Wildlife Reserve',
                               '1,205 km² protected reserve'),
    'Long Pasia': (4.4000, 115.7500, 15, 'Conservation Area',
                   'Remote interior highland'),
    'Lambir Hills': (4.2200, 114.0300, 12, 'National Park',
                     'Protected sandstone hills'),
    'Niah National Park': (3.8100, 113.7700, 15, 'National Park',
                           'Archaeological site, protected forest'),
}

# Seasonal cloud guidance for Borneo (best viewing months)
SEASONAL_GUIDANCE = {
    'Sabah Highlands (Kinabalu, Kundasang, Crocker Range)': {
        'best_months': 'February - April',
        'good_months': 'January, May',
        'avoid_months': 'October - December (monsoon)',
        'notes': 'Dry season brings clear skies. Morning is clearest before afternoon clouds build up.'
    },
    'Sabah East Coast (Sandakan, Lahad Datu, Semporna)': {
        'best_months': 'March - May',
        'good_months': 'February, June',
        'avoid_months': 'November - January (NE monsoon)',
        'notes': 'Drier than west coast during Mar-May. Some clear nights year-round on islands.'
    },
    'Sarawak Highlands (Bario, Ba Kelalan, Mulu)': {
        'best_months': 'February - April, July - August',
        'good_months': 'January, May, June',
        'avoid_months': 'November - January (monsoon)',
        'notes': 'Interior highlands are surprisingly clear. Bring rain gear regardless.'
    },
    'Sarawak Coast (Kuching, Miri, Bintulu, Sibu)': {
        'best_months': 'March - September',
        'good_months': 'February, October',
        'avoid_months': 'December - February (NE monsoon)',
        'notes': 'Coastal areas have more cloud. Best to go inland for clear skies.'
    },
    'Interior Borneo (Kapit, Belaga, Maliau)': {
        'best_months': 'February - April, July - August',
        'good_months': 'January, May, June',
        'avoid_months': 'November - December',
        'notes': 'Rainforest interior. Best clarity during drier months.'
    },
}

# ============================================================================
# HAZE SEASONAL CALENDAR FOR MALAYSIA
# ============================================================================

HAZE_SEASONAL_CALENDAR = {
    1:  ('Low', 'NE Monsoon rains', '20-50', 'Northeast monsoon brings rain, washes out haze. Clearest month.'),
    2:  ('Low', 'NE Monsoon', '25-60', 'Continued rain. Very low haze risk. Best for stargazing.'),
    3:  ('Low-Moderate', 'Transitional', '40-80', 'Transition period. Some dry days. Haze may start appearing.'),
    4:  ('Moderate', 'Local burning', '50-100', 'Hot season starts. Local burning possible. Monitor AQI.'),
    5:  ('Moderate', 'Local burning', '60-120', 'Dry season begins. Local fires in Sarawak/Sabah possible.'),
    6:  ('High', 'Kalimantan/Sumatra fires', '80-200', 'SW monsoon begins. Smoke from Indonesian fires drifts north.'),
    7:  ('Very High', 'Kalimantan fires', '100-250', 'PEAK HAZE SEASON. Transboundary smoke from Kalimantan.'),
    8:  ('Very High', 'Kalimantan/Sumatra fires', '120-300', 'PEAK HAZE SEASON. Worst air quality. Avoid stargazing.'),
    9:  ('Very High', 'Kalimantan fires', '100-250', 'Continued heavy haze. Wait for rain.'),
    10: ('High', 'Kalimantan fires fading', '80-200', 'Haze begins to decrease as monsoon returns.'),
    11: ('Moderate', 'Transitional', '50-120', 'NE monsoon returns. Rain washes haze away.'),
    12: ('Low', 'NE Monsoon', '30-70', 'Full monsoon. Clear skies, no haze. Great for stargazing.'),
}

# ============================================================================
# NEW FEATURE 1: MOON PHASE CALCULATION
# ============================================================================

def calculate_moon_phase(date: datetime = None) -> Dict:
    """Calculate moon phase using a simplified astronomical algorithm."""
    if date is None:
        date = datetime.now()
    
    known_new_moon = datetime(2000, 1, 6, 18, 14, 0)
    synodic_month = 29.530588853
    
    days_since = (date - known_new_moon).total_seconds() / 86400.0
    phase_fraction = (days_since % synodic_month) / synodic_month
    age_days = phase_fraction * synodic_month
    
    illumination = (1 - math.cos(2 * math.pi * phase_fraction)) / 2
    illumination_pct = illumination * 100
    
    if phase_fraction < 0.03 or phase_fraction > 0.97:
        phase_name, emoji = "New Moon", "🌑"
    elif phase_fraction < 0.22:
        phase_name, emoji = "Waxing Crescent", "🌒"
    elif phase_fraction < 0.28:
        phase_name, emoji = "First Quarter", "🌓"
    elif phase_fraction < 0.47:
        phase_name, emoji = "Waxing Gibbous", "🌔"
    elif phase_fraction < 0.53:
        phase_name, emoji = "Full Moon", "🌕"
    elif phase_fraction < 0.72:
        phase_name, emoji = "Waning Gibbous", "🌖"
    elif phase_fraction < 0.78:
        phase_name, emoji = "Last Quarter", "🌗"
    else:
        phase_name, emoji = "Waning Crescent", "🌘"
    
    viewing_score = 5.0 - (illumination * 4.5)
    
    if illumination < 0.15:
        impact, impact_emoji = "Excellent - Dark skies for deep-sky objects", "🌟"
    elif illumination < 0.35:
        impact, impact_emoji = "Good - Faint deep-sky objects still visible", "✨"
    elif illumination < 0.60:
        impact, impact_emoji = "Moderate - Brighter objects visible, faint ones washed out", "⭐"
    elif illumination < 0.85:
        impact, impact_emoji = "Poor - Only brightest objects visible", "⚠️"
    else:
        impact, impact_emoji = "Very Poor - Moon washes out most stars", "❌"
    
    return {
        'phase_name': phase_name,
        'emoji': emoji,
        'illumination_pct': round(illumination_pct, 1),
        'age_days': round(age_days, 1),
        'viewing_score': round(viewing_score, 2),
        'impact': impact,
        'impact_emoji': impact_emoji,
        'date': date.strftime('%Y-%m-%d %H:%M'),
    }


# ============================================================================
# NEW FEATURE 2: MILKY WAY VISIBILITY CALENDAR
# ============================================================================

def get_milky_way_visibility(lat: float, lon: float, date: datetime = None) -> Dict:
    """Determine if the Milky Way galactic core is visible."""
    if date is None:
        date = datetime.now()
    
    month = date.month
    
    if month in [3, 4, 5]:
        visibility = "Excellent"
        best_time = "2:00 AM - 5:00 AM"
        score = 5.0
        note = "Galactic core rises around 2 AM. Best months for viewing the core!"
    elif month in [6, 7, 8]:
        visibility = "Peak"
        best_time = "10:00 PM - 4:00 AM"
        score = 5.0
        note = "PEAK SEASON! Galactic core visible all night. Best viewing of the year."
    elif month in [9, 10]:
        visibility = "Good"
        best_time = "8:00 PM - 12:00 AM"
        score = 4.0
        note = "Core visible in early evening. Still great viewing."
    elif month in [2, 11]:
        visibility = "Limited"
        best_time = "3:00 AM - 5:00 AM"
        score = 2.5
        note = "Core barely above horizon. Outer arms only."
    else:
        visibility = "Poor"
        best_time = "Not visible"
        score = 1.0
        note = "Galactic core below horizon. Only outer Milky Way arms visible."
    
    abs_lat = abs(lat)
    if abs_lat < 3:
        lat_bonus = "Perfect - Directly overhead at zenith"
    elif abs_lat < 5:
        lat_bonus = "Excellent - High in the sky"
    elif abs_lat < 7:
        lat_bonus = "Good - Well positioned"
    else:
        lat_bonus = "Moderate - Lower in sky"
    
    if month in [1, 2, 11, 12]:
        next_window = "March - October (best: June - August)"
    else:
        next_window = "Currently in season!"
    
    return {
        'visibility': visibility,
        'best_time': best_time,
        'score': score,
        'note': note,
        'latitude_note': lat_bonus,
        'next_window': next_window,
        'month': month,
    }


# ============================================================================
# NEW FEATURE 3: ASTROPHOTOGRAPHY SCORE
# ============================================================================

def calculate_astrophotography_scores(result_data: Dict, moon_phase: Dict) -> Dict:
    """Calculate separate scores for naked-eye, telescope, and astrophotography."""
    base_score = result_data.get('suitability_percentage', 0)
    elevation_m = result_data.get('elevation_m', 0)
    lp_index = result_data.get('light_pollution_index', 0)
    humidity = result_data.get('humidity_pct')
    visibility_km = result_data.get('visibility_km')
    protected = result_data.get('protected_zone')
    moon_illum = moon_phase.get('illumination_pct', 50)
    haze_data = result_data.get('haze', {})
    haze_severity = haze_data.get('severity', 'None')
    haze_detected = haze_data.get('detected', False)
    
    # NEW v3.2.2: Only apply haze penalty if it's smoke (not fog)
    is_smoke_haze = haze_detected and haze_severity not in ['Fog', 'None']
    
    # NAKED-EYE
    naked_eye = base_score
    naked_eye -= (moon_illum / 100.0) * 25
    if lp_index >= 5:
        naked_eye -= 10
    if protected:
        naked_eye += 5
    if is_smoke_haze:
        if haze_severity == 'Heavy':
            naked_eye -= 20
        elif haze_severity == 'Moderate':
            naked_eye -= 10
        elif haze_severity == 'Light':
            naked_eye -= 5
    naked_eye = max(0, min(100, naked_eye))
    
    # TELESCOPE
    telescope = base_score
    telescope -= (moon_illum / 100.0) * 12
    if elevation_m > 1000:
        telescope += 8
    elif elevation_m > 500:
        telescope += 4
    if humidity and humidity > 85:
        telescope -= 8
    elif humidity and humidity > 70:
        telescope -= 3
    if is_smoke_haze:
        if haze_severity == 'Heavy':
            telescope -= 18
        elif haze_severity == 'Moderate':
            telescope -= 9
        elif haze_severity == 'Light':
            telescope -= 4
    telescope = max(0, min(100, telescope))
    
    # ASTROPHOTOGRAPHY
    astro = base_score
    astro -= (moon_illum / 100.0) * 30
    if lp_index >= 8:
        astro -= 25
    elif lp_index >= 5:
        astro -= 12
    elif lp_index <= 1:
        astro += 8
    if visibility_km and visibility_km < 10:
        astro -= 10
    elif visibility_km and visibility_km > 25:
        astro += 5
    if humidity and humidity > 90:
        astro -= 12
    elif humidity and humidity > 80:
        astro -= 5
    if protected:
        astro += 10
    if elevation_m > 1000:
        astro += 8
    if is_smoke_haze:
        if haze_severity == 'Heavy':
            astro -= 30
        elif haze_severity == 'Moderate':
            astro -= 15
        elif haze_severity == 'Light':
            astro -= 6
    astro = max(0, min(100, astro))
    
    def rate(score):
        if score >= 80:
            return "Excellent", "🌟"
        elif score >= 65:
            return "Good", "✨"
        elif score >= 50:
            return "Moderate", "⭐"
        elif score >= 35:
            return "Limited", "⚠️"
        else:
            return "Poor", "❌"
    
    naked_rating, naked_emoji = rate(naked_eye)
    telescope_rating, telescope_emoji = rate(telescope)
    astro_rating, astro_emoji = rate(astro)
    
    return {
        'naked_eye': {
            'score': round(naked_eye, 1),
            'rating': naked_rating,
            'emoji': naked_emoji,
            'note': 'Best for casual viewing, Milky Way, constellations'
        },
        'telescope': {
            'score': round(telescope, 1),
            'rating': telescope_rating,
            'emoji': telescope_emoji,
            'note': 'Best for planets, clusters, nebulae'
        },
        'astrophotography': {
            'score': round(astro, 1),
            'rating': astro_rating,
            'emoji': astro_emoji,
            'note': 'Best for long-exposure deep-sky imaging'
        },
    }


# ============================================================================
# HAZE DETECTION ENGINE (v3.2.2 — WITH FOG DETECTION)
# ============================================================================

def detect_haze(weather_data: Optional[Dict], air_quality: Optional[Dict], 
                location: Dict, date: datetime = None) -> Dict:
    """
    Detect transboundary smoke haze OR natural high-altitude fog.
    
    NEW in v3.2.2: Distinguishes between:
    - Natural mountain fog (cold + high elevation + clean air)
    - Smoke haze (warm + low elevation + dirty air)
    """
    if date is None:
        date = datetime.now()
    
    month = date.month
    seasonal = HAZE_SEASONAL_CALENDAR.get(month, HAZE_SEASONAL_CALENDAR[6])
    seasonal_risk, seasonal_source, seasonal_aqi, seasonal_note = seasonal
    
    result = {
        'detected': False,
        'severity': 'None',
        'confidence': 'Low',
        'indicators': [],
        'cause': 'Unknown',
        'aqi': None,
        'aqi_category': None,
        'pm25': None,
        'pm10': None,
        'seasonal_risk': seasonal_risk,
        'seasonal_source': seasonal_source,
        'seasonal_note': seasonal_note,
        'seasonal_aqi_range': seasonal_aqi,
        'month': month,
        'health_advisory': None,
        'action_recommendation': None,
        'pm25_level': None,
        'is_fog': False,  # NEW v3.2.2
    }
    
    pm25 = None
    pm10 = None
    aqi = None
    
    if air_quality:
        pm25 = air_quality.get('pm2_5')
        pm10 = air_quality.get('pm10')
        aqi = air_quality.get('us_aqi') or air_quality.get('european_aqi')
        
        result['pm25'] = pm25
        result['pm10'] = pm10
        result['aqi'] = aqi
        
        if pm25 is not None:
            if pm25 < 12:
                result['pm25_level'] = 'Good'
                result['indicators'].append(f"PM2.5: {pm25:.1f} µg/m³ (Good)")
            elif pm25 < 35:
                result['pm25_level'] = 'Moderate'
                result['indicators'].append(f"PM2.5: {pm25:.1f} µg/m³ (Moderate)")
            elif pm25 < 55:
                result['pm25_level'] = 'Unhealthy for Sensitive'
                result['indicators'].append(f"PM2.5: {pm25:.1f} µg/m³ (Unhealthy for sensitive groups)")
            elif pm25 < 150:
                result['pm25_level'] = 'Unhealthy'
                result['indicators'].append(f"PM2.5: {pm25:.1f} µg/m³ (UNHEALTHY)")
            elif pm25 < 250:
                result['pm25_level'] = 'Very Unhealthy'
                result['indicators'].append(f"PM2.5: {pm25:.1f} µg/m³ (VERY UNHEALTHY)")
            else:
                result['pm25_level'] = 'Hazardous'
                result['indicators'].append(f"PM2.5: {pm25:.1f} µg/m³ (HAZARDOUS)")
        
        if aqi is not None:
            if aqi <= 50:
                result['aqi_category'] = 'Good'
            elif aqi <= 100:
                result['aqi_category'] = 'Moderate'
            elif aqi <= 150:
                result['aqi_category'] = 'Unhealthy for Sensitive'
            elif aqi <= 200:
                result['aqi_category'] = 'Unhealthy'
            elif aqi <= 300:
                result['aqi_category'] = 'Very Unhealthy'
            else:
                result['aqi_category'] = 'Hazardous'
    
    visibility = None
    if weather_data:
        visibility = weather_data.get('visibility_km')
        if visibility is not None:
            if visibility < 2:
                result['indicators'].append(f"Visibility: {visibility:.1f} km (VERY LOW - heavy haze/fog)")
            elif visibility < 5:
                result['indicators'].append(f"Visibility: {visibility:.1f} km (LOW - likely haze)")
            elif visibility < 10:
                result['indicators'].append(f"Visibility: {visibility:.1f} km (reduced)")
            else:
                result['indicators'].append(f"Visibility: {visibility:.1f} km (normal)")
    
    humidity = None
    if weather_data:
        humidity = weather_data.get('humidity_pct')
        if humidity is not None and humidity > 85:
            result['indicators'].append(f"Humidity: {humidity:.0f}% (high - supports haze/fog formation)")
    
    # NEW v3.2.2: Get temperature for fog detection
    temperature = None
    if weather_data:
        temperature = weather_data.get('temperature_c')
    
    cloud_cover = None
    if weather_data:
        cloud_cover = weather_data.get('cloud_cover_pct')
        if cloud_cover is not None and cloud_cover > 80:
            result['indicators'].append(f"Cloud/smoke cover: {cloud_cover:.0f}%")
    
    if seasonal_risk in ['High', 'Very High']:
        result['indicators'].append(f"Season: {seasonal_risk} haze risk ({seasonal_source})")
    
    # ============================================================
    # NEW v3.2.2: CHECK FOR HIGH-ALTITUDE FOG FIRST
    # ============================================================
    elevation_m = location.get('elevation_m', 0)
    
    # Fog detection criteria:
    # 1. High elevation (>1000m)
    # 2. Cold temperature (<10°C)
    # 3. Low visibility (<5km)
    # 4. Clean air (PM2.5 < 35 µg/m³)
    is_high_altitude = elevation_m > 1000
    is_cold = temperature is not None and temperature < 10
    is_low_visibility = visibility is not None and visibility < 5
    is_clean_air = pm25 is None or pm25 < 35
    
    if is_high_altitude and is_cold and is_low_visibility and is_clean_air:
        # This is natural mountain fog, NOT smoke haze!
        result['detected'] = True
        result['severity'] = 'Fog'
        result['confidence'] = 'High'
        result['is_fog'] = True
        result['cause'] = f'Natural high-altitude fog (mountain cloud at {elevation_m:.0f}m, {temperature:.1f}°C)'
        result['indicators'].append(f"🌫️ Natural mountain fog detected (not smoke)")
        result['health_advisory'] = (
            "✅ Air quality is CLEAN. This is natural mountain fog — not smoke. "
            "Safe for outdoor activity (but cold — bring warm clothes!)."
        )
        result['action_recommendation'] = (
            f"☁️ Summit is inside a natural cloud (visibility {visibility:.1f} km). "
            f"Move to lower elevation (Laban Rata at 3,272m) for clearer views. "
            f"Check back tomorrow — summit fog often clears by morning."
        )
        return result
    
    # ============================================================
    # STANDARD HAZE DETECTION (not fog)
    # ============================================================
    severity_score = 0
    
    if pm25 is not None:
        if pm25 >= 150:
            severity_score += 5
        elif pm25 >= 55:
            severity_score += 3
        elif pm25 >= 35:
            severity_score += 2
        elif pm25 >= 12:
            severity_score += 1
    
    if aqi is not None:
        if aqi >= 200:
            severity_score += 5
        elif aqi >= 150:
            severity_score += 3
        elif aqi >= 100:
            severity_score += 2
        elif aqi >= 50:
            severity_score += 1
    
    if visibility is not None:
        if visibility < 2:
            severity_score += 4
        elif visibility < 5:
            severity_score += 3
        elif visibility < 10:
            severity_score += 1
    
    if humidity is not None and humidity > 90 and visibility is not None and visibility < 10:
        severity_score += 2
    
    if seasonal_risk in ['High', 'Very High']:
        severity_score += 1
    
    if severity_score >= 10:
        result['severity'] = 'Severe'
        result['confidence'] = 'Very High'
        result['detected'] = True
    elif severity_score >= 7:
        result['severity'] = 'Heavy'
        result['confidence'] = 'High'
        result['detected'] = True
    elif severity_score >= 4:
        result['severity'] = 'Moderate'
        result['confidence'] = 'Medium'
        result['detected'] = True
    elif severity_score >= 2:
        result['severity'] = 'Light'
        result['confidence'] = 'Medium'
        result['detected'] = True
    else:
        result['severity'] = 'None'
        result['confidence'] = 'Low'
        result['detected'] = False
    
    if month in [6, 7, 8, 9, 10] and result['detected']:
        result['cause'] = 'Transboundary smoke haze (Kalimantan/Sumatra fires - SW monsoon season)'
    elif result['detected']:
        result['cause'] = 'Local burning or regional smoke'
    else:
        result['cause'] = 'No significant haze detected'
    
    if result['severity'] in ['Heavy', 'Severe']:
        result['health_advisory'] = (
            "⚠️ HEALTH ADVISORY: Air quality is unhealthy. "
            "Wear N95 mask if going outdoors. Sensitive groups (children, elderly, "
            "respiratory issues) should stay indoors. Avoid outdoor exercise."
        )
    elif result['severity'] == 'Moderate':
        result['health_advisory'] = (
            "💛 Health Note: Air quality is degraded. "
            "Sensitive groups should limit outdoor activity. "
            "Consider wearing a mask outdoors."
        )
    elif result['severity'] == 'Light':
        result['health_advisory'] = (
            "💚 Minor: Slight haze. Sensitive individuals may notice reduced air quality. "
            "Fine for most outdoor activities."
        )
    else:
        result['health_advisory'] = "✅ Air quality is good. Safe for all outdoor activities."
    
    if result['severity'] in ['Heavy', 'Severe']:
        result['action_recommendation'] = (
            "🚫 NOT RECOMMENDED for stargazing tonight. Wait for rain to wash out haze, "
            "or choose a coastal site with sea breeze (better dispersion). "
            "Check back in 2-3 days after rainfall."
        )
    elif result['severity'] == 'Moderate':
        result['action_recommendation'] = (
            "⚠️ Marginal conditions. Haze will reduce visibility of faint objects. "
            "Only brightest stars/planets visible. Consider postponing for clearer night."
        )
    elif result['severity'] == 'Light':
        result['action_recommendation'] = (
            "✅ Acceptable conditions. Slight haze reduces contrast but viewing is possible. "
            "Best for bright objects (Moon, planets, bright stars)."
        )
    else:
        result['action_recommendation'] = (
            "🌟 Excellent air quality. Perfect for all types of stargazing."
        )
    
    return result


def get_air_quality(location: Dict) -> Optional[Dict]:
    """Fetch live air quality data from Open-Meteo Air Quality API."""
    try:
        url = "https://air-quality-api.open-meteo.com/v1/air-quality"
        params = {
            "latitude": location['lat'],
            "longitude": location['lon'],
            "current": "pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,"
                       "sulphur_dioxide,ozone,aerosol_optical_depth,"
                       "dust,uv_index,us_aqi,european_aqi",
            "timezone": "auto",
        }
        r = requests.get(url, params=params, timeout=5)
        data = r.json()
        cur = data.get("current", {})
        return {
            'pm2_5': cur.get('pm2_5'),
            'pm10': cur.get('pm10'),
            'carbon_monoxide': cur.get('carbon_monoxide'),
            'nitrogen_dioxide': cur.get('nitrogen_dioxide'),
            'sulphur_dioxide': cur.get('sulphur_dioxide'),
            'ozone': cur.get('ozone'),
            'aerosol_optical_depth': cur.get('aerosol_optical_depth'),
            'dust': cur.get('dust'),
            'uv_index': cur.get('uv_index'),
            'us_aqi': cur.get('us_aqi'),
            'european_aqi': cur.get('european_aqi'),
            'source': 'Open-Meteo Air Quality (Live)',
            'time': cur.get('time'),
        }
    except Exception:
        return None


# ============================================================================
# RECOMMENDATION ENGINE
# ============================================================================

def get_seasonal_guidance(lat: float, lon: float, elevation_m: float) -> Dict:
    """Determine best seasonal viewing window for a location."""
    if lat > 5.5 and lon > 115.5 and lon < 117.0:
        region = 'Sabah Highlands (Kinabalu, Kundasang, Crocker Range)'
    elif lat < 5.0 and lon > 117.0:
        region = 'Sabah East Coast (Sandakan, Lahad Datu, Semporna)'
    elif lat > 3.5 and lon > 114.5 and lon < 116.0:
        region = 'Sarawak Highlands (Bario, Ba Kelalan, Mulu)'
    elif lat > 3.5 and lon < 115.0:
        region = 'Sarawak Coast (Kuching, Miri, Bintulu, Sibu)'
    else:
        region = 'Interior Borneo (Kapit, Belaga, Maliau)'
    
    guidance = SEASONAL_GUIDANCE.get(region, SEASONAL_GUIDANCE['Interior Borneo (Kapit, Belaga, Maliau)'])
    return {'region': region, **guidance}


def generate_recommendation_strategy(result_data: Dict) -> Dict:
    """Generate recommendation strategy for stargazing site."""
    score = result_data.get('suitability_percentage', 0)
    details = result_data.get('details', {})
    elevation_m = result_data.get('elevation_m', 0)
    cloud_risk = result_data.get('cloud_risk', 'Unknown')
    light_pollution = result_data.get('light_pollution_index', 0)
    cloud_cover = result_data.get('cloud_cover_pct', None)
    humidity = result_data.get('humidity_pct', None)
    protected_zone = result_data.get('protected_zone', None)
    lat_deg = result_data.get('lat_deg', 0)
    haze = result_data.get('haze', {})

    recommendations = {
        'immediate_actions': [],
        'short_term_actions': [],
        'long_term_actions': [],
        'investment_required': 'Low',
        'overall_feasibility': 'High',
        'risk_level': 'Low',
    }

    def add_action(bucket, text, priority, cost):
        recommendations[bucket].append({
            'text': text, 'priority': priority, 'cost': cost
        })

    # v3.2.2: Handle fog differently from smoke haze
    haze_severity = haze.get('severity', 'None')
    is_fog = haze.get('is_fog', False)
    
    if is_fog:
        # Natural fog — not a health hazard, just a viewing issue
        add_action('short_term_actions',
            f'🌫️ Natural mountain fog at summit ({haze.get("cause", "High-altitude cloud")}). '
            f'Not smoke — air is clean. Go to lower elevation for clearer views.',
            'Medium', '💸')
    elif haze_severity in ['Heavy', 'Severe']:
        add_action('immediate_actions',
            f'🌫️ HAZE ALERT ({haze_severity}): {haze.get("cause", "Smoke haze detected")}. Stargazing severely impacted.',
            'Critical', '💸')
    elif haze_severity == 'Moderate':
        add_action('short_term_actions',
            f'🌫️ Moderate haze detected. Visibility reduced. Check Air Quality Index before heading out.',
            'High', '💸')
    elif haze_severity == 'Light':
        add_action('short_term_actions',
            f'💨 Light haze. Minor impact on viewing. Best for bright objects.',
            'Medium', '💸')

    if protected_zone:
        add_action('immediate_actions',
            f'🏞️ PROTECTED DARK-SKY ZONE: Inside "{protected_zone["name"]}" ({protected_zone["designation"]}). {protected_zone["description"]}.',
            'Low', '💸')

    if elevation_m < 20:
        add_action('short_term_actions',
            '⛰️ Low elevation (<20m). More atmosphere to look through. Consider portable telescope platforms.',
            'Medium', '💸💸')
    elif elevation_m < 100:
        add_action('short_term_actions',
            '🌄 Moderate elevation. Good for general stargazing. Standard observation deck recommended.',
            'Low', '💸')
    elif elevation_m < 500:
        add_action('immediate_actions',
            '✅ EXCELLENT ELEVATION (100-500m). Less atmospheric distortion. Ideal for telescope installation.',
            'Low', '💸')
    elif elevation_m < 1000:
        add_action('immediate_actions',
            '🌟 OUTSTANDING ELEVATION (500-1000m). Thin atmosphere, superb seeing conditions. Prime location!',
            'Low', '💸💸')
    else:
        add_action('immediate_actions',
            f'🏔️ EXCEPTIONAL HIGH-ALTITUDE SITE ({elevation_m:.0f}m). World-class observatory potential. Very thin atmosphere — likely ABOVE the light dome.',
            'Low', '💸💸💸')
        recommendations['investment_required'] = 'Moderate'

    if light_pollution >= 8 and not protected_zone:
        add_action('immediate_actions',
            '🚨 CRITICAL: HIGH LIGHT POLLUTION. Need light shields or relocate to darker site.',
            'Critical', '💸💸💸💸')
        recommendations['investment_required'] = 'Very High'
    elif light_pollution >= 5 and not protected_zone:
        add_action('short_term_actions',
            '💡 MODERATE LIGHT POLLUTION. Install light barriers and coordinate with local authorities for dark-sky lighting.',
            'High', '💸💸💸')
        if recommendations['investment_required'] != 'Very High':
            recommendations['investment_required'] = 'Moderate'
    else:
        add_action('immediate_actions',
            '✅ DARK-SKY CONDITIONS. Excellent for galaxy viewing and deep-sky photography.',
            'Low', '💸')

    if cloud_risk == 'High' and not protected_zone:
        add_action('short_term_actions',
            '☁️ HIGH SEASONAL CLOUD RISK. Plan for flexible viewing schedules and indoor planetarium backup.',
            'High', '💸💸💸')
        if recommendations['investment_required'] != 'Very High':
            recommendations['investment_required'] = 'Moderate'
    elif cloud_risk == 'Low':
        add_action('immediate_actions',
            '✅ LOW CLOUD RISK. Excellent year-round viewing potential.',
            'Low', '💸')

    if lat_deg < 3:
        add_action('immediate_actions',
            f'🌌 EXCELLENT LATITUDE ({lat_deg:.1f}°N). Near equator — can view BOTH Northern AND Southern sky objects!',
            'Low', '💸')
    elif lat_deg < 5:
        add_action('immediate_actions',
            f'🌌 GOOD LATITUDE ({lat_deg:.1f}°N). Excellent access to Milky Way core and Magellanic Clouds.',
            'Low', '💸')
    else:
        add_action('short_term_actions',
            f'🌌 MODERATE LATITUDE ({lat_deg:.1f}°N). Still good viewing. Milky Way visible seasonally.',
            'Low', '💸')

    if cloud_cover is not None:
        if cloud_cover > 70:
            add_action('short_term_actions',
                f'☁️ HIGH CURRENT CLOUD COVER ({cloud_cover:.0f}%). Not the best night right now. Check seasonal guidance below.',
                'Medium', '💸')
        elif cloud_cover < 20:
            add_action('immediate_actions',
                f'✅ EXCELLENT CLEAR SKIES NOW ({cloud_cover:.0f}% cloud cover). Ideal viewing conditions tonight!',
                'Low', '💸')

    if humidity is not None and humidity > 85:
        add_action('short_term_actions',
            f'💧 HIGH HUMIDITY ({humidity:.0f}%). Install dew heaters for telescopes. Consider dehumidified storage.',
            'Medium', '💸💸')

    infra_details = details.get('infrastructure_access', {}).get('value', {})
    if isinstance(infra_details, dict):
        if infra_details.get('airports', 0) == 0:
            add_action('long_term_actions',
                '✈️ No airport nearby. Consider helipad for equipment delivery and visitor access.',
                'Medium', '💸💸💸')
        if infra_details.get('major_roads', 0) == 0:
            add_action('short_term_actions',
                '🛣️ Limited road access. Improve access roads for telescope equipment and visitors.',
                'High', '💸💸💸')
        if infra_details.get('accommodation', 0) == 0 and not protected_zone:
            add_action('long_term_actions',
                '🏨 No accommodation nearby. Build eco-lodge or observatory guest facilities.',
                'Medium', '💸💸💸💸')

    critical_count = sum(
        1 for a in recommendations['immediate_actions']
        if a['priority'] == 'Critical'
    )
    high_count = sum(
        1 for a in recommendations['short_term_actions']
        if a['priority'] == 'High'
    )

    if score >= 80:
        score_band, score_emoji = 'Excellent', '🌟'
    elif score >= 65:
        score_band, score_emoji = 'Good', '✨'
    elif score >= 50:
        score_band, score_emoji = 'Moderate', '⭐'
    elif score >= 35:
        score_band, score_emoji = 'Limited', '⚠️'
    else:
        score_band, score_emoji = 'Poor', '❌'

    if critical_count >= 3:
        feasibility = '❌ Poor - Major critical issues must be resolved before development'
        risk_level = 'Very High'
    elif critical_count == 2:
        feasibility = '⚠️ Limited - Multiple critical issues require resolution'
        risk_level = 'High'
    elif critical_count == 1:
        feasibility = '⭐ Moderate - One critical issue requires resolution'
        risk_level = 'High'
    elif high_count >= 2:
        feasibility = '⭐ Moderate - Several high-priority preparations required'
        risk_level = 'Medium'
    else:
        feasibility = f'{score_emoji} {score_band} - ' + {
            'Excellent': 'World-class stargazing destination potential',
            'Good': 'Excellent viewing site with minor improvements',
            'Moderate': 'Good viewing site requiring some investment',
            'Limited': 'Challenging conditions, major investment needed',
            'Poor': 'Not recommended for astronomy development',
        }[score_band]
        risk_level = {
            'Excellent': 'Low', 'Good': 'Low',
            'Moderate': 'Medium', 'Limited': 'High', 'Poor': 'Very High',
        }[score_band]

    recommendations['overall_feasibility'] = feasibility
    recommendations['risk_level'] = risk_level
    recommendations['critical_action_count'] = critical_count
    recommendations['high_action_count'] = high_count
    recommendations['total_action_count'] = len(
        recommendations['immediate_actions']
        + recommendations['short_term_actions']
        + recommendations['long_term_actions']
    )

    recommendations['timeline_summary'] = {
        'immediate': f"{len(recommendations['immediate_actions'])} actions (0-6 months)",
        'short_term': f"{len(recommendations['short_term_actions'])} actions (6-18 months)",
        'long_term': f"{len(recommendations['long_term_actions'])} actions (18-36 months)"
    }
    return recommendations


# ============================================================================
# CACHE MANAGEMENT
# ============================================================================

class APICache:
    def __init__(self, cache_dir: str = "astro_cache", ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)

    def _get_cache_key(self, url: str, params: Dict) -> str:
        key_str = url + json.dumps(params, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()

    def get(self, url: str, params: Dict) -> Optional[Dict]:
        cache_key = self._get_cache_key(url, params)
        cache_file = self.cache_dir / f"{cache_key}.json"
        if cache_file.exists():
            modified_time = datetime.fromtimestamp(cache_file.stat().st_mtime)
            if datetime.now() - modified_time < self.ttl:
                try:
                    with open(cache_file, 'r') as f:
                        return json.load(f)
                except Exception:
                    return None
        return None

    def set(self, url: str, params: Dict, data: Dict) -> None:
        cache_key = self._get_cache_key(url, params)
        cache_file = self.cache_dir / f"{cache_key}.json"
        try:
            with open(cache_file, 'w') as f:
                json.dump(data, f)
        except Exception:
            pass

    def clear(self):
        for f in self.cache_dir.glob("*.json"):
            f.unlink()

    def get_stats(self) -> Dict:
        files = list(self.cache_dir.glob("*.json"))
        return {'total_cached': len(files), 'cache_dir': str(self.cache_dir)}

api_cache = APICache()

# ============================================================================
# SABAH LOCATIONS
# ============================================================================

SABAH_LOCATIONS = {
    'Kota Kinabalu City Center': (5.9804, 116.0735),
    'Tanjung Aru Beach': (5.9400, 116.0500),
    'Likas Bay': (5.9500, 116.0200),
    'Signal Hill': (5.9750, 116.0700),
    'Sabah Museum': (5.9600, 116.0650),
    '1Borneo Mall': (6.0200, 116.1100),
    'Sutera Harbour': (5.9600, 116.0600),
    'Universiti Malaysia Sabah': (6.0300, 116.1200),
    'Penampang': (5.9000, 116.0800),
    'Putatan': (5.8800, 116.0600),
    'Tuaran': (6.1800, 116.2400),
    'Papar': (5.7300, 115.9300),
    'Kinarut': (5.8200, 116.0500),
    'Lok Kawi': (5.8500, 116.0300),
    'Menggatal': (6.0200, 116.1400),
    'Sepanggar': (6.0400, 116.0900),
    'Inanam': (6.0000, 116.1200),
    'Telipok': (6.0800, 116.1900),
    'Likas': (5.9600, 116.0300),
    'Luyang': (5.9300, 116.0700),
    'Donggongon': (5.9000, 116.0900),
    'Keningau': (5.3300, 116.1600),
    'Tenom': (5.1300, 115.9500),
    'Beaufort': (5.3500, 115.7500),
    'Sipitang': (5.0800, 115.5500),
    'Nabawan': (5.0800, 116.4300),
    'Tambunan': (5.6700, 116.3600),
    'Kuala Penyu': (5.5700, 115.5800),
    'Membakut': (5.4700, 115.7800),
    'Weston': (5.2700, 115.4800),
    'Kemabong': (5.0800, 116.0800),
    'Sook': (5.1300, 116.2200),
    'Melalap': (5.0800, 115.9000),
    'Bongawan': (5.5300, 115.8300),
    'Klias': (5.4300, 115.6800),
    'Limbawang': (5.1700, 115.5800),
    'Kudat': (6.8860, 116.8430),
    'Kota Marudu': (6.5000, 116.7400),
    'Pitas': (6.7200, 117.0700),
    'Banggi Island': (7.2300, 117.1700),
    'Malawali Island': (7.1500, 117.1300),
    'Tanjung Simpang Mengayau': (7.0900, 116.9100),
    'Bakapit': (6.8000, 116.8000),
    'Matunggong': (6.7700, 116.7900),
    'Sandakan City Center': (5.8400, 118.1200),
    'Sandakan Airport': (5.9010, 118.0580),
    'Sepilok Orangutan Centre': (5.8650, 117.9420),
    'Gomantong Caves': (5.5300, 118.0700),
    'Sukau': (5.5000, 118.2500),
    'Kinabatangan River': (5.4000, 117.8000),
    'Telupid': (5.6300, 117.1300),
    'Beluran': (5.8800, 117.5600),
    'Pamol': (5.4800, 118.0800),
    'Batu Putih': (5.3800, 117.9200),
    'Muanad': (5.4800, 118.1800),
    'Bilit': (5.4200, 117.8200),
    'Abai': (5.3500, 117.6800),
    'Tawau City Center': (4.2435, 117.8853),
    'Tawau Airport': (4.3133, 117.9183),
    'Tawau Hills Park': (4.3500, 117.9000),
    'Lahad Datu': (5.0300, 118.3300),
    'Felda Sahabat': (5.0620, 119.0810),
    'Dent Haven': (5.2680, 119.2620),
    'Semporna': (4.4800, 118.6100),
    'Kunak': (4.6800, 118.2500),
    'Silam': (4.8700, 118.2300),
    'Kalabakan': (4.2200, 117.4800),
    'Maliau Basin': (4.7200, 117.5200),
    'Danum Valley': (4.9500, 117.7800),
    'Tabin Wildlife Reserve': (5.2000, 118.6500),
    'Tungku': (4.7000, 118.2000),
    'Merotai': (4.3000, 117.8500),
    'Apas': (4.2800, 117.8800),
    'Balung': (4.1800, 117.6800),
    'Umas Umas': (4.1500, 117.5800),
    'Bombalai': (4.1200, 117.4800),
    'Tanjung Batu': (4.0500, 117.3800),
    'Mount Kinabalu': (6.0750, 116.5583),
    'Kinabalu National Park': (6.0100, 116.5400),
    'Kundasang': (5.9800, 116.5700),
    'Ranau': (5.9500, 116.6700),
    'Mesilau': (6.0400, 116.5900),
    'Poring Hot Springs': (6.0500, 116.7000),
    'Crocker Range': (5.8000, 116.3000),
    'Trus Madi': (5.5000, 116.4000),
    'Long Pasia': (4.4000, 115.7500),
    'Eastern Sabah Hills': (5.0000, 117.8500),
    'Pulau Gaya': (5.9800, 116.0200),
    'Pulau Manukan': (5.9700, 116.0000),
    'Pulau Mamutik': (5.9600, 115.9900),
    'Pulau Sapi': (5.9500, 115.9900),
    'Pulau Sulug': (5.9400, 115.9800),
    'Pulau Sipadan': (4.1140, 118.6250),
    'Pulau Mabul': (4.2400, 118.6200),
    'Pulau Kapalai': (4.2100, 118.6600),
    'Pulau Ligitan': (4.1500, 118.8800),
    'Pulau Bohey Dulang': (4.5800, 118.7800),
    'Pulau Bum Bum': (4.5000, 118.7100),
    'Pulau Sebatik': (4.1300, 117.7800),
    'Pulau Tiga': (5.7200, 115.6300),
    'Pulau Dinawan': (5.7000, 115.5800),
}

# ============================================================================
# SARAWAK LOCATIONS
# ============================================================================

SARAWAK_LOCATIONS = {
    'Kuching City Center': (1.5497, 110.3633),
    'Kuching Waterfront': (1.5597, 110.3433),
    'Kuching Airport': (1.4843, 110.3469),
    'Sarawak Museum': (1.5547, 110.3633),
    'Borneo Convention Centre': (1.5647, 110.3833),
    'Stutong Park': (1.5347, 110.3833),
    'Damai Beach': (1.7000, 110.3800),
    'Santubong': (1.7000, 110.3800),
    'Bako National Park': (1.7400, 110.4800),
    'Semenggoh Wildlife Centre': (1.4000, 110.3300),
    'Bau': (1.4100, 110.1500),
    'Lundu': (1.6700, 109.8500),
    'Puncak Borneo': (1.2500, 110.1000),
    'Padawan': (1.3500, 110.2000),
    'Serian': (1.1700, 110.5700),
    'Siburan': (1.3000, 110.3500),
    'Tebedu': (1.1200, 110.5300),
    'Kota Sentosa': (1.4800, 110.3300),
    'Matang': (1.6200, 110.1800),
    'Kuching Wetlands': (1.5800, 110.3200),
    'Kota Samarahan': (1.4500, 110.5000),
    'Asajaya': (1.6000, 110.6200),
    'Simunjan': (1.3800, 110.7500),
    'Sebuyau': (1.5200, 110.9300),
    'Sadong Jaya': (1.4700, 110.7300),
    'Sri Aman': (1.2000, 111.5000),
    'Lubok Antu': (1.0500, 111.8300),
    'Engkilili': (1.1300, 111.6700),
    'Pantu': (1.0800, 111.4200),
    'Lingga': (1.3300, 111.1500),
    'Betong': (1.4100, 111.5300),
    'Debak': (1.5600, 111.4200),
    'Pusa': (1.4800, 111.3000),
    'Saratok': (1.7400, 111.3200),
    'Spaoh': (1.4500, 111.4500),
    'Maludam': (1.6500, 111.2500),
    'Roban': (1.6800, 111.3800),
    'Sarikei': (2.1000, 111.8000),
    'Bintangor': (2.1500, 111.9000),
    'Julau': (2.0200, 111.9100),
    'Pakan': (1.8800, 111.7800),
    'Matu': (2.1000, 111.5300),
    'Daro': (2.0500, 111.4800),
    'Jakar': (2.0800, 111.6500),
    'Sibu City Center': (2.2871, 111.8301),
    'Sibu Airport': (2.2586, 111.9661),
    'Kanowit': (2.1000, 112.1500),
    'Selangau': (2.5200, 112.3200),
    'Tatau': (2.8800, 112.8500),
    'Nanga Dap': (2.3200, 112.1000),
    'Durin': (2.2000, 111.9000),
    'Mukah': (2.9064, 112.0800),
    'Dalat': (2.7500, 111.9700),
    'Oya': (2.8500, 111.8500),
    'Balingian': (2.9200, 112.5300),
    'Tanjung Manis': (2.7100, 111.6200),
    'Igan': (2.8200, 111.7500),
    'Kapit': (2.0000, 112.5000),
    'Song': (2.0100, 112.5400),
    'Belaga': (2.7000, 113.7800),
    'Bakun Dam': (2.7600, 113.9300),
    'Murum Dam': (2.9400, 114.1700),
    'Baleh': (2.3000, 113.2000),
    'Nanga Merit': (1.8000, 112.8000),
    'Bintulu City Center': (3.1746, 113.0316),
    'Bintulu Airport': (3.1232, 113.0195),
    'Tanjung Batu Beach': (3.1946, 113.0116),
    'Bintulu Port': (3.1746, 113.0316),
    'Sebauh': (3.1000, 112.9800),
    'Samalaju': (3.4500, 113.1200),
    'Tubau': (3.1800, 113.1300),
    'Jepak': (3.1500, 112.9800),
    'Kemena': (3.2000, 113.0000),
    'Miri City Center': (4.3995, 113.9918),
    'Miri Airport': (4.3223, 113.9868),
    'Tanjung Lobang': (4.4295, 113.9618),
    'Marudi': (4.1800, 114.3200),
    'Lutong': (4.4700, 114.0200),
    'Bekenu': (4.0600, 113.7700),
    'Niah National Park': (3.8100, 113.7700),
    'Lambir Hills': (4.2200, 114.0300),
    'Sibuti': (3.8000, 113.6300),
    'Kuala Baram': (4.5800, 114.0000),
    'Sungai Tujoh': (4.5000, 113.9500),
    'Piasau': (4.4200, 113.9800),
    'Permyjaya': (4.4500, 114.0000),
    'Limbang': (4.7500, 115.0000),
    'Lawas': (4.8500, 115.4000),
    'Sundar': (4.7200, 115.5800),
    'Trusan': (4.8700, 115.2000),
    'Long Semadoh': (4.0500, 115.5000),
    'Ba Kelalan': (3.9700, 115.6200),
    'Bario': (3.7300, 115.4700),
    'Mulu National Park': (4.0450, 114.9380),
    'Gunung Mulu': (4.0500, 114.9300),
    'Deer Cave': (4.0300, 114.9100),
    'Clearwater Cave': (4.0200, 114.9200),
    'Wind Cave': (4.0400, 114.9000),
    'Tebangan': (4.8000, 115.1000),
    'Merapok': (4.8300, 115.3500),
    'Bario Highlands': (3.7300, 115.4700),
    'Ba Kelalan Highlands': (3.9700, 115.6200),
    'Long Pasia': (4.4000, 115.7500),
    'Kelabit Highlands': (3.8000, 115.5000),
    'Long Banga': (3.6000, 115.4000),
    'Long Lellang': (3.7000, 115.3500),
    'Pa Dalih': (3.8500, 115.5200),
    'Pa Ramapuh': (3.9000, 115.5500),
}

BORNEO_LOCATIONS = {**SABAH_LOCATIONS, **SARAWAK_LOCATIONS}

# ============================================================================
# STARGAZING CANDIDATES
# ============================================================================

STARGAZING_CANDIDATES = {
    'Mount Kinabalu Summit, Sabah': (6.0750, 116.5583),
    'Kundasang Highlands, Sabah': (5.9800, 116.5700),
    'Mesilau, Sabah': (6.0400, 116.5900),
    'Trus Madi, Sabah': (5.5000, 116.4000),
    'Crocker Range, Sabah': (5.8000, 116.3000),
    'Tambunan Valley, Sabah': (5.6700, 116.3600),
    'Keningau Highlands, Sabah': (5.3300, 116.1600),
    'Maliau Basin, Sabah': (4.7200, 117.5200),
    'Danum Valley, Sabah': (4.9500, 117.7800),
    'Long Pasia, Sabah': (4.4000, 115.7500),
    'Tawau Hills, Sabah': (4.3500, 117.9000),
    'Kalabakan, Sabah': (4.2200, 117.4800),
    'Pulau Sipadan, Sabah': (4.1140, 118.6250),
    'Pulau Mabul, Sabah': (4.2400, 118.6200),
    'Pulau Bohey Dulang, Sabah': (4.5800, 118.7800),
    'Kudat Peninsula, Sabah': (6.8860, 116.8430),
    'Tanjung Simpang Mengayau, Sabah': (7.0900, 116.9100),
    'Banggi Island, Sabah': (7.2300, 117.1700),
    'Pulau Tiga, Sabah': (5.7200, 115.6300),
    'Kinabatangan, Sabah': (5.4000, 117.8000),
    'Tabin Reserve, Sabah': (5.2000, 118.6500),
    'Ranau Highlands, Sabah': (5.9500, 116.6700),
    'Poring, Sabah': (6.0500, 116.7000),
    'Bario Highlands, Sarawak': (3.7300, 115.4700),
    'Ba Kelalan, Sarawak': (3.9700, 115.6200),
    'Kelabit Highlands, Sarawak': (3.8000, 115.5000),
    'Mulu National Park, Sarawak': (4.0450, 114.9380),
    'Gunung Mulu, Sarawak': (4.0500, 114.9300),
    'Lambir Hills, Sarawak': (4.2200, 114.0300),
    'Niah National Park, Sarawak': (3.8100, 113.7700),
    'Long Semadoh, Sarawak': (4.0500, 115.5000),
    'Long Banga, Sarawak': (3.6000, 115.4000),
    'Long Lellang, Sarawak': (3.7000, 115.3500),
    'Pa Dalih, Sarawak': (3.8500, 115.5200),
    'Bakun Dam Area, Sarawak': (2.7600, 113.9300),
    'Murum Dam Area, Sarawak': (2.9400, 114.1700),
    'Belaga, Sarawak': (2.7000, 113.7800),
    'Kapit Interior, Sarawak': (2.0000, 112.5000),
    'Baleh, Sarawak': (2.3000, 113.2000),
    'Puncak Borneo, Sarawak': (1.2500, 110.1000),
    'Bako National Park, Sarawak': (1.7400, 110.4800),
    'Santubong Peninsula, Sarawak': (1.7000, 110.3800),
    'Bau Gold Mine Area, Sarawak': (1.4100, 110.1500),
    'Lundu Coast, Sarawak': (1.6700, 109.8500),
    'Tanjung Manis, Sarawak': (2.7100, 111.6200),
    'Samalaju, Sarawak': (3.4500, 113.1200),
    'Sibuti Coast, Sarawak': (3.8000, 113.6300),
    'Kuala Baram, Sarawak': (4.5800, 114.0000),
}

# ============================================================================
# STATIC FALLBACK DATA
# ============================================================================

STATIC_AIRPORTS = {
    'Kota Kinabalu International': (5.9375, 116.0490),
    'Sandakan Airport': (5.9010, 118.0580),
    'Tawau Airport': (4.3133, 117.9183),
    'Kudat Airport': (6.9180, 116.8280),
    'Lahad Datu Airport': (5.0310, 118.3200),
    'Semporna Airport': (4.4800, 118.6100),
    'Keningau Airport': (5.3300, 116.1600),
    'Ranau Airport': (5.9500, 116.6700),
    'Kota Marudu Airport': (6.5000, 116.7400),
    'Pitas Airport': (6.7200, 117.0700),
    'Telupid Airport': (5.6300, 117.1300),
    'Beluran Airport': (5.8800, 117.5600),
    'Kunak Airport': (4.6800, 118.2500),
    'Sipitang Airport': (5.0800, 115.5500),
    'Beaufort Airport': (5.3500, 115.7500),
    'Tenom Airport': (5.1300, 115.9500),
    'Tambunan Airport': (5.6700, 116.3600),
    'Papar Airport': (5.7300, 115.9300),
    'Tuaran Airport': (6.1800, 116.2400),
    'Pulau Sipadan Airport': (4.1140, 118.6250),
    'Kuching International': (1.4843, 110.3469),
    'Miri Airport': (4.3223, 113.9868),
    'Sibu Airport': (2.2586, 111.9661),
    'Bintulu Airport': (3.1232, 113.0195),
    'Limbang Airport': (4.7560, 115.0100),
    'Lawas Airport': (4.8500, 115.4000),
    'Mukah Airport': (2.9064, 112.0800),
    'Sarikei Airport': (2.1160, 111.5360),
    'Kapit Airport': (2.0000, 112.5000),
    'Betong Airport': (1.4100, 111.5300),
    'Sri Aman Airport': (1.2000, 111.5000),
    'Marudi Airport': (4.1800, 114.3200),
    'Bario Airport': (3.7300, 115.4700),
    'Ba Kelalan Airport': (3.9700, 115.6200),
    'Mulu Airport': (4.0450, 114.9380),
    'Long Semadoh Airport': (4.0500, 115.5000),
    'Sundar Airport': (4.7200, 115.5800),
    'Lutong Airport': (4.4700, 114.0200),
    'Tatau Airport': (2.8800, 112.8500),
    'Selangau Airport': (2.5200, 112.3200),
    'Kanowit Airport': (2.1000, 112.1500),
    'Daro Airport': (2.0500, 111.4800),
    'Matu Airport': (2.1000, 111.5300),
    'Dalat Airport': (2.7500, 111.9700),
    'Oya Airport': (2.8500, 111.8500),
    'Lubok Antu Airport': (1.0500, 111.8300),
    'Engkilili Airport': (1.1300, 111.6700),
    'Pusa Airport': (1.4800, 111.3000),
    'Saratok Airport': (1.7400, 111.3200),
    'Sebauh Airport': (3.1000, 112.9800),
    'Balingian Airport': (2.9200, 112.5300),
}

STATIC_SETTLEMENTS = {
    'Kota Kinabalu': {'coords': (5.9804, 116.0735), 'population': 500000},
    'Sandakan': {'coords': (5.8400, 118.1200), 'population': 150000},
    'Tawau': {'coords': (4.2435, 117.8853), 'population': 120000},
    'Lahad Datu': {'coords': (5.0300, 118.3300), 'population': 30000},
    'Kudat': {'coords': (6.8860, 116.8430), 'population': 20000},
    'Semporna': {'coords': (4.4800, 118.6100), 'population': 25000},
    'Keningau': {'coords': (5.3300, 116.1600), 'population': 20000},
    'Ranau': {'coords': (5.9500, 116.6700), 'population': 15000},
    'Kota Marudu': {'coords': (6.5000, 116.7400), 'population': 12000},
    'Beaufort': {'coords': (5.3500, 115.7500), 'population': 10000},
    'Tenom': {'coords': (5.1300, 115.9500), 'population': 8000},
    'Tambunan': {'coords': (5.6700, 116.3600), 'population': 7000},
    'Pitas': {'coords': (6.7200, 117.0700), 'population': 6000},
    'Kunak': {'coords': (4.6800, 118.2500), 'population': 8000},
    'Sipitang': {'coords': (5.0800, 115.5500), 'population': 5000},
    'Papar': {'coords': (5.7300, 115.9300), 'population': 7000},
    'Tuaran': {'coords': (6.1800, 116.2400), 'population': 10000},
    'Penampang': {'coords': (5.9000, 116.0800), 'population': 45000},
    'Putatan': {'coords': (5.8800, 116.0600), 'population': 30000},
    'Telupid': {'coords': (5.6300, 117.1300), 'population': 4000},
    'Beluran': {'coords': (5.8800, 117.5600), 'population': 5000},
    'Kinabatangan': {'coords': (5.4000, 117.8000), 'population': 3000},
    'Kuching': {'coords': (1.5497, 110.3633), 'population': 600000},
    'Miri': {'coords': (4.3995, 113.9918), 'population': 300000},
    'Sibu': {'coords': (2.2871, 111.8301), 'population': 200000},
    'Bintulu': {'coords': (3.1746, 113.0316), 'population': 150000},
    'Limbang': {'coords': (4.7500, 115.0000), 'population': 20000},
    'Lawas': {'coords': (4.8500, 115.4000), 'population': 15000},
    'Mukah': {'coords': (2.9064, 112.0800), 'population': 18000},
    'Sarikei': {'coords': (2.1160, 111.5360), 'population': 25000},
    'Kapit': {'coords': (2.0000, 112.5000), 'population': 15000},
    'Betong': {'coords': (1.4100, 111.5300), 'population': 12000},
    'Sri Aman': {'coords': (1.2000, 111.5000), 'population': 15000},
    'Marudi': {'coords': (4.1800, 114.3200), 'population': 10000},
    'Bario': {'coords': (3.7300, 115.4700), 'population': 1000},
    'Ba Kelalan': {'coords': (3.9700, 115.6200), 'population': 2000},
    'Lutong': {'coords': (4.4700, 114.0200), 'population': 15000},
    'Samalaju': {'coords': (3.4500, 113.1200), 'population': 5000},
    'Sebauh': {'coords': (3.1000, 112.9800), 'population': 8000},
    'Balingian': {'coords': (2.9200, 112.5300), 'population': 5000},
    'Dalat': {'coords': (2.7500, 111.9700), 'population': 8000},
    'Oya': {'coords': (2.8500, 111.8500), 'population': 6000},
    'Tanjung Manis': {'coords': (2.7100, 111.6200), 'population': 7000},
    'Kanowit': {'coords': (2.1000, 112.1500), 'population': 5000},
    'Selangau': {'coords': (2.5200, 112.3200), 'population': 4000},
    'Tatau': {'coords': (2.8800, 112.8500), 'population': 3000},
    'Song': {'coords': (2.0100, 112.5400), 'population': 3000},
    'Belaga': {'coords': (2.7000, 113.7800), 'population': 2000},
}

STARGAZING_FACILITY_TAGS = {
    'observatory': [('amenity', 'observatory'), ('man_made', 'observatory')],
    'hotel': [('tourism', 'hotel'), ('tourism', 'guest_house'), ('tourism', 'resort')],
    'campsite': [('tourism', 'camp_site'), ('tourism', 'caravan_site')],
    'viewpoint': [('tourism', 'viewpoint'), ('tourism', 'attraction')],
    'restaurant': [('amenity', 'restaurant'), ('amenity', 'cafe')],
    'fuel': [('amenity', 'fuel'), ('amenity', 'charging_station')],
    'hospital': [('amenity', 'hospital'), ('amenity', 'clinic')],
    'parking': [('amenity', 'parking')],
}

# ============================================================================
# DATA CLASSES
# ============================================================================

@dataclass
class Location:
    lat: float
    lon: float
    name: str = ""
    properties: Dict = field(default_factory=dict)

@dataclass
class AnalysisStep:
    step_number: int
    name: str
    description: str
    status: str = "pending"
    result: Any = None
    execution_time: float = 0.0
    reasoning: str = ""

@dataclass
class AnalysisResult:
    query: str
    steps: List[AnalysisStep] = field(default_factory=list)
    final_result: Any = None
    total_time: float = 0.0
    timestamp: str = ""
    success: bool = False

@dataclass
class MemoryEntry:
    query: str
    query_embedding: List[float] = field(default_factory=list)
    result_summary: str = ""
    success: bool = False
    execution_time: float = 0.0
    timestamp: str = ""
    parameters_used: Dict = field(default_factory=dict)

# ============================================================================
# REPOSITORY PATTERN
# ============================================================================

class MemoryRepository:
    def __init__(self, db_path: str = "borneo_starview_memory.db"):
        self.db_path = db_path
        self._init_database()

    def _init_database(self):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_memory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                query_hash TEXT NOT NULL,
                result_summary TEXT,
                success INTEGER,
                execution_time REAL,
                parameters TEXT,
                timestamp TEXT,
                embedding BLOB
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS learned_parameters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                analysis_type TEXT NOT NULL,
                parameter_name TEXT NOT NULL,
                optimal_value TEXT,
                success_rate REAL,
                usage_count INTEGER DEFAULT 1,
                last_updated TEXT
            )
        """)
        conn.commit()
        conn.close()

    def store_analysis(self, entry: MemoryEntry):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        query_hash = hashlib.md5(entry.query.lower().encode()).hexdigest()
        cursor.execute("""
            INSERT INTO analysis_memory
            (query, query_hash, result_summary, success, execution_time, parameters, timestamp, embedding)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            entry.query, query_hash, entry.result_summary,
            1 if entry.success else 0, entry.execution_time,
            json.dumps(entry.parameters_used), entry.timestamp,
            pickle.dumps(entry.query_embedding)
        ))
        conn.commit()
        conn.close()

    def get_all_analyses(self, limit: int = 20) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM analysis_memory ORDER BY timestamp DESC LIMIT ?", (limit,))
        rows = cursor.fetchall()
        results = []
        for row in rows:
            results.append({
                'query': row[1],
                'result_summary': row[3],
                'success': bool(row[4]),
                'execution_time': row[5],
                'parameters': json.loads(row[6]) if row[6] else {},
                'timestamp': row[7]
            })
        conn.close()
        return results

    def find_similar_analyses(self, query: str, limit: int = 5) -> List[Dict]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM analysis_memory ORDER BY timestamp DESC LIMIT 100")
        rows = cursor.fetchall()
        if not query or not query.strip():
            conn.close()
            return []
        keywords = query.lower().split()
        results = []
        for row in rows:
            stored_query = row[1].lower()
            match_score = sum(1 for kw in keywords if kw in stored_query)
            if match_score > 0:
                results.append({
                    'query': row[1],
                    'result_summary': row[3],
                    'success': bool(row[4]),
                    'execution_time': row[5],
                    'parameters': json.loads(row[6]) if row[6] else {},
                    'timestamp': row[7],
                    'match_score': match_score
                })
        conn.close()
        results.sort(key=lambda x: x['match_score'], reverse=True)
        return results[:limit]

    def get_learned_parameter(self, analysis_type: str, parameter_name: str) -> Optional[str]:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT optimal_value, success_rate FROM learned_parameters
            WHERE analysis_type = ? AND parameter_name = ?
            ORDER BY success_rate DESC LIMIT 1
        """, (analysis_type, parameter_name))
        row = cursor.fetchone()
        conn.close()
        return row[0] if row else None

    def update_learned_parameter(self, analysis_type: str, parameter_name: str,
                                  value: str, success: bool):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, success_rate, usage_count FROM learned_parameters
            WHERE analysis_type = ? AND parameter_name = ? AND optimal_value = ?
        """, (analysis_type, parameter_name, value))
        row = cursor.fetchone()
        if row:
            new_count = row[2] + 1
            new_rate = ((row[1] * row[2]) + (1 if success else 0)) / new_count
            cursor.execute("""
                UPDATE learned_parameters
                SET success_rate = ?, usage_count = ?, last_updated = ?
                WHERE id = ?
            """, (new_rate, new_count, datetime.now().isoformat(), row[0]))
        else:
            cursor.execute("""
                INSERT INTO learned_parameters
                (analysis_type, parameter_name, optimal_value, success_rate, usage_count, last_updated)
                VALUES (?, ?, ?, ?, 1, ?)
            """, (analysis_type, parameter_name, value, 1.0 if success else 0.0, datetime.now().isoformat()))
        conn.commit()
        conn.close()

    def get_analysis_stats(self) -> Dict:
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM analysis_memory")
        total = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM analysis_memory WHERE success = 1")
        successful = cursor.fetchone()[0]
        cursor.execute("SELECT AVG(execution_time) FROM analysis_memory")
        avg_time = cursor.fetchone()[0] or 0
        conn.close()
        return {
            'total_analyses': total,
            'successful_analyses': successful,
            'success_rate': successful / total if total > 0 else 0,
            'avg_execution_time': avg_time
        }

# ============================================================================
# STRATEGY PATTERN
# ============================================================================

class AnalysisStrategy(ABC):
    @abstractmethod
    def analyse(self, location: Location, params: Dict) -> Dict:
        pass

    @abstractmethod
    def get_name(self) -> str:
        pass


class StargazingSuitabilityStrategy(AnalysisStrategy):
    """HYBRID Strategy v3.2.2 with fog detection."""

    def get_name(self) -> str:
        return "Stargazing Suitability Analysis v3.2.2"

    def _haversine(self, lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        R = 6371
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
        return R * 2 * math.asin(min(1, math.sqrt(a)))

    def _get_elevation_quick(self, location: Location) -> tuple:
        try:
            elevation_url = f"https://api.open-elevation.com/api/v1/lookup?locations={location.lat},{location.lon}"
            response = requests.get(elevation_url, timeout=3)
            data = response.json()
            elev = data['results'][0]['elevation']
            if elev > 1000:
                return 5.0, elev, 'Live Elevation API'
            elif elev > 500:
                return 4.8, elev, 'Live Elevation API'
            elif elev > 200:
                return 4.3, elev, 'Live Elevation API'
            elif elev > 100:
                return 3.8, elev, 'Live Elevation API'
            elif elev > 50:
                return 3.3, elev, 'Live Elevation API'
            else:
                return 2.5, elev, 'Live Elevation API'
        except Exception:
            lat, lon = location.lat, location.lon
            if lat > 5.8 and lat < 6.2 and lon > 116.4 and lon < 116.8:
                return 5.0, 1500, 'Fallback: Kinabalu region'
            elif lat > 3.5 and lat < 4.5 and lon > 115.0 and lon < 115.8:
                return 4.8, 1000, 'Fallback: Kelabit Highlands'
            elif lat > 5.3 and lat < 5.8 and lon > 116.2 and lon < 116.6:
                return 4.5, 800, 'Fallback: Crocker Range'
            elif lat > 4.5 and lon > 117.0:
                return 3.8, 300, 'Fallback: E. Sabah hills'
            elif lat > 2.5 and lon > 114.0 and lon < 115.5:
                return 4.0, 500, 'Fallback: Sarawak interior'
            else:
                return 3.0, 50, 'Fallback: Lowland area'

    def _check_protected_zone(self, location: Location) -> tuple:
        for name, (lat, lon, radius_km, designation, desc) in PROTECTED_DARK_SKY_ZONES.items():
            dist = self._haversine(location.lat, location.lon, lat, lon)
            if dist <= radius_km:
                return {
                    'name': name,
                    'designation': designation,
                    'description': desc,
                    'distance_km': round(dist, 1)
                }
        return None

    def _get_weather(self, location: Location) -> Optional[Dict]:
        try:
            url = "https://api.open-meteo.com/v1/forecast"
            params = {
                "latitude": location.lat,
                "longitude": location.lon,
                "current": "temperature_2m,relative_humidity_2m,cloud_cover,"
                           "visibility,wind_speed_10m,wind_direction_10m,dew_point_2m",
                "wind_speed_unit": "ms",
                "timezone": "auto",
            }
            r = requests.get(url, params=params, timeout=4)
            data = r.json()
            cur = data.get("current", {})
            visibility_m = cur.get("visibility")
            return {
                "temperature_c": cur.get("temperature_2m"),
                "humidity_pct": cur.get("relative_humidity_2m"),
                "cloud_cover_pct": cur.get("cloud_cover"),
                "visibility_km": visibility_m / 1000 if visibility_m else None,
                "wind_speed_ms": cur.get("wind_speed_10m"),
                "wind_direction_deg": cur.get("wind_direction_10m"),
                "dew_point_c": cur.get("dew_point_2m"),
                "source": "Open-Meteo (Live)",
                "time": cur.get("time"),
            }
        except Exception:
            return None

    def _score_cloud_cover(self, cloud_cover_pct: Optional[float]) -> tuple:
        if cloud_cover_pct is None:
            return 3.0, "Unknown", "Weather unavailable — neutral score"
        if cloud_cover_pct < 10:
            return 5.0, "Excellent", f"Crystal clear ({cloud_cover_pct:.0f}% cloud)"
        elif cloud_cover_pct < 25:
            return 4.5, "Very Good", f"Mostly clear ({cloud_cover_pct:.0f}% cloud)"
        elif cloud_cover_pct < 50:
            return 3.5, "Good", f"Partly cloudy ({cloud_cover_pct:.0f}% cloud)"
        elif cloud_cover_pct < 75:
            return 2.5, "Moderate", f"Mostly cloudy ({cloud_cover_pct:.0f}% cloud)"
        else:
            return 1.5, "Poor", f"Heavy cloud cover ({cloud_cover_pct:.0f}%)"

    def _geographic_score_light_pollution(self, location: Location, elevation_m: float) -> tuple:
        """FIXED v3.1: Population-weighted, distance-weighted light pollution."""
        lat, lon = location.lat, location.lon
        
        total_light_pollution = 0.0
        nearest_major = 999
        nearest_major_name = None
        
        for name, data in STATIC_SETTLEMENTS.items():
            s_lat, s_lon = data['coords']
            pop = data.get('population', 1000)
            dist = self._haversine(lat, lon, s_lat, s_lon)
            
            if dist > 200:
                continue
            
            if pop >= 50000 and dist < nearest_major:
                nearest_major = dist
                nearest_major_name = name
            
            if dist < 1:
                dist = 1
            contribution = (pop / 100000) / (dist ** 1.5)
            total_light_pollution += contribution
        
        if elevation_m > 1500 and total_light_pollution < 3.0:
            return 5.0, 0, 'Geographic: Above light dome (high alt)'
        if elevation_m > 1000 and total_light_pollution < 5.0:
            return 4.8, 1, 'Geographic: Highland dark sky'
        if elevation_m > 800 and total_light_pollution < 6.0:
            return 4.5, 1, 'Geographic: Highland dark sky'
        
        if total_light_pollution < 0.01:
            return 5.0, 0, 'Geographic: Pristine dark sky'
        elif total_light_pollution < 0.05:
            return 4.8, 1, 'Geographic: Very dark sky'
        elif total_light_pollution < 0.15:
            return 4.5, 2, 'Geographic: Dark sky'
        elif total_light_pollution < 0.4:
            return 4.0, 3, 'Geographic: Mostly dark'
        elif total_light_pollution < 0.8:
            return 3.5, 4, 'Geographic: Suburban sky'
        elif total_light_pollution < 1.5:
            return 3.0, 5, 'Geographic: Semi-dark'
        elif total_light_pollution < 3.0:
            return 2.0, 7, 'Geographic: Light pollution'
        elif total_light_pollution < 6.0:
            return 1.5, 8, 'Geographic: Significant light pollution'
        else:
            return 1.0, 10, 'Geographic: Heavy light pollution'

    def _geographic_score_atmospheric_clarity(self, location: Location, elevation_m: float) -> tuple:
        lat, lon = location.lat, location.lon

        if elevation_m > 1500:
            return 5.0, 80, 'Geographic: High-altitude (above clouds)'
        if elevation_m > 1000:
            return 4.7, 60, 'Geographic: High-altitude'

        if lon > 117.5:
            coastal_dist = 5
        elif lon > 116.5:
            coastal_dist = 15
        elif lon > 115.5:
            coastal_dist = 25
        elif lon > 114.5:
            coastal_dist = 40
        else:
            coastal_dist = 60

        if coastal_dist > 50:
            return 5.0, coastal_dist, 'Geographic: Deep inland'
        elif coastal_dist > 30:
            return 4.3, coastal_dist, 'Geographic: Inland'
        elif coastal_dist > 15:
            return 3.5, coastal_dist, 'Geographic: Coastal influence'
        else:
            return 2.5, coastal_dist, 'Geographic: Coastal'

    def _geographic_score_infrastructure(self, location: Location) -> tuple:
        lat, lon = location.lat, location.lon
        min_dist = 999
        for name, coords in STATIC_AIRPORTS.items():
            a_lat, a_lon = coords
            dist = self._haversine(lat, lon, a_lat, a_lon)
            min_dist = min(min_dist, dist)
        details = {
            'airports': 1 if min_dist < 60 else 0,
            'major_roads': 2 if min_dist < 30 else 0,
            'power_facilities': 1 if min_dist < 40 else 0,
            'accommodation': 1 if min_dist < 20 else 0
        }
        if min_dist < 30:
            return 4.5, details, 'Geographic: Near airport'
        elif min_dist < 60:
            return 3.5, details, 'Geographic: Airport nearby'
        elif min_dist < 100:
            return 2.5, details, 'Geographic: Some access'
        else:
            return 1.5, details, 'Geographic: Remote'

    def _geographic_score_land(self, location: Location, protected_zone: Optional[Dict]) -> tuple:
        if protected_zone:
            details = {'forest_areas': 40, 'developed_areas': 1, 'open_areas': 30}
            return 5.0, details, 'Geographic: Protected park (vast land)'

        lat, lon = location.lat, location.lon
        min_dist = 999
        for name, data in STATIC_SETTLEMENTS.items():
            s_lat, s_lon = data['coords']
            dist = self._haversine(lat, lon, s_lat, s_lon)
            min_dist = min(min_dist, dist)
        details = {
            'forest_areas': 30 if min_dist > 50 else 10,
            'developed_areas': 2 if min_dist > 50 else 10,
            'open_areas': 40 if min_dist > 30 else 15
        }
        if min_dist > 80:
            return 5.0, details, 'Geographic: Abundant land'
        elif min_dist > 50:
            return 4.0, details, 'Geographic: Good land'
        elif min_dist > 30:
            return 3.0, details, 'Geographic: Moderate land'
        elif min_dist > 15:
            return 2.5, details, 'Geographic: Limited land'
        else:
            return 2.0, details, 'Geographic: Scarce land'

    def _geographic_score_cloud_risk(self, lat: float, lon: float, elevation_m: float, protected_zone: Optional[Dict]) -> tuple:
        """FIXED v3.2.1: Coastal check added."""
        # FIX 1: Check low elevation FIRST — coastal cities have more clouds
        if elevation_m < 50:
            return 3.0, 'Moderate', 'Geographic: Coastal (low elevation)'
        
        # FIX 2: Now check high altitude
        if elevation_m > 1500:
            return 4.5, 'Low', 'Geographic: Above cloud layer'
        if elevation_m > 1000:
            return 4.2, 'Low', 'Geographic: Highland climate'

        if protected_zone and lon > 114.0 and lon < 116.0:
            return 4.3, 'Low', 'Geographic: Protected inland'

        if lon > 115.0 and lon < 116.0 and lat > 3.5:
            return 4.0, 'Low', 'Geographic: Highland climate'
        elif lat > 5.5 and lon > 116.0 and lon < 117.0:
            return 3.8, 'Low', 'Geographic: Highland'
        elif lon > 114.0 and lon < 115.5:
            return 4.0, 'Low', 'Geographic: Interior'
        elif lat < 5.0 and lon > 117.0:
            return 2.8, 'High', 'Geographic: Coastal'
        else:
            return 3.2, 'Moderate', 'Geographic: Typical'

    def _score_latitudinal_advantage(self, lat: float) -> float:
        abs_lat = abs(lat)
        if abs_lat <= 2:
            return 5.0
        elif abs_lat <= 4:
            return 4.7
        elif abs_lat <= 6:
            return 4.3
        elif abs_lat <= 8:
            return 3.8
        else:
            return 3.0

    def _try_osm_in_background(self, location: Location, radius: int) -> Optional[Dict]:
        try:
            overpass_url = "https://overpass-api.de/api/interpreter"
            results = {}
            query = f"""
            [out:json][timeout:5];
            (
              node["tourism"~"hotel|guest_house|resort|camp_site|viewpoint"](around:{radius},{location.lat},{location.lon});
            );
            out count;
            """
            response = requests.post(overpass_url, data={'data': query}, timeout=5)
            results['tourism_count'] = len(response.json().get('elements', []))

            query = f"""
            [out:json][timeout:5];
            (
              node["amenity"~"restaurant|cafe|fuel|parking"](around:{radius},{location.lat},{location.lon});
            );
            out count;
            """
            response = requests.post(overpass_url, data={'data': query}, timeout=5)
            results['amenities_count'] = len(response.json().get('elements', []))

            query = f"""
            [out:json][timeout:5];
            (
              way["highway"~"motorway|trunk|primary"](around:{radius},{location.lat},{location.lon});
            );
            out count;
            """
            response = requests.post(overpass_url, data={'data': query}, timeout=5)
            results['road_count'] = len(response.json().get('elements', []))
            return results
        except Exception:
            return None

    def analyse(self, location: Location, params: Dict) -> Dict:
        radius = params.get('radius', 10000)
        weights = params.get('weights', {
            'light_pollution': 0.22,
            'atmospheric_clarity': 0.18,
            'cloud_risk': 0.15,
            'cloud_cover': 0.12,
            'elevation': 0.10,
            'latitudinal_advantage': 0.08,
            'infrastructure_access': 0.08,
            'land_availability': 0.07,
        })

        scores = {}
        details = {}
        data_source_details = []
        osm_data = None
        osm_available = False
        weather_data = None
        air_quality_data = None
        haze_data = None

        elevation_score, elevation_m, elev_source = self._get_elevation_quick(location)
        protected_zone = self._check_protected_zone(location)

        # 1. LIGHT POLLUTION
        lp_score, lp_index, lp_source = self._geographic_score_light_pollution(location, elevation_m)

        if protected_zone:
            lp_score = max(lp_score, 4.7)
            lp_index = min(lp_index, 1)
            data_source_details.append(f"🏞️ Protected Zone: {protected_zone['name']} ({protected_zone['designation']})")
            lp_source = f"Protected: {protected_zone['name']}"

        data_source_details.append(f"Light Pollution: {lp_source}")
        scores['light_pollution'] = lp_score
        details['light_pollution'] = {
            'score': lp_score,
            'value': f"Level {lp_index}/10" if not protected_zone else f"Level {lp_index}/10 (Protected)",
            'weight': weights['light_pollution'],
            'source': lp_source
        }

        # 2. ATMOSPHERIC CLARITY
        clarity_score, coastal_dist, clarity_source = self._geographic_score_atmospheric_clarity(location, elevation_m)
        data_source_details.append(f"Clarity: {clarity_source}")
        scores['atmospheric_clarity'] = clarity_score
        details['atmospheric_clarity'] = {
            'score': clarity_score,
            'value': f"{coastal_dist:.0f}km from coast" if elevation_m < 1000 else f"High altitude ({elevation_m:.0f}m)",
            'weight': weights['atmospheric_clarity'],
            'source': clarity_source
        }

        # 3. ELEVATION
        data_source_details.append(f"Elevation: {elev_source} ({elevation_m:.0f}m)")
        scores['elevation'] = elevation_score
        details['elevation'] = {
            'score': elevation_score,
            'value': f"{elevation_m:.0f}m",
            'weight': weights['elevation'],
            'source': elev_source
        }

        # 4. CLOUD RISK
        cloud_risk_score, cloud_risk, cloud_risk_source = self._geographic_score_cloud_risk(
            location.lat, location.lon, elevation_m, protected_zone
        )
        data_source_details.append(f"Cloud Risk: {cloud_risk_source}")
        scores['cloud_risk'] = cloud_risk_score
        details['cloud_risk'] = {
            'score': cloud_risk_score,
            'value': cloud_risk,
            'weight': weights['cloud_risk'],
            'source': cloud_risk_source
        }

        # 5. LATITUDE
        lat_score = self._score_latitudinal_advantage(location.lat)
        scores['latitudinal_advantage'] = lat_score
        details['latitudinal_advantage'] = {
            'score': lat_score,
            'value': f"{abs(location.lat):.1f}°{'N' if location.lat > 0 else 'S'}",
            'weight': weights['latitudinal_advantage'],
            'source': 'Geographic'
        }

        # 6. INFRASTRUCTURE
        infra_score, infra_details, infra_source = self._geographic_score_infrastructure(location)
        data_source_details.append(f"Infrastructure: {infra_source}")
        scores['infrastructure_access'] = infra_score
        details['infrastructure_access'] = {
            'score': infra_score,
            'value': infra_details,
            'weight': weights['infrastructure_access'],
            'source': infra_source
        }

        # 7. LAND
        land_score, land_details, land_source = self._geographic_score_land(location, protected_zone)
        data_source_details.append(f"Land: {land_source}")
        scores['land_availability'] = land_score
        details['land_availability'] = {
            'score': land_score,
            'value': land_details,
            'weight': weights['land_availability'],
            'source': land_source
        }

        # 8. CLOUD COVER (Live)
        weather_data = self._get_weather(location)
        if weather_data:
            cc = weather_data.get('cloud_cover_pct')
            cc_score, cc_rating, cc_explanation = self._score_cloud_cover(cc)
            data_source_details.append(f"Cloud Cover: {cc_explanation}")
            weather_data['cloud_rating'] = cc_rating
            weather_data['cloud_explanation'] = cc_explanation
        else:
            cc_score, cc_rating, cc_explanation = 3.0, "Unknown", "Weather unavailable"
            data_source_details.append("Cloud Cover: Weather API unavailable")

        scores['cloud_cover'] = cc_score
        details['cloud_cover'] = {
            'score': cc_score,
            'value': weather_data.get('cloud_cover_pct') and f"{weather_data['cloud_cover_pct']:.0f}%" or "N/A",
            'weight': weights['cloud_cover'],
            'source': weather_data.get('source', 'Unavailable') if weather_data else 'Unavailable'
        }

        # ============ v3.2.2: HAZE/FOG DETECTION ============
        air_quality_data = get_air_quality({'lat': location.lat, 'lon': location.lon})
        # NEW v3.2.2: Pass elevation to detect_haze for fog detection
        haze_data = detect_haze(
            weather_data, 
            air_quality_data, 
            {'lat': location.lat, 'lon': location.lon, 'elevation_m': elevation_m}
        )
        
        if haze_data['detected']:
            if haze_data.get('is_fog'):
                data_source_details.append(f"🌫️ Fog Detected: {haze_data['severity']} ({haze_data['confidence']} confidence)")
            else:
                data_source_details.append(
                    f"🌫️ Haze Detected: {haze_data['severity']} ({haze_data['confidence']} confidence)"
                )
        
        if air_quality_data:
            pm25 = air_quality_data.get('pm2_5')
            if pm25 is not None:
                data_source_details.append(f"Air Quality: PM2.5 {pm25:.1f} µg/m³")

        # ============ BASE SCORE ============
        total_score = sum(scores[key] * weights.get(key, 0) for key in scores.keys() if key in weights)
        max_possible = sum(weights.values()) * 5.0
        percentage = (total_score / max_possible) * 100 if max_possible > 0 else 0

        # ============ CRITICAL PENALTIES ============
        penalty = 0.0
        penalty_reasons = []

        if not protected_zone:
            if lp_index >= 8:
                penalty += 20.0
                penalty_reasons.append(f"Heavy light pollution (Level {lp_index}/10): -20%")
            elif lp_index >= 5:
                penalty += 10.0
                penalty_reasons.append(f"Significant light pollution (Level {lp_index}/10): -10%")

        if cloud_risk == 'High' and elevation_m < 1000:
            penalty += 12.0
            penalty_reasons.append("High seasonal cloud risk: -12%")

        if coastal_dist < 10 and elevation_m < 500:
            penalty += 8.0
            penalty_reasons.append("Coastal location (cloud/haze risk): -8%")

        if weather_data and weather_data.get('cloud_cover_pct'):
            if weather_data['cloud_cover_pct'] > 70:
                penalty += 10.0
                penalty_reasons.append(f"Heavy cloud cover now ({weather_data['cloud_cover_pct']:.0f}%): -10%")

        # v3.2.2: HAZE/FOG PENALTIES (only apply if it's actual smoke)
        haze_severity = haze_data.get('severity', 'None')
        is_fog = haze_data.get('is_fog', False)
        
        if is_fog:
            # Fog penalty is smaller — it's not a health hazard, just viewing
            penalty += 8.0
            penalty_reasons.append(f"Natural mountain fog (viewing blocked): -8%")
        elif haze_severity == 'Severe':
            penalty += 25.0
            penalty_reasons.append(f"SEVERE HAZE detected: -25%")
        elif haze_severity == 'Heavy':
            penalty += 18.0
            penalty_reasons.append(f"Heavy haze detected: -18%")
        elif haze_severity == 'Moderate':
            penalty += 10.0
            penalty_reasons.append(f"Moderate haze detected: -10%")
        elif haze_severity == 'Light':
            penalty += 4.0
            penalty_reasons.append(f"Light haze detected: -4%")

        percentage = max(0.0, min(100.0, percentage - penalty))

        if percentage >= 80:
            rating, emoji, rec = 'Excellent', '🌟', 'World-class stargazing destination potential'
        elif percentage >= 65:
            rating, emoji, rec = 'Good', '✨', 'Excellent viewing site with minor improvements'
        elif percentage >= 50:
            rating, emoji, rec = 'Moderate', '⭐', 'Good viewing site requiring some investment'
        elif percentage >= 35:
            rating, emoji, rec = 'Limited', '⚠️', 'Challenging conditions, major investment needed'
        else:
            rating, emoji, rec = 'Poor', '❌', 'Not recommended for astronomy development'

        try:
            osm_data = self._try_osm_in_background(location, radius)
            if osm_data and any(v > 0 for v in osm_data.values()):
                osm_available = True
                data_source_details.append(
                    f"🌐 OSM: {osm_data.get('tourism_count', 0)} tourism, "
                    f"{osm_data.get('amenities_count', 0)} amenities"
                )
        except Exception:
            pass

        seen = set()
        unique_details = []
        for d in data_source_details:
            if d not in seen:
                seen.add(d)
                unique_details.append(d)

        return {
            'success': True,
            'scores': scores,
            'details': details,
            'weighted_score': total_score,
            'max_possible_score': max_possible,
            'suitability_percentage': round(percentage, 1),
            'base_percentage': round((total_score / max_possible * 100) if max_possible > 0 else 0, 1),
            'penalty_applied': round(penalty, 1),
            'penalty_reasons': penalty_reasons,
            'rating': rating,
            'rating_emoji': emoji,
            'recommendation': rec,
            'radius_used': radius,
            'location': f"{location.name or 'Borneo location'} ({location.lat:.4f}, {location.lon:.4f})",
            'location_name': location.name or 'Borneo location',
            'elevation_m': elevation_m,
            'light_pollution_index': lp_index,
            'coastal_distance_km': coastal_dist,
            'cloud_risk': cloud_risk,
            'lat_deg': abs(location.lat),
            'lon': location.lon,
            'lat': location.lat,
            'protected_zone': protected_zone,
            'data_sources': [d for d in unique_details],
            'data_source_details': unique_details,
            'used_osm': osm_available,
            'osm_data': osm_data if osm_available else None,
            'weather': weather_data,
            'cloud_cover_pct': weather_data.get('cloud_cover_pct') if weather_data else None,
            'humidity_pct': weather_data.get('humidity_pct') if weather_data else None,
            'visibility_km': weather_data.get('visibility_km') if weather_data else None,
            'temperature_c': weather_data.get('temperature_c') if weather_data else None,
            'dew_point_c': weather_data.get('dew_point_c') if weather_data else None,
            'wind_speed_ms': weather_data.get('wind_speed_ms') if weather_data else None,
            'wind_direction_deg': weather_data.get('wind_direction_deg') if weather_data else None,
            'haze': haze_data,
            'air_quality': air_quality_data,
            'used_fallback': True,
            'from_cache': False,
            'analysis_method': 'HYBRID v3.2.2: Fog + Haze + Coastal Fix + Population-Weighted + Weather + Moon'
        }


class ProximityAnalysisStrategy(AnalysisStrategy):
    def get_name(self) -> str:
        return "Proximity Analysis"

    def analyse(self, location: Location, params: Dict) -> Dict:
        amenity_type = params.get('amenity_type', 'hotel')
        radius = params.get('radius', 5000)
        tags_to_query = STARGAZING_FACILITY_TAGS.get(amenity_type, [('amenity', amenity_type)])
        query_parts = []
        for key, value in tags_to_query:
            query_parts.append(f'node["{key}"="{value}"](around:{radius},{location.lat},{location.lon});')
            query_parts.append(f'way["{key}"="{value}"](around:{radius},{location.lat},{location.lon});')
        query_body = "\n".join(query_parts)
        query = f"""[out:json][timeout:45];
(
{query_body}
);
out center;"""
        try:
            headers = {'User-Agent': 'BorneoAstroViewGeoAI/3.2.2'}
            response = requests.post("https://overpass-api.de/api/interpreter",
                                   data={'data': query}, headers=headers, timeout=45)
            response.raise_for_status()
            data = response.json()
            elements = data.get('elements', [])
            results = []
            seen_locations = set()
            for elem in elements:
                lat = elem.get('lat') or elem.get('center', {}).get('lat')
                lon = elem.get('lon') or elem.get('center', {}).get('lon')
                if lat and lon:
                    loc_key = f"{round(lat, 5)}_{round(lon, 5)}"
                    if loc_key not in seen_locations:
                        seen_locations.add(loc_key)
                        tags = elem.get('tags', {})
                        name = tags.get('name', tags.get('brand', 'Unknown'))
                        results.append({
                            'name': name, 'lat': lat, 'lon': lon,
                            'type': amenity_type, 'tags': tags
                        })
            return {
                'success': True, 'count': len(results),
                'amenities': results, 'radius': radius,
                'amenity_type': amenity_type,
                'location': f"Borneo ({location.lat:.4f}, {location.lon:.4f})"
            }
        except Exception as e:
            return {
                'success': False, 'error': str(e),
                'amenities': [], 'count': 0,
                'radius': radius, 'amenity_type': amenity_type
            }


class StrategySelector:
    _strategies = {
        'stargazing': StargazingSuitabilityStrategy,
        'proximity': ProximityAnalysisStrategy,
    }

    @classmethod
    def get_strategy(cls, strategy_type: str) -> AnalysisStrategy:
        strategy_class = cls._strategies.get(strategy_type)
        if not strategy_class:
            raise ValueError(f"Unknown strategy: {strategy_type}")
        return strategy_class()

    @classmethod
    def available_strategies(cls) -> List[str]:
        return list(cls._strategies.keys())

# ============================================================================
# RATE LIMITING
# ============================================================================

class RateLimiter:
    def __init__(self, calls_per_second: float = 0.5):
        self.calls_per_second = calls_per_second
        self.last_call = 0

    def wait(self):
        now = time.time()
        time_since_last = now - self.last_call
        min_interval = 1.0 / self.calls_per_second
        if time_since_last < min_interval:
            time.sleep(min_interval - time_since_last)
        self.last_call = time.time()

# ============================================================================
# MAIN AGENT CLASS
# ============================================================================

class BorneoAstroViewGeoAIAgent:
    def __init__(self):
        self.memory_repo = MemoryRepository()
        self.rate_limiter = RateLimiter(calls_per_second=0.5)
        self.short_term_memory: Dict[str, Any] = {}
        self.current_analysis: Optional[AnalysisResult] = None

    def reason_about_query(self, query: str) -> tuple:
        query_lower = query.lower()
        steps = []
        steps.append({
            'step': 'Understanding Query',
            'reasoning': f"Analysing stargazing site selection request: '{query}'",
            'action': 'parse_intent'
        })
        similar = self.memory_repo.find_similar_analyses(query, limit=3)
        if similar:
            steps.append({
                'step': 'Memory Recall',
                'reasoning': f"Found {len(similar)} similar past analyses.",
                'action': 'apply_learned_parameters',
                'prior_experience': similar[0]
            })
        analysis_type = 'stargazing'
        steps.append({
            'step': 'Strategy Selection',
            'reasoning': 'Using Stargazing Suitability strategy v3.2.2 with fog detection.',
            'action': 'use_stargazing_strategy'
        })
        learned_radius = self.memory_repo.get_learned_parameter(analysis_type, 'radius')
        if learned_radius:
            steps.append({
                'step': 'Parameter Optimisation',
                'reasoning': f"Using learned radius of {learned_radius}m.",
                'action': 'apply_learned_radius',
                'value': learned_radius
            })
        else:
            steps.append({
                'step': 'Parameter Selection',
                'reasoning': 'Using default radius of 10km.',
                'action': 'use_default_radius',
                'value': '10000'
            })
        steps.append({
            'step': 'Moon Phase Calculation',
            'reasoning': 'Calculating current moon phase and its impact on viewing conditions.',
            'action': 'calculate_moon'
        })
        steps.append({
            'step': 'Milky Way Check',
            'reasoning': 'Determining galactic core visibility for current date.',
            'action': 'check_milky_way'
        })
        steps.append({
            'step': 'Haze & Fog Analysis',
            'reasoning': 'Checking for smoke haze vs natural mountain fog.',
            'action': 'detect_haze'
        })
        steps.append({
            'step': 'Execution Planning',
            'reasoning': 'Ready to execute stargazing suitability analysis.',
            'action': 'prepare_execution'
        })
        return steps, analysis_type

    def execute_analysis(self, location: Location, query: str,
                         params: Dict, progress_callback: Callable = None) -> AnalysisResult:
        start_time = time.time()
        result = AnalysisResult(query=query, timestamp=datetime.now().isoformat())
        reasoning_steps, analysis_type = self.reason_about_query(query)
        for i, step_info in enumerate(reasoning_steps):
            result.steps.append(AnalysisStep(
                step_number=i + 1,
                name=step_info['step'],
                description=step_info['reasoning'],
                status='completed',
                reasoning=step_info['reasoning']
            ))
        if progress_callback:
            progress_callback(0.3, "Reasoning complete, executing hybrid analysis...")
        try:
            strategy = StrategySelector.get_strategy(analysis_type)
            self.rate_limiter.wait()
            analysis_result = strategy.analyse(location, params)
            analysis_result['from_cache'] = False
            
            moon_phase = calculate_moon_phase()
            analysis_result['moon_phase'] = moon_phase
            
            milky_way = get_milky_way_visibility(location.lat, location.lon)
            analysis_result['milky_way'] = milky_way
            
            astro_scores = calculate_astrophotography_scores(analysis_result, moon_phase)
            analysis_result['astrophotography_scores'] = astro_scores
            
            if analysis_result.get('success'):
                used_osm = analysis_result.get('used_osm', False)
                protected = analysis_result.get('protected_zone')
                haze = analysis_result.get('haze', {})
                method_note = analysis_result.get('analysis_method', 'HYBRID v3.2.2')
                if protected:
                    method_note += f" | Protected: {protected['name']}"
                if haze.get('detected'):
                    if haze.get('is_fog'):
                        method_note += f" | FOG: {haze['severity']}"
                    else:
                        method_note += f" | HAZE: {haze['severity']}"
                result.steps.append(AnalysisStep(
                    step_number=len(result.steps) + 1,
                    name="Data Source Validation",
                    description=f"Method: {method_note}",
                    status='completed',
                    reasoning=f"Used {'OSM + Geographic' if used_osm else 'Geographic'} rules"
                ))
            result.steps.append(AnalysisStep(
                step_number=len(result.steps) + 1,
                name=f"Execute {strategy.get_name()}",
                description=f"Running {analysis_type} analysis on {location.name or 'Borneo location'}",
                status='completed' if analysis_result.get('success') else 'failed',
                result=analysis_result,
                reasoning=f"Analysis complete"
            ))
            result.final_result = analysis_result
            result.success = analysis_result.get('success', False)
        except Exception as e:
            result.steps.append(AnalysisStep(
                step_number=len(result.steps) + 1,
                name="Analysis Execution",
                description="Executing spatial analysis",
                status='failed',
                reasoning=f"Error: {str(e)}"
            ))
            result.success = False
        if progress_callback:
            progress_callback(0.8, "Storing results in memory...")
        result.total_time = time.time() - start_time
        memory_entry = MemoryEntry(
            query=query,
            result_summary=str(result.final_result)[:500] if result.final_result else "",
            success=result.success,
            execution_time=result.total_time,
            timestamp=result.timestamp,
            parameters_used=params
        )
        self.memory_repo.store_analysis(memory_entry)
        if result.success:
            self.memory_repo.update_learned_parameter(
                analysis_type, 'radius', str(params.get('radius', 10000)), True
            )
        self.short_term_memory['last_analysis'] = result
        self.short_term_memory['last_location'] = location
        if progress_callback:
            progress_callback(1.0, "Complete")
        return result

# ============================================================================
# UI HELPERS
# ============================================================================

def init_session_state():
    if 'agent' not in st.session_state:
        st.session_state.agent = BorneoAstroViewGeoAIAgent()
    if 'analysis_history' not in st.session_state:
        st.session_state.analysis_history = []
    if 'selected_location' not in st.session_state:
        st.session_state.selected_location = Location(
            lat=6.0750, lon=116.5583, name="Mount Kinabalu Summit, Sabah"
        )
    if 'reasoning_log' not in st.session_state:
        st.session_state.reasoning_log = []
    if 'current_results' not in st.session_state:
        st.session_state.current_results = None
    if 'basemap_choice' not in st.session_state:
        st.session_state.basemap_choice = "OpenStreetMap"
    if 'show_radius_circle' not in st.session_state:
        st.session_state.show_radius_circle = True
    if 'comparison_mode' not in st.session_state:
        st.session_state.comparison_mode = False
    if 'candidate_scores' not in st.session_state:
        st.session_state.candidate_scores = {}


def render_region_selector():
    regions = {
        '🌏 All Borneo': 'all',
        '🏝️ Sabah Only': 'sabah',
        '🏝️ Sarawak Only': 'sarawak',
        '🌟 Stargazing Candidates': 'candidates'
    }
    selected_region = st.selectbox("Select Region", options=list(regions.keys()), index=0)
    region_key = regions[selected_region]
    if region_key == 'sabah':
        locations = SABAH_LOCATIONS
        st.info(f"🏝️ {len(locations)} locations in Sabah")
    elif region_key == 'sarawak':
        locations = SARAWAK_LOCATIONS
        st.info(f"🏝️ {len(locations)} locations in Sarawak")
    elif region_key == 'candidates':
        locations = STARGAZING_CANDIDATES
        st.info(f"🌟 {len(locations)} stargazing candidates")
    else:
        locations = BORNEO_LOCATIONS
        st.info(f"🌏 {len(locations)} locations across Borneo")
    return locations, region_key


def render_haze_alert_card(haze: Dict):
    """Render haze OR fog alert card — v3.2.2 distinguishes them."""
    if not haze or not haze.get('detected'):
        return
    
    severity = haze.get('severity', 'None')
    is_fog = haze.get('is_fog', False)
    
    if is_fog:
        # Blue fog alert
        color = '#00f0ff'
        icon = '🌫️'
        st.markdown(f"""
        <div class="fog-alert recommendation-container" style="border: 2px solid {color};
             background: {color}11; box-shadow: 0 0 30px {color}44;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="font-size: 3rem;">{icon}</div>
                <div style="flex: 1;">
                    <div style="color: {color}; font-family: 'Courier New', monospace;
                         font-size: 1.3rem; font-weight: 900; letter-spacing: 2px;">
                        🌫️ NATURAL FOG
                    </div>
                    <div style="color: #d0d0e8; font-family: 'Courier New', monospace;
                         font-size: 0.85rem; margin-top: 5px;">
                        Confidence: {haze.get('confidence', 'Unknown')} · {haze.get('cause', 'Unknown cause')}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        return
    
    # Standard haze alert (colors by severity)
    colors = {
        'Severe': ('#ff2d95', '🚨'),
        'Heavy': ('#ff6600', '🔥'),
        'Moderate': ('#ffe84d', '⚠️'),
        'Light': ('#00f0ff', '💨'),
    }
    color, icon = colors.get(severity, ('#8080a0', 'ℹ️'))
    
    st.markdown(f"""
    <div class="haze-alert recommendation-container" style="border: 2px solid {color};
         background: {color}11; box-shadow: 0 0 30px {color}44;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="font-size: 3rem;">{icon}</div>
            <div style="flex: 1;">
                <div style="color: {color}; font-family: 'Courier New', monospace;
                     font-size: 1.3rem; font-weight: 900; letter-spacing: 2px;">
                    HAZE ALERT: {severity.upper()}
                </div>
                <div style="color: #d0d0e8; font-family: 'Courier New', monospace;
                     font-size: 0.85rem; margin-top: 5px;">
                    Confidence: {haze.get('confidence', 'Unknown')} · {haze.get('cause', 'Unknown cause')}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        st.markdown("""
        <div style="text-align: center; padding: 10px 0;">
            <div style="font-size: 2.5rem; font-family: 'Courier New', monospace;
                 background: linear-gradient(90deg, #00f0ff, #b026ff, #ff2d95);
                 -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                 font-weight: 900; letter-spacing: 4px;">
                ASTROVIEW
            </div>
            <div style="color: #00f0ff; font-size: 0.8rem; font-family: 'Courier New', monospace;
                 letter-spacing: 6px;">
                SELECTOR v3.2.2
            </div>
            <div class="cyber-divider"></div>
        </div>
        """, unsafe_allow_html=True)
        cache_stats = api_cache.get_stats()
        st.markdown(f"""
        <div style="color: #a0a0c0; font-family: 'Courier New', monospace; font-size: 0.7rem;
             text-align: center; border: 1px solid rgba(0, 240, 255, 0.1);
             border-radius: 4px; padding: 4px 8px; margin-bottom: 10px;">
            ⚡ CACHE: {cache_stats['total_cached']} RESPONSES
        </div>
        """, unsafe_allow_html=True)
        
        moon = calculate_moon_phase()
        st.markdown(f"""
        <div style="text-align: center; padding: 10px; border: 1px solid rgba(0, 240, 255, 0.15);
             border-radius: 8px; background: rgba(0, 240, 255, 0.03); margin-bottom: 10px;">
            <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.6rem;
                 letter-spacing: 1px;">CURRENT MOON</div>
            <div style="font-size: 1.8rem;">{moon['emoji']}</div>
            <div style="color: #00f0ff; font-family: 'Courier New', monospace; font-size: 0.8rem;">
                {moon['phase_name']}
            </div>
            <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.65rem;">
                {moon['illumination_pct']}% illuminated
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        current_month = datetime.now().month
        seasonal = HAZE_SEASONAL_CALENDAR.get(current_month, HAZE_SEASONAL_CALENDAR[6])
        seasonal_risk, seasonal_source, seasonal_aqi, seasonal_note = seasonal
        
        risk_colors = {
            'Low': '#39ff14',
            'Low-Moderate': '#00f0ff',
            'Moderate': '#ffe84d',
            'High': '#ff6600',
            'Very High': '#ff2d95'
        }
        risk_color = risk_colors.get(seasonal_risk, '#8080a0')
        
        st.markdown(f"""
        <div style="text-align: center; padding: 10px; border: 1px solid {risk_color}44;
             border-radius: 8px; background: {risk_color}11; margin-bottom: 10px;">
            <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.6rem;
                 letter-spacing: 1px;">HAZE SEASON</div>
            <div style="font-size: 1.5rem;">🌫️</div>
            <div style="color: {risk_color}; font-family: 'Courier New', monospace; font-size: 0.8rem;
                 font-weight: bold;">
                {seasonal_risk} Risk
            </div>
            <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.6rem;">
                AQI {seasonal_aqi}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        st.markdown('<div style="color:#00f0ff;font-family:Courier New,monospace;letter-spacing:2px;font-size:0.9rem;margin-bottom:10px;">⚡ LOCATION SELECTOR</div>', unsafe_allow_html=True)
        locations, region = render_region_selector()
        quick_location = st.selectbox("Select Location", list(locations.keys()), index=0)
        if st.button("⚡ GO TO LOCATION", use_container_width=True):
            coords = locations[quick_location]
            st.session_state.selected_location = Location(
                lat=coords[0], lon=coords[1], name=quick_location
            )
            st.rerun()
        st.caption("Or click on the map to select any location")
        st.divider()
        st.markdown('<div style="color:#00f0ff;font-family:Courier New,monospace;letter-spacing:2px;font-size:0.9rem;margin-bottom:10px;">🗺️ MAP SETTINGS</div>', unsafe_allow_html=True)
        basemap_choice = st.radio(
            "Map Style",
            options=["🗺️ OpenStreetMap", "🛰️ Satellite"],
            index=0 if st.session_state.basemap_choice == "OpenStreetMap" else 1,
            horizontal=True,
            label_visibility="collapsed"
        )
        st.session_state.basemap_choice = "Satellite" if "Satellite" in basemap_choice else "OpenStreetMap"
        st.session_state.show_radius_circle = st.checkbox("Show Search Radius", value=True)
        st.divider()
        st.markdown('<div style="color:#00f0ff;font-family:Courier New,monospace;letter-spacing:2px;font-size:0.9rem;margin-bottom:10px;">⚙️ ANALYSIS PARAMETERS</div>', unsafe_allow_html=True)
        radius = st.slider("Assessment Radius (m)", 2000, 20000, 10000, 1000)
        st.divider()
        st.markdown('<div style="color:#00f0ff;font-family:Courier New,monospace;letter-spacing:2px;font-size:0.9rem;margin-bottom:10px;">📊 SITE RANKING</div>', unsafe_allow_html=True)
        if st.session_state.current_results:
            result_data = st.session_state.current_results
            if 'suitability_percentage' in result_data:
                pct = result_data['suitability_percentage']
                rating = result_data['rating']
                color = "#39ff14" if pct >= 80 else "#00f0ff" if pct >= 65 else "#ff2d95" if pct >= 50 else "#ff6600"
                st.markdown(f"""
                <div style="text-align: center; padding: 15px; border: 1px solid rgba(0, 240, 255, 0.2);
                     border-radius: 8px; background: rgba(0, 240, 255, 0.05);">
                    <div style="font-size: 2.5rem; font-weight: 900; color: {color};
                         font-family: 'Courier New', monospace;">{pct}%</div>
                    <div style="color: #d0d0e8; font-family: 'Courier New', monospace;
                         letter-spacing: 2px; font-size: 0.8rem;">{rating}</div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Run an analysis to see site ranking")
        if st.button("🔄 COMPARE ALL", use_container_width=True):
            st.session_state.comparison_mode = True
            st.rerun()
        if st.button("🧹 CLEAR", use_container_width=True):
            st.session_state.current_results = None
            st.session_state.reasoning_log = []
            st.session_state.candidate_scores = {}
            st.rerun()
        if st.button("🗑️ CLEAR CACHE", use_container_width=True):
            api_cache.clear()
            st.success("Cache cleared!")
            st.rerun()
        st.divider()
        st.markdown('<div style="color:#00f0ff;font-family:Courier New,monospace;letter-spacing:2px;font-size:0.9rem;margin-bottom:10px;">🧠 AGENT MEMORY</div>', unsafe_allow_html=True)
        stats = st.session_state.agent.memory_repo.get_analysis_stats()
        col1, col2 = st.columns(2)
        with col1:
            st.metric("ANALYSES", stats['total_analyses'])
        with col2:
            st.metric("SUCCESS", f"{stats['success_rate']*100:.0f}%")
        if st.button("🗑️ CLEAR MEMORY", use_container_width=True):
            Path("borneo_starview_memory.db").unlink(missing_ok=True)
            st.session_state.agent = BorneoAstroViewGeoAIAgent()
            st.session_state.analysis_history = []
            st.session_state.current_results = None
            st.session_state.reasoning_log = []
            st.rerun()
        return {'radius': radius}


def get_tiles_for_basemap(basemap_choice: str) -> str:
    if basemap_choice == "Satellite":
        return "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"
    return "OpenStreetMap"


def render_map(params: Dict):
    st.subheader("🗺️ Borneo Stargazing Site Map")
    center = [5.0, 117.0]
    location_name = "Borneo"
    if st.session_state.selected_location:
        center = [st.session_state.selected_location.lat, st.session_state.selected_location.lon]
        location_name = st.session_state.selected_location.name or "Borneo Location"

    basemap_choice = st.session_state.get('basemap_choice', 'OpenStreetMap')
    try:
        if basemap_choice == "Satellite":
            m = folium.Map(location=center, zoom_start=7,
                          tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                          attr='Esri World Imagery')
        else:
            m = folium.Map(location=center, zoom_start=7, tiles="OpenStreetMap")
    except Exception:
        m = folium.Map(location=center, zoom_start=7)

    for name, (lat, lon, radius_km, designation, desc) in PROTECTED_DARK_SKY_ZONES.items():
        folium.Circle(
            [lat, lon], radius=radius_km * 1000,
            color='#b026ff', fill=True, fillColor='#b026ff',
            fillOpacity=0.08, weight=1,
            tooltip=f"🏞️ {name} ({designation})"
        ).add_to(m)

    if st.session_state.selected_location:
        marker_color = 'purple'
        result_data = st.session_state.get('current_results', None)
        if result_data and 'suitability_percentage' in result_data:
            pct = result_data['suitability_percentage']
            if pct >= 80:
                marker_color = 'darkpurple'
            elif pct >= 65:
                marker_color = 'purple'
            elif pct >= 50:
                marker_color = 'blue'
            elif pct >= 35:
                marker_color = 'gray'
            else:
                marker_color = 'darkred'
        folium.Marker(
            center,
            popup=f"<b>🌟 {location_name}</b><br>Lat: {center[0]:.6f}<br>Lon: {center[1]:.6f}",
            tooltip="🌟 Stargazing Site",
            icon=folium.Icon(color=marker_color, icon='star', prefix='fa')
        ).add_to(m)
        if st.session_state.get('show_radius_circle', True):
            radius = params.get('radius', 10000)
            folium.Circle(center, radius=radius, color='#b026ff',
                         fill=True, fillColor='#b026ff', fillOpacity=0.1,
                         weight=2, tooltip=f"Radius: {radius}m").add_to(m)

    try:
        Fullscreen(position='topleft').add_to(m)
    except Exception:
        pass
    try:
        MiniMap(toggle_display=True, position='bottomright').add_to(m)
    except Exception:
        pass
    try:
        MousePosition(position='bottomleft', prefix='Coords: ').add_to(m)
    except Exception:
        pass

    map_data = st_folium(m, width=None, height=500, use_container_width=True)
    if map_data and map_data.get('last_clicked'):
        clicked_lat = map_data['last_clicked']['lat']
        clicked_lon = map_data['last_clicked']['lng']
        if st.session_state.selected_location is None or \
           abs(st.session_state.selected_location.lat - clicked_lat) > 0.0001 or \
           abs(st.session_state.selected_location.lon - clicked_lon) > 0.0001:
            st.session_state.selected_location = Location(lat=clicked_lat, lon=clicked_lon, name="Borneo Location")
            st.rerun()


def render_query_interface(params: Dict):
    st.subheader("💬 Natural Language Query")
    with st.expander("💡 Example Stargazing Queries", expanded=False):
        st.markdown("""
        **🌟 Stargazing Site Selection:**
        - "Find the best stargazing spot in Sabah"
        - "Which location has the darkest skies?"
        - "Where can I see the Milky Way clearly in Borneo?"

        **🌫️ Haze-Aware Queries (v3.2):**
        - "Is there haze tonight at Mount Kinabalu?"
        - "Check air quality at Bario Highlands"
        - "Is it safe for astrophotography tonight?"

        **📸 Astrophotography:**
        - "Best site for Milky Way photography"
        - "Which location is best for deep-sky imaging?"
        """)
    query = st.text_area(
        "Describe what you want to analyse for stargazing:",
        placeholder="e.g., Find the best stargazing spot in Sabah",
        height=100
    )
    col1, col2 = st.columns([1, 1])
    with col1:
        analyse_btn = st.button("🌟 ANALYSE SITE", type="primary", use_container_width=True)
    with col2:
        clear_btn = st.button("🧹 CLEAR", use_container_width=True)
    if clear_btn:
        st.session_state.current_results = None
        st.session_state.reasoning_log = []
        st.rerun()
    if analyse_btn and st.session_state.selected_location:
        with st.spinner("🌌 Analysing..."):
            progress_bar = st.progress(0)
            status_text = st.empty()
            def update_progress(progress, status):
                progress_bar.progress(progress)
                status_text.text(status)
            result = st.session_state.agent.execute_analysis(
                st.session_state.selected_location,
                query if query else "Evaluate this site for stargazing",
                params,
                progress_callback=update_progress
            )
            st.session_state.analysis_history.append(result)
            st.session_state.reasoning_log = result.steps
            st.session_state.current_results = result.final_result
            progress_bar.empty()
            status_text.empty()
            if result.success:
                st.success(f"✅ Analysis complete in {result.total_time:.2f}s")
                st.rerun()
            else:
                st.error("❌ Analysis failed. Check reasoning log.")
    elif analyse_btn:
        st.warning("Please select a location in Borneo first!")


def render_reasoning_log():
    st.subheader("🧠 Agent Reasoning")
    if not st.session_state.reasoning_log:
        st.info("Run a stargazing site analysis to see reasoning.")
        return
    for step in st.session_state.reasoning_log:
        status_icon = "✅" if step.status == "completed" else "❌" if step.status == "failed" else "⏳"
        with st.expander(f"{status_icon} Step {step.step_number}: {step.name}", expanded=False):
            st.write(f"**Reasoning:** {step.reasoning}")
            if step.execution_time > 0:
                st.write(f"**Execution Time:** {step.execution_time:.3f}s")


# ============================================================================
# EXPORT FUNCTIONALITY
# ============================================================================

def generate_export_csv(result_data: Dict) -> str:
    rows = []
    rows.append(['Category', 'Metric', 'Value'])
    rows.append(['Location', 'Name', result_data.get('location_name', 'Unknown')])
    rows.append(['Location', 'Latitude', result_data.get('lat', 0)])
    rows.append(['Location', 'Longitude', result_data.get('lon', 0)])
    rows.append(['Overall', 'Suitability %', result_data.get('suitability_percentage', 0)])
    rows.append(['Overall', 'Rating', result_data.get('rating', 'Unknown')])
    rows.append(['Overall', 'Recommendation', result_data.get('recommendation', '')])
    rows.append(['Overall', 'Base Score %', result_data.get('base_percentage', 0)])
    rows.append(['Overall', 'Penalty %', result_data.get('penalty_applied', 0)])
    
    pz = result_data.get('protected_zone')
    if pz:
        rows.append(['Protected Zone', 'Name', pz.get('name', '')])
        rows.append(['Protected Zone', 'Designation', pz.get('designation', '')])
    else:
        rows.append(['Protected Zone', 'Name', 'None'])
    
    haze = result_data.get('haze', {})
    rows.append(['Haze', 'Detected', haze.get('detected', False)])
    rows.append(['Haze', 'Is Fog', haze.get('is_fog', False)])
    rows.append(['Haze', 'Severity', haze.get('severity', 'None')])
    rows.append(['Haze', 'Confidence', haze.get('confidence', 'N/A')])
    rows.append(['Haze', 'Cause', haze.get('cause', 'N/A')])
    rows.append(['Haze', 'Seasonal Risk', haze.get('seasonal_risk', 'N/A')])
    if haze.get('pm25'):
        rows.append(['Haze', 'PM2.5 (µg/m³)', haze.get('pm25')])
    if haze.get('aqi'):
        rows.append(['Haze', 'AQI', haze.get('aqi')])
    if haze.get('health_advisory'):
        rows.append(['Haze', 'Health Advisory', haze.get('health_advisory')])
    
    details = result_data.get('details', {})
    scores = result_data.get('scores', {})
    for key, detail in details.items():
        rows.append(['Score', key.replace('_', ' ').title(), f"{scores.get(key, 0):.2f}/5"])
        rows.append(['Score Value', key.replace('_', ' ').title(), str(detail.get('value', 'N/A'))])
        rows.append(['Score Weight', key.replace('_', ' ').title(), f"{detail.get('weight', 0)*100:.0f}%"])
        rows.append(['Score Source', key.replace('_', ' ').title(), str(detail.get('source', 'Unknown'))])
    
    w = result_data.get('weather')
    if w:
        rows.append(['Weather', 'Cloud Cover %', w.get('cloud_cover_pct', 'N/A')])
        rows.append(['Weather', 'Temperature °C', w.get('temperature_c', 'N/A')])
        rows.append(['Weather', 'Humidity %', w.get('humidity_pct', 'N/A')])
        rows.append(['Weather', 'Visibility km', w.get('visibility_km', 'N/A')])
        rows.append(['Weather', 'Wind m/s', w.get('wind_speed_ms', 'N/A')])
        rows.append(['Weather', 'Dew Point °C', w.get('dew_point_c', 'N/A')])
    
    moon = result_data.get('moon_phase')
    if moon:
        rows.append(['Moon', 'Phase', moon.get('phase_name', 'Unknown')])
        rows.append(['Moon', 'Illumination %', moon.get('illumination_pct', 0)])
        rows.append(['Moon', 'Impact', moon.get('impact', '')])
    
    mw = result_data.get('milky_way')
    if mw:
        rows.append(['Milky Way', 'Visibility', mw.get('visibility', '')])
        rows.append(['Milky Way', 'Best Time', mw.get('best_time', '')])
        rows.append(['Milky Way', 'Note', mw.get('note', '')])
    
    astro = result_data.get('astrophotography_scores')
    if astro:
        for mode, data in astro.items():
            rows.append(['Astro Score', mode.replace('_', ' ').title(), f"{data['score']}% ({data['rating']})"])
    
    df = pd.DataFrame(rows, columns=['Category', 'Metric', 'Value'])
    return df.to_csv(index=False)


def generate_export_json(result_data: Dict) -> str:
    export_data = {
        'export_timestamp': datetime.now().isoformat(),
        'version': 'v3.2.2',
        'location': {
            'name': result_data.get('location_name', 'Unknown'),
            'latitude': result_data.get('lat', 0),
            'longitude': result_data.get('lon', 0),
        },
        'overall': {
            'suitability_percentage': result_data.get('suitability_percentage', 0),
            'rating': result_data.get('rating', 'Unknown'),
            'recommendation': result_data.get('recommendation', ''),
            'base_percentage': result_data.get('base_percentage', 0),
            'penalty_applied': result_data.get('penalty_applied', 0),
            'penalty_reasons': result_data.get('penalty_reasons', []),
        },
        'protected_zone': result_data.get('protected_zone'),
        'haze': result_data.get('haze'),
        'air_quality': result_data.get('air_quality'),
        'scores': {k: round(v, 2) for k, v in result_data.get('scores', {}).items()},
        'details': {},
        'weather': result_data.get('weather'),
        'moon_phase': result_data.get('moon_phase'),
        'milky_way': result_data.get('milky_way'),
        'astrophotography_scores': result_data.get('astrophotography_scores'),
        'data_sources': result_data.get('data_source_details', []),
    }
    for key, detail in result_data.get('details', {}).items():
        export_data['details'][key] = {
            'score': detail.get('score', 0),
            'value': str(detail.get('value', 'N/A')),
            'weight': detail.get('weight', 0),
            'source': detail.get('source', 'Unknown'),
        }
    return json.dumps(export_data, indent=2, default=str)


def render_export_section(result_data: Dict):
    st.write("---")
    st.write("**📊 Export Report**")
    st.caption("Download the full analysis report (includes haze & air quality data) for presentations, planning, or documentation.")
    
    location_name = result_data.get('location_name', 'Borneo_Location')
    safe_name = "".join(c for c in location_name if c.isalnum() or c in (' ', '-', '_')).replace(' ', '_')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M')
    
    col1, col2 = st.columns(2)
    with col1:
        csv_data = generate_export_csv(result_data)
        st.download_button(
            label="📥 Download CSV Report",
            data=csv_data,
            file_name=f"astroview_{safe_name}_{timestamp}.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with col2:
        json_data = generate_export_json(result_data)
        st.download_button(
            label="📥 Download JSON Report",
            data=json_data,
            file_name=f"astroview_{safe_name}_{timestamp}.json",
            mime="application/json",
            use_container_width=True,
        )


# ============================================================================
# RESULTS RENDERING
# ============================================================================

def render_results():
    st.subheader("🌟 Stargazing Site Analysis Results")
    if not st.session_state.analysis_history:
        st.info("No analysis results yet. Run a stargazing analysis.")
        return
    last_result = st.session_state.analysis_history[-1]
    if not last_result.final_result:
        st.warning("No results available.")
        return
    result_data = last_result.final_result
    if not result_data.get('success', False):
        st.error(f"Analysis failed: {result_data.get('error', 'Unknown error')}")
        return
    if 'suitability_percentage' in result_data:
        if result_data.get('protected_zone'):
            pz = result_data['protected_zone']
            st.success(f"🏞️ **Protected Dark-Sky Zone:** {pz['name']} ({pz['designation']})")

        haze = result_data.get('haze', {})
        if haze.get('detected'):
            render_haze_alert_card(haze)

        if result_data.get('used_osm', False):
            st.success("🌐 **HYBRID v3.2.2: Fog + Haze + Coastal Fix**")
        else:
            st.success("📍 **Geographic Rules v3.2.2 (INSTANT)**")

        # ============ v3.2.2: HAZE OR FOG DETAIL PANEL ============
        if haze.get('detected') or haze.get('aqi'):
            st.write("---")
            is_fog = haze.get('is_fog', False)
            if is_fog:
                st.write("**🌫️ Natural Mountain Fog Analysis**")
            else:
                st.write("**🌫️ Haze & Air Quality Analysis**")
            
            hz1, hz2, hz3 = st.columns([1.2, 1, 1])
            
            with hz1:
                sev = haze.get('severity', 'None')
                if is_fog:
                    sev_colors = {'Fog': '#00f0ff'}
                    label_prefix = "FOG"
                else:
                    sev_colors = {
                        'Severe': '#ff2d95',
                        'Heavy': '#ff6600',
                        'Moderate': '#ffe84d',
                        'Light': '#00f0ff',
                        'None': '#39ff14',
                    }
                    label_prefix = "HAZE"
                sev_color = sev_colors.get(sev, '#8080a0')
                display_icon = '🌫️' if is_fog else '🌫️'
                st.markdown(f"""
                <div style="text-align: center; padding: 15px; border: 1px solid {sev_color}66;
                     border-radius: 10px; background: {sev_color}11;">
                    <div style="font-size: 2rem;">{display_icon}</div>
                    <div style="color: {sev_color}; font-family: 'Courier New', monospace;
                         font-size: 0.9rem; font-weight: bold;">{label_prefix}: {sev.upper()}</div>
                    <div style="color: #8080a0; font-family: 'Courier New', monospace;
                         font-size: 0.65rem; margin-top: 5px;">
                        Confidence: {haze.get('confidence', 'N/A')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with hz2:
                if haze.get('pm25') is not None:
                    st.metric("PM2.5", f"{haze['pm25']:.1f} µg/m³")
                if haze.get('aqi') is not None:
                    st.metric("AQI", f"{haze['aqi']}")
            
            with hz3:
                if haze.get('pm10') is not None:
                    st.metric("PM10", f"{haze['pm10']:.1f} µg/m³")
                st.metric("Month Risk", haze.get('seasonal_risk', 'N/A'))
            
            if haze.get('health_advisory'):
                if is_fog:
                    st.success(haze['health_advisory'])
                else:
                    st.info(haze['health_advisory'])
            
            if haze.get('action_recommendation'):
                sev = haze.get('severity', 'None')
                if is_fog:
                    st.info(haze['action_recommendation'])
                elif sev in ['Heavy', 'Severe']:
                    st.error(haze['action_recommendation'])
                elif sev == 'Moderate':
                    st.warning(haze['action_recommendation'])
                else:
                    st.success(haze['action_recommendation'])
            
            if haze.get('indicators'):
                with st.expander("🔍 Detection Indicators"):
                    for ind in haze['indicators']:
                        st.write(f"• {ind}")

        moon = result_data.get('moon_phase')
        if moon:
            st.write("---")
            st.write("**🌙 Current Moon Phase**")
            moon_col1, moon_col2, moon_col3 = st.columns([1, 2, 2])
            with moon_col1:
                st.markdown(f"""
                <div style="text-align: center; padding: 15px; border: 1px solid rgba(255, 232, 77, 0.3);
                     border-radius: 10px; background: rgba(255, 232, 77, 0.05);">
                    <div style="font-size: 3rem;">{moon['emoji']}</div>
                    <div style="color: #ffe84d; font-family: 'Courier New', monospace;
                         font-size: 0.9rem; font-weight: bold;">{moon['phase_name']}</div>
                </div>
                """, unsafe_allow_html=True)
            with moon_col2:
                st.metric("Illumination", f"{moon['illumination_pct']}%")
                st.metric("Moon Age", f"{moon['age_days']} days")
            with moon_col3:
                st.metric("Viewing Impact", moon['impact_emoji'])
                st.caption(f"**{moon['impact']}**")

        mw = result_data.get('milky_way')
        if mw:
            st.write("---")
            st.write("**🌌 Milky Way Visibility**")
            mw_col1, mw_col2, mw_col3 = st.columns([1, 2, 2])
            visibility_color = {
                'Peak': '#39ff14',
                'Excellent': '#00f0ff',
                'Good': '#ffe84d',
                'Limited': '#ff6600',
                'Poor': '#ff2d95'
            }.get(mw['visibility'], '#8080a0')
            with mw_col1:
                st.markdown(f"""
                <div style="text-align: center; padding: 15px; border: 1px solid {visibility_color}66;
                     border-radius: 10px; background: {visibility_color}11;">
                    <div style="font-size: 2rem;">🌌</div>
                    <div style="color: {visibility_color}; font-family: 'Courier New', monospace;
                         font-size: 0.9rem; font-weight: bold;">{mw['visibility']}</div>
                </div>
                """, unsafe_allow_html=True)
            with mw_col2:
                st.metric("Best Viewing Time", mw['best_time'])
                st.metric("Latitude Position", mw['latitude_note'].split(' - ')[0])
            with mw_col3:
                st.info(f"📝 {mw['note']}")
                st.caption(f"**Next window:** {mw['next_window']}")

        astro = result_data.get('astrophotography_scores')
        if astro:
            st.write("---")
            st.write("**📸 Activity-Specific Scores**")
            st.caption("Different activities have different requirements. Haze affects astrophotography most.")
            
            ac1, ac2, ac3 = st.columns(3)
            with ac1:
                naked = astro['naked_eye']
                st.markdown(f"""
                <div style="text-align: center; padding: 15px; border: 1px solid rgba(0, 240, 255, 0.3);
                     border-radius: 10px; background: rgba(0, 240, 255, 0.05);">
                    <div style="font-size: 1.8rem;">👁️</div>
                    <div style="color: #00f0ff; font-family: 'Courier New', monospace;
                         font-size: 0.7rem; letter-spacing: 1px;">NAKED EYE</div>
                    <div style="font-size: 1.8rem; font-weight: 900; color: #ffffff;
                         font-family: 'Courier New', monospace;">{naked['score']}%</div>
                    <div style="color: #ffe84d; font-family: 'Courier New', monospace;
                         font-size: 0.8rem;">{naked['emoji']} {naked['rating']}</div>
                    <div style="color: #8080a0; font-family: 'Courier New', monospace;
                         font-size: 0.65rem; margin-top: 5px;">{naked['note']}</div>
                </div>
                """, unsafe_allow_html=True)
            with ac2:
                tel = astro['telescope']
                st.markdown(f"""
                <div style="text-align: center; padding: 15px; border: 1px solid rgba(176, 38, 255, 0.3);
                     border-radius: 10px; background: rgba(176, 38, 255, 0.05);">
                    <div style="font-size: 1.8rem;">🔭</div>
                    <div style="color: #b026ff; font-family: 'Courier New', monospace;
                         font-size: 0.7rem; letter-spacing: 1px;">TELESCOPE</div>
                    <div style="font-size: 1.8rem; font-weight: 900; color: #ffffff;
                         font-family: 'Courier New', monospace;">{tel['score']}%</div>
                    <div style="color: #ffe84d; font-family: 'Courier New', monospace;
                         font-size: 0.8rem;">{tel['emoji']} {tel['rating']}</div>
                    <div style="color: #8080a0; font-family: 'Courier New', monospace;
                         font-size: 0.65rem; margin-top: 5px;">{tel['note']}</div>
                </div>
                """, unsafe_allow_html=True)
            with ac3:
                photo = astro['astrophotography']
                st.markdown(f"""
                <div style="text-align: center; padding: 15px; border: 1px solid rgba(255, 45, 149, 0.3);
                     border-radius: 10px; background: rgba(255, 45, 149, 0.05);">
                    <div style="font-size: 1.8rem;">📸</div>
                    <div style="color: #ff2d95; font-family: 'Courier New', monospace;
                         font-size: 0.7rem; letter-spacing: 1px;">ASTROPHOTOGRAPHY</div>
                    <div style="font-size: 1.8rem; font-weight: 900; color: #ffffff;
                         font-family: 'Courier New', monospace;">{photo['score']}%</div>
                    <div style="color: #ffe84d; font-family: 'Courier New', monospace;
                         font-size: 0.8rem;">{photo['emoji']} {photo['rating']}</div>
                    <div style="color: #8080a0; font-family: 'Courier New', monospace;
                         font-size: 0.65rem; margin-top: 5px;">{photo['note']}</div>
                </div>
                """, unsafe_allow_html=True)

        st.write("---")
        if result_data.get('penalty_applied', 0) > 0:
            with st.expander(f"⚠️ Score Penalty: -{result_data['penalty_applied']}%"):
                st.write(f"**Base score:** {result_data.get('base_percentage', 0)}%")
                st.write(f"**Penalty:** -{result_data['penalty_applied']}%")
                st.write("**Reasons:**")
                for r in result_data.get('penalty_reasons', []):
                    st.warning(r)
                st.write(f"**Final score:** {result_data['suitability_percentage']}%")

        if 'data_source_details' in result_data:
            with st.expander("📊 Data Sources Used"):
                for detail in result_data['data_source_details']:
                    if '🏞️' in detail:
                        st.success(detail)
                    elif '🌫️' in detail:
                        st.warning(detail)
                    elif '🌐' in detail:
                        st.success(detail)
                    elif 'Air Quality' in detail:
                        st.info(f"💨 {detail}")
                    elif 'Cloud' in detail:
                        st.info(f"☁️ {detail}")
                    elif 'Light Pollution' in detail:
                        st.info(f"💡 {detail}")
                    elif 'Elevation' in detail:
                        st.info(f"⛰️ {detail}")
                    else:
                        st.info(f"📍 {detail}")

        weather = result_data.get('weather')
        if weather:
            with st.expander("🌤️ Live Weather (Open-Meteo)", expanded=False):
                wc1, wc2, wc3 = st.columns(3)
                with wc1:
                    if weather.get('cloud_cover_pct') is not None:
                        st.metric("☁️ Cloud Cover", f"{weather['cloud_cover_pct']:.0f}%",
                                  delta=weather.get('cloud_rating', ''))
                    if weather.get('temperature_c') is not None:
                        st.metric("🌡️ Temperature", f"{weather['temperature_c']:.1f}°C")
                with wc2:
                    if weather.get('humidity_pct') is not None:
                        st.metric("💧 Humidity", f"{weather['humidity_pct']:.0f}%")
                    if weather.get('visibility_km') is not None:
                        st.metric("👁️ Visibility", f"{weather['visibility_km']:.0f} km")
                with wc3:
                    if weather.get('dew_point_c') is not None:
                        st.metric("💦 Dew Point", f"{weather['dew_point_c']:.1f}°C")
                    if weather.get('wind_speed_ms') is not None:
                        st.metric("💨 Wind", f"{weather['wind_speed_ms']:.1f} m/s")
                if weather.get('cloud_explanation'):
                    st.caption(f"**Assessment:** {weather['cloud_explanation']}")

        if result_data.get('used_osm', False) and result_data.get('osm_data'):
            with st.expander("🌐 OSM Data Found"):
                st.json(result_data['osm_data'])

        c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
        with c1:
            st.metric("🌟 Stargazing Suitability", f"{result_data['suitability_percentage']}%",
                      delta=f"{result_data['rating']} {result_data['rating_emoji']}")
            st.caption(result_data['recommendation'])
        with c2:
            st.metric("Elevation", f"{result_data.get('elevation_m', 0):.0f}m")
        with c3:
            st.metric("Latitude", f"{result_data.get('lat_deg', 0):.1f}°N")
        with c4:
            cc = result_data.get('cloud_cover_pct')
            st.metric("☁️ Cloud", f"{cc:.0f}%" if cc is not None else "N/A")

        with st.expander("🔍 Why This Score? (Top Contributing Factors)", expanded=False):
            details = result_data.get('details', {})
            scores = result_data.get('scores', {})
            contributions = []
            for key, detail in details.items():
                w = detail.get('weight', 0)
                s = scores.get(key, 0)
                contributions.append({
                    'factor': key.replace('_', ' ').title(),
                    'score': s,
                    'weight': w,
                    'weighted': s * w,
                    'source': detail.get('source', 'Unknown')
                })
            contributions.sort(key=lambda x: x['weighted'], reverse=True)
            st.write("**Top positive contributors:**")
            for c in contributions[:3]:
                bar = "█" * int(c['weighted'] * 20)
                st.write(f"✅ **{c['factor']}** — Score: {c['score']:.1f}/5, Weight: {c['weight']*100:.0f}% — `{bar}` {c['weighted']:.2f}")
            st.write("**Lowest contributors:**")
            for c in contributions[-3:]:
                bar = "█" * int(c['weighted'] * 20)
                st.write(f"⚠️ **{c['factor']}** — Score: {c['score']:.1f}/5, Weight: {c['weight']*100:.0f}% — `{bar}` {c['weighted']:.2f}")

        st.write("---")
        st.write("**Detailed Scoring Breakdown:**")
        details = result_data.get('details', {})
        scores = result_data.get('scores', {})
        score_data = []
        for key, detail in details.items():
            weight = detail.get('weight', 0)
            score = scores.get(key, 0)
            weighted = score * weight
            source = detail.get('source', 'Unknown')
            if 'Protected' in source or '🏞️' in str(source):
                source_emoji = '🏞️'
            elif 'Geographic' in source:
                source_emoji = '📍'
            elif 'Live' in source:
                source_emoji = '✅'
            elif 'Open-Meteo' in source:
                source_emoji = '🌤️'
            elif 'Fallback' in source:
                source_emoji = '⚠️'
            else:
                source_emoji = 'ℹ️'
            score_data.append({
                'Criteria': key.replace('_', ' ').title(),
                'Score': f"{score:.1f}/5",
                'Value': detail.get('value', 'N/A'),
                'Weight': f"{weight*100:.0f}%",
                'Weighted': f"{weighted:.2f}",
                'Source': f"{source_emoji} {source[:40]}"
            })
        df = pd.DataFrame(score_data)
        st.dataframe(df, use_container_width=True, hide_index=True)
        chart_data = pd.DataFrame([
            {'Criteria': row['Criteria'], 'Score': float(row['Score'].split('/')[0])}
            for row in score_data
        ])
        st.bar_chart(chart_data.set_index('Criteria'))

        st.write("---")
        st.write("**📅 Best Viewing Season**")
        seasonal = get_seasonal_guidance(
            result_data.get('lat', 0),
            result_data.get('lon', 0),
            result_data.get('elevation_m', 0)
        )
        st.info(f"""
        **Region:** {seasonal['region']}

        🌟 **Best months:** {seasonal['best_months']}
        
        ✨ **Good months:** {seasonal['good_months']}
        
        ⚠️ **Avoid:** {seasonal['avoid_months']}
        
        📝 *{seasonal['notes']}*
        """)

        st.write("---")
        st.write("**🌫️ Malaysia Haze Season Calendar**")
        current_m = datetime.now().month
        month_data = []
        for m in range(1, 13):
            risk, source, aqi, desc = HAZE_SEASONAL_CALENDAR[m]
            marker = " ⬅️ NOW" if m == current_m else ""
            month_data.append({
                'Month': datetime(2024, m, 1).strftime('%b'),
                'Haze Risk': risk,
                'Source': source,
                'Typical AQI': aqi,
                'Now': marker,
            })
        df_haze = pd.DataFrame(month_data)
        st.dataframe(df_haze, use_container_width=True, hide_index=True)
        
        current_seasonal = HAZE_SEASONAL_CALENDAR[current_m]
        st.caption(f"**Current month ({datetime(2024, current_m, 1).strftime('%B')}):** "
                   f"{current_seasonal[0]} haze risk — {current_seasonal[3]}")

        st.write("---")
        st.write("**📋 Detailed Recommendation Strategy**")
        recommendations = generate_recommendation_strategy(result_data)

        risk = recommendations.get('risk_level', 'Unknown')
        risk_color = ('#ff2d95' if risk in ('High', 'Very High')
                      else '#39ff14' if risk == 'Low' else '#ffe84d')

        st.markdown(f"""
        <div class="recommendation-container">
            <div class="recommendation-title">🎯 Overall Feasibility</div>
            <div style="color: #ffffff; font-family: 'Courier New', monospace; font-size: 1.1rem; padding: 10px;">
                {recommendations.get('overall_feasibility', 'Assessment not available')}
            </div>
            <div style="display: flex; gap: 15px; margin-top: 10px; flex-wrap: wrap;">
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.8rem; border: 1px solid rgba(0,240,255,0.1); padding: 8px 15px; border-radius: 8px;">
                    💰 Investment: <span style="color: #00f0ff; font-weight: bold;">{recommendations.get('investment_required', 'Unknown')}</span>
                </div>
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.8rem; border: 1px solid rgba(255,45,149,0.3); padding: 8px 15px; border-radius: 8px;">
                    ⚠️ Risk: <span style="color: {risk_color}; font-weight: bold;">{risk}</span>
                </div>
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.8rem; border: 1px solid rgba(255,45,149,0.3); padding: 8px 15px; border-radius: 8px;">
                    🚨 Critical: <span style="color: #ff2d95; font-weight: bold;">{recommendations.get('critical_action_count', 0)}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if recommendations['immediate_actions']:
            st.markdown('<div class="recommendation-container"><div class="recommendation-title">🔴 IMMEDIATE ACTIONS (0-6 Months)</div>', unsafe_allow_html=True)
            for action in recommendations['immediate_actions']:
                st.markdown(f"""
                <div class="recommendation-item">
                    <span class="icon">{action.get('priority', '')}</span>
                    {action['text']}
                    <span style="float: right; color: #8080a0; font-size: 0.8rem;">{action.get('cost', '')}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        if recommendations['short_term_actions']:
            st.markdown('<div class="recommendation-container"><div class="recommendation-title">🟡 SHORT-TERM ACTIONS (6-18 Months)</div>', unsafe_allow_html=True)
            for action in recommendations['short_term_actions']:
                st.markdown(f"""
                <div class="recommendation-item">
                    <span class="icon">{action.get('priority', '')}</span>
                    {action['text']}
                    <span style="float: right; color: #8080a0; font-size: 0.8rem;">{action.get('cost', '')}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        if recommendations['long_term_actions']:
            st.markdown('<div class="recommendation-container"><div class="recommendation-title">🟢 LONG-TERM ACTIONS (18-36 Months)</div>', unsafe_allow_html=True)
            for action in recommendations['long_term_actions']:
                st.markdown(f"""
                <div class="recommendation-item">
                    <span class="icon">{action.get('priority', '')}</span>
                    {action['text']}
                    <span style="float: right; color: #8080a0; font-size: 0.8rem;">{action.get('cost', '')}</span>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

        render_export_section(result_data)


def render_comparison_mode():
    st.subheader("🔄 Stargazing Site Comparison Dashboard")
    with st.spinner("Analysing all candidate sites..."):
        results = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        for i, (name, coords) in enumerate(STARGAZING_CANDIDATES.items()):
            status_text.text(f"Analysing: {name}")
            progress_bar.progress((i + 1) / len(STARGAZING_CANDIDATES))
            location = Location(lat=coords[0], lon=coords[1], name=name)
            params = {'radius': 10000}
            try:
                strategy = StrategySelector.get_strategy('stargazing')
                result = strategy.analyse(location, params)
                if result.get('success'):
                    moon = calculate_moon_phase()
                    astro = calculate_astrophotography_scores(result, moon)
                    mw = get_milky_way_visibility(coords[0], coords[1])
                    haze = result.get('haze', {})
                    is_fog = haze.get('is_fog', False)
                    haze_label = '🌫️ Fog' if is_fog else haze.get('severity', 'None')
                    results.append({
                        'Site': name,
                        'Suitability %': result['suitability_percentage'],
                        'Rating': result['rating'],
                        'Elevation (m)': result.get('elevation_m', 0),
                        'Light Pollution': result.get('light_pollution_index', 0),
                        'Cloud Risk': result.get('cloud_risk', 'Unknown'),
                        'Haze': haze_label,
                        'AstroPhoto %': astro['astrophotography']['score'],
                        'Protected': '🏞️' if result.get('protected_zone') else '',
                    })
            except Exception as e:
                results.append({
                    'Site': name, 'Suitability %': 0, 'Rating': 'Error',
                    'Elevation (m)': 0, 'Light Pollution': 0, 'Cloud Risk': 'Unknown',
                    'Haze': 'N/A', 'AstroPhoto %': 0, 'Protected': '',
                })
        progress_bar.empty()
        status_text.empty()
        if results:
            df = pd.DataFrame(results)
            df_sorted = df.sort_values('Suitability %', ascending=False)
            st.write(f"**📊 Comparison of {len(results)} Sites**")
            top_site = df_sorted.iloc[0]
            st.success(f"🌟 **Top Recommended: {top_site['Site']}** ({top_site['Suitability %']:.1f}%)")
            display_cols = ['Site', 'Suitability %', 'Rating', 'Elevation (m)', 'Light Pollution', 'Haze', 'Cloud Risk', 'AstroPhoto %', 'Protected']
            st.dataframe(df_sorted[display_cols], use_container_width=True, hide_index=True)
            chart_data = df_sorted[['Site', 'Suitability %']].set_index('Site')
            st.bar_chart(chart_data)

            basemap_choice = st.session_state.get('basemap_choice', 'OpenStreetMap')
            if basemap_choice == "Satellite":
                m = folium.Map(location=[5.0, 117.0], zoom_start=7,
                              tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                              attr='Esri World Imagery')
            else:
                m = folium.Map(location=[5.0, 117.0], zoom_start=7, tiles="OpenStreetMap")

            for _, row in df.iterrows():
                score = row['Suitability %']
                if score >= 80:
                    color = 'darkpurple'
                elif score >= 65:
                    color = 'purple'
                elif score >= 50:
                    color = 'blue'
                elif score >= 35:
                    color = 'gray'
                else:
                    color = 'darkred'
                coords = STARGAZING_CANDIDATES.get(row['Site'], (0, 0))
                folium.Marker(
                    coords,
                    popup=f"<b>{row['Site']}</b><br>Score: {score:.1f}%<br>Rating: {row['Rating']}<br>Haze: {row['Haze']}<br>AstroPhoto: {row['AstroPhoto %']}%",
                    tooltip=f"{row['Site']}: {score:.1f}%",
                    icon=folium.Icon(color=color, icon='star', prefix='fa')
                ).add_to(m)
            try:
                Fullscreen(position='topleft').add_to(m)
            except Exception:
                pass
            st_folium(m, width=None, height=400, use_container_width=True)

            timestamp = datetime.now().strftime('%Y%m%d_%H%M')
            st.download_button(
                label="📥 Download Comparison CSV",
                data=df_sorted[display_cols].to_csv(index=False),
                file_name=f"astroview_comparison_{timestamp}.csv",
                mime="text/csv",
                use_container_width=True,
            )

            selected_site = st.selectbox("Select a site for detailed analysis:", df_sorted['Site'].tolist())
            if selected_site:
                coords = STARGAZING_CANDIDATES[selected_site]
                st.session_state.selected_location = Location(
                    lat=coords[0], lon=coords[1], name=selected_site
                )
                st.session_state.comparison_mode = False
                st.rerun()


def render_memory_explorer():
    st.subheader("💾 Memory Explorer")
    tab1, tab2 = st.tabs(["Past Analyses", "Learned Parameters"])
    with tab1:
        all_analyses = st.session_state.agent.memory_repo.get_all_analyses(limit=20)
        if all_analyses:
            st.write(f"**{len(all_analyses)} past analyses**")
            for entry in all_analyses:
                query_preview = entry['query'][:50] + "..." if len(entry['query']) > 50 else entry['query']
                with st.expander(f"{'✅' if entry['success'] else '❌'} {query_preview}", expanded=False):
                    st.write(f"**Query:** {entry['query']}")
                    st.write(f"**Time:** {entry['execution_time']:.2f}s")
                    st.write(f"**Timestamp:** {entry['timestamp']}")
        else:
            st.info("No past analyses yet.")
    with tab2:
        try:
            conn = sqlite3.connect("borneo_starview_memory.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM learned_parameters ORDER BY success_rate DESC")
            rows = cursor.fetchall()
            conn.close()
            if rows:
                df = pd.DataFrame(rows, columns=['ID', 'Analysis Type', 'Parameter', 'Value', 'Success Rate', 'Usage Count', 'Last Updated'])
                st.dataframe(df[['Analysis Type', 'Parameter', 'Value', 'Success Rate', 'Usage Count']], use_container_width=True)
            else:
                st.info("No learned parameters yet.")
        except Exception:
            st.info("No learned parameters yet.")


def main():
    st.set_page_config(page_title="Borneo AstroView v3.2.2", page_icon="🌌", layout="wide")
    st.markdown(CYBERPUNK_CSS, unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align: center; padding: 20px 0 10px 0;">
        <div class="main-title">🌌 BORNEO ASTROVIEW</div>
        <div class="subtitle">SABAH &amp; SARAWAK · STARGAZING SITE SELECTOR v3.2.2</div>
        <div class="cyber-divider"></div>
        <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.7rem;
             letter-spacing: 4px; margin-top: 5px;">
            🌫️ FOG DETECTION · 💨 AIR QUALITY · 🏞️ PROTECTED ZONES · 🌙 MOON · 🌌 MILKY WAY · 📊 EXPORT
        </div>
    </div>
    """, unsafe_allow_html=True)
    init_session_state()
    total_locations = len(SABAH_LOCATIONS) + len(SARAWAK_LOCATIONS)
    st.markdown(f"""
    <div style="display: flex; justify-content: space-between; padding: 8px 15px;
         border: 1px solid rgba(0, 240, 255, 0.1); border-radius: 8px;
         background: rgba(0, 240, 255, 0.03); margin-bottom: 15px; flex-wrap: wrap; gap: 10px;">
        <span style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.7rem;">
            📍 LOCATIONS: <span style="color: #00f0ff; font-weight: bold;">{total_locations}</span>
        </span>
        <span style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.7rem;">
            🏞️ PROTECTED: <span style="color: #b026ff; font-weight: bold;">{len(PROTECTED_DARK_SKY_ZONES)}</span>
        </span>
        <span style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.7rem;">
            🌟 CANDIDATES: <span style="color: #39ff14; font-weight: bold;">{len(STARGAZING_CANDIDATES)}</span>
        </span>
        <span style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.7rem;">
            🌫️ NEW: <span style="color: #00f0ff; font-weight: bold;">v3.2.2 Fog Detection</span>
        </span>
    </div>
    """, unsafe_allow_html=True)

    if st.session_state.get('comparison_mode', False):
        render_comparison_mode()
        if st.button("← BACK TO SINGLE SITE"):
            st.session_state.comparison_mode = False
            st.rerun()
        return

    params = render_sidebar()
    col1, col2 = st.columns([1.5, 1])
    with col1:
        render_map(params)
        render_query_interface(params)
    with col2:
        if st.session_state.selected_location:
            name = st.session_state.selected_location.name or "Borneo Location"
            st.markdown(f"""
            <div style="padding: 10px 15px; border: 1px solid rgba(0, 240, 255, 0.15);
                 border-radius: 8px; background: rgba(0, 240, 255, 0.03); margin-bottom: 15px;">
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.6rem;">
                    SELECTED LOCATION</div>
                <div style="color: #00f0ff; font-family: 'Courier New', monospace; font-size: 0.9rem;">
                    {name}</div>
                <div style="color: #8080a0; font-family: 'Courier New', monospace; font-size: 0.6rem;">
                    {st.session_state.selected_location.lat:.4f}, {st.session_state.selected_location.lon:.4f}</div>
            </div>
            """, unsafe_allow_html=True)
        render_reasoning_log()
    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        render_results()
    with col2:
        render_memory_explorer()
    st.markdown("""
    <div class="cyber-divider"></div>
    <div style="text-align: center; padding: 15px 0; color: #333; font-family: 'Courier New', monospace;
         font-size: 0.6rem; letter-spacing: 2px;">
        <span style="color: #00f0ff;">[</span>
        BORNEO ASTROVIEW v3.2.2 · FOG DETECTION EDITION
        <span style="color: #00f0ff;">]</span>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()