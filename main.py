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

/* 위젯 라벨 (설계 목표 등) */
[data-testid="stWidgetLabel"] p,
[data-testid="stWidgetLabel"] label {
    color: #65e2d1 !important;
    font-weight: 700 !important;
}

[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li {
    color: #e7eef9;
    opacity: 1;
}

/* 사이드바 제목 보정 */
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] strong,
[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] b {
    color: #65e2d1 !important;
    font-size: 16px !important;
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

/* ---------------------------------------------------------
   선택창 (Selectbox) 및 드래그 영역 민트색 강화 CSS
--------------------------------------------------------- */

/* 선택창 최외각 컨테이너 */
div[data-baseweb="select"] {
    background-color: #162b47 !important;
    border-radius: 8px !important;
}

/* 선택창 내부 입력영역 전체 */
div[data-baseweb="select"] > div {
    background-color: #162b47 !important;
    border: 1.5px solid #65e2d1 !important;
    border-radius: 8px !important;
}

/* 선택창 텍스트 (범용 이동 로봇 등) - 강제 민트색 및 흰색 배경 제거 */
div[data-baseweb="select"] * {
    background-color: transparent !important;
    color: #65e2d1 !important;
    -webkit-text-fill-color: #65e2d1 !important;
    font-weight: 700 !important;
}

/* 드래그/선택 하이라이트 영역 민트색 커스텀 */
div[data-baseweb="select"] *::selection {
    background-color: #102e30 !important;
    color: #65e2d1 !important;
}

/* 드롭다운 아이콘 (화살표) */
div[data-baseweb="select"] svg {
    fill: #65e2d1 !important;
    color: #65e2d1 !important;
}

/* 클릭 시 열리는 옵션 메뉴 팝업 */
ul[data-baseweb="menu"] {
    background-color: #101c2e !important;
    border: 1px solid #65e2d1 !important;
}

ul[data-baseweb="menu"] * {
    color: #65e2d1 !important;
    -webkit-text-fill-color: #65e2d1 !important;
    font-weight: 600 !important;
}

ul[data-baseweb="menu"] li:hover {
    background-color: #162b47 !important;
}

/* 텍스트 입력창 (stTextInput) 스타일 */
div[data-testid="stTextInput"] input {
    background-color: #162b47 !important;
    color: #ffffff !important;
    border: 1px solid #365378 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}

/* 익스팬더 (stExpander) 헤더 스타일 */
div[data-testid="stExpander"] {
    background-color: #101c2e !important;
    border: 1px solid #293b53 !important;
    border-radius: 12px !important;
}

div[data-testid="stExpander"] summary {
    background-color: #162a42 !important;
    color: #65e2d1 !important;
    border-radius: 10px !important;
}

div[data-testid="stExpander"] summary p,
div[data-testid="stExpander"] summary span,
div[data-testid="stExpander"] summary svg {
    color: #65e2d1 !important;
    fill: #65e2d1 !important;
    font-weight: 700 !important;
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
                radial-gradient(ellipse at 50% 75%, #1c3550 0%, transparent 65%),
                linear-gradient(145deg, #101c2d, #0b1320);
            padding: 8px 10px 10px;
        }}

        .topline {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            gap: 8px;
            font-family: monospace;
            font-size: 10px;
            letter-spacing: 1.3px;
            color: #65e2d1;
            padding: 3px 5px 0;
        }}

        .top-right {{
            display: flex;
            align-items: center;
            gap: 7px;
        }}

        .status {{
            color: #e8f2ff;
            background: #152b40;
            border: 1px solid #365775;
            border-radius: 999px;
            padding: 4px 8px;
            font-size: 9px;
            white-space: nowrap;
        }}

        .control-btn {{
            border: 1px solid #4a6a8b;
            background: #1a3049;
            color: #ffffff;
            border-radius: 7px;
            padding: 6px 10px;
            font-size: 10px;
            font-weight: 700;
            cursor: pointer;
            white-space: nowrap;
        }}

        .control-btn:hover {{
            background: #25486a;
            border-color: #65e2d1;
        }}

        svg {{
            display: block;
            width: 100%;
            height: auto;
            max-height: 220px;
        }}

        #robot {{
            transform-box: view-box;
            transform-origin: center;
            animation: {drive_style};
        }}

        .wheel {{
            transform-box: fill-box;
            transform-origin: center;
            animation: {wheel_style};
        }}

        .sensor {{
            animation: sensorPulse {pulse_duration:.2f}s ease-in-out infinite alternate;
        }}

        .floorGlow {{
            animation: floorPulse 2.5s ease-in-out infinite alternate;
        }}

        @keyframes drive {{
            0%   {{ transform: translateX(-115px) translateY(0px); }}
            10%  {{ transform: translateX(-92px) translateY(-1px); }}
            25%  {{ transform: translateX(-45px) translateY(0px); }}
            50%  {{ transform: translateX(115px) translateY(0px); }}
            65%  {{ transform: translateX(70px) translateY(-1px); }}
            85%  {{ transform: translateX(-45px) translateY(0px); }}
            100% {{ transform: translateX(-115px) translateY(0px); }}
        }}

        @keyframes spin {{
            from {{ transform: rotate(0deg); }}
            to   {{ transform: rotate(360deg); }}
        }}

        @keyframes sensorPulse {{
            from {{ opacity: .55; }}
            to   {{ opacity: 1; }}
        }}

        @keyframes floorPulse {{
            from {{ opacity: .35; }}
            to   {{ opacity: .75; }}
        }}

        .paused #robot,
        .paused .wheel,
        .paused .sensor,
        .paused .floorGlow {{
            animation-play-state: paused !important;
        }}

        @media (prefers-reduced-motion: reduce) {{
            #robot, .wheel, .sensor, .floorGlow {{
                animation: none !important;
            }}
        }}
    </style>
    </head>

    <body>
    <div class="wrap" id="preview">
      <div class="topline">
        <span>DESIGN PREVIEW / LIVE MODEL</span>

        <div class="top-right">
          <span class="status" id="status">{movement_label}</span>
          <button class="control-btn" id="toggleBtn" type="button">
            ❚❚ 멈춤
          </button>
        </div>
      </div>

      <svg viewBox="0 0 420 250"
           xmlns="http://www.w3.org/2000/svg"
           role="img"
           aria-label="속도와 가속도에 반응하는 로봇 개념도">

        <defs>
          <linearGradient id="bodyGrad" x1="0" y1="0" x2="1" y2="1">
            <stop offset="0%" stop-color="#6ba8ff"/>
            <stop offset="100%" stop-color="#244c7a"/>
          </linearGradient>

          <linearGradient id="floorGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="0%" stop-color="#263c58" stop-opacity=".8"/>
            <stop offset="100%" stop-color="#0b1421" stop-opacity="0"/>
          </linearGradient>

          <filter id="glow">
            <feGaussianBlur stdDeviation="4" result="blur"/>
            <feMerge>
              <feMergeNode in="blur"/>
              <feMergeNode in="SourceGraphic"/>
            </feMerge>
          </filter>
        </defs>

        <ellipse class="floorGlow"
                 cx="210" cy="184" rx="148" ry="25"
                 fill="url(#floorGrad)"/>

        <g id="robot">

          <!-- Chassis -->
          <path d="M78 137 L122 104 L300 104 L345 137
                   L302 161 L120 161 Z"
                fill="#17263a"
                stroke="#45617f"
                stroke-width="2"/>

          <path d="M122 104 L300 104 L330 125 L100 125 Z"
                fill="#29415f"
                stroke="#547397"
                stroke-width="1.5"/>

          <path d="M100 125 L330 125 L302 151 L120 151 Z"
                fill="url(#bodyGrad)"
                stroke="#7cb5ff"
                stroke-width="1.5"/>

          <!-- Top panel -->
          <path d="M155 91 L180 76 L260 76 L286 91
                   L270 105 L170 105 Z"
                fill="#1d3048"
                stroke="#6ba8ff"
                stroke-width="1.5"/>

          <!-- Battery indicator -->
          <rect x="188" y="84" width="44" height="12" rx="3"
                fill="#101a28" stroke="#91b8e8" stroke-width="1"/>

          <rect x="192" y="87" width="27" height="6" rx="2"
                fill="#65e2d1"/>

          <!-- Sensor -->
          <g class="sensor" filter="url(#glow)">
            <rect x="187" y="63" width="46" height="17" rx="5"
                  fill="#65e2d1"/>
            <circle cx="210" cy="61" r="7"
                    fill="#65e2d1"
                    stroke="#b7fff4"
                    stroke-width="2"/>
          </g>

          <!-- Sensor rays -->
          <g stroke="#65e2d1" stroke-width="1.5"
             stroke-linecap="round" opacity=".8">
            <path d="M210 51 V42"/>
            <path d="M201 46 L196 41"/>
            <path d="M219 46 L224 41"/>
          </g>

          <!-- Left wheel -->
          <g class="wheel">
            <circle cx="124" cy="155" r="{wheel_r+4}"
                    fill="#050a11"
                    stroke="#52657d"
                    stroke-width="2"/>
            <circle cx="124" cy="155" r="{wheel_r-3}"
                    fill="#1b2b40"
                    stroke="#7d94b1"
                    stroke-width="2"/>

            <g stroke="#9db6d5" stroke-width="2">
              <path d="M124 {155-wheel_r+3} V{155+wheel_r-3}"/>
              <path d="M{124-wheel_r+3} 155 H{124+wheel_r-3}"/>
              <path d="M{124-wheel_r*.65:.1f} {155-wheel_r*.65:.1f}
                       L{124+wheel_r*.65:.1f} {155+wheel_r*.65:.1f}"/>
              <path d="M{124-wheel_r*.65:.1f} {155+wheel_r*.65:.1f}
                       L{124+wheel_r*.65:.1f} {155-wheel_r*.65:.1f}"/>
            </g>

            <circle cx="124" cy="155" r="5" fill="#65e2d1"/>
          </g>

          <!-- Right wheel -->
          <g class="wheel">
            <circle cx="296" cy="155" r="{wheel_r+4}"
                    fill="#050a11"
                    stroke="#52657d"
                    stroke-width="2"/>
            <circle cx="296" cy="155" r="{wheel_r-3}"
                    fill="#1b2b40"
                    stroke="#7d94b1"
                    stroke-width="2"/>

            <g stroke="#9db6d5" stroke-width="2">
              <path d="M296 {155-wheel_r+3} V{155+wheel_r-3}"/>
              <path d="M{296-wheel_r+3} 155 H{296+wheel_r-3}"/>
              <path d="M{296-wheel_r*.65:.1f} {155-wheel_r*.65:.1f}
                       L{296+wheel_r*.65:.1f} {155+wheel_r*.65:.1f}"/>
              <path d="M{296-wheel_r*.65:.1f} {155+wheel_r*.65:.1f}
                       L{296+wheel_r*.65:.1f} {155-wheel_r*.65:.1f}"/>
            </g>

            <circle cx="296" cy="155" r="5" fill="#65e2d1"/>
          </g>

          <!-- Chassis detail -->
          <path d="M148 131 H282"
                stroke="#b6d4ff"
                stroke-opacity=".65"
                stroke-width="2"
                stroke-dasharray="5 5"/>

          <circle cx="160" cy="141" r="3" fill="#65e2d1"/>
          <circle cx="270" cy="141" r="3" fill="#65e2d1"/>

        </g>

        <text x="210" y="218" text-anchor="middle"
              fill="#d5e4f6"
              font-family="monospace"
              font-size="11">
          SPEED {speed:.1f} km/h
        </text>

        <text x="210" y="234" text-anchor="middle"
              fill="#9fb4ce"
              font-family="monospace"
              font-size="10">
          ACCELERATION {accel:.2f} m/s²
        </text>

      </svg>
    </div>

    <script>
      const preview = document.getElementById("preview");
      const toggleBtn = document.getElementById("toggleBtn");
      const status = document.getElementById("status");

      let paused = false;

      toggleBtn.addEventListener("click", function () {{
          paused = !paused;

          if (paused) {{
              preview.classList.add("paused");
              toggleBtn.textContent = "▶ 다시 움직이기";
              status.textContent = "PAUSED";
          }} else {{
              preview.classList.remove("paused");
              toggleBtn.textContent = "❚❚ 멈춤";
              status.textContent = "{movement_label}";
          }}
      }});
    </script>
    </body>
    </html>
    """


# ---------------------------------------------------------
# DESIGN CONTROLS
# ---------------------------------------------------------

def make_design(prefix, defaults):
    st.markdown(f"### {prefix} · {defaults['name']}")

    with st.expander(
        f"{prefix} 설계 사양 조정",
        expanded=(prefix == "A"),
    ):
        name = st.text_input(
            "설계 이름",
            value=defaults["name"],
            key=f"{prefix}_name",
        )

        mass = st.slider(
            "차체 질량 (kg)",
            2.0,
            20.0,
            float(defaults["mass"]),
            0.5,
            key=f"{prefix}_mass",
        )

        payload = st.slider(
            "적재 질량 (kg)",
            0.0,
            15.0,
            float(defaults["payload"]),
            0.5,
            key=f"{prefix}_payload",
        )

        motor_w = st.slider(
            "모터 1개당 정격 출력 (W)",
            20,
            200,
            int(defaults["motor_w"]),
            10,
            key=f"{prefix}_power",
        )

        motor_count = st.selectbox(
            "모터 개수",
            [1, 2, 4],
            index=[1, 2, 4].index(defaults["motor_count"]),
            key=f"{prefix}_count",
        )

        motor_rpm = st.slider(
            "모터 정격 회전수 (RPM)",
            500,
            6000,
            int(defaults["motor_rpm"]),
            100,
            key=f"{prefix}_rpm",
        )

        gear_ratio = st.slider(
            "감속비 (입력:출력)",
            1.0,
            30.0,
            float(defaults["gear_ratio"]),
            0.5,
            key=f"{prefix}_gear",
        )

        wheel_radius = st.slider(
            "바퀴 반지름 (cm)",
            3.0,
            15.0,
            float(defaults["wheel_radius"]),
            0.5,
            key=f"{prefix}_wheel",
        )

        battery_v = st.selectbox(
            "배터리 전압 (V)",
            [12, 24, 36, 48],
            index=[12, 24, 36, 48].index(defaults["battery_v"]),
            key=f"{prefix}_volt",
        )

        battery_ah = st.slider(
            "배터리 용량 (Ah)",
            2.0,
            20.0,
            float(defaults["battery_ah"]),
            0.5,
            key=f"{prefix}_ah",
        )

        efficiency = st.slider(
            "구동계 효율 (%)",
            50,
            95,
            int(defaults["efficiency"]),
            5,
            key=f"{prefix}_eff",
        )

        rolling = st.slider(
            "구름 저항 계수",
            0.01,
            0.10,
            float(defaults["rolling"]),
            0.005,
            key=f"{prefix}_rolling",
        )

        slope = st.slider(
            "주행 경사각 (°)",
            0,
            20,
            int(defaults["slope"]),
            1,
            key=f"{prefix}_slope",
        )

    result = calculate_robot(
        mass,
        payload,
        motor_w,
        motor_count,
        motor_rpm,
        gear_ratio,
        wheel_radius,
        battery_v,
        battery_ah,
        efficiency,
        rolling,
        slope,
    )

    params = {
        "name": name,
        "mass": mass,
        "payload": payload,
        "motor_w": motor_w,
        "motor_count": motor_count,
        "motor_rpm": motor_rpm,
        "gear_ratio": gear_ratio,
        "wheel_radius": wheel_radius,
        "battery_v": battery_v,
        "battery_ah": battery_ah,
        "efficiency": efficiency,
        "rolling": rolling,
        "slope": slope,
    }

    return params, result


# ---------------------------------------------------------
# REPORT / CSV
# ---------------------------------------------------------

def make_report(params, result):
    rows = [
        ["설계 이름", params["name"], ""],
        ["차체 질량", params["mass"], "kg"],
        ["적재 질량", params["payload"], "kg"],
        ["총 이동 질량", result["total_mass"], "kg"],
        ["모터 개수", params["motor_count"], "개"],
        ["모터 1개당 정격 출력", params["motor_w"], "W"],
        ["총 모터 출력", result["total_power"], "W"],
        ["모터 회전수", params["motor_rpm"], "RPM"],
        ["감속비", params["gear_ratio"], "비율"],
        ["바퀴 반지름", params["wheel_radius"], "cm"],
        ["배터리 전압", params["battery_v"], "V"],
        ["배터리 용량", params["battery_ah"], "Ah"],
        ["배터리 에너지", result["battery_wh"], "Wh"],
        ["예상 최고 속도", result["speed_kmh"], "km/h"],
        ["이론적 구동력", result["traction_force"], "N"],
        ["추정 가속도", result["acceleration"], "m/s²"],
        ["예상 작동 시간", result["runtime_minutes"], "min"],
        ["추정 주행 가능 거리", result["range_km"], "km"],
    ]

    return pd.DataFrame(rows, columns=["항목", "값", "단위"])


def csv_download(df, label, filename):
    data = df.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        label,
        data=data,
        file_name=filename,
        mime="text/csv",
        key=filename,
    )


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    """
<div class="hero">
    <div class="eyebrow">ENGINEERING WORKBENCH / V 1.0</div>
    <div class="hero-title">Design your own robot.</div>
    <div class="hero-sub">
        사양을 바꾸고, 물리 모델로 성능을 예측하고, 설계안을 비교하세요.
        ROBO LAB은 로봇 설계의 기초 원리를 체험하기 위한 교육용 시뮬레이터입니다.
    </div>
    <div style="margin-top:16px">
        <span class="status-pill">● LOCAL CALCULATION</span>
        &nbsp;
        <span class="status-pill">PHYSICS-BASED ESTIMATES</span>
    </div>
