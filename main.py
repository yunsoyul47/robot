import math
import pandas as pd
import streamlit as st

# ==================================================
# ROBO LAB | ROBOT DESIGN & ENGINEERING SIMULATOR
# ==================================================

st.set_page_config(
    page_title="ROBO LAB",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- CSS 디자인 ----------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #f5f7fc, #eaf0fa);
    font-family: 'Space Grotesk', sans-serif;
}
.block-container {
    max-width: 1400px;
    padding-top: 2rem;
}
.hero {
    background: linear-gradient(120deg, #17212f, #304c78, #526dce);
    color: white;
    padding: 35px;
    border-radius: 24px;
    margin-bottom: 25px;
}
.hero h1 {
    color: white;
    font-size: 46px;
    margin: 8px 0;
}
.hero p {
    color: #d6e2f8;
}
.kicker {
    color: #66e2d1;
    letter-spacing: 3px;
    font-size: 12px;
}
.metric-card {
    background: white;
    border: 1px solid #e0e7f2;
    border-radius: 18px;
    padding: 20px;
    min-height: 125px;
    margin-bottom: 12px;
}
.metric-label {
    color: #657286;
    font-size: 14px;
}
.metric-value {
    color: #17212f;
    font-size: 29px;
    font-weight: 700;
    margin-top: 8px;
}
.metric-unit {
    color: #7b8798;
    font-size: 12px;
    margin-top: 5px;
}
.section-label {
    color: #526dce;
    letter-spacing: 2px;
    font-size: 12px;
    font-weight: 700;
}
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e0e7f2;
    padding: 15px;
    border-radius: 14px;
}
[data-testid="stSidebar"] {
    background: #eef2f9;
}
</style>
""", unsafe_allow_html=True)


# ---------------- 성능 계산 모델 ----------------
def calculate_robot(
    mass,
    power,
    wheel_radius_cm,
    battery_ah,
    voltage,
    drive_type,
    motor_rpm,
    gear_ratio,
    efficiency_pct,
    rolling_resistance,
    slope_deg,
    frontal_area=0.12,
    drag_coefficient=0.9
):
    g = 9.81
    air_density = 1.225

    radius = wheel_radius_cm / 100
    efficiency = efficiency_pct / 100
    gear_ratio = max(gear_ratio, 0.1)

    # 배터리 에너지
    battery_wh = battery_ah * voltage
    usable_energy_wh = battery_wh * 0.85

    # 평균 전력 소비량을 정격 출력의 70%로 가정
    average_power = max(power * 0.70, 1)

    runtime_hours = usable_energy_wh / average_power
    runtime_minutes = runtime_hours * 60

    # 감속 후 바퀴 회전수와 회전 속도
    wheel_rpm = motor_rpm / gear_ratio
    wheel_speed = wheel_rpm * 2 * math.pi * radius / 60

    # 모터 출력으로부터 바퀴 토크 추정
    motor_omega = max(motor_rpm * 2 * math.pi / 60, 0.1)
    motor_torque = power / motor_omega
    wheel_torque = motor_torque * gear_ratio * efficiency

    # 바퀴에서 발생하는 구동력의 근사값
    torque_force = wheel_torque / max(radius, 0.001)

    # 경사로와 구름 저항
    angle = math.radians(slope_deg)
    resistance = mass * g * (
        rolling_resistance * math.cos(angle)
        + math.sin(angle)
    )
    resistance = max(resistance, 0)

    # 공기 저항을 고려한 출력 제한 속도
    available_power = power * efficiency

    def drag_force(speed):
        return (
            0.5 * air_density * drag_coefficient
            * frontal_area * speed ** 2
        )

    def required_power(speed):
        return (resistance + drag_force(speed)) * speed

    low, high = 0.0, max(wheel_speed, 0.1)

    for _ in range(60):
        mid = (low + high) / 2
        if required_power(mid) <= available_power:
            low = mid
        else:
            high = mid

    speed_mps = min(wheel_speed, low)
    speed_kmh = speed_mps * 3.6

    # 토크와 출력에 따른 구동력 제한
    power_force = available_power / max(speed_mps, 0.25)
    traction_force = min(torque_force, power_force)

    # 순힘과 가속도
    net_force = traction_force - resistance
    acceleration = max(net_force / max(mass, 0.1), 0)

    # 경사로 주행 가능성의 단순 추정
    required_grade_force = mass * g * (
        math.sin(angle)
        + rolling_resistance * math.cos(angle)
    )
    slope_possible = traction_force >= required_grade_force

    # 에너지 소비량 근사
    energy_per_km = average_power / max(speed_kmh, 0.1)

    current = power / max(voltage * efficiency, 0.1)

    return {
        "mass": mass,
        "power": power,
        "wheel_radius": wheel_radius_cm,
        "battery_ah": battery_ah,
        "voltage": voltage,
        "drive_type": drive_type,
        "battery_wh": battery_wh,
        "speed_mps": speed_mps,
        "speed_kmh": speed_kmh,
        "wheel_rpm": wheel_rpm,
        "wheel_torque": wheel_torque,
        "traction_force": traction_force,
        "acceleration": acceleration,
        "runtime_hours": runtime_hours,
        "runtime_minutes": runtime_minutes,
        "energy_per_km": energy_per_km,
        "slope_possible": slope_possible,
        "required_grade_force": required_grade_force,
        "current": current,
        "efficiency_pct": efficiency_pct,
        "motor_rpm": motor_rpm,
        "gear_ratio": gear_ratio,
        "rolling_resistance": rolling_resistance,
        "slope_deg": slope_deg,
    }


# ---------------- 화면 표시 함수 ----------------
def metric_card(label, value, unit):
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        <div class="metric-unit">{unit}</div>
    </div>
    """, unsafe_allow_html=True)


