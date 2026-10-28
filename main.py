
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
   선택창 가독성 개선: 선택된 값은 밝은 배경 + 진한 글자,
   펼쳐진 목록은 어두운 배경 + 밝은 글자
--------------------------------------------------------- */

/* 선택창 바깥 영역 */
[data-testid="stSelectbox"] [data-baseweb="select"] {
    background-color: #f8fbff !important;
    border-radius: 8px !important;
}

/* 선택창 실제 입력 영역 */
[data-testid="stSelectbox"] [data-baseweb="select"] > div,
[data-testid="stSelectbox"] [data-baseweb="select"] [role="combobox"] {
    background-color: #f8fbff !important;
    border: 1.5px solid #65e2d1 !important;
    border-radius: 8px !important;
    min-height: 42px !important;
}

/* 선택되어 있는 항목의 글자: 흰 배경에서 진한 남색으로 표시 */
[data-testid="stSelectbox"] [data-baseweb="select"] *,
[data-testid="stSelectbox"] [data-baseweb="select"] span,
[data-testid="stSelectbox"] [data-baseweb="select"] div {
    color: #102033 !important;
    -webkit-text-fill-color: #102033 !important;
    font-weight: 700 !important;
    opacity: 1 !important;
}

/* 선택창 화살표 */
[data-testid="stSelectbox"] [data-baseweb="select"] svg {
    fill: #176b67 !important;
    color: #176b67 !important;
    opacity: 1 !important;
}

/* 펼쳐지는 옵션 목록 */
ul[data-baseweb="menu"],
div[data-baseweb="popover"] ul {
    background-color: #101c2e !important;
    border: 1px solid #65e2d1 !important;
}

/* 옵션 목록의 글자 */
ul[data-baseweb="menu"] *,
div[data-baseweb="popover"] ul * {
    color: #f2f7ff !important;
    -webkit-text-fill-color: #f2f7ff !important;
