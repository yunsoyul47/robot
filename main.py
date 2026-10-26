import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="ROBO LAB",
    page_icon="🤖",
    layout="wide"
)

# 1. 페이지 메뉴를 먼저 정의
st.sidebar.title("🤖 ROBO LAB")

page = st.sidebar.radio(
    "메뉴 선택",
    ["설계 연구소", "성능 분석", "설계안 비교", "공학 원리", "프로젝트 소개"]
)

# 2. page 변수를 정의한 다음 조건문 실행
if page == "설계 연구소":
    st.title("🤖 로봇 설계 연구소")
    st.write("로봇의 구조와 성능을 설계해 보세요.")

elif page == "성능 분석":
    st.title("📊 로봇 성능 분석")
    st.write("설계한 로봇의 성능을 분석합니다.")

elif page == "설계안 비교":
    st.title("⚖️ 설계안 비교")
    st.write("여러 로봇 설계안을 비교합니다.")

elif page == "공학 원리":
    st.title("⚙️ 로봇 공학 원리")
    st.write("로봇에 적용되는 물리 및 공학 원리를 알아봅니다.")

elif page == "프로젝트 소개":
    st.title("📘 프로젝트 소개")
    st.write("ROBO LAB 프로젝트를 소개합니다.")