def report_text(name, purpose, result):
    slope = (
        "설정한 경사 조건에서 구동력이 충분할 가능성이 있습니다."
        if result["slope_possible"]
        else "설정한 경사 조건에서 구동력이 부족할 가능성이 있습니다."
    )

    return f"""# ROBO LAB 설계 분석 보고서

## 1. 설계 개요
- 설계 이름: {name}
- 설계 목적: {purpose}
- 로봇 질량: {result['mass']:.1f} kg
- 모터 출력 합계: {result['power']} W
- 구동 방식: {result['drive_type']}
- 바퀴 반지름: {result['wheel_radius']:.1f} cm
- 배터리: {result['voltage']} V / {result['battery_ah']:.1f} Ah

## 2. 예상 성능
- 예상 최고 속도: {result['speed_kmh']:.2f} km/h
- 바퀴 구동력 추정치: {result['traction_force']:.2f} N
- 바퀴 토크 추정치: {result['wheel_torque']:.2f} N·m
- 가속도 추정치: {result['acceleration']:.2f} m/s²
- 예상 작동 시간: {result['runtime_hours']:.2f} h
- 배터리 에너지: {result['battery_wh']:.1f} Wh
- 에너지 소비 추정치: {result['energy_per_km']:.2f} Wh/km
- 경사로 평가: {slope}

## 3. 설계 장점과 한계
모터 출력과 감속비는 구동력 확보에 영향을 주며,
로봇 질량은 가속과 경사로 주행에 영향을 줍니다.
배터리 에너지가 증가하면 일반적으로 작동 시간 증가에 유리합니다.

본 결과는 교육용 근사 모델입니다.
실제 모터의 토크-회전수 곡선, 전류 제한, 타이어 접지력,
배터리 방전 특성 및 실제 주행 시험 결과에 따라 성능이 달라집니다.

## 4. 개선 방향
실제 제작 전 모터 데이터시트와 배터리 사양을 확인하고,
평지와 경사로에서 속도, 전류, 온도 및 작동 시간을 측정해
계산 결과를 검증하는 것이 좋습니다.
"""


# ---------------- 페이지 메뉴 ----------------
# 반드시 page를 먼저 정의한 뒤 페이지 조건문 실행
with st.sidebar:
    st.markdown("## 🤖 ROBO LAB")
    st.caption("ROBOT DESIGN & ENGINEERING SIMULATOR")

    page = st.radio(
        "NAVIGATION",
        [
            "설계 연구소",
            "성능 분석",
            "설계안 비교",
            "분석 보고서",
            "공학 원리",
            "프로젝트 소개"
        ]
    )

    st.divider()
    st.caption("EDUCATIONAL SIMULATION")
    st.caption("계산 결과는 실제 성능의 보증값이 아닙니다.")


