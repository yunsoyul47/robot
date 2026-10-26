
defaults_a = {
    "name": "Explorer A", "mass": 8.0, "payload": 2.0, "motor_w": 100,
    "motor_count": 2, "motor_rpm": 3000, "gear_ratio": 10.0,
    "wheel_radius": 8.0, "battery_v": 24, "battery_ah": 8.0,
    "efficiency": 80, "rolling": 0.03, "slope": 0,
}
defaults_b = {
    "name": "Endurance B", "mass": 7.0, "payload": 1.0, "motor_w": 60,
    "motor_count": 2, "motor_rpm": 2500, "gear_ratio": 12.0,
    "wheel_radius": 7.0, "battery_v": 24, "battery_ah": 12.0,
    "efficiency": 85, "rolling": 0.025, "slope": 0,
}

if page == "설계 연구소":
    st.markdown('<div class="section-kicker">01 / CONFIGURATION</div>', unsafe_allow_html=True)
    st.header("로봇 설계")
    st.write("왼쪽 메뉴에서 설계 목표를 선택하고, 아래에서 로봇의 사양을 조절하세요.")

    params, result = make_design("A", defaults_a)
    left, right = st.columns([1.1, 0.9], gap="large")
    with left:
        st.markdown('<div class="section-kicker">DESIGN PREVIEW</div>', unsafe_allow_html=True)
        st.markdown(robot_svg(params["wheel_radius"], result["total_mass"], params["motor_count"]), unsafe_allow_html=True)
        st.caption("개념도: 실제 크기·부품 배치·CAD 형상을 나타내지 않습니다.")
    with right:
        st.markdown('<div class="section-kicker">PERFORMANCE OUTPUT</div>', unsafe_allow_html=True)
        m1, m2 = st.columns(2)
        m1.metric("예상 최고 속도", f'{result["speed_kmh"]:.1f} km/h')
        m2.metric("예상 작동 시간", f'{result["runtime_minutes"]:.0f} min')
        m3, m4 = st.columns(2)
        m3.metric("이론적 구동력", f'{result["traction_force"]:.1f} N')
        m4.metric("추정 가속도", f'{result["accel"]:.2f} m/s²')
        m5, m6 = st.columns(2)
        m5.metric("배터리 에너지", f'{result["battery_wh"]:.0f} Wh')
        m6.metric("총 모터 출력", f'{result["total_motor_power"]} W')

    st.markdown("---")
    st.markdown('<div class="section-kicker">02 / PERFORMANCE ANALYSIS</div>', unsafe_allow_html=True)
    st.header("성능 분석")
    masses = list(range(2, 21, 2))
    mass_rows = []
    for test_mass in masses:
        test = calculate_robot(
            test_mass, params["motor_w"], params["motor_rpm"], params["gear_ratio"],
            params["wheel_radius"], params["battery_v"], params["battery_ah"],
            params["efficiency"], params["motor_count"], params["rolling"],
            params["slope"], params["payload"]
        )
        mass_rows.append({"차체 질량 (kg)": test_mass, "추정 가속도 (m/s²)": test["accel"],
                          "예상 최고 속도 (km/h)": test["speed_kmh"]})
    graph1, graph2 = st.columns(2)
    with graph1:
        st.markdown("**차체 질량과 가속도**")
        st.line_chart(pd.DataFrame(mass_rows).set_index("차체 질량 (kg)")["추정 가속도 (m/s²)"])
    with graph2:
        st.markdown("**차체 질량과 최고 속도**")
        st.line_chart(pd.DataFrame(mass_rows).set_index("차체 질량 (kg)")["예상 최고 속도 (km/h)"])

    st.markdown("### 설계 진단")
    diagnostics = []
    if result["net_force"] <= 0:
        diagnostics.append("현재 설정에서 모델상 저항을 이길 여유 구동력이 없습니다. 모터·감속비·바퀴·경사 조건을 확인하세요.")
    else:
        diagnostics.append("모델상 구동력은 설정된 주행 저항보다 큽니다. 실제 가속 성능은 토크 곡선과 접지력에 따라 달라집니다.")
    if result["speed_kmh"] > 25:
        diagnostics.append("추정 속도가 높습니다. 실제 제작 시 제동, 안정성, 모터 회전수 및 안전 제한을 별도로 검토하세요.")
    if result["runtime_minutes"] < 30:
        diagnostics.append("추정 작동 시간이 짧습니다. 배터리 용량을 늘리거나 평균 소비 전력을 줄이는 설계를 검토하세요.")
    if params["slope"] > 10:
        diagnostics.append("경사각이 큽니다. 무게중심, 전복 위험, 바퀴 접지력 및 제동 성능을 추가로 검토해야 합니다.")
    if params["payload"] > params["mass"]:
        diagnostics.append("적재 질량이 차체 질량보다 큽니다. 구조 강도와 구동부 하중을 확인하세요.")
    for d in diagnostics:
        st.info(d)

    report = pd.DataFrame([
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
    ], columns=["항목", "값", "단위"])
    csv_data = report.to_csv(index=False).encode("utf-8-sig")
    st.download_button("⬇ 설계 보고서 CSV 다운로드", data=csv_data, file_name="robo_lab_design_report.csv", mime="text/csv")

