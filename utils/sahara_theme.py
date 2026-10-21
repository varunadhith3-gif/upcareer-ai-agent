import streamlit as st

def apply_sahara_theme():
    """
    Applies the Sahara warm-minimalist spatial UI theme across Streamlit components.
    Design tokens:
      - Canvas / Base Background: #FAF8F5 (warm cream / alabaster)
      - Surface High / Card:      #FFFFFF and #F4EFEA
      - Border / Hairline:        #E8DFD5
      - Input Border (Distinct):  #9a9088 (darker warm tone for high visibility)
      - Primary Accent:           #C2652A (Sun-baked Terracotta)
      - Primary Hover:            #A9531F
      - Text Primary (Headings):  #26211C (Deep warm espresso - EB Garamond)
      - Text Secondary (Body):    #38322c and #4a423a (High contrast dark taupe - Manrope)
      - Sublabels / Microcopy:    #38322c (Bold, high-contrast, JetBrains Mono)
      - Status / Accent:          #16A34A (Green), #C2652A (Warm), #DC2626 (Critical)
    """
    theme_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400..800;1,400..800&family=Manrope:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap');

    /* ── Root Foundation ────────────────────────────────────────────── */
    :root {
        --sahara-bg: #FAF8F5;
        --sahara-surface: #FFFFFF;
        --sahara-surface-alt: #F4EFEA;
        --sahara-border: #E8DFD5;
        --sahara-input-border: #9a9088;
        --sahara-primary: #C2652A;
        --sahara-primary-hover: #A9531F;
        --sahara-text-primary: #26211C;
        --sahara-text-secondary: #4a423a;
        --sahara-text-sublabel: #38322c;
        --sahara-radius: 8px;
    }

    html, body, [data-testid="stAppViewContainer"] {
        background-color: #FAF8F5 !important;
        font-family: 'Manrope', -apple-system, BlinkMacSystemFont, sans-serif !important;
        color: #26211C !important;
    }

    [data-testid="stHeader"] {
        background-color: rgba(250, 248, 245, 0.92) !important;
        backdrop-filter: blur(12px) !important;
        border-bottom: 1px solid #E8DFD5 !important;
    }

    [data-testid="stMainBlockContainer"] {
        background-color: #FAF8F5 !important;
        padding-top: 1.8rem !important;
        padding-bottom: 3.5rem !important;
    }

    /* ── Fix Broken Keyboard Double Icon Artifact & Sidebar Header ──── */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarHeader"],
    header[data-testid="stSidebarHeader"],
    [data-testid="stSidebarHeader"] button,
    [data-testid="stSidebarHeader"] *,
    button[kind="headerNoPadding"],
    [data-testid="collapsedControl"],
    button[aria-label="Close sidebar"],
    button[aria-label="Open sidebar"],
    button[aria-label*="sidebar" i] {
        display: none !important;
        visibility: hidden !important;
        height: 0 !important;
        width: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        overflow: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    /* Protect native Material icon font from getting replaced by sans-serif */
    .material-symbols-rounded,
    .material-symbols-outlined,
    .material-icons,
    [data-testid="stIconMaterial"] {
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
        font-feature-settings: 'liga' 1 !important;
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

    /* ── Input Field & Text Area Enhanced Visibility ─────────────────── */
    div[data-baseweb="input"],
    div[data-baseweb="base-input"],
    [data-testid="stTextInput"] > div,
    [data-testid="stTextInput"] > div > div {
        background-color: #ffffff !important;
        border: 1.5px solid #9a9088 !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 3px rgba(38,33,28,0.04) !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }

    div[data-baseweb="input"]:focus-within,
    div[data-baseweb="base-input"]:focus-within,
    [data-testid="stTextInput"] > div:focus-within {
        border-color: #C2652A !important;
        box-shadow: 0 0 0 3px rgba(194,101,42,0.18) !important;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] input,
    [data-testid="stTextInput"] input {
        background-color: #ffffff !important;
        border: none !important;
        color: #26211C !important;
        font-family: 'Manrope', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
    }

    div[data-baseweb="textarea"],
    [data-testid="stTextArea"] > div,
    [data-testid="stTextArea"] > div > div {
        background-color: #ffffff !important;
        border: 1.5px solid #9a9088 !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 3px rgba(38,33,28,0.04) !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }

    div[data-baseweb="textarea"]:focus-within,
    [data-testid="stTextArea"] > div:focus-within {
        border-color: #C2652A !important;
        box-shadow: 0 0 0 3px rgba(194,101,42,0.18) !important;
    }

    div[data-baseweb="textarea"] textarea,
    [data-testid="stTextArea"] textarea {
        background-color: #ffffff !important;
        border: none !important;
        color: #26211C !important;
        font-family: 'Manrope', sans-serif !important;
        font-size: 0.95rem !important;
        font-weight: 500 !important;
        line-height: 1.55 !important;
    }

    div[data-baseweb="select"] > div,
    [data-testid="stSelectbox"] > div > div {
        background-color: #ffffff !important;
        border: 1.5px solid #9a9088 !important;
        border-radius: 8px !important;
        box-shadow: 0 1px 3px rgba(38,33,28,0.04) !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }

    div[data-baseweb="select"] > div:focus-within,
    [data-testid="stSelectbox"] > div > div:focus-within {
        border-color: #C2652A !important;
        box-shadow: 0 0 0 3px rgba(194,101,42,0.18) !important;
    }

    div[data-baseweb="select"] * {
        color: #26211C !important;
        font-family: 'Manrope', sans-serif !important;
    }

    /* Popover dropdowns */
    ul[data-baseweb="menu"],
    div[data-baseweb="popover"] {
        background-color: #ffffff !important;
        border: 1.5px solid #9a9088 !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 16px rgba(38,33,28,0.12) !important;
    }

    li[data-baseweb="menu-item"] {
        color: #26211C !important;
        font-family: 'Manrope', sans-serif !important;
    }

    li[data-baseweb="menu-item"]:hover,
    li[data-baseweb="menu-item"][aria-selected="true"] {
        background-color: #F4EFEA !important;
        color: #C2652A !important;
    }

    /* Chat input box */
    [data-testid="stChatInput"],
    [data-testid="stChatInput"] > div,
    div[data-testid="stChatInput"] div[data-baseweb="textarea"] {
        background-color: #ffffff !important;
        border: 1.5px solid #9a9088 !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 6px rgba(38,33,28,0.05) !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease !important;
    }

    [data-testid="stChatInput"]:focus-within,
    [data-testid="stChatInput"] > div:focus-within {
        border-color: #C2652A !important;
        box-shadow: 0 0 0 3px rgba(194,101,42,0.18) !important;
    }

    [data-testid="stChatInput"] textarea {
        background-color: #ffffff !important;
        border: none !important;
        color: #26211C !important;
        font-family: 'Manrope', sans-serif !important;
        font-size: 0.95rem !important;
    }

    input::placeholder, textarea::placeholder {
        color: #7d736a !important;
        opacity: 1 !important;
    }

    /* ── Muted Sub-labels, Captions & Microcopy Visibility ───────────── */
    [data-testid="stCaptionContainer"],
    [data-testid="stCaptionContainer"] *,
    .stCaption,
    small {
        font-size: 0.90rem !important;
        color: #38322c !important;
        font-weight: 600 !important;
        line-height: 1.5 !important;
    }

    [data-testid="stWidgetLabel"] label,
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] span {
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        color: #26211C !important;
    }

    .sahara-subtitle,
    .dash-disclaimer {
        font-size: 0.95rem !important;
        color: #38322c !important;
        line-height: 1.6 !important;
        font-weight: 500 !important;
    }

    .sahara-sublabel,
    .section-sublabel,
    .dash-card-title,
    .stat-label,
    .metric-label {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.86rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.05em !important;
        text-transform: uppercase !important;
        color: #26211C !important;
        margin-bottom: 0.35rem !important;
    }

    .stat-sublabel {
        font-size: 0.84rem !important;
        color: #38322c !important;
        font-weight: 600 !important;
        margin-top: 0.3rem !important;
    }

    .sb-subtitle {
        font-size: 0.84rem !important;
        color: #4a423a !important;
        font-weight: 600 !important;
    }

    .divider {
        color: #26211C !important;
        font-size: 0.84rem !important;
        font-weight: 800 !important;
        font-family: 'JetBrains Mono', monospace;
        letter-spacing: 0.05em;
    }

    /* ── Slider Component Improvements (Profile Settings) ────────────── */
    [data-testid="stSlider"] {
        padding-top: 0.8rem !important;
        padding-bottom: 1.4rem !important;
    }

    /* Slider Track */
    [data-testid="stSlider"] div[data-baseweb="slider"] > div {
        background-color: #dcd4cc !important;
        height: 8px !important;
        border-radius: 4px !important;
    }

    /* Slider Active Progress Fill */
    [data-testid="stSlider"] div[data-baseweb="slider"] > div > div {
        background-color: #C2652A !important;
        height: 8px !important;
        border-radius: 4px !important;
    }

    /* Slider Thumb Handle */
    [data-testid="stSlider"] div[role="slider"] {
        background-color: #FFFFFF !important;
        border: 3.5px solid #C2652A !important;
        box-shadow: 0 2px 8px rgba(194, 101, 42, 0.35) !important;
        width: 24px !important;
        height: 24px !important;
        transition: transform 0.15s ease !important;
    }
    [data-testid="stSlider"] div[role="slider"]:hover {
        transform: scale(1.15) !important;
    }

    /* Active Drag Value (Floating Tooltip / Pill) */
    [data-testid="stSliderThumbValue"],
    [data-testid="stSlider"] div[role="slider"] + div,
    [data-testid="stSlider"] div[class*="StyledThumbValue"],
    [data-testid="stSlider"] div[role="slider"] div {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.1rem !important;
        font-weight: 800 !important;
        color: #26211C !important;
        background-color: #FFFFFF !important;
        border: 2px solid #C2652A !important;
        border-radius: 6px !important;
        padding: 0.25rem 0.65rem !important;
        box-shadow: 0 3px 10px rgba(38,33,28,0.18) !important;
        z-index: 10 !important;
    }

    /* Slider End Values (Min: 2 & Max: 40) - Bolder, Darker, Larger */
    [data-testid="stSlider"] [data-testid="stTickBar"] div,
    [data-testid="stSlider"] [data-testid="stTickBar"] span,
    [data-testid="stSliderTickBar"] div,
    [data-testid="stSliderTickBar"] span,
    [data-testid="stSlider"] div[class*="TickBar"] div,
    [data-testid="stSlider"] div[data-baseweb="slider"] ~ div div,
    [data-testid="stSlider"] div[data-baseweb="slider"] + div div,
    [data-testid="stSlider"] div[data-baseweb="slider"] ~ div span,
    [data-testid="stSlider"] div[data-baseweb="slider"] + div span,
    div[data-testid="stSlider"] div[data-testid="stTickBar"] > div,
    div[data-testid="stSlider"] div[data-testid="stTickBar"] > div > div {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        color: #26211C !important;
        opacity: 1 !important;
        line-height: 1.3 !important;
    }

    /* ── Sidebar Shell ──────────────────────────────────────────────── */
    [data-testid="stSidebar"] {
        background-color: #F4EFEA !important;
        border-right: 1px solid #E8DFD5 !important;
    }

    [data-testid="stSidebarUserContent"] {
        display: flex !important;
        flex-direction: column !important;
        min-height: 94vh !important;
        padding: 1.2rem 0.9rem !important;
    }

    /* ── Streamlit Native Buttons ───────────────────────────────────── */
    .stButton > button {
        background-color: #FFFFFF !important;
        color: #38322c !important;
        border: 1px solid #9a9088 !important;
        border-radius: 8px !important;
        padding: 0.55rem 1.15rem !important;
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
        border: 1.5px solid #C2652A !important;
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

    /* File Uploader */
    [data-testid="stFileUploader"] {
        background-color: #FFFFFF !important;
        border: 1.5px dashed #9a9088 !important;
        border-radius: 8px !important;
        padding: 1.2rem !important;
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
        font-size: 1.1rem !important;
        font-weight: 600 !important;
        color: #26211C !important;
    }

    /* Checkboxes */
    [data-testid="stCheckbox"] label span {
        color: #26211C !important;
        font-family: 'Manrope', sans-serif !important;
        font-size: 0.94rem !important;
        font-weight: 500 !important;
    }

    /* Tabs */
    button[data-baseweb="tab"] {
        font-family: 'Manrope', sans-serif !important;
        font-weight: 600 !important;
        color: #4a423a !important;
        border-radius: 6px 6px 0 0 !important;
        padding: 0.55rem 1.25rem !important;
    }

    button[data-baseweb="tab"][aria-selected="true"] {
        color: #C2652A !important;
        border-bottom-color: #C2652A !important;
        font-weight: 700 !important;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        font-family: 'EB Garamond', Georgia, serif !important;
        font-size: 2.2rem !important;
        font-weight: 600 !important;
        color: #26211C !important;
    }

    [data-testid="stMetricLabel"] {
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 0.8rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.06em !important;
        color: #38322c !important;
        font-weight: 700 !important;
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
        padding: 1.25rem !important;
        margin-bottom: 0.85rem !important;
    }

    [data-testid="stChatMessage"][data-testid*="user"] {
        background-color: #F4EFEA !important;
        border: 1px solid #E8DFD5 !important;
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
        border-color: #9a9088 !important;
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
        border: 1px solid rgba(194, 101, 42, 0.28);
        border-radius: 20px;
        padding: 0.25rem 0.85rem;
        font-size: 0.78rem;
        font-weight: 700;
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

    /* Backward compatibility mappings for dashboard classes */
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
        border: 1px solid rgba(194, 101, 42, 0.28);
        border-radius: 20px;
        padding: 0.25rem 0.85rem;
        font-size: 0.78rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        color: #C2652A;
        letter-spacing: 0.04em;
        text-transform: uppercase;
        margin-bottom: 0.6rem;
    }

    .dash-card, .premium-card, .settings-card, .tracker-card {
        background-color: #FFFFFF !important;
        border: 1px solid #E8DFD5 !important;
        border-radius: 8px !important;
        padding: 1.6rem !important;
        margin-bottom: 1.25rem !important;
        box-shadow: 0 1px 3px rgba(38, 33, 28, 0.04), 0 4px 12px rgba(38, 33, 28, 0.02) !important;
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
        border-color: #9a9088;
    }

    .stat-card.present { border-left: 3.5px solid #16A34A; }
    .stat-card.partial  { border-left: 3.5px solid #C2652A; }
    .stat-card.missing  { border-left: 3.5px solid #DC2626; }

    .stat-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
    .stat-dot.green  { background: #16A34A; box-shadow: 0 0 6px rgba(22,163,74,0.3); }
    .stat-dot.yellow { background: #C2652A; box-shadow: 0 0 6px rgba(194,101,42,0.3); }
    .stat-dot.red    { background: #DC2626; box-shadow: 0 0 6px rgba(220,38,38,0.3); }

    .stat-info { flex: 1; }

    .stat-count {
        font-family: 'EB Garamond', Georgia, serif;
        font-size: 2.2rem;
        font-weight: 700;
        line-height: 1;
    }

    .stat-count.green  { color: #16A34A; }
    .stat-count.yellow { color: #C2652A; }
    .stat-count.red    { color: #DC2626; }

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

    .divider::before, .divider::after {
        content: '';
        flex: 1;
        border-bottom: 1.5px solid #9a9088;
    }
    .divider:not(:empty)::before { margin-right: 0.6em; }
    .divider:not(:empty)::after { margin-left: 0.6em; }

    /* Progress Tracker metric cards */
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

    /* Danger zone */
    .danger-zone {
        border: 1.5px solid rgba(220, 38, 38, 0.35) !important;
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