</div>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:
    st.markdown("## 🤖 ROBO LAB")
    st.caption("ROBOT DESIGN STUDIO")
    st.markdown("---")

    page = st.radio(
        "WORKSPACE",
        [
            "설계 연구소",
            "설계안 비교",
            "공학 원리",
            "사용 설명서",
            "프로젝트 정보",
        ],
    )

    st.markdown("---")
    st.markdown("**설계 목표**")

    objective = st.selectbox(
        "어떤 로봇을 설계할까요?",
        [
            "범용 이동 로봇",
            "빠른 주행 로봇",
            "장시간 작동 로봇",
            "경사로 주행 로봇",
            "적재용 로봇",
        ],
    )

    st.caption(
        "계산 결과는 교육용 추정값입니다. 실제 제작 시 "
        "부품 사양과 안전 조건을 별도로 확인하세요."
    )


# ---------------------------------------------------------
# DEFAULT DESIGNS
# ---------------------------------------------------------

defaults_a = {
    "name": "Explorer A",
    "mass": 8.0,
    "payload": 2.0,
    "motor_w": 100,
    "motor_count": 2,
    "motor_rpm": 3000,
    "gear_ratio": 10.0,
    "wheel_radius": 8.0,
    "battery_v": 24,
    "battery_ah": 8.0,
    "efficiency": 80,
    "rolling": 0.03,
    "slope": 0,
}

