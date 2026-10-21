import streamlit as st

def apply_sahara_theme():
    """
    Applies the Sahara warm-minimalist spatial UI theme across Streamlit components.
    Tokens:
      - Canvas / Base Background: #FAF8F5 (warm cream / alabaster)
      - Surface High / Card:      #FFFFFF and #F4EFEA
      - Border / Divider:         #E8DFD5 (subtle 1px hairline)
      - Primary Accent:           #C2652A (Sun-baked Terracotta)
      - Primary Hover:            #A9531F
      - Text Primary (Headings):  #26211C (Deep warm espresso - EB Garamond)
      - Text Secondary (Body):    #6B6258 (Muted warm taupe - Manrope)
      - Text Muted:               #968D82
      - Status / Accent:          #16A34A (Green), #C2652A (Warm), #DC2626 (Critical)
    """
    theme_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400..800;1,400..800&family=Manrope:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

    /* ── Root Foundation ────────────────────────────────────────────── */
    :root {
        --sahara-bg: #FAF8F5;
        --sahara-surface: #FFFFFF;
        --sahara-surface-alt: #F4EFEA;
        --sahara-border: #E8DFD5;
        --sahara-primary: #C2652A;
        --sahara-primary-hover: #A9531F;
        --sahara-text-primary: #26211C;
        --sahara-text-secondary: #6B6258;
        --sahara-text-muted: #968D82;
        --sahara-radius: 8px;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FAF8F5 !important;
        font-family: 'Manrope', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #26211C !important;
    }

    [data-testid="stHeader"] {
        background-color: rgba(250, 248, 245, 0.88) !important;
        backdrop-filter: blur(12px) !important;
        border-bottom: 1px solid #E8DFD5 !important;
    }

    [data-testid="stMainBlockContainer"] {
        background-color: #FAF8F5 !important;
        padding-top: 2rem !important;
        padding-bottom: 3rem !important;
    }

    /* ── Typography ─────────────────────────────────────────────────── */
    h1, h2, h3, h4 {
        font-family: 'EB Garamond', Georgia, serif !important;
        color: #26211C !important;
        font-weight: 600 !important;
        letter-spacing: -0.015em !important;
        line-height: 1.25 !important;
    }

    h5, h6 {
        font-family: 'Manrope', sans-serif !important;
        color: #26211C !important;
        font-weight: 700 !important;
        letter-spacing: -0.01em !important;
    }

    p, span, label, div {
        font-family: 'Manrope', sans-serif;
    }

    /* ── Sidebar Shell ──────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background-color: #F4EFEA !important;
        border-right: 1px solid #E8DFD5 !important;
    }

    [data-testid="stSidebar"] * {
        font-family: 'Manrope', sans-serif !important;
    }

    [data-testid="stSidebarUserContent"] {
        display: flex !important;
        flex-direction: column !important;
        min-height: 94vh !important;
        padding: 1rem 0.8rem !important;
    }

    /* ── Streamlit Native Buttons ───────────────────────────────────── */
    .stButton > button {
        background-color: #FFFFFF !important;
        color: #6B6258 !important;
        border: 1px solid #E8DFD5 !important;
        border-radius: 8px !important;
        padding: 0.55rem 1.1rem !important;
        font-family: 'Manrope', sans-serif !important;
        font-size: 0.9rem !important;
        font-weight: 600 !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 1px 2px rgba(38,33,28,0.03) !important;
    }

    .stButton > button:hover {
        background-color: #F4EFEA !important;
        color: #C2652A !important;
        border-color: #C2652A !important;
        box-shadow: 0 2px 6px rgba(194,101,42,0.12) !important;
        transform: translateY(-1px) !important;
    }

    /* Primary Buttons & Form Submit Buttons */
    .stButton > button[kind="primary"],
    .stButton > button[data-testid="baseButton-primary"],
    button[kind="primaryFormSubmit"] {
        background-color: #C2652A !important;
        color: #FFFFFF !important;
        border: 1px solid #C2652A !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 8px rgba(194,101,42,0.22) !important;
    }

    .stButton > button[kind="primary"]:hover,
    .stButton > button[data-testid="baseButton-primary"]:hover,
    button[kind="primaryFormSubmit"]:hover {
        background-color: #A9531F !important;
        border-color: #A9531F !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 14px rgba(169,83,31,0.28) !important;
        transform: translateY(-1px) !important;
    }

    /* ── Streamlit Form Inputs & Controls ───────────────────────────── */
    div[data-baseweb="input"],
    div[data-baseweb="textarea"],
    div[data-baseweb="select"] > div {
        background-color: #FFFFFF !important;
        border: 1px solid #E8DFD5 !important;
        border-radius: 8px !important;
        color: #26211C !important;
        box-shadow: 0 1px 2px rgba(38,33,28,0.02) !important;
    }

    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="textarea"]:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border-color: #C2652A !important;
        box-shadow: 0 0 0 3px rgba(194,101,42,0.14) !important;
    }

    input, textarea, select {
        color: #26211C !important;
        font-family: 'Manrope', sans-serif !important;
    }

    /* File Uploader */
    [data-testid="stFileUploader"] {
        background-color: #FFFFFF !important;
        border: 1px dashed #D5C4B5 !important;
        border-radius: 8px !important;
        padding: 1rem !important;
        transition: border-color 0.2s ease !important;
    }

    [data-testid="stFileUploader"]:hover {
        border-color: #C2652A !important;
    }

    [data-testid="stFileUploader"] section {
        background-color: transparent !important;
    }

    /* Expanders */
    [data-testid="stExpander"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E8DFD5 !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 3px rgba(38,33,28,0.03) !important;
        margin-bottom: 0.75rem !important;
    }

    [data-testid="stExpander"] summary {
        font-family: 'EB Garamond', Georgia, serif !important;
        font-size: 1.05rem !important;
        font-weight: 600 !important;
        color: #26211C !important;
    }

    /* Checkboxes */
    [data-testid="stCheckbox"] label span {
        color: #26211C !important;
        font-family: 'Manrope', sans-serif !important;
        font-size: 0.92rem !important;
    }

    /* Sliders */
    [data-testid="stSlider"] > div > div > div > div {
        background-color: #C2652A !important;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        font-family: 'Manrope', sans-serif !important;
        font-weight: 600 !important;
        color: #6B6258 !important;
        border-radius: 6px 6px 0 0 !important;
        padding: 0.5rem 1.2rem !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #C2652A !important;
        border-bottom-color: #C2652A !important;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'EB Garamond', Georgia, serif !important;
        font-size: 2.2rem !important;
        font-weight: 600 !important;
        color: #26211C !important;
    }

    [data-testid="stMetricLabel"] {
        font-family: 'Manrope', sans-serif !important;
        font-size: 0.75rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        color: #968D82 !important;
        font-weight: 600 !important;
    }

    /* Alerts */
    [data-testid="stAlert"] {
        border-radius: 8px !important;
        font-family: 'Manrope', sans-serif !important;
    }

    div[data-testid="stAlert"][data-test-color="info"] {
        background-color: #F4EFEA !important;
        color: #26211C !important;
        border: 1px solid #E8DFD5 !important;
    }

    div[data-testid="stAlert"][data-test-color="success"] {
        background-color: #F0FDF4 !important;
        color: #166534 !important;
        border: 1px solid #BBF7D0 !important;
    }

    div[data-testid="stAlert"][data-test-color="warning"] {
        background-color: #FFFBEB !important;
        color: #92400E !important;
        border: 1px solid #FDE68A !important;
    }

    div[data-testid="stAlert"][data-test-color="error"] {
        background-color: #FEF2F2 !important;
        color: #991B1B !important;
        border: 1px solid #FECACA !important;
    }

    /* Chat Messages */
    [data-testid="stChatMessage"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E8DFD5 !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 3px rgba(38,33,28,0.03) !important;
        padding: 1.2rem !important;
        margin-bottom: 0.8rem !important;
    }

    [data-testid="stChatMessage"][data-testid*="user"] {
        background-color: #F4EFEA !important;
        border: 1px solid #E8DFD5 !important;
    }

    [data-testid="stChatInput"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E8DFD5 !important;
        border-radius: 8px !important;
    }

    /* ── Sahara Spatial Card & Header Design System Classes ──────────── */
    .sahara-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E8DFD5 !important;
        border-radius: 8px !important;
        padding: 1.6rem !important;
        margin-bottom: 1.25rem !important;
        box-shadow: 0 1px 3px rgba(38, 33, 28, 0.04), 0 4px 12px rgba(38, 33, 28, 0.02) !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease, transform 0.2s ease !important;
    }

    .sahara-card:hover {
        border-color: #D5C4B5 !important;
        box-shadow: 0 4px 16px rgba(38, 33, 28, 0.06) !important;
        transform: translateY(-1px);
    }

    .sahara-card-alt {
        background-color: #F4EFEA !important;
        border: 1px solid #E8DFD5 !important;
        border-radius: 8px !important;
        padding: 1.4rem !important;
        margin-bottom: 1.2rem !important;
    }

    .sahara-header {
        padding: 1.8rem 0 1.2rem 0;
        border-bottom: 1px solid #E8DFD5;
        margin-bottom: 1.8rem;
    }

    .sahara-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        background-color: rgba(194, 101, 42, 0.08);
        border: 1px solid rgba(194, 101, 42, 0.24);
        border-radius: 20px;
        padding: 0.25rem 0.8rem;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
        color: #C2652A;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }

    .sahara-title {
        font-family: 'EB Garamond', Georgia, serif;
        font-size: 2.35rem;
        font-weight: 600;
        color: #26211C;
        letter-spacing: -0.015em;
        line-height: 1.2;
        margin: 0.2rem 0 0.4rem 0;
    }

    .sahara-subtitle {
        font-family: 'Manrope', sans-serif;
        font-size: 0.92rem;
        color: #6B6258;
        max-width: 680px;
        line-height: 1.6;
    }

    /* Backward compatibility mappings for existing page classes */
    .dash-header {
        padding: 1.8rem 0 1.2rem 0;
        border-bottom: 1px solid #E8DFD5;
        margin-bottom: 1.8rem;
    }

    .dash-welcome {
        font-family: 'EB Garamond', Georgia, serif !important;
        font-size: 2.35rem !important;
        font-weight: 600 !important;
        color: #26211C !important;
        letter-spacing: -0.015em !important;
        margin: 0.2rem 0 0.4rem 0 !important;
    }

    .dash-welcome span {
        color: #C2652A !important;
        font-style: italic;
    }

    .dash-role-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        background-color: rgba(194, 101, 42, 0.08);
        border: 1px solid rgba(194, 101, 42, 0.24);
        border-radius: 20px;
        padding: 0.25rem 0.8rem;
        font-size: 0.75rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
        color: #C2652A;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }

    .dash-disclaimer {
        font-size: 0.82rem;
        color: #968D82;
        margin-top: 0.35rem;
    }

    .dash-card, .premium-card, .settings-card, .tracker-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E8DFD5 !important;
        border-radius: 8px !important;
        padding: 1.6rem !important;
        margin-bottom: 1.25rem !important;
        box-shadow: 0 1px 3px rgba(38, 33, 28, 0.04), 0 4px 12px rgba(38, 33, 28, 0.02) !important;
    }

    .dash-card-title {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.74rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.08em !important;
        text-transform: uppercase !important;
        color: #968D82 !important;
        margin-bottom: 0.3rem !important;
    }

    .dash-card-role {
        font-family: 'EB Garamond', Georgia, serif !important;
        font-size: 1.45rem !important;
        font-weight: 600 !important;
        color: #26211C !important;
        margin-bottom: 0.8rem !important;
    }

    .stat-cards-row {
        display: flex;
        gap: 1.2rem;
        margin-top: 0.8rem;
        margin-bottom: 1.2rem;
    }

    .stat-card {
        flex: 1;
        background: #FFFFFF;
        border: 1px solid #E8DFD5;
        border-radius: 8px;
        padding: 1.25rem 1.4rem;
        display: flex;
        align-items: center;
        gap: 1rem;
        box-shadow: 0 1px 3px rgba(38,33,28,0.04);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .stat-card:hover {
        transform: translateY(-1px);
        border-color: #D5C4B5;
    }

    .stat-card.present { border-left: 3px solid #16A34A; }
    .stat-card.partial  { border-left: 3px solid #C2652A; }
    .stat-card.missing  { border-left: 3px solid #DC2626; }

    .stat-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
    .stat-dot.green  { background: #16A34A; box-shadow: 0 0 6px rgba(22,163,74,0.3); }
    .stat-dot.yellow { background: #C2652A; box-shadow: 0 0 6px rgba(194,101,42,0.3); }
    .stat-dot.red    { background: #DC2626; box-shadow: 0 0 6px rgba(220,38,38,0.3); }

    .stat-info { flex: 1; }
    .stat-label {
        font-size: 0.72rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
        color: #968D82;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.25rem;
    }

    .stat-count {
        font-family: 'EB Garamond', Georgia, serif;
        font-size: 2.2rem;
        font-weight: 700;
        line-height: 1;
    }

    .stat-count.green  { color: #16A34A; }
    .stat-count.yellow { color: #C2652A; }
    .stat-count.red    { color: #DC2626; }
    .stat-sublabel { font-size: 0.76rem; color: #6B6258; margin-top: 0.25rem; }

    /* Login Container */
    .login-container {
        max-width: 460px;
        margin: 3.5rem auto;
        background: #FFFFFF;
        padding: 2.5rem;
        border-radius: 8px;
        border: 1px solid #E8DFD5;
        box-shadow: 0 4px 20px rgba(38, 33, 28, 0.05);
    }

    .login-container h1 {
        font-family: 'EB Garamond', Georgia, serif !important;
        font-size: 2.3rem !important;
        font-weight: 600 !important;
        color: #26211C !important;
        text-align: center;
        margin-bottom: 0.25rem;
    }

    .divider {
        display: flex;
        align-items: center;
        text-align: center;
        color: #968D82;
        margin: 1.5rem 0;
        font-size: 0.75rem;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.05em;
    }

    .divider::before, .divider::after {
        content: '';
        flex: 1;
        border-bottom: 1px solid #E8DFD5;
    }
    .divider:not(:empty)::before { margin-right: 0.6em; }
    .divider:not(:empty)::after { margin-left: 0.6em; }

    /* Progress Tracker cards */
    .metric-container { display: flex; gap: 1.25rem; margin-top: 1.2rem; }
    .metric-box {
        flex: 1;
        background: #F4EFEA;
        border: 1px solid #E8DFD5;
        border-radius: 8px;
        padding: 1.25rem 1rem;
        text-align: center;
    }
    .metric-value {
        font-family: 'EB Garamond', Georgia, serif;
        font-size: 2.2rem;
        font-weight: 700;
        color: #C2652A;
    }
    .metric-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.74rem;
        color: #6B6258;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-top: 0.35rem;
    }

    /* Danger zone */
    .danger-zone {
        border: 1px solid rgba(220, 38, 38, 0.3) !important;
        background: #FEF2F2 !important;
    }

    .section-title {
        font-family: 'EB Garamond', Georgia, serif !important;
        font-size: 1.4rem !important;
        font-weight: 600 !important;
        color: #26211C !important;
        margin-bottom: 0.8rem !important;
    }
    </style>
    """
    st.markdown(theme_css, unsafe_allow_html=True)