elif page == "설계안 비교":
    st.markdown('<div class="section-kicker">03 / DESIGN COMPARISON</div>', unsafe_allow_html=True)
    st.header("두 설계안 비교")
    st.write("두 로봇의 조건을 조절하고 성능 차이를 비교해 보세요.")
    col_a, col_b = st.columns(2, gap="large")
    with col_a:
        pa, ra = make_design("A", defaults_a)
    with col_b:
        pb, rb = make_design("B", defaults_b)

    st.markdown("---")
    st.subheader("성능 비교 결과")
    compare = pd.DataFrame({
        "항목": ["총 이동 질량 (kg)", "총 모터 출력 (W)", "예상 최고 속도 (km/h)",
                 "추정 가속도 (m/s²)", "이론적 구동력 (N)", "배터리 에너지 (Wh)",
                 "예상 작동 시간 (min)", "추정 주행 가능 거리 (km)"],
        pa["name"]: [ra["total_mass"], ra["total_motor_power"], ra["speed_kmh"], ra["accel"],
                     ra["traction_force"], ra["battery_wh"], ra["runtime_minutes"], ra["range_km"]],
        pb["name"]: [rb["total_mass"], rb["total_motor_power"], rb["speed_kmh"], rb["accel"],
                     rb["traction_force"], rb["battery_wh"], rb["runtime_minutes"], rb["range_km"]],
    })
    st.dataframe(compare.set_index("항목").style.format("{:.2f}"), use_container_width=True)
    chart_df = pd.DataFrame({
        "성능 지표": ["최고 속도 (km/h)", "가속도 (m/s²)", "작동 시간 (min)"],
        pa["name"]: [ra["speed_kmh"], ra["accel"], ra["runtime_minutes"]],
        pb["name"]: [rb["speed_kmh"], rb["accel"], rb["runtime_minutes"]],
    }).set_index("성능 지표")
    st.bar_chart(chart_df)
    st.markdown("### 비교 분석")
    speed_winner = pa["name"] if ra["speed_kmh"] > rb["speed_kmh"] else pb["name"] if rb["speed_kmh"] > ra["speed_kmh"] else "두 설계안이 동일"
    runtime_winner = pa["name"] if ra["runtime_minutes"] > rb["runtime_minutes"] else pb["name"] if rb["runtime_minutes"] > ra["runtime_minutes"] else "두 설계안이 동일"
    st.success(f"속도 측면: **{speed_winner}** 설계안의 모델상 최고 속도가 더 높습니다.")
    st.success(f"작동 시간 측면: **{runtime_winner}** 설계안의 추정 작동 시간이 더 깁니다.")
    st.caption("속도와 작동 시간은 단순화한 모델의 추정치이며, 실제 주행 시험 결과와 다를 수 있습니다.")
    st.download_button("⬇ 비교 결과 CSV 다운로드", data=compare.to_csv(index=False).encode("utf-8-sig"),
                       file_name="robo_lab_comparison.csv", mime="text/csv")

elif page == "공학 원리":
    st.markdown('<div class="section-kicker">04 / ENGINEERING NOTES</div>', unsafe_allow_html=True)
    st.header("계산에 사용한 공학 원리")
    st.write("이 시뮬레이터는 기본적인 물리 관계를 이용해 설계 조건의 영향을 탐색합니다.")
    with st.expander("1. 배터리 에너지", expanded=True):
        st.latex(r"E = VQ")
        st.write("전압 V와 용량 Q(Ah)를 곱하면 Wh 단위의 명목 에너지를 추정할 수 있습니다. 실제 사용 가능 에너지는 배터리 화학, 방전율, 온도, 보호회로에 따라 달라집니다.")
    with st.expander("2. 바퀴의 선속도"):
        st.latex(r"v = r\omega")
        st.write("바퀴 반지름 r과 각속도 ω로 이상적인 선속도를 계산합니다. 감속기를 사용하면 출력 회전수는 모터 회전수를 감속비로 나눈 값으로 근사합니다.")
    with st.expander("3. 토크와 구동력"):
        st.latex(r"F = \frac{\tau}{r}")
        st.write("바퀴 토크 τ가 커지면 이상적인 구동력이 커지고, 바퀴 반지름이 커지면 같은 토크에서 구동력은 작아집니다. 접지력 한계와 모터 토크 곡선은 이 간단한 모델에 완전히 포함되어 있지 않습니다.")
    with st.expander("4. 뉴턴의 운동 법칙"):
        st.latex(r"a = \frac{F_{\mathrm{net}}}{m}")
        st.write("가속도는 알짜힘을 질량으로 나눈 값입니다. 실제 로봇에는 회전 관성, 구동 손실, 모터의 토크 변화, 제어 알고리즘 등이 영향을 줍니다.")
    with st.expander("5. 작동 시간 근사"):
        st.latex(r"t \approx \frac{E_{\mathrm{usable}}}{P_{\mathrm{average}}}")
        st.write("평균 소비 전력이 커질수록 작동 시간은 짧아집니다. 이 앱은 명목 배터리 에너지의 85%를 사용 가능 에너지로 가정하고, 모터 정격 출력의 일정 비율을 평균 소비 전력으로 가정합니다.")
    st.warning("교육용 단순 모델입니다. 안전이 중요한 실제 로봇의 제작·운용을 위한 검증된 설계 도구가 아닙니다.")

else:
    st.markdown('<div class="section-kicker">05 / ABOUT THE PROJECT</div>', unsafe_allow_html=True)
    st.header("프로젝트 정보")
    st.markdown(
        """
        ### 프로젝트 목표
        로봇의 기계적 사양을 바꾸며 물리 법칙과 설계 선택이 예상 성능에 어떤 영향을 주는지 탐구합니다.

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

        이 앱은 인터넷에서 이미지나 외부 API를 불러오지 않아도 계산과 시각화 기능이 작동합니다. 다만 CSS의 웹 폰트는 인터넷 연결이 가능할 때만 적용되며, 연결이 없으면 기본 글꼴로 표시됩니다.
        """
    )

st.markdown('<div class="footer">ROBO LAB · EDUCATIONAL ROBOT DESIGN SIMULATOR · ESTIMATES ONLY</div>', unsafe_allow_html=True)