defaults_b = {
    "name": "Endurance B",
    "mass": 7.0,
    "payload": 1.0,
    "motor_w": 60,
    "motor_count": 2,
    "motor_rpm": 2500,
    "gear_ratio": 12.0,
    "wheel_radius": 7.0,
    "battery_v": 24,
    "battery_ah": 12.0,
    "efficiency": 85,
    "rolling": 0.025,
    "slope": 0,
}


# =========================================================
# PAGE 1: DESIGN LAB
# =========================================================

if page == "설계 연구소":
    st.markdown(
        '<div class="section-kicker">01 / CONFIGURATION</div>',
        unsafe_allow_html=True,
    )
    st.header("로봇 설계")
    st.write("설계 사양을 바꾸며 로봇의 예상 성능을 확인하세요.")

    params, result = make_design("A", defaults_a)

    left, right = st.columns([1.1, 0.9], gap="large")

    with left:
        st.markdown(
            '<div class="section-kicker">DESIGN PREVIEW</div>',
            unsafe_allow_html=True,
        )

        components.html(
            robot_svg(
                params["wheel_radius"],
                result["total_mass"],
                params["motor_count"],
                result["speed_kmh"],
                result["acceleration"],
            ),
            height=295,
            scrolling=False,
        )

        st.caption(
            "개념도: 애니메이션은 계산된 속도와 가속도를 시각화한 것으로, "
            "실제 주행 성능을 그대로 재현하지는 않습니다."
        )

    with right:
        st.markdown(
            '<div class="section-kicker">PERFORMANCE OUTPUT</div>',
            unsafe_allow_html=True,
        )

        c1, c2 = st.columns(2)
        c1.metric("예상 최고 속도", f'{result["speed_kmh"]:.1f} km/h')
        c2.metric("예상 작동 시간", f'{result["runtime_minutes"]:.0f} min')

        c3, c4 = st.columns(2)
        c3.metric("이론적 구동력", f'{result["traction_force"]:.1f} N')
        c4.metric("추정 가속도", f'{result["acceleration"]:.2f} m/s²')

        c5, c6 = st.columns(2)
        c5.metric("배터리 에너지", f'{result["battery_wh"]:.0f} Wh')
        c6.metric("총 모터 출력", f'{result["total_power"]:.0f} W')

    st.markdown("---")
    st.markdown(
        '<div class="section-kicker">02 / PERFORMANCE ANALYSIS</div>',
        unsafe_allow_html=True,
    )
    st.header("성능 분석")

    masses = list(range(2, 21, 2))
    graph_rows = []

    for test_mass in masses:
        test = calculate_robot(
            test_mass,
            params["payload"],
            params["motor_w"],
            params["motor_count"],
            params["motor_rpm"],
            params["gear_ratio"],
            params["wheel_radius"],
            params["battery_v"],
            params["battery_ah"],
            params["efficiency"],
            params["rolling"],
            params["slope"],
        )

        graph_rows.append({
            "차체 질량 (kg)": test_mass,
            "추정 가속도 (m/s²)": test["acceleration"],
            "예상 최고 속도 (km/h)": test["speed_kmh"],
        })

    graph_df = pd.DataFrame(graph_rows).set_index("차체 질량 (kg)")

    graph1, graph2 = st.columns(2)

    with graph1:
        st.markdown("### 차체 질량과 가속도")
        st.line_chart(graph_df[["추정 가속도 (m/s²)"]])

    with graph2:
        st.markdown("### 차체 질량과 최고 속도")
        st.line_chart(graph_df[["예상 최고 속도 (km/h)"]])

    st.markdown("### 설계 진단")

    if result["net_force"] <= 0:
        st.warning(
            "모델상 저항을 이길 여유 구동력이 부족합니다. "
            "모터 출력, 감속비, 바퀴와 경사 조건을 확인하세요."
        )
    else:
        st.info(
            "모델상 구동력은 설정된 주행 저항보다 큽니다. "
            "실제 가속 성능은 모터 토크 곡선과 접지력에 따라 달라집니다."
        )

    if result["runtime_minutes"] < 30:
        st.warning(
            "추정 작동 시간이 짧습니다. 배터리 용량과 평균 소비 전력을 검토하세요."
        )

    if params["payload"] > params["mass"]:
        st.warning(
            "적재 질량이 차체 질량보다 큽니다. 구조 강도와 구동부 하중을 확인하세요."
        )

    st.markdown("### 설계 보고서")

    report = make_report(params, result)
    st.dataframe(report, use_container_width=True, hide_index=True)

    csv_download(
        report,
        "⬇ 설계 보고서 CSV 다운로드",
        "robo_lab_design_report.csv",
    )


