import streamlit as st
import plotly.graph_objects as go
import json
import os
import hashlib
from streamlit_oauth import OAuth2Component
import base64
from utils.sidebar import render_sidebar
from utils.sahara_theme import apply_sahara_theme

st.set_page_config(
    page_title="UpCareer AI - Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_sahara_theme()

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
    <div class="login-container">
        <h1>UpCareer <span style="color:#C2652A; font-style:italic;">AI</span></h1>
        <p style="color: #4a423a; font-size: 0.95rem; font-weight: 500; margin-bottom: 1.5rem; text-align: center;">Sign in or create an account to track your career journey</p>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 4, 1])
    with col2:
        # Initialize the OAuth configuration
        oauth2 = OAuth2Component(
            st.secrets["GOOGLE_CLIENT_ID"],
            st.secrets["GOOGLE_CLIENT_SECRET"],
            "https://accounts.google.com/o/oauth2/v2/auth",
            "https://oauth2.googleapis.com/token"
        )
        
        # Render the working Google login button
        result = oauth2.authorize_button(
            name="Continue with Google",
            redirect_uri=st.secrets["GOOGLE_REDIRECT_URI"],
            scope="openid email profile",
            key="google_login",
            use_container_width=True
        )
        
        # Handle successful authentication
        if result and "token" in result:
            st.session_state["logged_in"] = True
            
            # Decode Google's returned token to extract the user's email and name
            id_token = result["token"]["id_token"]
            payload = id_token.split(".")[1]
            payload += "=" * ((4 - len(payload) % 4) % 4) # Fix padding
            user_info = json.loads(base64.b64decode(payload))
            
            st.session_state["user_email"] = user_info.get("email")
            st.session_state["user_name"] = user_info.get("given_name", "User")
            st.rerun()

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

if not st.session_state.get("analysis_complete", False):
    st.markdown(
        f"""
        <div class="sahara-card" style="text-align:center;padding:3.5rem 2rem;margin-top:1.5rem;">
            <div class="sahara-pill">Active Profile Status</div>
            <div class="sahara-title" style="font-size:2rem;margin-bottom:0.5rem;">Welcome, {st.session_state.get('user_name', '')}</div>
            <div class="sahara-subtitle" style="margin:0 auto 1.5rem auto;">
                To generate your live career readiness metrics and personalized roadmap, please upload your resume on the Analysis page first.
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.page_link("pages/1_Resume_Analysis.py", label="Go to Resume Analysis")
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
    <div class="dash-role-pill">Target role: {role}</div>
    <div class="dash-welcome">Welcome back, <span>{name}</span></div>
    <div class="dash-disclaimer">Your score actively syncs with your Career Roadmap progress.</div>
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
        number={"font": {"size": 52, "color": "#26211C", "family": "EB Garamond, Georgia, serif"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 0, "tickcolor": "rgba(0,0,0,0)", "showticklabels": False},
            "bar": {"color": "#C2652A", "thickness": 0.72},
            "bgcolor": "rgba(0,0,0,0)", "borderwidth": 0,
            "steps": [{"range": [0, 100], "color": "#F4EFEA"}],
            "threshold": {"line": {"color": "#16A34A", "width": 4}, "thickness": 0.85, "value": score},
        },
        domain={"x": [0, 1], "y": [0, 1]},
    ))

    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=260, margin=dict(t=30, b=10, l=20, r=20))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

with col_right:
    bars_html = ""
    for cat, cat_score in cats.items():
        bars_html += (
            "<div style='margin-bottom:1.05rem;'>"
            "<div style='display:flex;justify-content:space-between;align-items:baseline;margin-bottom:0.35rem;'>"
            "<span style='font-size:0.88rem;font-weight:600;color:#26211C;'>{cat}</span>"
            "<span style='font-size:0.88rem;font-weight:800;font-family:\"JetBrains Mono\",monospace;color:#C2652A;min-width:2.2rem;text-align:right;'>{score}%</span>"
            "</div>"
            "<div style='background:#F4EFEA;border-radius:20px;height:8px;width:100%;overflow:hidden;margin-bottom:0.25rem;border:1px solid #E8DFD5;'>"
            "<div style='height:100%;border-radius:20px;background:linear-gradient(90deg,#C2652A 0%,#16A34A 100%);width:{pct}%;'></div>"
            "</div></div>"
        ).format(cat=cat, score=cat_score, pct=cat_score)

    st.markdown(
        "<div class='dash-card'>"
        "<div class='dash-card-title'>Analysis Breakdown</div>"
        "<div class='dash-card-role' style='font-size:1.35rem;margin-bottom:1rem;'>Live Competency Scores</div>"
        + bars_html + "</div>", unsafe_allow_html=True
    )

st.markdown(f"""
<div class="stat-cards-row">
    <div class="stat-card present"><div class="stat-dot green"></div><div class="stat-info"><div class="stat-label">Present</div><div class="stat-count green">{n_present}</div><div class="stat-sublabel">Mastered skills matched</div></div></div>
    <div class="stat-card partial"><div class="stat-dot yellow"></div><div class="stat-info"><div class="stat-label">Partial</div><div class="stat-count yellow">{n_partial}</div><div class="stat-sublabel">Partial-gap skills</div></div></div>
    <div class="stat-card missing"><div class="stat-dot red"></div><div class="stat-info"><div class="stat-label">Missing</div><div class="stat-count red">{n_missing}</div><div class="stat-sublabel">Critical skills missing</div></div></div>
</div>
""", unsafe_allow_html=True)