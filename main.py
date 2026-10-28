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