# =========================================================
# PAGE 2: DESIGN COMPARISON
# =========================================================

elif page == "설계안 비교":
    st.markdown(
        '<div class="section-kicker">03 / DESIGN COMPARISON</div>',
        unsafe_allow_html=True,
    )
    st.header("두 설계안 비교")
    st.write("두 로봇의 조건을 조절하고 성능 차이를 비교해 보세요.")

    col_a, col_b = st.columns(2, gap="large")

    with col_a:
        pa, ra = make_design("A", defaults_a)

    with col_b:
        pb, rb = make_design("B", defaults_b)

    name_a = pa["name"].strip() or "설계 A"
    name_b = pb["name"].strip() or "설계 B"

    if name_a == name_b:
        name_a += " (A)"
        name_b += " (B)"

    st.markdown("---")
    st.subheader("성능 비교 결과")

    compare = pd.DataFrame({
        "항목": [
            "총 이동 질량 (kg)",
            "총 모터 출력 (W)",
            "예상 최고 속도 (km/h)",
            "추정 가속도 (m/s²)",
            "이론적 구동력 (N)",
            "배터리 에너지 (Wh)",
            "예상 작동 시간 (min)",
            "추정 주행 가능 거리 (km)",
        ],
        name_a: [
            ra["total_mass"],
            ra["total_power"],
            ra["speed_kmh"],
            ra["acceleration"],
            ra["traction_force"],
            ra["battery_wh"],
            ra["runtime_minutes"],
            ra["range_km"],
        ],
        name_b: [
            rb["total_mass"],
            rb["total_power"],
            rb["speed_kmh"],
            rb["acceleration"],
            rb["traction_force"],
            rb["battery_wh"],
            rb["runtime_minutes"],
            rb["range_km"],
        ],
    })

    st.dataframe(
        compare.set_index("항목").style.format("{:.2f}"),
        use_container_width=True,
    )

    st.markdown("### 성능 그래프")

    chart_df = pd.DataFrame({
        name_a: [
            ra["speed_kmh"],
            ra["acceleration"],
            ra["runtime_minutes"],
        ],
        name_b: [
            rb["speed_kmh"],
            rb["acceleration"],
            rb["runtime_minutes"],
        ],
    }, index=[
        "최고 속도 (km/h)",
        "가속도 (m/s²)",
        "작동 시간 (min)",
    ])

    st.bar_chart(chart_df)

    st.markdown("### 비교 분석")

    speed_winner = (
        name_a if ra["speed_kmh"] > rb["speed_kmh"]
        else name_b if rb["speed_kmh"] > ra["speed_kmh"]
        else "두 설계안이 동일"
    )

    runtime_winner = (
        name_a if ra["runtime_minutes"] > rb["runtime_minutes"]
        else name_b if rb["runtime_minutes"] > ra["runtime_minutes"]
        else "두 설계안이 동일"
    )

    st.success(f"속도 측면: **{speed_winner}** 설계안의 추정 속도가 더 높습니다.")
    st.success(f"작동 시간 측면: **{runtime_winner}** 설계안의 추정 작동 시간이 더 깁니다.")

    csv_download(
        compare,
        "⬇ 비교 결과 CSV 다운로드",
        "robo_lab_comparison.csv",
    )


