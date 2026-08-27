import streamlit as st
import os
import inspect

def render_sidebar():
    # Define navigation pages
    pages = [
        {"path": "Home.py",                       "label": "Dashboard",        "icon": "📊"},
        {"path": "pages/1_Resume_Analysis.py",    "label": "Resume Analysis",  "icon": "📄"},
        {"path": "pages/2_Skill_Gap_Report.py",   "label": "Skill Gap Report", "icon": "🎯"},
        {"path": "pages/3_Career_Roadmap.py",     "label": "Career Roadmap",   "icon": "🗺️"},
        {"path": "pages/4_Progress_Tracker.py",   "label": "Progress Tracker", "icon": "📈"},
        {"path": "pages/5_AI_Career_Mentor.py",   "label": "AI Career Mentor", "icon": "🤖"},
        {"path": "pages/6_Profile_Settings.py",   "label": "Profile Settings", "icon": "⚙️"},
    ]

    # Determine the calling script's basename to highlight the active page
    caller_filename = "Home.py"
    for frame in inspect.stack():
        filename = frame.filename
        if "sidebar.py" not in filename and "streamlit" not in filename.lower():
            caller_filename = filename
            break

    active_basename = os.path.basename(caller_filename)

    # Page-to-URL slug mapping for the active anchor href
    # Streamlit's internal router uses the filename stem (without .py)
    def page_url(path):
        stem = os.path.splitext(os.path.basename(path))[0]
        if stem == "Home":
            return "/"
        # Streamlit converts filename spaces/underscores to URL slugs
        return "/" + stem.replace(" ", "_")

    # ── Custom CSS ──────────────────────────────────────────────────────────
    custom_css = """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700;800&family=Inter:wght@300;400;500;600;700&display=swap');

    /* ── App-wide foundation ─────────────────────────── */
    [data-testid="stAppViewContainer"] {
        background-color: #0D0D0D !important;
        font-family: 'Inter', sans-serif !important;
    }
    [data-testid="stHeader"] {
        background-color: rgba(13,13,13,0.85) !important;
        backdrop-filter: blur(12px) !important;
        border-bottom: 1px solid rgba(255,255,255,0.05) !important;
    }
    [data-testid="stMainBlockContainer"] {
        background-color: #0D0D0D !important;
    }

    /* ── Sidebar shell ───────────────────────────────── */
    [data-testid="stSidebar"] {
        background-color: #161616 !important;
        border-right: 1px solid rgba(255,255,255,0.05) !important;
    }
    [data-testid="stSidebarUserContent"] {
        display: flex !important;
        flex-direction: column !important;
        min-height: 93vh !important;
    }

    /* ── Sidebar header ──────────────────────────────── */
    .sb-header {
        padding: 1.5rem 0.5rem 1.2rem 0.5rem;
        border-bottom: 1px solid rgba(255,255,255,0.06);
        margin-bottom: 0.75rem;
    }
    .sb-logo-row {
        display: flex;
        align-items: center;
        gap: 0.55rem;
    }
    .sb-logo   { font-size: 1.9rem; line-height: 1; }
    .sb-title  {
        font-size: 1.35rem;
        font-weight: 800;
        font-family: 'Outfit', sans-serif;
        color: #FFFFFF;
        letter-spacing: -0.4px;
    }
    .sb-subtitle {
        font-size: 0.75rem;
        color: #A0A0A0;
        margin-top: 0.25rem;
        margin-left: 0.1rem;
    }

    /* ── Nav items – via st.page_link (inactive) ─────── */
    div[data-testid="stPageLink"] {
        padding: 0 !important;
        margin: 0 !important;
    }
    div[data-testid="stPageLink"] a {
        display: flex !important;
        align-items: center !important;
        gap: 0.6rem !important;
        padding: 0.55rem 0.9rem !important;
        border-radius: 9px !important;
        text-decoration: none !important;
        background: transparent !important;
        border: none !important;
        color: #A0A0A0 !important;
        font-size: 0.88rem !important;
        font-weight: 500 !important;
        transition: background 0.2s ease, color 0.2s ease !important;
    }
    div[data-testid="stPageLink"] a:hover {
        background: rgba(255,255,255,0.05) !important;
        color: #FFFFFF !important;
    }
    div[data-testid="stPageLink"] p {
        color: inherit !important;
        font-size: 0.88rem !important;
        margin: 0 !important;
    }

    /* ── Active nav item – rendered as HTML anchor ───── */
    .sb-active-link {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.55rem 0.9rem;
        border-radius: 9px;
        background-color: #FFC107;
        color: #0D0D0D !important;
        font-size: 0.88rem;
        font-weight: 700;
        text-decoration: none;
        cursor: default;
        pointer-events: none;       /* active page, disable click */
        margin-bottom: 0.35rem;
        font-family: 'Inter', sans-serif;
    }

    /* ── Nav list wrapper ────────────────────────────── */
    .sb-nav {
        display: flex;
        flex-direction: column;
        gap: 0.25rem;
        flex: 1;
    }

    /* ── Footer / sign-out pinned to bottom ──────────── */
    .sb-footer {
        margin-top: auto;
        padding-top: 1rem;
        border-top: 1px solid rgba(255,255,255,0.06);
    }

    /* ── Body typography & helpers ───────────────────── */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
    }
    .accent-text  { color: #FFC107 !important; }
    .secondary-text { color: #A0A0A0 !important; }

    /* Premium card */
    .premium-card {
        background-color: #161616 !important;
        border: 1px solid rgba(255,255,255,0.06) !important;
        border-radius: 14px !important;
        padding: 1.6rem !important;
        margin-bottom: 1.2rem !important;
        transition: border-color 0.3s ease, box-shadow 0.3s ease, transform 0.25s ease !important;
    }
    .premium-card:hover {
        border-color: rgba(255,193,7,0.35) !important;
        box-shadow: 0 6px 28px rgba(255,193,7,0.08) !important;
        transform: translateY(-2px);
    }

    /* Buttons */
    .stButton > button {
        background-color: transparent !important;
        color: #A0A0A0 !important;
        border: 1px solid rgba(255,255,255,0.1) !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.25s ease !important;
    }
    .stButton > button:hover {
        background-color: rgba(255,193,7,0.12) !important;
        color: #FFC107 !important;
        border-color: rgba(255,193,7,0.4) !important;
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

    # ── Sidebar content ──────────────────────────────────────────────────────
    with st.sidebar:
        # 1. Header
        st.markdown(
            """
            <div class="sb-header">
                <div class="sb-logo-row">
                    <span class="sb-logo">🚀</span>
                    <span class="sb-title">UpCareer AI</span>
                </div>
                <div class="sb-subtitle">Career guidance engine</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 2. Navigation
        st.markdown('<div class="sb-nav">', unsafe_allow_html=True)
        for p in pages:
            is_active = active_basename == os.path.basename(p["path"])
            if is_active:
                # Render active item as a styled HTML element (no click needed)
                st.markdown(
                    f'<span class="sb-active-link">{p["icon"]}&nbsp;&nbsp;{p["label"]}</span>',
                    unsafe_allow_html=True,
                )
            else:
                st.page_link(p["path"], label=p["label"], icon=p["icon"])
        st.markdown("</div>", unsafe_allow_html=True)

        # 3. Sign-out pinned at bottom
        st.markdown('<div class="sb-footer">', unsafe_allow_html=True)
        if st.button("↩  Sign out", key="sign_out_btn", use_container_width=True):
            st.session_state.clear()
            st.toast("Signed out successfully!", icon="ℹ️")
        st.markdown("</div>", unsafe_allow_html=True)
