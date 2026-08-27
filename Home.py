import streamlit as st
import plotly.graph_objects as go
import json
import os
import hashlib
from utils.sidebar import render_sidebar

st.set_page_config(
    page_title="UpCareer AI - Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── LOCAL DATABASE SETUP ──────────────────────────────────────────────────────
USER_DB_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_DB_FILE):
        return {}
    with open(USER_DB_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB_FILE, "w") as f:
        json.dump(users, f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# ── 1. AUTHENTICATION GATEKEEPER ──────────────────────────────────────────────
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.markdown("""
    <style>
    .login-container { max-width: 450px; margin: 4rem auto; background: #161616; padding: 2.5rem; border-radius: 16px; border: 1px solid rgba(255,255,255,0.08); }
    .google-btn { background: #FFFFFF; color: #000000; font-weight: 600; padding: 0.6rem; border-radius: 8px; margin-bottom: 1rem; width: 100%; border: none; cursor: not-allowed; text-align: center; display: block; text-decoration: none; opacity: 0.7;}
    .divider { display: flex; align-items: center; text-align: center; color: #666; margin: 1.5rem 0; font-size: 0.8rem; }
    .divider::before, .divider::after { content: ''; flex: 1; border-bottom: 1px solid #333; }
    .divider:not(:empty)::before { margin-right: .5em; }
    .divider:not(:empty)::after { margin-left: .5em; }
    </style>
    <div class="login-container">
        <h1 style="font-family: Outfit; font-size: 2.2rem; margin-bottom: 0.2rem; text-align: center;">UpCareer <span style="color:#FFC107;">AI</span></h1>
        <p style="color: #888; font-size: 0.9rem; margin-bottom: 1.5rem; text-align: center;">Sign in or create an account to track your progress</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        # Placeholder for real Google Auth
        st.markdown('<div class="google-btn">🌐 Continue with Google (Requires Cloud API)</div>', unsafe_allow_html=True)
        st.markdown('<div class="divider">OR USE EMAIL</div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["Sign In", "Create Account"])
        
        # --- LOGIN TAB ---
        with tab1:
            with st.form("login_form"):
                login_email = st.text_input("Email Address")
                login_password = st.text_input("Password", type="password")
                submitted_login = st.form_submit_button("Sign In", use_container_width=True)
                
                if submitted_login:
                    users_db = load_users()
                    if login_email in users_db:
                        if users_db[login_email]["password"] == hash_password(login_password):
                            st.session_state["logged_in"] = True
                            st.session_state["user_email"] = login_email
                            st.session_state["user_name"] = users_db[login_email]["first_name"]
                            st.session_state["last_name"] = users_db[login_email]["last_name"]
                            st.rerun()
                        else:
                            st.error("Incorrect password.")
                    else:
                        st.error("Account not found. Please create one.")
                        
        # --- SIGN UP TAB ---
        with tab2:
            with st.form("signup_form"):
                first_name = st.text_input("First Name")
                last_name = st.text_input("Last Name")
                signup_email = st.text_input("Email Address")
                signup_password = st.text_input("Create Password", type="password")
                submitted_signup = st.form_submit_button("Create Account", use_container_width=True)
                
                if submitted_signup:
                    users_db = load_users()
                    if signup_email in users_db:
                        st.error("An account with this email already exists!")
                    elif not first_name or not signup_email or not signup_password:
                        st.error("Please fill in all required fields.")
                    else:
                        # Save new user to our local JSON database
                        users_db[signup_email] = {
                            "first_name": first_name.strip().title(),
                            "last_name": last_name.strip().title(),
                            "password": hash_password(signup_password)
                        }
                        save_users(users_db)
                        st.success("Account created! You can now log in.")

    st.markdown('</div>', unsafe_allow_html=True)
    st.stop() # Stops the rest of the dashboard from loading

# ── 2. MAIN DASHBOARD (If Logged In) ──────────────────────────────────────────
render_sidebar()

st.markdown("""
<style>
.dash-header { padding: 2rem 0 1.4rem 0; border-bottom: 1px solid rgba(255,255,255,0.06); margin-bottom: 1.8rem; }
.dash-welcome { font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 800; color: #FFFFFF; letter-spacing: -0.5px; margin: 0 0 0.25rem 0; }
.dash-welcome span { color: #FFC107; }
.dash-role-pill { display: inline-flex; align-items: center; gap: 0.4rem; background: rgba(255,193,7,0.10); border: 1px solid rgba(255,193,7,0.25); border-radius: 20px; padding: 0.22rem 0.75rem; font-size: 0.8rem; font-weight: 600; color: #FFC107; margin-bottom: 0.6rem; }
.dash-disclaimer { font-size: 0.74rem; color: #666; font-style: italic; margin-top: 0.4rem; }
.dash-card { background-color: #161616; border: 1px solid rgba(255,255,255,0.06); border-radius: 16px; padding: 1.6rem; margin-bottom: 1.2rem; height: 100%; }
.dash-card-title { font-family: 'Outfit', sans-serif; font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #A0A0A0; margin-bottom: 0.2rem; }
.dash-card-role { font-family: 'Outfit', sans-serif; font-size: 1.1rem; font-weight: 700; color: #FFFFFF; margin-bottom: 0.8rem; }
.stat-cards-row { display: flex; gap: 1rem; margin-top: 0.6rem; margin-bottom: 1rem; }
.stat-card { flex: 1; background: #161616; border: 1px solid rgba(255,255,255,0.06); border-radius: 14px; padding: 1.2rem 1.4rem; display: flex; align-items: center; gap: 1rem; }
.stat-card.present { border-color: rgba(72,199,142,0.18); }
.stat-card.partial  { border-color: rgba(255,193,7,0.18); }
.stat-card.missing  { border-color: rgba(255,82,82,0.18); }
.stat-dot { width: 12px; height: 12px; border-radius: 50%; flex-shrink: 0; }
.stat-dot.green  { background:#48C78E; box-shadow: 0 0 8px #48C78E;}
.stat-dot.yellow { background:#FFC107; box-shadow: 0 0 8px #FFC107;}
.stat-dot.red    { background:#FF5252; box-shadow: 0 0 8px #FF5252;}
.stat-info { flex: 1; }
.stat-label { font-size: 0.75rem; font-weight: 600; color: #888; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.2rem; }
.stat-count { font-family: 'Outfit', sans-serif; font-size: 2rem; font-weight: 800; line-height: 1; }
.stat-count.green  { color: #48C78E; }
.stat-count.yellow { color: #FFC107; }
.stat-count.red    { color: #FF5252; }
.stat-sublabel { font-size: 0.71rem; color: #666; margin-top: 0.15rem; }
</style>
""", unsafe_allow_html=True)

if not st.session_state.get("analysis_complete", False):
    st.markdown(
        "<div style='background:#161616;border:1px solid rgba(255,255,255,0.06); border-radius:16px;padding:3.5rem 2rem;text-align:center;margin-top:1rem;'>"
        "<div style='font-size:3rem;margin-bottom:1rem;'>📊</div>"
        f"<div style='font-family:Outfit,sans-serif;font-size:1.3rem;font-weight:700; color:#FFFFFF;margin-bottom:0.5rem;'>Welcome, {st.session_state.get('user_name', '')}!</div>"
        "<div style='font-size:0.85rem;color:#777;max-width:420px;margin:0 auto 1.4rem auto; line-height:1.6;'>"
        "To generate your live dashboard, please upload your resume on the Analysis page first.</div>"
        "</div>", unsafe_allow_html=True
    )
    st.page_link("pages/1_Resume_Analysis.py", label="📄 Go to Resume Analysis", icon=None)
    st.stop()

# Load real values
name        = st.session_state.get("user_name", "Candidate")
role        = st.session_state.get("target_role", "Target Role")
score       = st.session_state.get("readiness_score", 0)
cats        = st.session_state.get("category_scores", {})
n_present   = st.session_state.get("skills_present", 0)
n_partial   = st.session_state.get("skills_partial", 0)
n_missing   = st.session_state.get("skills_missing", 0)

st.markdown(f"""
<div class="dash-header">
    <div class="dash-role-pill">🎯 &nbsp;Target role: {role}</div>
    <div class="dash-welcome">Welcome back, <span>{name}</span> 👋</div>
    <div class="dash-disclaimer">ℹ️ Your score actively syncs with your Career Roadmap progress.</div>
</div>
""", unsafe_allow_html=True)

col_left, col_right = st.columns([1, 1.55], gap="large")

with col_left:
    st.markdown(f"""
    <div class="dash-card">
        <div class="dash-card-title">Career Readiness Score</div>
        <div class="dash-card-role">{role}</div>
    """, unsafe_allow_html=True)

    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=score,
        number={"font": {"size": 52, "color": "#FFFFFF", "family": "Outfit, sans-serif"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 0, "tickcolor": "rgba(0,0,0,0)", "showticklabels": False},
            "bar": {"color": "#FFC107", "thickness": 0.72},
            "bgcolor": "rgba(0,0,0,0)", "borderwidth": 0,
            "steps": [{"range": [0, 100], "color": "#272727"}],
            "threshold": {"line": {"color": "#48C78E", "width": 4}, "thickness": 0.85, "value": score},
        },
        domain={"x": [0, 1], "y": [0, 1]},
    ))

    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=260, margin=dict(t=30, b=10, l=20, r=20))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    cat_meta = {"Skills": "🛠️", "Experience": "💼", "Projects": "🗂️", "Education": "🎓", "Certifications": "📜"}
    bars_html = ""
    for cat, cat_score in cats.items():
        icon = cat_meta.get(cat, "•")
        bars_html += (
            "<div style='margin-bottom:1.05rem;'>"
            "<div style='display:flex;justify-content:space-between;align-items:baseline;margin-bottom:0.3rem;'>"
            "<span style='font-size:0.84rem;font-weight:600;color:#FFFFFF;'>{icon}&nbsp; {cat}</span>"
            "<span style='font-size:0.84rem;font-weight:700;color:#FFC107;min-width:2.2rem;text-align:right;'>{score}</span>"
            "</div>"
            "<div style='background:rgba(255,255,255,0.07);border-radius:20px;height:6px;width:100%;overflow:hidden;margin-bottom:0.25rem;'>"
            "<div style='height:100%;border-radius:20px;background:linear-gradient(90deg,#FFC107 0%,#48C78E 100%);width:{pct}%;'></div>"
            "</div></div>"
        ).format(icon=icon, cat=cat, score=cat_score, pct=cat_score)

    st.markdown(
        "<div style='background-color:#161616;border:1px solid rgba(255,255,255,0.06); border-radius:16px;padding:1.6rem;margin-bottom:1.2rem;'>"
        "<div style='font-family:Outfit,sans-serif;font-size:1.15rem;font-weight:700; color:#FFFFFF;margin-bottom:1.1rem;'>Live Score breakdown</div>"
        + bars_html + "</div>", unsafe_allow_html=True
    )

st.markdown(f"""
<div class="stat-cards-row">
    <div class="stat-card present"><div class="stat-dot green"></div><div class="stat-info"><div class="stat-label">Present</div><div class="stat-count green">{n_present}</div><div class="stat-sublabel">Mastered skills matched</div></div></div>
    <div class="stat-card partial"><div class="stat-dot yellow"></div><div class="stat-info"><div class="stat-label">Partial</div><div class="stat-count yellow">{n_partial}</div><div class="stat-sublabel">Partial-gap skills</div></div></div>
    <div class="stat-card missing"><div class="stat-dot red"></div><div class="stat-info"><div class="stat-label">Missing</div><div class="stat-count red">{n_missing}</div><div class="stat-sublabel">Critical skills missing</div></div></div>
</div>
""", unsafe_allow_html=True)