import streamlit as st
import json
import os
from utils.sidebar import render_sidebar
from utils.sahara_theme import apply_sahara_theme

st.set_page_config(
    page_title="UpCareer AI - Profile Settings",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Protect this page — boot them back to Home if not logged in
if not st.session_state.get("logged_in", False):
    st.switch_page("Home.py")

apply_sahara_theme()
render_sidebar()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sahara-header">
    <div class="sahara-pill">Account Management</div>
    <div class="sahara-title">Profile Settings</div>
    <div class="sahara-subtitle">
        Manage your profile, target roles, study bandwidth, and account security preferences.
    </div>
</div>
""", unsafe_allow_html=True)

# Database helper functions
USER_DB_FILE = "users.json"

def load_users():
    if not os.path.exists(USER_DB_FILE):
        return {}
    with open(USER_DB_FILE, "r") as f:
        return json.load(f)

def save_users(users):
    with open(USER_DB_FILE, "w") as f:
        json.dump(users, f)

# ── Load persisted bandwidth on first visit (restores value from users.json) ──
if "study_bandwidth" not in st.session_state:
    users_db = load_users()
    current_email = st.session_state.get("user_email", "")
    if current_email and current_email in users_db:
        saved_bw = users_db[current_email].get("study_bandwidth", 10)
        st.session_state["study_bandwidth"] = saved_bw
    else:
        st.session_state["study_bandwidth"] = 10

# ── 1. Personal & Role Preferences ────────────────────────────────────────────
st.markdown('<div class="sahara-card">', unsafe_allow_html=True)
st.markdown('<div class="sahara-sublabel">ACCOUNT &amp; CAREER</div>', unsafe_allow_html=True)
st.markdown('<div style="font-family:\'EB Garamond\',Georgia,serif;font-size:1.55rem;font-weight:600;color:#26211C;margin-bottom:1.2rem;">Personal &amp; Career Preferences</div>', unsafe_allow_html=True)

current_email = st.session_state.get("user_email", "")

with st.form("profile_form"):
    col1, col2 = st.columns(2)
    with col1:
        new_first = st.text_input("First Name", value=st.session_state.get("user_name", ""))
    with col2:
        new_last = st.text_input("Last Name", value=st.session_state.get("last_name", ""))
        
    st.text_input("Email Address (Locked)", value=current_email, disabled=True)
    
    current_role = st.session_state.get("target_role", "Data Scientist")
    role_options = ["Data Scientist", "Software Engineer", "Embedded Systems Engineer", "Product Manager", "ML Engineer"]
    if current_role not in role_options:
        role_options.append(current_role)
    role_idx = role_options.index(current_role)
    
    new_role = st.selectbox("Target Career Role", options=role_options, index=role_idx)
    study_hours = st.slider(
        "Weekly Study Bandwidth (Hours)",
        min_value=2,
        max_value=40,
        value=st.session_state.get("study_bandwidth", 10),
        step=2,
        help="Allocates hours per week to calculate personalized module pacing."
    )
    
    # Extra high-contrast marker row reinforcing min and max values
    st.markdown("""
    <div style="display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace; font-size: 0.95rem; font-weight: 800; color: #26211C; margin-top: -0.4rem; margin-bottom: 0.8rem; padding: 0 0.2rem;">
        <span>Min: 2 Hours</span>
        <span>Max: 40 Hours</span>
    </div>
    """, unsafe_allow_html=True)
    
    if st.form_submit_button("Save Settings", use_container_width=True):
        prev_bandwidth = st.session_state.get("study_bandwidth", 10)
        st.session_state["user_name"] = new_first
        st.session_state["last_name"] = new_last
        st.session_state["target_role"] = new_role
        st.session_state["study_bandwidth"] = study_hours

        # If bandwidth changed, mark the roadmap as stale so it recalculates pacing
        if study_hours != prev_bandwidth:
            st.session_state["roadmap_stale"] = True
        
        # Sync changes back to local JSON database (including bandwidth)
        users_db = load_users()
        if current_email in users_db:
            users_db[current_email]["first_name"] = new_first
            users_db[current_email]["last_name"] = new_last
            users_db[current_email]["study_bandwidth"] = study_hours
            save_users(users_db)
            
        st.success("Profile and preferences successfully updated! Career Roadmap pacing will reflect your new bandwidth.")

st.markdown('</div>', unsafe_allow_html=True)

# ── 2. Data Management (Danger Zone) ──────────────────────────────────────────
st.markdown('<div class="sahara-card" style="border: 1.5px solid #DC2626; background: #FFF5F5;">', unsafe_allow_html=True)
st.markdown('<div class="sahara-sublabel" style="color: #DC2626;">DANGER ZONE</div>', unsafe_allow_html=True)
st.markdown('<div style="font-family:\'EB Garamond\',Georgia,serif;font-size:1.55rem;font-weight:600;color:#991B1B;margin-bottom:0.4rem;">Reset Profile Data</div>', unsafe_allow_html=True)
st.markdown('<p style="color:#7F1D1D;font-size:0.92rem;margin-bottom:1.1rem;">Wipe your current resume analysis, score breakdowns, and roadmap checklist state to start fresh.</p>', unsafe_allow_html=True)

if st.button("Reset All Analysis & Progress Data"):
    keys_to_wipe = [
        "analysis_complete", "readiness_score", "category_scores", "match_results", 
        "roadmap_skills", "roadmap_progress", "resume_text", "resume_filename", 
        "last_evaluated_role", "skills_present", "skills_partial", "skills_missing",
        "job_description", "agent_chat"
    ]
    for k in list(st.session_state.keys()):
        if k.startswith("saved_task_") or k.startswith("task_") or k in keys_to_wipe:
            del st.session_state[k]
    st.success("Application data wiped. You can now re-run a fresh analysis.")

st.markdown('</div>', unsafe_allow_html=True)

# ── 3. Session Management ─────────────────────────────────────────────────────
st.markdown('<div class="sahara-card">', unsafe_allow_html=True)
st.markdown('<div class="sahara-sublabel">ACCOUNT SECURITY</div>', unsafe_allow_html=True)
st.markdown('<div style="font-family:\'EB Garamond\',Georgia,serif;font-size:1.55rem;font-weight:600;color:#26211C;margin-bottom:0.4rem;">Session Management</div>', unsafe_allow_html=True)
st.markdown('<p style="color:#4a423a;font-size:0.92rem;margin-bottom:1.1rem;">Securely sign out of your local session.</p>', unsafe_allow_html=True)

if st.button("Sign Out", type="primary", use_container_width=True):
    st.session_state.clear()
    st.switch_page("Home.py")

st.markdown('</div>', unsafe_allow_html=True)