# =========================================================
# PAGE 3: ENGINEERING PRINCIPLES
# =========================================================

elif page == "공학 원리":
    st.markdown(
        '<div class="section-kicker">04 / ENGINEERING NOTES</div>',
        unsafe_allow_html=True,
    )
    st.header("계산에 사용한 공학 원리")

    with st.expander("1. 배터리 에너지 (Energy)", expanded=True):
        st.latex(r"E = V \times Q")
        st.write(
            "전압 V(Volt)와 용량 Q(Ah)를 곱하면 Wh 단위의 명목 에너지를 "
            "계산할 수 있습니다. 실제 사용 가능 에너지는 방전율, 온도, "
            "배터리 종류와 보호회로에 따라 달라집니다."
        )

    with st.expander("2. 바퀴의 선속도 (Linear Velocity)"):
        st.latex(r"v = r \times \omega")
        st.write(
            "바퀴 반지름 r과 각속도 ω로 이상적인 선속도를 계산합니다. "
            "감속기를 사용하면 출력 회전수는 모터 회전수를 감속비로 나눈 값으로 근사합니다."
        )

    with st.expander("3. 토크와 구동력 (Torque & Force)"):
        st.latex(r"F = \frac{\tau}{r}")
        st.write(
            "바퀴 토크가 커지면 이상적인 구동력이 커집니다. "
            "같은 토크에서는 바퀴 반지름이 클수록 구동력이 작아집니다."
        )

    with st.expander("4. 주행 저항 및 가속도 (Resistance & Acceleration)"):
        st.latex(r"F_{\text{net}} = F_{\text{traction}} - (F_{\text{rolling}} + F_{\text{slope}})")
        st.latex(r"a = \frac{F_{\text{net}}}{m}")
        st.write(
            "구름 저항과 경사 저항의 합보다 견인력(구동력)이 더 커야 로봇이 가속할 수 있습니다. "
            "뉴턴의 제2법칙(F=ma)에 따라 알짜힘을 전체 질량으로 나누어 가속도를 계산합니다."
        )