# ---------------- 공통 헤더 ----------------
st.markdown("""
<div class="hero">
    <div class="kicker">ROBOT DESIGN & ENGINEERING SIMULATOR</div>
    <h1>ROBO LAB</h1>
    <p>설계하고, 시뮬레이션하고, 더 나은 로봇을 발견하세요.</p>
</div>
""", unsafe_allow_html=True)


# ---------------- 설계 변수 입력 ----------------
with st.sidebar:
    st.markdown("### ROBOT CONFIGURATION")

    robot_name = st.text_input("설계 이름", "ROBO-01")

    purpose = st.selectbox(
        "설계 목적",
        ["범용 주행 로봇", "빠른 이동", "장시간 작동",
         "경사로 주행", "물체 운반"]
    )

    mass = st.slider("로봇 질량 (kg)", 2.0, 20.0, 8.0, 0.5)
    power = st.slider("모터 출력 총합 (W)", 20, 200, 100, 10)
    wheel_radius = st.slider("바퀴 반지름 (cm)", 3.0, 15.0, 8.0, 0.5)

    battery_ah = st.slider("배터리 용량 (Ah)", 2.0, 20.0, 10.0, 0.5)
    voltage = st.select_slider(
        "배터리 전압 (V)",
        options=[12, 18, 24, 36, 48],
        value=24
    )

    drive_type = st.selectbox("구동 방식", ["2륜 구동", "4륜 구동"])

    with st.expander("고급 설정"):
        motor_rpm = st.slider("모터 회전수 (rpm)", 500, 6000, 3000, 100)
        gear_ratio = st.slider("감속비", 1.0, 30.0, 10.0, 0.5)
        efficiency = st.slider("구동계 효율 (%)", 50, 95, 80)
        rolling_resistance = st.slider(
            "구름 저항 계수", 0.005, 0.12, 0.03, 0.005
        )
        slope = st.slider("주행 경사각 (°)", 0.0, 20.0, 5.0, 0.5)


result = calculate_robot(
    mass, power, wheel_radius, battery_ah, voltage,
    drive_type, motor_rpm, gear_ratio, efficiency,
    rolling_resistance, slope
)


# ==================================================
# PAGE 1: 설계 연구소
# ==================================================
if page == "설계 연구소":

    st.markdown('<div class="section-label">01 / ROBOT CONFIGURATION</div>',
                unsafe_allow_html=True)
    st.subheader("로봇의 사양을 설정하세요")
    st.write("왼쪽 메뉴의 값을 바꾸면 성능 결과가 자동으로 갱신됩니다.")

    left, right = st.columns([1, 1.15], gap="large")

    with left:
        st.markdown("### ROBOT SPECIFICATION")

        metric_card("로봇 질량", f"{mass:.1f}", "kg")
        metric_card("모터 출력", f"{power}", "W")
        metric_card("배터리 에너지", f"{result['battery_wh']:.0f}", "Wh")

        st.markdown("### DRIVE SYSTEM")
        st.write(f"구동 방식: **{drive_type}**")
        st.write(f"모터 회전수: **{motor_rpm:,} rpm**")
        st.write(f"감속비: **{gear_ratio:.1f}:1**")
        st.write(f"구동계 효율 가정: **{efficiency}%**")

    with right:
        st.markdown('<div class="section-label">PERFORMANCE ANALYSIS</div>',
                    unsafe_allow_html=True)

        c1, c2 = st.columns(2)
        with c1:
            metric_card("예상 최고 속도", f"{result['speed_kmh']:.2f}", "km/h")
            metric_card("바퀴 구동력", f"{result['traction_force']:.2f}", "N · 추정치")
            metric_card("가속도", f"{result['acceleration']:.2f}", "m/s² · 추정치")
        with c2:
            metric_card("예상 작동 시간", f"{result['runtime_hours']:.2f}", "시간")
            metric_card("바퀴 토크", f"{result['wheel_torque']:.2f}", "N·m · 추정치")
            metric_card("에너지 소비량", f"{result['energy_per_km']:.2f}", "Wh/km · 추정치")

        st.markdown("### 경사로 주행 분석")
        if result["slope_possible"]:
            st.success(f"{slope:.1f}° 경사: 단순 모델에서 구동력 확보 가능성이 있습니다.")
        else:
            st.warning(f"{slope:.1f}° 경사: 구동력이 부족할 가능성이 있습니다.")

    st.divider()
    st.markdown("### 질량에 따른 가속도 변화")

    mass_values = [x / 2 for x in range(4, 41)]
    acceleration_values = []

    for m in mass_values:
        r = calculate_robot(
            m, power, wheel_radius, battery_ah, voltage,
            drive_type, motor_rpm, gear_ratio, efficiency,
            rolling_resistance, slope
        )
        acceleration_values.append({
            "질량 (kg)": m,
            "가속도 (m/s²)": r["acceleration"]
        })

    mass_df = pd.DataFrame(acceleration_values).set_index("질량 (kg)")
    st.line_chart(mass_df)

    st.info(
        "같은 순힘에서 질량이 증가하면 가속도는 작아지는 경향이 있습니다. "
        "실제 결과는 모터 특성, 접지력, 감속비 및 주행 저항에도 영향을 받습니다."
    )


