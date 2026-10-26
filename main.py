import math
import csv
import io
import streamlit as st
import pandas as pd

page = "설계 연구소"

# ============================================================
# ROBO LAB — Robot Design Simulator
# ============================================================

st.set_page_config(
    page_title="ROBO LAB | Robot Design Studio",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

    :root {
        --ink: #F1F5FC;
        --muted: #C5D3E6;
        --panel: #121C2B;
        --line: #40536D;
        --blue: #6BA8FF;
        --cyan: #65E2D1;
    }

    /* 기본 화면 */
    .stApp {
        background: radial-gradient(
            ellipse at 10% 0%,
            #162B47 0%,
            #0B1220 43%,
            #080D16 100%
        );
        color: var(--ink);
    }

    html, body, [class*="css"] {
        font-family: 'Manrope', sans-serif;
    }

    /* 기본 글씨 색상 및 대비 */
    [data-testid="stAppViewContainer"],
    [data-testid="stAppViewContainer"] p,
    [data-testid="stAppViewContainer"] label,
    [data-testid="stAppViewContainer"] li {
        color: #F1F5FC;
    }

    h1, h2, h3 {
        color: #F5F8FF !important;
        letter-spacing: -0.04em;
    }

    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li,
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] p {
        color: #D6E1F0 !important;
    }

    /* 사이드바 */
    [data-testid="stSidebar"] {
        background: #0C1421;
        border-right: 1px solid #40536D;
    }

    [data-testid="stSidebar"] * {
        color: #F1F5FC;
    }

    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] {
        color: #F1F5FC !important;
    }

    /* 상단 소개 영역 */
    .hero {
        padding: 24px 26px;
        border: 1px solid #40536D;
        border-radius: 20px;
        background: linear-gradient(
            120deg,
            rgba(28, 53, 83, .98),
            rgba(14, 25, 41, .98)
        );
        margin-bottom: 22px;
    }

    .eyebrow {
        font-family: 'DM Mono', monospace;
        font-size: 11px;
        letter-spacing: 2px;
        color: #65E2D1;
        font-weight: 700;
    }

    .hero-title {
        font-size: clamp(32px, 4vw, 52px);
        line-height: 1.08;
        font-weight: 800;
        margin: 8px 0 10px;
        color: #FFFFFF;
    }

    .hero-sub {
        color: #D6E3F4;
        font-size: 14px;
        max-width: 760px;
        line-height: 1.8;
    }

    .section-kicker {
        font-family: 'DM Mono', monospace;
        color: #65E2D1;
        font-size: 11px;
        letter-spacing: 1.6px;
        margin-bottom: 4px;
        font-weight: 700;
    }

    /* 패널 */
    .panel {
        border: 1px solid #40536D;
        background: rgba(18, 28, 43, .92);
        padding: 17px 18px;
        border-radius: 16px;
    }

    .tiny-label {
        color: #C5D3E6 !important;
        font-size: 12px;
    }

    .big-value {
        font-size: 26px;
        font-weight: 800;
        color: #F5F8FF;
        letter-spacing: -1px;
    }

    .unit {
        color: #C5D3E6 !important;
        font-size: 12px;
    }

    .note {
        color: #C5D3E6 !important;
        font-size: 12px;
        line-height: 1.75;
    }

    .status-pill {
        display: inline-block;
        padding: 5px 9px;
        border-radius: 999px;
        border: 1px solid #32736D;
        background: #102E30;
        color: #9AFFF0;
        font-size: 10px;
        font-family: 'DM Mono', monospace;
        letter-spacing: 1px;
        font-weight: 700;
    }

    /* 성능 지표 */
    div[data-testid="stMetric"] {
        background: rgba(18, 28, 43, .95);
        border: 1px solid #40536D;
        padding: 15px 17px;
        border-radius: 14px;
    }

    [data-testid="stMetricLabel"],
    [data-testid="stMetricLabel"] * {
        color: #D6E1F0 !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricValue"],
    [data-testid="stMetricValue"] * {
        color: #FFFFFF !important;
        font-weight: 800 !important;
    }

    [data-testid="stMetricDelta"] {
        color: #9AFFF0 !important;
    }

    /* 버튼 */
    .stButton > button,
    .stDownloadButton > button {
        border-radius: 10px;
        font-weight: 700;
        min-height: 42px;
        border: 1px solid #526987;
    }

    .stButton > button[kind="primary"] {
        background: #6BA8FF;
        color: #07111E;
        border: 0;
    }

    .stButton > button:hover,
    .stDownloadButton > button:hover {
        border-color: #65E2D1;
        color: #FFFFFF;
    }

    hr {
        border-color: #40536D;
    }

    /* 로봇 개념도 */
    .robot-svg-wrap {
        display: flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(145deg, #101C2D, #0B1320);
        border: 1px solid #40536D;
        border-radius: 18px;
        padding: 16px;
        min-height: 240px;
    }

    .footer {
        color: #B8C8DC;
        font-size: 11px;
        text-align: center;
        padding: 24px 0 10px;
    }

    /* ======================================================
       가독성 개선 CSS
       어두운 배경에서 흐릿하게 보이는 글씨의 대비를 높임
       ====================================================== */

    /* 슬라이더, 입력창 등 모든 위젯 라벨 */
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] *,
    [data-testid="stSlider"] label,
    [data-testid="stSelectbox"] label,
    [data-testid="stTextInput"] label,
    [data-testid="stNumberInput"] label,
    [data-testid="stRadio"] label,
    [data-testid="stCheckbox"] label,
    [data-testid="stMultiSelect"] label {
        color: #F1F5FC !important;
        font-weight: 600 !important;
    }

    /* 입력창 아래 설명과 도움말 */
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] *,
    [data-testid="stHelp"],
    [data-testid="stMarkdownContainer"] p {
        color: #D6E1F0 !important;
    }

    /* 펼치기 메뉴 */
    [data-testid="stExpander"] details {
        background-color: #111D2E !important;
        border: 1px solid #40536D !important;
        border-radius: 10px !important;
    }

    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary:hover {
        background-color: #1A2A40 !important;
        color: #FFFFFF !important;
        border-color: #526987 !important;
        border-radius: 8px !important;
    }

    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] summary svg {
        color: #FFFFFF !important;
        fill: #FFFFFF !important;
        font-weight: 700 !important;
    }

    /* 슬라이더 수치 */
    [data-testid="stSlider"] [data-testid="stMarkdownContainer"] p {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    [data-testid="stSlider"] [role="slider"] {
        border-color: #FF5A64 !important;
    }

    /* 입력창: 밝은 배경과 어두운 글씨 */
    input,
    textarea {
        background-color: #F1F5FC !important;
        color: #101827 !important;
        border-color: #71839D !important;
        caret-color: #101827 !important;
    }

    input::placeholder,
    textarea::placeholder {
        color: #526176 !important;
        opacity: 1 !important;
    }

    /* 드롭다운 선택 상자 */
    [data-baseweb="select"] > div {
        background-color: #F1F5FC !important;
        border-color: #71839D !important;
        color: #101827 !important;
    }

    [data-baseweb="select"] input,
    [data-baseweb="select"] span,
    [data-baseweb="select"] div {
        color: #101827 !important;
    }

    /* 드롭다운 목록 */
    [role="listbox"],
    [role="option"] {
        background-color: #F1F5FC !important;
        color: #101827 !important;
    }

    [role="option"] * {
        color: #101827 !important;
    }

    [role="option"]:hover {
        background-color: #DCE8F7 !important;
    }

    /* 체크박스와 라디오 */
    [data-testid="stCheckbox"] label,
    [data-testid="stRadio"] label {
        color: #F1F5FC !important;
    }

    /* 경고, 성공, 정보 메시지 */
    [data-testid="stAlert"] p,
    [data-testid="stAlert"] span {
        color: #F1F5FC !important;
    }

    /* 표 */
    [data-testid="stDataFrame"],
    [data-testid="stTable"] {
        border: 1px solid #40536D;
        border-radius: 8px;
    }

    /* 그래프 영역 설명 */
    [data-testid="stVegaLiteChart"],
    [data-testid="stArrowVegaLiteChart"] {
        color: #F1F5FC !important;
    }

    /* 키보드 접근 시 테두리 표시 */
    button:focus-visible,
    input:focus-visible,
    textarea:focus-visible {
        outline: 2px solid #65E2D1 !important;
        outline-offset: 2px !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 물리 계산 함수
# ============================================================

def calculate_robot(
    mass,
    motor_w,
    motor_rpm,
    gear_ratio,
    wheel_radius_cm,
    battery_v,
    battery_ah,
    efficiency_pct,
    motor_count,
    rolling_coeff,
    slope_deg,
    payload_kg,
):
    """단순화한 물리 모델. 실제 하드웨어 성능을 보장하지 않는 추정값입니다."""

    total_mass = max(0.1, mass + payload_kg)
    radius = max(0.01, wheel_radius_cm / 100.0)
    eta = max(0.05, min(1.0, efficiency_pct / 100.0))

    total_motor_power = motor_w * motor_count
    wheel_rpm = motor_rpm / max(0.1, gear_ratio)
    omega = wheel_rpm * 2 * math.pi / 60.0
    ideal_speed = omega * radius
    available_power = total_motor_power * eta

    motor_omega = motor_rpm * 2 * math.pi / 60.0
    wheel_torque = (
        motor_w * eta / max(motor_omega, 0.5)
    ) * gear_ratio

    total_torque = wheel_torque * motor_count
    traction_force = total_torque / radius

    theta = math.radians(slope_deg)
    gravity = 9.81

    rolling_force = (
        rolling_coeff * total_mass * gravity * math.cos(theta)
    )
    slope_force = total_mass * gravity * math.sin(theta)
    resistance = max(0.0, rolling_force + slope_force)

    net_force = max(0.0, traction_force - resistance)
    accel = net_force / total_mass

    if resistance > 0.01:
        power_limited_speed = available_power / resistance
        estimated_speed = min(
            ideal_speed,
            max(0.0, power_limited_speed),
        )
    else:
        estimated_speed = ideal_speed

    battery_wh = battery_v * battery_ah
    usable_wh = battery_wh * 0.85

    average_power = max(
        1.0,
        total_motor_power * 0.65 / max(0.1, eta),
    )

    runtime_hours = usable_wh / average_power
    runtime_minutes = runtime_hours * 60.0
    range_km = estimated_speed * runtime_hours * 3.6

    return {
        "total_mass": total_mass,
        "total_motor_power": total_motor_power,
        "wheel_rpm": wheel_rpm,
        "ideal_speed": ideal_speed,
        "estimated_speed": estimated_speed,
        "speed_kmh": estimated_speed * 3.6,
        "wheel_torque": wheel_torque,
        "total_torque": total_torque,
        "traction_force": traction_force,
        "resistance": resistance,
        "net_force": net_force,
        "accel": accel,
        "battery_wh": battery_wh,
        "usable_wh": usable_wh,
        "runtime_minutes": runtime_minutes,
        "range_km": range_km,
        "slope_force": slope_force,
        "rolling_force": rolling_force,
        "available_power": available_power,
    }


# ============================================================
# 로봇 SVG 개념도
# ============================================================

def robot_svg(wheel_radius_cm, mass, motor_count, color="#6ba8ff"):
    """외부 이미지 없이 코드 내부에서 로봇 개념도를 생성합니다."""

    wheel_r = max(12, min(25, wheel_radius_cm * 1.2))

    return f"""
    <div class="robot-svg-wrap">
    <svg viewBox="0 0 420 220" width="100%"
         style="max-width:430px"
         role="img" aria-label="로봇 차체 개념도">
      <defs>
        <linearGradient id="bodyGrad" x1="0" y1="0" x2="1" y2="1">
          <stop offset="0%" stop-color="{color}" stop-opacity=".95"/>
          <stop offset="100%" stop-color="#244c7a" stop-opacity=".95"/>
        </linearGradient>
        <linearGradient id="floorGrad" x1="0" y1="0" x2="0" y2="1">
          <stop offset="0%" stop-color="#263c58" stop-opacity=".7"/>
          <stop offset="100%" stop-color="#0b1421" stop-opacity="0"/>
        </linearGradient>
      </defs>

      <ellipse cx="210" cy="174" rx="145" ry="24"
               fill="url(#floorGrad)"/>

      <path d="M78 137 L122 104 L300 104 L345 137
               L302 161 L120 161 Z"
            fill="#17263a" stroke="#45617f" stroke-width="2"/>

      <path d="M122 104 L300 104 L330 125 L100 125 Z"
            fill="#29415f" stroke="#547397" stroke-width="1.5"/>

      <path d="M100 125 L330 125 L302 151 L120 151 Z"
            fill="url(#bodyGrad)" stroke="#7cb5ff" stroke-width="1.5"/>

      <path d="M155 91 L180 76 L260 76 L286 91
               L270 105 L170 105 Z"
            fill="#1d3048" stroke="#6ba8ff" stroke-width="1.5"/>

      <rect x="187" y="63" width="46" height="17"
            rx="5" fill="#65e2d1" fill-opacity=".85"/>

      <circle cx="210" cy="61" r="7"
              fill="#65e2d1" stroke="#b7fff4" stroke-width="2"/>

      <path d="M210 52 V39 M202 44 L210 36 L218 44"
            stroke="#65e2d1" stroke-width="2"
            fill="none" stroke-linecap="round"/>

      <g>
        <circle cx="124" cy="155" r="{wheel_r+4}"
                fill="#050a11" stroke="#52657d" stroke-width="2"/>
        <circle cx="124" cy="155" r="{wheel_r-3}"
                fill="#1b2b40" stroke="#7d94b1" stroke-width="2"/>
        <circle cx="124" cy="155" r="5" fill="#65e2d1"/>

        <circle cx="296" cy="155" r="{wheel_r+4}"
                fill="#050a11" stroke="#52657d" stroke-width="2"/>
        <circle cx="296" cy="155" r="{wheel_r-3}"
                fill="#1b2b40" stroke="#7d94b1" stroke-width="2"/>
        <circle cx="296" cy="155" r="5" fill="#65e2d1"/>
      </g>

      <path d="M148 131 H282"
            stroke="#b6d4ff" stroke-opacity=".65"
            stroke-width="2" stroke-dasharray="5 5"/>

      <text x="210" y="194" text-anchor="middle"
            fill="#d6e3f4" font-family="monospace" font-size="11">
        CONCEPT MODEL • {mass:.1f} kg • {motor_count} MOTOR(S)
      </text>

      <text x="210" y="211" text-anchor="middle"
            fill="#b8c8dc" font-family="monospace" font-size="9">
        ILLUSTRATIVE DESIGN — NOT A CAD MODEL
      </text>
    </svg>
    </div>
    """


# ============================================================
# 설계 입력 함수
# ============================================================

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
            2.0, 20.0, float(defaults["mass"]), 0.5,
            key=f"{prefix}_mass",
        )

        payload = st.slider(
            "적재 질량 (kg)",
            0.0, 15.0, float(defaults["payload"]), 0.5,
            key=f"{prefix}_payload",
        )

        motor_w = st.slider(
            "모터 1개당 정격 출력 (W)",
            20, 200, int(defaults["motor_w"]), 10,
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
            500, 6000, int(defaults["motor_rpm"]), 100,
            key=f"{prefix}_rpm",
        )

        gear_ratio = st.slider(
            "감속비 (입력:출력)",
            1.0, 30.0, float(defaults["gear_ratio"]), 0.5,
            key=f"{prefix}_gear",
        )

        wheel_radius = st.slider(
            "바퀴 반지름 (cm)",
            3.0, 15.0, float(defaults["wheel_radius"]), 0.5,
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
            2.0, 20.0, float(defaults["battery_ah"]), 0.5,
            key=f"{prefix}_ah",
        )

        efficiency = st.slider(
            "구동계 효율 (%)",
            50, 95, int(defaults["efficiency"]), 5,
            key=f"{prefix}_eff",
        )

        rolling = st.slider(
            "구름 저항 계수",
            0.01, 0.10, float(defaults["rolling"]), 0.005,
            key=f"{prefix}_rolling",
        )

        slope = st.slider(
            "주행 경사각 (°)",
            0, 20, int(defaults["slope"]), 1,
            key=f"{prefix}_slope",
        )

    result = calculate_robot(
        mass,
        motor_w,
        motor_rpm,
        gear_ratio,
        wheel_radius,
        battery_v,
        battery_ah,
        efficiency,
        motor_count,
        rolling,
        slope,
        payload,
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


# ============================================================
# 상단 소개
# ============================================================

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


# ============================================================
# 사이드바
# ============================================================

with st.sidebar:
    st.markdown("## 🤖 ROBO LAB")
    st.caption("ROBOT DESIGN STUDIO")
    st.markdown("---")

    page = st.radio(
        "WORKSPACE",
        ["설계 연구소", "설계안 비교", "공학 원리", "프로젝트 정보"],
        index=0,
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

    st.markdown(
        """
        <p class="note">
        모든 결과는 단순화한 이론 모델에 따른 추정값입니다.
        실제 제작 전에는 부품 사양과 안전 한계를 확인해야 합니다.
        </p>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# 기본 설계값
# ============================================================

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


# ============================================================
# 1. 설계 연구소
# ============================================================

if page == "설계 연구소":
    st.markdown(
        '<div class="section-kicker">01 / CONFIGURATION</div>',
        unsafe_allow_html=True,
    )

    st.header("로봇 설계")
    st.write(
        "왼쪽 메뉴에서 설계 목표를 선택하고, "
        "아래에서 로봇의 사양을 조절하세요."
    )

    params, result = make_design("A", defaults_a)

    left, right = st.columns([1.1, 0.9], gap="large")

    with left:
        st.markdown(
            '<div class="section-kicker">DESIGN PREVIEW</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            robot_svg(
                params["wheel_radius"],
                result["total_mass"],
                params["motor_count"],
            ),
            unsafe_allow_html=True,
        )

        st.caption(
            "개념도: 실제 크기·부품 배치·CAD 형상을 나타내지 않습니다."
        )

    with right:
        st.markdown(
            '<div class="section-kicker">PERFORMANCE OUTPUT</div>',
            unsafe_allow_html=True,
        )

        m1, m2 = st.columns(2)
        m1.metric(
            "예상 최고 속도",
            f'{result["speed_kmh"]:.1f} km/h',
        )
        m2.metric(
            "예상 작동 시간",
            f'{result["runtime_minutes"]:.0f} min',
        )

        m3, m4 = st.columns(2)
        m3.metric(
            "이론적 구동력",
            f'{result["traction_force"]:.1f} N',
        )
        m4.metric(
            "추정 가속도",
            f'{result["accel"]:.2f} m/s²',
        )

        m5, m6 = st.columns(2)
        m5.metric(
            "배터리 에너지",
            f'{result["battery_wh"]:.0f} Wh',
        )
        m6.metric(
            "총 모터 출력",
            f'{result["total_motor_power"]} W',
        )

    st.markdown("---")
    st.markdown(
        '<div class="section-kicker">02 / PERFORMANCE ANALYSIS</div>',
        unsafe_allow_html=True,
    )

    st.header("성능 분석")

    masses = list(range(2, 21, 2))
    mass_rows = []

    for test_mass in masses:
        test = calculate_robot(
            test_mass,
            params["motor_w"],
            params["motor_rpm"],
            params["gear_ratio"],
            params["wheel_radius"],
            params["battery_v"],
            params["battery_ah"],
            params["efficiency"],
            params["motor_count"],
            params["rolling"],
            params["slope"],
            params["payload"],
        )

        mass_rows.append(
            {
                "차체 질량 (kg)": test_mass,
                "추정 가속도 (m/s²)": test["accel"],
                "예상 최고 속도 (km/h)": test["speed_kmh"],
            }
        )

    graph1, graph2 = st.columns(2)

    with graph1:
        st.markdown("**차체 질량과 가속도**")
        st.line_chart(
            pd.DataFrame(mass_rows).set_index("차체 질량 (kg)")[
                "추정 가속도 (m/s²)"
            ]
        )

    with graph2:
        st.markdown("**차체 질량과 최고 속도**")
        st.line_chart(
            pd.DataFrame(mass_rows).set_index("차체 질량 (kg)")[
                "예상 최고 속도 (km/h)"
            ]
        )

    st.markdown("### 설계 진단")

    diagnostics = []

    if result["net_force"] <= 0:
        diagnostics.append(
            "현재 설정에서 모델상 저항을 이길 여유 구동력이 없습니다. "
            "모터·감속비·바퀴·경사 조건을 확인하세요."
        )
    else:
        diagnostics.append(
            "모델상 구동력은 설정된 주행 저항보다 큽니다. "
            "실제 가속 성능은 토크 곡선과 접지력에 따라 달라집니다."
        )

    if result["speed_kmh"] > 25:
        diagnostics.append(
            "추정 속도가 높습니다. 실제 제작 시 제동, 안정성, "
            "모터 회전수 및 안전 제한을 별도로 검토하세요."
        )

    if result["runtime_minutes"] < 30:
        diagnostics.append(
            "추정 작동 시간이 짧습니다. 배터리 용량을 늘리거나 "
            "평균 소비 전력을 줄이는 설계를 검토하세요."
        )

    if params["slope"] > 10:
        diagnostics.append(
            "경사각이 큽니다. 무게중심, 전복 위험, 바퀴 접지력 "
            "및 제동 성능을 추가로 검토해야 합니다."
        )

    if params["payload"] > params["mass"]:
        diagnostics.append(
            "적재 질량이 차체 질량보다 큽니다. "
            "구조 강도와 구동부 하중을 확인하세요."
        )

    for diagnostic in diagnostics:
        st.info(diagnostic)

    report = pd.DataFrame(
        [
            ["설계 이름", params["name"], ""],
            ["차체 질량", params["mass"], "kg"],
            ["적재 질량", params["payload"], "kg"],
            ["총 이동 질량", result["total_mass"], "kg"],
            ["모터 개수", params["motor_count"], "개"],
            ["모터 1개당 정격 출력", params["motor_w"], "W"],
            ["총 모터 출력", result["total_motor_power"], "W"],
            ["모터 회전수", params["motor_rpm"], "RPM"],
            ["감속비", params["gear_ratio"], "비율"],
            ["바퀴 반지름", params["wheel_radius"], "cm"],
            ["배터리 전압", params["battery_v"], "V"],
            ["배터리 용량", params["battery_ah"], "Ah"],
            ["배터리 에너지", result["battery_wh"], "Wh"],
            ["추정 최고 속도", result["speed_kmh"], "km/h"],
            ["이론적 구동력", result["traction_force"], "N"],
            ["추정 가속도", result["accel"], "m/s²"],
            ["추정 작동 시간", result["runtime_minutes"], "min"],
            ["추정 주행 가능 거리", result["range_km"], "km"],
        ],
        columns=["항목", "값", "단위"],
    )

    csv_data = report.to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "⬇ 설계 보고서 CSV 다운로드",
        data=csv_data,
        file_name="robo_lab_design_report.csv",
        mime="text/csv",
    )


# ============================================================
# 2. 설계안 비교
# ============================================================

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

    st.markdown("---")
    st.subheader("성능 비교 결과")

    compare = pd.DataFrame(
        {
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
            pa["name"]: [
                ra["total_mass"],
                ra["total_motor_power"],
                ra["speed_kmh"],
                ra["accel"],
                ra["traction_force"],
                ra["battery_wh"],
                ra["runtime_minutes"],
                ra["range_km"],
            ],
            pb["name"]: [
                rb["total_mass"],
                rb["total_motor_power"],
                rb["speed_kmh"],
                rb["accel"],
                rb["traction_force"],
                rb["battery_wh"],
                rb["runtime_minutes"],
                rb["range_km"],
            ],
        }
    )

    st.dataframe(
        compare.set_index("항목").style.format("{:.2f}"),
        use_container_width=True,
    )

    chart_df = pd.DataFrame(
        {
            "성능 지표": [
                "최고 속도 (km/h)",
                "가속도 (m/s²)",
                "작동 시간 (min)",
            ],
            pa["name"]: [
                ra["speed_kmh"],
                ra["accel"],
                ra["runtime_minutes"],
            ],
            pb["name"]: [
                rb["speed_kmh"],
                rb["accel"],
                rb["runtime_minutes"],
            ],
        }
    ).set_index("성능 지표")

    st.bar_chart(chart_df)

    st.markdown("### 비교 분석")

    speed_winner = (
        pa["name"]
        if ra["speed_kmh"] > rb["speed_kmh"]
        else pb["name"]
        if rb["speed_kmh"] > ra["speed_kmh"]
        else "두 설계안이 동일"
    )

    runtime_winner = (
        pa["name"]
        if ra["runtime_minutes"] > rb["runtime_minutes"]
        else pb["name"]
        if rb["runtime_minutes"] > ra["runtime_minutes"]
        else "두 설계안이 동일"
    )

    st.success(
        f"속도 측면: **{speed_winner}** 설계안의 "
        "모델상 최고 속도가 더 높습니다."
    )

    st.success(
        f"작동 시간 측면: **{runtime_winner}** 설계안의 "
        "추정 작동 시간이 더 깁니다."
    )

    st.caption(
        "속도와 작동 시간은 단순화한 모델의 추정치이며, "
        "실제 주행 시험 결과와 다를 수 있습니다."
    )

    st.download_button(
        "⬇ 비교 결과 CSV 다운로드",
        data=compare.to_csv(index=False).encode("utf-8-sig"),
        file_name="robo_lab_comparison.csv",
        mime="text/csv",
    )


# ============================================================
# 3. 공학 원리
# ============================================================

elif page == "공학 원리":
    st.markdown(
        '<div class="section-kicker">04 / ENGINEERING NOTES</div>',
        unsafe_allow_html=True,
    )

    st.header("계산에 사용한 공학 원리")
    st.write(
        "이 시뮬레이터는 기본적인 물리 관계를 이용해 "
        "설계 조건의 영향을 탐색합니다."
    )

    with st.expander("1. 배터리 에너지", expanded=True):
        st.latex(r"E = VQ")
        st.write(
            "전압 V와 용량 Q(Ah)를 곱하면 Wh 단위의 명목 에너지를 "
            "추정할 수 있습니다. 실제 사용 가능 에너지는 배터리 화학, "
            "방전율, 온도, 보호회로에 따라 달라집니다."
        )

    with st.expander("2. 바퀴의 선속도"):
        st.latex(r"v = r\omega")
        st.write(
            "바퀴 반지름 r과 각속도 ω로 이상적인 선속도를 계산합니다. "
            "감속기를 사용하면 출력 회전수는 모터 회전수를 "
            "감속비로 나눈 값으로 근사합니다."
        )

    with st.expander("3. 토크와 구동력"):
        st.latex(r"F = \frac{\tau}{r}")
        st.write(
            "바퀴 토크 τ가 커지면 이상적인 구동력이 커지고, "
            "바퀴 반지름이 커지면 같은 토크에서 구동력은 작아집니다. "
            "접지력 한계와 모터 토크 곡선은 이 간단한 모델에 "
            "완전히 포함되어 있지 않습니다."
        )

    with st.expander("4. 뉴턴의 운동 법칙"):
        st.latex(r"a = \frac{F_{\mathrm{net}}}{m}")
        st.write(
            "가속도는 알짜힘을 질량으로 나눈 값입니다. 실제 로봇에는 "
            "회전 관성, 구동 손실, 모터의 토크 변화, 제어 알고리즘 "
            "등이 영향을 줍니다."
        )

    with st.expander("5. 작동 시간 근사"):
        st.latex(r"t \approx \frac{E_{\mathrm{usable}}}{P_{\mathrm{average}}}")
        st.write(
            "평균 소비 전력이 커질수록 작동 시간은 짧아집니다. "
            "이 앱은 명목 배터리 에너지의 85%를 사용 가능 에너지로 "
            "가정하고, 모터 정격 출력의 일정 비율을 평균 소비 전력으로 "
            "가정합니다."
        )

    st.warning(
        "교육용 단순 모델입니다. 안전이 중요한 실제 로봇의 "
        "제작·운용을 위한 검증된 설계 도구가 아닙니다."
    )


# ============================================================
# 4. 프로젝트 정보
# ============================================================

else:
    st.markdown(
        '<div class="section-kicker">05 / ABOUT THE PROJECT</div>',
        unsafe_allow_html=True,
    )

    st.header("프로젝트 정보")

    st.markdown(
        """
        ### 프로젝트 목표

        로봇의 기계적 사양을 바꾸며 물리 법칙과 설계 선택이
        예상 성능에 어떤 영향을 주는지 탐구합니다.

        ### 사용 기술

        - **Python** — 계산 로직
        - **Streamlit** — 웹 UI와 상호작용
        - **Pandas** — 표와 보고서 데이터
        - **SVG / CSS** — 코드 내부의 로봇 개념도와 디자인

        ### 탐구 질문 예시

        1. 같은 모터 출력에서 차체 질량이 증가하면 가속도는 어떻게 변할까?
        2. 배터리 용량을 늘리면 예상 작동 시간은 얼마나 변할까?
        3. 감속비와 바퀴 반지름은 속도와 구동력에 어떤 영향을 줄까?
        4. 빠른 로봇과 오래 작동하는 로봇의 설계 조건은 어떻게 다를까?

        ### 배포 방법

        1. 이 코드를 `main.py`로 저장합니다.
        2. GitHub 저장소에 업로드합니다.
        3. Streamlit Community Cloud에서 저장소와 `main.py`를 선택해 배포합니다.

        이 앱은 외부 이미지나 API 없이 계산과 시각화 기능이 작동합니다.
        CSS의 웹 폰트는 인터넷 연결이 가능할 때만 적용되며,
        연결이 없으면 기본 글꼴로 표시됩니다.
        """
    )


# ============================================================
# 하단 푸터
# ============================================================

st.markdown(
    """
    <div class="footer">
        ROBO LAB · EDUCATIONAL ROBOT DESIGN SIMULATOR · ESTIMATES ONLY
    </div>
    """,
    unsafe_allow_html=True,
)
