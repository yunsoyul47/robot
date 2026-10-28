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
    