# ==================================================
# PAGE 2: 성능 분석
# ==================================================
elif page == "성능 분석":

    st.markdown('<div class="section-label">02 / PERFORMANCE ANALYSIS</div>',
                unsafe_allow_html=True)
    st.subheader("설계 변수별 성능 변화")

    tab1, tab2, tab3 = st.tabs(
        ["모터 출력", "로봇 질량", "배터리 용량"]
    )

    with tab1:
        rows = []
        for p in range(20, 201, 10):
            r = calculate_robot(
                mass, p, wheel_radius, battery_ah, voltage,
                drive_type, motor_rpm, gear_ratio, efficiency,
                rolling_resistance, slope
            )
            rows.append({
                "모터 출력 (W)": p,
                "최고 속도 (km/h)": r["speed_kmh"],
                "구동력 (N)": r["traction_force"],
                "가속도 (m/s²)": r["acceleration"]
            })

        df = pd.DataFrame(rows).set_index("모터 출력 (W)")
        st.markdown("#### 모터 출력에 따른 최고 속도와 구동력")
        st.line_chart(df[["최고 속도 (km/h)", "구동력 (N)"]])
        st.markdown("#### 모터 출력에 따른 가속도")
        st.line_chart(df[["가속도 (m/s²)"]])
        st.dataframe(df.round(2), use_container_width=True)

    with tab2:
        rows = []
        for m in [x / 2 for x in range(4, 41)]:
            r = calculate_robot(
                m, power, wheel_radius, battery_ah, voltage,
                drive_type, motor_rpm, gear_ratio, efficiency,
                rolling_resistance, slope
            )
            rows.append({
                "질량 (kg)": m,
                "가속도 (m/s²)": r["acceleration"],
                "필요 구동력 (N)": r["required_grade_force"]
            })

        df = pd.DataFrame(rows).set_index("질량 (kg)")
        st.line_chart(df)
        st.dataframe(df.round(2), use_container_width=True)

    with tab3:
        rows = []
        for ah in [x / 2 for x in range(4, 41)]:
            r = calculate_robot(
                mass, power, wheel_radius, ah, voltage,
                drive_type, motor_rpm, gear_ratio, efficiency,
                rolling_resistance, slope
            )
            rows.append({
                "배터리 용량 (Ah)": ah,
                "작동 시간 (h)": r["runtime_hours"],
                "에너지 (Wh)": r["battery_wh"]
            })

        df = pd.DataFrame(rows).set_index("배터리 용량 (Ah)")
        st.line_chart(df)
        st.dataframe(df.round(2), use_container_width=True)

    st.caption(
        "그래프는 현재 설정을 기준으로 한 교육용 계산 결과입니다. "
        "각 지표의 단위가 다르므로 수치표도 함께 확인하세요."
    )


