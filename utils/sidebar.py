import streamlit as st
import os
import inspect

def render_sidebar():
    # Define navigation pages
    pages = [
        {"path": "Home.py",                       "label": "Dashboard"},
        {"path": "pages/1_Resume_Analysis.py",    "label": "Resume Analysis"},
        {"path": "pages/2_Skill_Gap_Report.py",   "label": "Skill Gap Report"},
        {"path": "pages/3_Career_Roadmap.py",     "label": "Career Roadmap"},
        {"path": "pages/4_Progress_Tracker.py",   "label": "Progress Tracker"},
        {"path": "pages/5_AI_Career_Mentor.py",   "label": "AI Career Mentor"},
        {"path": "pages/6_Profile_Settings.py",   "label": "Profile Settings"},
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

    # ── Custom CSS for Sidebar & Global Navigation ──────────────────────────
    custom_css = """
    <style>
    /* ── Hide broken keyboard_double artifact and collapse control ───── */
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

    .material-symbols-rounded,
    .material-symbols-outlined,
    .material-icons,
    [data-testid="stIconMaterial"] {
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
        font-feature-settings: 'liga' 1 !important;
    }

    /* ── Sidebar shell ───────────────────────────────── */
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

    /* ── Sidebar header ──────────────────────────────── */
    .sb-header {
        padding: 0.8rem 0.4rem 1.2rem 0.4rem;
        border-bottom: 1px solid #E8DFD5;
        margin-bottom: 1rem;
    }
    .sb-logo-row {
        display: flex;
        align-items: center;
        gap: 0.55rem;
    }
    .sb-title {
        font-size: 1.55rem;
        font-weight: 600;
        font-family: 'EB Garamond', Georgia, serif;
        color: #26211C;
        letter-spacing: -0.015em;
    }
    .sb-title span {
        color: #C2652A;
        font-style: italic;
    }
    .sb-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.35rem;
        background-color: rgba(194, 101, 42, 0.08);
        border: 1px solid rgba(194, 101, 42, 0.28);
        border-radius: 12px;
        padding: 0.18rem 0.6rem;
        font-size: 0.72rem;
        font-weight: 700;
        font-family: 'JetBrains Mono', monospace;
        color: #C2652A;
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-top: 0.35rem;
    }
    .sb-subtitle {
        font-size: 0.82rem;
        color: #4a423a;
        font-weight: 600;
        margin-top: 0.3rem;
        font-family: 'Manrope', sans-serif;
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
        padding: 0.6rem 0.9rem !important;
        border-radius: 8px !important;
        text-decoration: none !important;
        background: transparent !important;
        border: 1px solid transparent !important;
        color: #4a423a !important;
        font-size: 0.9rem !important;
        font-family: 'Manrope', sans-serif !important;
        font-weight: 600 !important;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    div[data-testid="stPageLink"] a:hover {
        background: #FFFFFF !important;
        border-color: #9a9088 !important;
        color: #C2652A !important;
        transform: translateX(2px) !important;
        box-shadow: 0 1px 3px rgba(38,33,28,0.04) !important;
    }
    div[data-testid="stPageLink"] p {
        color: inherit !important;
        font-size: 0.9rem !important;
        margin: 0 !important;
    }

    /* ── Active nav item – rendered as HTML element ──── */
    .sb-active-link {
        display: flex;
        align-items: center;
        gap: 0.6rem;
        padding: 0.6rem 0.9rem;
        border-radius: 8px;
        background-color: #C2652A;
        color: #FFFFFF !important;
        font-size: 0.9rem;
        font-weight: 700;
        text-decoration: none;
        cursor: default;
        pointer-events: none;
        margin-bottom: 0.35rem;
        font-family: 'Manrope', sans-serif;
        box-shadow: 0 2px 6px rgba(194, 101, 42, 0.25);
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
        border-top: 1px solid #E8DFD5;
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
                    <span class="sb-title">UpCareer <span>AI</span></span>
                </div>
                <div class="sb-badge">Career Engine</div>
                <div class="sb-subtitle">Precision guidance platform</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # 2. Navigation
        st.markdown('<div class="sb-nav">', unsafe_allow_html=True)
        for p in pages:
            is_active = active_basename == os.path.basename(p["path"])
            if is_active:
                st.markdown(
                    f'<span class="sb-active-link">{p["label"]}</span>',
                    unsafe_allow_html=True,
                )
            else:
                st.page_link(p["path"], label=p["label"])
        st.markdown("</div>", unsafe_allow_html=True)

        # 3. Sign-out pinned at bottom
        st.markdown('<div class="sb-footer">', unsafe_allow_html=True)
        if st.button("Sign out", key="sign_out_btn", use_container_width=True):
            st.session_state.clear()
            st.toast("Signed out successfully.")
        st.markdown("</div>", unsafe_allow_html=True)
