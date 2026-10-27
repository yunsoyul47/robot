import math
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# =========================================================
# ROBO LAB | Robot Design Studio
# =========================================================

st.set_page_config(
    page_title="ROBO LAB | Robot Design Studio",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# CSS
# ---------------------------------------------------------

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
    --ink: #edf4ff;
    --muted: #b9c8dc;
    --line: #293b53;
    --blue: #6ba8ff;
    --cyan: #65e2d1;
}

.stApp {
    background: radial-gradient(ellipse at 10% 0%, #162b47 0%, #0b1220 43%, #080d16 100%);
    color: var(--ink);
}

html, body, [class*="css"] {
    font-family: 'Manrope', sans-serif;
}

[data-testid="stSidebar"] {
    background: #0c1421;
    border-right: 1px solid #26354a;
}

[data-testid="stSidebar"] * {
    color: #edf4ff;
}

h1, h2, h3 {
    color: #ffffff !important;
    font-weight: 800 !important;
    letter-spacing: -0.035em;
}

.hero {
    padding: 24px 26px;
    border: 1px solid #2b4260;
    border-radius: 20px;
    background: linear-gradient(120deg, #1c3553, #0e1929);
    margin-bottom: 24px;
}

.hero-title {
    font-size: clamp(32px, 4vw, 52px);
    line-height: 1.1;
    font-weight: 800;
    color: #f2f7ff;
    margin: 8px 0;
}

.hero-sub {
    color: #d9e5f5;
    font-size: 14px;
    line-height: 1.8;
}

.eyebrow, .section-kicker {
    font-family: 'DM Mono', monospace;
    color: #65e2d1;
    font-size: 11px;
    letter-spacing: 1.7px;
}

.status-pill {
    display: inline-block;
    padding: 6px 10px;
    border-radius: 999px;
    border: 1px solid #285c59;
    background: #102e30;
    color: #80f0df;
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 1px;
}

div[data-testid="stMetric"] {
    background: rgba(18, 28, 43, .92);
    border: 1px solid #30435c;
    padding: 15px;
    border-radius: 14px;
}

div[data-testid="stMetricLabel"],
div[data-testid="stMetricLabel"] p {
    color: #d5e2f3 !important;
}

div[data-testid="stMetricValue"] {
    color: #ffffff !important;
}

[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label {
    color: #e2eaf6 !important;
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: #e7eef9;
    opacity: 1;
}

[data-testid="stAlert"] {
    background: #142b46 !important;
    border: 1px solid #42658b !important;
}

[data-testid="stAlert"] p,
[data-testid="stAlert"] span,
[data-testid="stAlert"] div {
    color: #ffffff !important;
    opacity: 1 !important;
    font-weight: 600 !important;
}

.stButton > button {
    border-radius: 10px;
    font-weight: 700;
    min-height: 42px;
}

[data-testid="stDownloadButton"] button {
    background: #eaf2ff !important;
    color: #102033 !important;
    border: 1px solid #8ba6c8 !important;
    font-weight: 800 !important;
    opacity: 1 !important;
}

[data-testid="stDownloadButton"] button p,
[data-testid="stDownloadButton"] button span,
[data-testid="stDownloadButton"] button svg {
    color: #102033 !important;
    fill: #102033 !important;
    -webkit-text-fill-color: #102033 !important;
    opacity: 1 !important;
    font-weight: 800 !important;
}

[data-testid="stDownloadButton"] button:hover {
    background: #65e2d1 !important;
}

/* Selectbox 스타일 수정 (드롭다운 배경 dark화 및 텍스트 흰색 가독성 확보) */
div[data-baseweb="select"] > div {
    background-color: #162b47 !important;
    border: 1px solid #293b53 !important;
    color: #ffffff !important;
}

div[data-baseweb="select"] span {
    color: #ffffff !important;
    font-weight: 600 !important;
}

div[data-baseweb="select"] svg {
    fill: #ffffff !important;
}

hr {
    border-color: #293b53;
}

.footer {
    color: #a9bad0;
    font-size: 11px;
    text-align: center;
    padding: 24px 0 10px;
}
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# PHYSICS CALCULATION
# ---------------------------------------------------------

def calculate_robot(
    mass,
    payload,
    motor_w,
    motor_count,
    motor_rpm,
    gear_ratio,
    wheel_radius_cm,
    battery_v,
    battery_ah,
    efficiency,
    rolling_coeff,
    slope_deg,
):
    mass = max(0.1, float(mass))
    payload = max(0, float(payload))
    total_mass = mass + payload

    motor_count = max(1, int(motor_count))
    motor_w = max(0, float(motor_w))
    motor_rpm = max(0, float(motor_rpm))
    gear_ratio = max(0.1, float(gear_ratio))

    radius = max(0.01, float(wheel_radius_cm) / 100)
    eta = max(0.05, min(1.0, float(efficiency) / 100))

    total_power = motor_w * motor_count

    wheel_rpm = motor_rpm / gear_ratio
    wheel_omega = wheel_rpm * 2 * math.pi / 60
    ideal_speed = wheel_omega * radius

    motor_omega = motor_rpm * 2 * math.pi / 60

    if motor_omega > 0:
        motor_torque = motor_w * eta / motor_omega
    else:
        motor_torque = 0

    wheel_torque = motor_torque * gear_ratio
    total_torque = wheel_torque * motor_count
    traction_force = total_torque / radius

    gravity = 9.81
    theta = math.radians(max(0, min(45, float(slope_deg))))

    rolling_force = (
        float(rolling_coeff) * total_mass * gravity * math.cos(theta)
    )

    slope_force = total_mass * gravity * math.sin(theta)
    resistance = max(0, rolling_force + slope_force)

    net_force = max(0, traction_force - resistance)
    acceleration = net_force / total_mass

    if resistance > 0.01:
        power_limited_speed = total_power * eta / resistance
        estimated_speed = min(ideal_speed, power_limited_speed)
    else:
        estimated_speed = ideal_speed

    battery_wh = float(battery_v) * float(battery_ah)
    usable_wh = battery_wh * 0.85

    average_power = max(1, total_power * 0.65 / eta)

    runtime_hours = usable_wh / average_power
    runtime_minutes = runtime_hours * 60
    range_km = estimated_speed * runtime_hours * 3.6

    return {
        "total_mass": total_mass,
        "total_power": total_power,
        "wheel_rpm": wheel_rpm,
        "ideal_speed": ideal_speed,
        "speed_kmh": estimated_speed * 3.6,
        "wheel_torque": wheel_torque,
        "traction_force": traction_force,
        "resistance": resistance,
        "net_force": net_force,
        "acceleration": acceleration,
        "battery_wh": battery_wh,
        "runtime_minutes": runtime_minutes,
        "range_km": range_km,
        "rolling_force": rolling_force,
        "slope_force": slope_force,
    }


# ---------------------------------------------------------
# ANIMATED ROBOT PREVIEW
# ---------------------------------------------------------

def robot_svg(wheel_radius_cm, mass, motor_count, speed_kmh, acceleration):
    wheel_r = max(12, min(25, wheel_radius_cm * 1.2))

    speed = max(0.0, float(speed_kmh))
    accel = max(0.0, float(acceleration))

    if speed < 0.05:
        drive_duration = 0
        wheel_duration = 0
        drive_style = "none"
        wheel_style = "none"
        movement_label = "STATIONARY"
    else:
        drive_duration = max(2.0, min(12.0, 12.0 / max(0.5, speed / 2)))
        wheel_duration = max(0.18, min(2.0, 5.0 / max(1.0, speed)))
        drive_style = f"drive {drive_duration:.2f}s ease-in-out infinite"
        wheel_style = f"spin {wheel_duration:.2f}s linear infinite"
        movement_label = "MOVING"

    accel_factor = min(1.0, accel / 5.0)
    ease_x1 = 0.05 + 0.25 * accel_factor
    ease_x2 = 0.55 + 0.40 * accel_factor
    easing = f"cubic-bezier({ease_x1:.2f}, 0.10, {ease_x2:.2f}, 1)"

    if speed >= 0.05:
        drive_style = f"drive {drive_duration:.2f}s {easing} infinite"

    pulse_duration = max(0.35, 1.8 - min(accel, 5.0) * 0.22)

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        * {{
            box-sizing: border-box;
        }}

        html, body {{
            margin: 0;
            padding: 0;
            background: transparent;
            overflow: hidden;
            font-family: Arial, sans-serif;
        }}

        .wrap {{
            width: 100%;
            min-height: 270px;
            overflow: hidden;
            border: 1px solid #293b53;
            border-radius: 18px;
            background:
                radial-gradient(ellipse at 50%