# ==================================================
# PAGE 3: 설계안 비교
# ==================================================
elif page == "설계안 비교":

    st.markdown('<div class="section-label">03 / DESIGN COMPARISON</div>',
                unsafe_allow_html=True)
    st.subheader("A 로봇과 B 로봇의 성능 비교")
    st.write("A 로봇은 현재 설계값을 사용합니다. B 로봇의 사양을 별도로 설정하세요.")

    st.markdown("### A ROBOT")
    st.write(
        f"{robot_name} · {mass:.1f} kg · {power} W · "
        f"{voltage} V · {battery_ah:.1f} Ah"
    )

    a, b = st.columns(2)

    with a:
        st.markdown("### A 로봇 · 현재 설계")
        st.metric("최고 속도", f"{result['speed_kmh']:.2f} km/h")
        st.metric("구동력", f"{result['traction_force']:.2f} N")
        st.metric("작동 시간", f"{result['runtime_hours']:.2f} h")
        st.metric("가속도", f"{result['acceleration']:.2f} m/s²")

    with b:
        st.markdown("### B 로봇 · 비교 설계")

        b_mass = st.slider("B 질량 (kg)", 2.0, 20.0, 10.0, 0.5)
        b_power = st.slider("B 모터 출력 (W)", 20, 200, 120, 10)
        b_radius = st.slider("B 바퀴 반지름 (cm)", 3.0, 15.0, 8.0, 0.5)
        b_ah = st.slider("B 배터리 용량 (Ah)", 2.0, 20.0, 12.0, 0.5)
        b_voltage = st.select_slider(
            "B 배터리 전압 (V)", [12, 18, 24, 36, 48], value=24
        )
        b_drive = st.selectbox("B 구동 방식", ["2륜 구동", "4륜 구동"])

        rb = calculate_robot(
            b_mass, b_power, b_radius, b_ah, b_voltage,
            b_drive, motor_rpm, gear_ratio, efficiency,
            rolling_resistance, slope
        )

        st.metric("최고 속도", f"{rb['speed_kmh']:.2f} km/h")
        st.metric("구동력", f"{rb['traction_force']:.2f} N")
        st.metric("작동 시간", f"{rb['runtime_hours']:.2f} h")
        st.metric("가속도", f"{rb['acceleration']:.2f} m/s²")

    comparison = pd.DataFrame({
        "항목": [
            "질량 (kg)", "모터 출력 (W)", "최고 속도 (km/h)",
            "구동력 (N)", "작동 시간 (h)", "가속도 (m/s²)",
            "배터리 에너지 (Wh)"
        ],
        "A 로봇": [
            mass, power, result["speed_kmh"],
            result["traction_force"], result["runtime_hours"],
            result["acceleration"], result["battery_wh"]
        ],
        "B 로봇": [
            b_mass, b_power, rb["speed_kmh"],
            rb["traction_force"], rb["runtime_hours"],
            rb["acceleration"], rb["battery_wh"]
        ]
    })

    st.markdown("### 성능 비교표")
    st.dataframe(comparison.round(2), use_container_width=True, hide_index=True)

    faster = "A 로봇" if result["speed_kmh"] >= rb["speed_kmh"] else "B 로봇"
    longer = "A 로봇" if result["runtime_hours"] >= rb["runtime_hours"] else "B 로봇"
    stronger = "A 로봇" if result["traction_force"] >= rb["traction_force"] else "B 로봇"

    st.markdown("### 자동 평가")
    st.write(f"- 속도 중심 설계: **{faster}**의 예상 최고 속도가 더 높습니다.")
    st.write(f"- 장시간 작동: **{longer}**의 예상 작동 시간이 더 깁니다.")
    st.write(f"- 구동력 중심 설계: **{stronger}**의 추정 구동력이 더 큽니다.")

    st.caption("실제 설계 선택 시 안전 여유, 비용, 모터 사양과 배터리 무게도 고려하세요.")


