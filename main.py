
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