# =========================================================
# PAGE 4: USER MANUAL
# =========================================================

elif page == "사용 설명서":
    st.markdown(
        '<div class="section-kicker">05 / USER GUIDE</div>',
        unsafe_allow_html=True,
    )
    st.header("사용 설명서")

    st.markdown("""
    ### 🛠️ 주요 기능 설명
    1. **설계 연구소**
       - 슬라이더 및 입력 폼을 통해 차체 질량, 모터 사양, 감속비, 바퀴 크기 등을 실시간으로 조정합니다.
       - 시뮬레이터 애니메이션과 하단 매트릭을 통해 최고 속도, 가속도, 작동 시간 등의 변화를 관찰할 수 있습니다.
       - 설계를 완성한 후 CSV 버튼을 통해 설계 보고서를 다운로드할 수 있습니다.

    2. **설계안 비교**
       - 서로 다른 2개의 설계(A/B) 파라미터를 동시 비교하여 최적의 모듈 구성을 탐색합니다.

    3. **공학 원리**
       - 구동 시뮬레이션 계산 모델에 사용된 주요 물리 수식과 원리를 확인합니다.
    """)


# =========================================================
# PAGE 5: PROJECT INFO
# =========================================================

elif page == "프로젝트 정보":
    st.markdown(
        '<div class="section-kicker">06 / ABOUT PROJECT</div>',
        unsafe_allow_html=True,
    )
    st.header("프로젝트 정보")

    st.markdown("""
    **ROBO LAB | Robot Design Studio v1.0**
    
    본 스튜디오는 로봇공학 기초 물리 메커니즘을 시각적으로 학습할 수 있도록 제작된 인터랙티브 교육용 시뮬레이터입니다.

    - **개발 프레임워크**: Python, Streamlit, HTML/CSS/SVG Animations
    - **핵심 계산**: 차체 역학, 감속기-바퀴 선속도 및 모터 토크, 배터리 소모 전력 모델링
    """)


# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.markdown("---")
st.markdown(
    '<div class="footer">ROBO LAB © 2026. All rights reserved. Designed for Educational Simulation.</div>',
    unsafe_allow_html=True,
)