# ==================================================
# PAGE 4: 분석 보고서
# ==================================================
elif page == "분석 보고서":

    st.markdown('<div class="section-label">04 / DESIGN REPORT</div>',
                unsafe_allow_html=True)
    st.subheader("설계 분석 보고서")
    st.write("현재 입력한 사양과 계산 결과를 보고서로 생성합니다.")

    report = report_text(robot_name, purpose, result)
    st.markdown(report)

    st.download_button(
        "📄 보고서 다운로드 (Markdown)",
        data=report.encode("utf-8"),
        file_name="robo_lab_report.md",
        mime="text/markdown",
        use_container_width=True
    )

    result_csv = pd.DataFrame([{
        "설계 이름": robot_name,
        "설계 목적": purpose,
        "질량(kg)": mass,
        "모터 출력(W)": power,
        "바퀴 반지름(cm)": wheel_radius,
        "구동 방식": drive_type,
        "배터리 전압(V)": voltage,
        "배터리 용량(Ah)": battery_ah,
        "최고 속도(km/h)": result["speed_kmh"],
        "구동력(N)": result["traction_force"],
        "작동 시간(h)": result["runtime_hours"],
        "가속도(m/s^2)": result["acceleration"],
        "에너지 소비(Wh/km)": result["energy_per_km"]
    }]).to_csv(index=False).encode("utf-8-sig")

    st.download_button(
        "📊 계산 결과 CSV 다운로드",
        data=result_csv,
        file_name="robo_lab_results.csv",
        mime="text/csv",
        use_container_width=True
    )


# ==================================================
# PAGE 5: 공학 원리
# ==================================================
elif page == "공학 원리":

    st.markdown('<div class="section-label">05 / ENGINEERING PRINCIPLES</div>',
                unsafe_allow_html=True)
    st.subheader("로봇에 적용되는 물리·공학 원리")

    with st.expander("1. 배터리 에너지", expanded=True):
        st.latex(r"E = VQ")
        st.write("전압(V)과 용량(Ah)의 곱으로 배터리 에너지(Wh)를 근사합니다.")

    with st.expander("2. 감속비와 바퀴 회전수"):
        st.latex(r"n_{wheel} = \frac{n_{motor}}{G}")
        st.write("감속비가 커지면 바퀴 회전수는 감소하고, 일반적으로 바퀴 토크 확보에 유리합니다.")

    with st.expander("3. 힘과 가속도"):
        st.latex(r"F_{net} = ma")
        st.write("같은 순힘에서 질량이 증가하면 가속도는 작아집니다.")

    with st.expander("4. 전력과 속도"):
        st.latex(r"P = Fv")
        st.write("같은 출력에서는 더 큰 힘을 낼수록 가능한 속도가 낮아질 수 있습니다.")

    with st.expander("5. 경사로 주행"):
        st.latex(r"F_{grade} = mg\sin\theta")
        st.write("경사각이 커질수록 중력에 맞서 필요한 구동력이 증가합니다.")

    st.warning(
        "이 시뮬레이터는 교육용 근사 모델입니다. "
        "실제 제작 전에는 모터 토크-회전수 곡선, 전류 제한, "
        "타이어 접지력과 배터리 방전 특성을 확인해야 합니다."
    )


# ==================================================
# PAGE 6: 프로젝트 소개
# ==================================================
elif page == "프로젝트 소개":

    st.markdown('<div class="section-label">06 / ABOUT ROBO LAB</div>',
                unsafe_allow_html=True)
    st.subheader("ROBO LAB 프로젝트")

    st.write(
        "ROBO LAB은 로봇의 질량, 모터, 바퀴, 배터리 등의 설계 변수를 바꾸며 "
        "기계공학과 물리학의 원리가 로봇 성능에 미치는 영향을 탐구하는 "
        "교육용 시뮬레이터입니다."
    )

    st.markdown("### 주요 기능")
    st.markdown("""
    - 로봇 사양을 직접 설정하는 설계 연구소
    - 성능 자동 계산과 변수별 그래프 분석
    - A 로봇과 B 로봇의 성능 비교
    - 설계 분석 보고서와 CSV 파일 생성
    - 물리·기계공학 공식과 원리 설명
    """)

    st.markdown("### 계산 모델의 가정")
    st.markdown("""
    - 모터 출력은 전체 모터의 합산 출력으로 입력합니다.
    - 평균 전력 소비량은 정격 출력의 70%로 가정합니다.
    - 배터리 사용 가능 에너지는 명목 에너지의 85%로 가정합니다.
    - 실제 모터 특성, 접지력, 제어기 및 배터리 성능은 단순화되어 있습니다.
    """)

    st.info(
        "탐구 보고서에는 계산 결과뿐 아니라 사용한 가정과 모델의 한계도 기록하세요."
    )


# ---------------- Footer ----------------
st.divider()
st.caption(
    "ROBO LAB · Educational Engineering Simulator · "
    "모든 성능 값은 근사 추정치이며 실제 성능을 보장하지 않습니다."
)
