import math
from io import StringIO

import pandas as pd
import streamlit as st

# ============================================================
# ROBO LAB | Robot Design & Engineering Simulator
# Single-file Streamlit app for GitHub + Streamlit Cloud
# ============================================================

st.set_page_config(
    page_title="ROBO LAB | Robot Engineering Simulator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Styling ----------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');
    :root { --ink:#eaf4ff; --muted:#9bb1c8; --blue:#5c8dff; --cyan:#54f0dc; --panel:#0e1b2c; --line:#25435d; }
    .stApp { background: radial-gradient(ellipse at 50% -12%, #183a59 0%, #0a1422 45%, #060b13 100%); color:var(--ink); }
    html, body, [class*="css"] { font-family:'Space Grotesk', sans-serif; }
    .block-container { padding-top:1.35rem; padding-bottom:3rem; max-width:1450px; }
    [data-testid="stSidebar"] { background:linear-gradient(180deg,#091321 0%,#0d1b2b 100%); border-right:1px solid #203d55; }
    [data-testid="stSidebar"] * { color:#eaf4ff; }
    h1,h2,h3 { letter-spacing:-.035em; }
    .hero { position:relative; overflow:hidden; padding:1.8rem 2rem; border-radius:22px; color:white; border:1px solid #2c5877; background:linear-gradient(115deg,rgba(13,29,47,.97) 0%,rgba(20,54,79,.96) 58%,rgba(31,78,105,.94) 100%); box-shadow:0 18px 48px rgba(0,0,0,.22); margin-bottom:1.35rem; }
    .hero:after { content:'ROBOTICS // SYSTEM ONLINE'; position:absolute; right:22px; bottom:18px; color:rgba(111,244,226,.52); font:10px 'DM Mono',monospace; letter-spacing:.13em; }
    .hero-kicker,.section-label { color:#54f0dc; font-family:'DM Mono',monospace; letter-spacing:.15em; font-size:.74rem; font-weight:600; }
    .hero h1 { font-size:clamp(2.1rem,4vw,3.25rem); line-height:1.05; margin:.45rem 0; color:white; font-weight:700; }
    .hero p { color:#bfd5e9; margin:0; }
    .metric-card { background:linear-gradient(145deg,rgba(17,38,57,.96),rgba(10,24,38,.96)); border:1px solid #2b526c; border-radius:16px; padding:1rem 1.1rem; min-height:118px; box-shadow:inset 0 1px rgba(255,255,255,.025),0 8px 22px rgba(0,0,0,.13); }
    .metric-label { color:#a5bfd3; font-size:.82rem; margin-bottom:.5rem; }
    .metric-value { color:#f0fbff; font-size:1.7rem; font-weight:700; line-height:1.1; }
    .metric-unit { color:#7ce8dc; font-size:.82rem; margin-top:.35rem; }
    .panel { background:rgba(13,29,45,.8); border:1px solid #25435d; border-radius:18px; padding:1.2rem 1.3rem; margin-bottom:1rem; }
    .tag { display:inline-block; padding:.28rem .65rem; border-radius:999px; background:#123d4d; color:#7ef6e5; font-size:.75rem; font-weight:600; }
    .small-note { color:#a3b9ce; font-size:.82rem; }
    div[data-testid="stMetric"] { background:rgba(13,29,45,.9); border:1px solid #25435d; padding:1rem; border-radius:15px; }
    div[data-testid="stMetric"] label, div[data-testid="stMetric"] [data-testid="stMetricValue"] { color:#edf8ff; }
    div.stButton > button, div.stDownloadButton > button { border-radius:11px; font-weight:600; border:1px solid #2d657c; }
    div.stButton > button[kind="primary"] { background:linear-gradient(100deg,#147b91,#2868c9); color:white; }
    div[data-testid="stExpander"] { border:1px solid #25435d; border-radius:14px; background:rgba(11,25,40,.7); }
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div { background:#102337; border-color:#31516a; }
    div[data-testid="stSlider"] [data-baseweb="slider"] { padding-top:.25rem; }
    [data-testid="stMarkdownContainer"] p, [data-testid="stMarkdownContainer"] li { color:inherit; }
    .stTabs [data-baseweb="tab-list"] { gap:8px; }
    .stTabs [data-baseweb="tab"] { background:#102338; border-radius:9px 9px 0 0; }
    .stAlert { border-radius:12px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------- Engineering model ----------
G = 9.81
AIR_DENSITY = 1.225


def estimate_robot(
    mass_kg: float,
    motor_power_w: float,
    wheel_radius_cm: float,
    battery_ah: float,
    battery_voltage_v: float,
    drive_type: str,
    motor_rpm: float,
    gear_ratio: float,
    drivetrain_efficiency_pct: float,
    rolling_resistance: float,
    slope_deg: float,
    frontal_area_m2: float,
    drag_coefficient: float,
) -> dict:
    """Simplified engineering estimate; not a substitute for measured motor curves."""
    radius = max(wheel_radius_cm / 100.0, 0.001)
    efficiency = drivetrain_efficiency_pct / 100.0
    driven_wheels = 2 if drive_type == "2륜 구동" else 4

    # Wheel speed from motor RPM and reduction ratio.
    wheel_rpm = motor_rpm / max(gear_ratio, 0.01)
    rotational_speed_mps = (wheel_rpm / 60.0) * (2 * math.pi * radius)

    # Approximate total output torque from total motor power and motor angular velocity.
    motor_omega = max(motor_rpm * 2 * math.pi / 60.0, 0.1)
    total_motor_torque_nm = motor_power_w / motor_omega
    total_wheel_torque_nm = total_motor_torque_nm * gear_ratio * efficiency
    torque_force_n = total_wheel_torque_nm / radius

    # Estimate a usable steady speed by balancing power with rolling + grade + aerodynamic drag.
    slope_rad = math.radians(slope_deg)
    base_resistance_n = mass_kg * G * (
