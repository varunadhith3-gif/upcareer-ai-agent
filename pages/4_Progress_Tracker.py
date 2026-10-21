import streamlit as st
from utils.sidebar import render_sidebar
from utils.sahara_theme import apply_sahara_theme

st.set_page_config(
    page_title="UpCareer AI - Progress Tracker",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_sahara_theme()
render_sidebar()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="sahara-header">
    <div class="sahara-pill">Activity Overview</div>
    <div class="sahara-title">Progress Tracker</div>
    <div class="sahara-subtitle">
        Monitor your upskilling momentum and track completed milestones across your target roadmap.
    </div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.get("analysis_complete", False):
    st.warning("No active profile data found! Please head to **Resume Analysis** and run your first report.")
    st.stop()

# BUG-03 fix: Sync roadmap_progress nested dict into flat session_state keys so
# this page always sees the latest saved checkboxes regardless of navigation order.
roadmap_progress = st.session_state.get("roadmap_progress", {})
for _prog_key, _prog_val in roadmap_progress.items():
    st.session_state[_prog_key] = _prog_val

target_role = st.session_state.get("target_role", "Target Role")
match_results = st.session_state.get("match_results", {})
evaluated = match_results.get("evaluated", {"missing": [], "partial": [], "mastered": []})
skills_to_learn = [s[0] if isinstance(s, (tuple, list)) else s for s in evaluated.get("missing", [])]

total_tasks = max(len(skills_to_learn) * 3, 1)
completed_tasks = 0

for skill in skills_to_learn:
    # Check BOTH naming conventions so it never misses a completed task
    if st.session_state.get(f"saved_task_{skill}_course", False) or st.session_state.get(f"task_{skill}_course", False): 
        completed_tasks += 1
    if st.session_state.get(f"saved_task_{skill}_project", False) or st.session_state.get(f"task_{skill}_project", False): 
        completed_tasks += 1
    if st.session_state.get(f"saved_task_{skill}_reading", False) or st.session_state.get(f"task_{skill}_reading", False): 
        completed_tasks += 1

progress_pct = int((completed_tasks / total_tasks) * 100)

# ── Metrics Dashboard Card ────────────────────────────────────────────────    
st.markdown(f"""
<div class="sahara-card">
    <div class="sahara-sublabel">COMPLETION STATUS</div>
    <div style="font-family:'EB Garamond',Georgia,serif;font-size:1.6rem;font-weight:600;color:#26211C;margin-bottom:0.3rem;">
        Target: {target_role}
    </div>
    <div style="font-size:0.92rem;color:#4a423a;margin-bottom:1rem;">
        Overall completion status across your identified skill gaps.
    </div>
""", unsafe_allow_html=True)

st.progress(progress_pct / 100.0)

st.markdown(f"""
    <div class="metric-container" style="display:flex;gap:1.25rem;margin-top:1.2rem;">
        <div class="metric-box" style="flex:1;background:#F4EFEA;border:1px solid #E8DFD5;border-radius:8px;padding:1.25rem 1rem;text-align:center;">
            <div class="metric-value" style="font-family:'EB Garamond',Georgia,serif;font-size:2.2rem;font-weight:700;color:#C2652A;">{progress_pct}%</div>
            <div class="metric-label" style="font-family:'JetBrains Mono',monospace;font-size:0.84rem;color:#26211C;font-weight:800;letter-spacing:0.05em;text-transform:uppercase;margin-top:0.4rem;">Roadmap Complete</div>
        </div>
        <div class="metric-box" style="flex:1;background:#F4EFEA;border:1px solid #E8DFD5;border-radius:8px;padding:1.25rem 1rem;text-align:center;">
            <div class="metric-value" style="font-family:'EB Garamond',Georgia,serif;font-size:2.2rem;font-weight:700;color:#16A34A;">{completed_tasks}</div>
            <div class="metric-label" style="font-family:'JetBrains Mono',monospace;font-size:0.84rem;color:#26211C;font-weight:800;letter-spacing:0.05em;text-transform:uppercase;margin-top:0.4rem;">Tasks Finished</div>
        </div>
        <div class="metric-box" style="flex:1;background:#F4EFEA;border:1px solid #E8DFD5;border-radius:8px;padding:1.25rem 1rem;text-align:center;">
            <div class="metric-value" style="font-family:'EB Garamond',Georgia,serif;font-size:2.2rem;font-weight:700;color:#DC2626;">{total_tasks - completed_tasks}</div>
            <div class="metric-label" style="font-family:'JetBrains Mono',monospace;font-size:0.84rem;color:#26211C;font-weight:800;letter-spacing:0.05em;text-transform:uppercase;margin-top:0.4rem;">Tasks Remaining</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── Detailed Activity Breakdown ───────────────────────────────────────────────
st.markdown("<div class='sahara-sublabel' style='margin-top:1.5rem;margin-bottom:0.4rem;'>MILESTONE CHECKLIST</div>", unsafe_allow_html=True)
st.markdown("<p style='color:#4a423a;font-size:0.92rem;margin-bottom:1rem;'>A breakdown of your learning milestones by skill module:</p>", unsafe_allow_html=True)

if not skills_to_learn:
    st.success("You have no pending skill gaps to track! You are fully prepared.")
else:
    for skill in skills_to_learn:
        c_done = 1 if (st.session_state.get(f"saved_task_{skill}_course", False) or st.session_state.get(f"task_{skill}_course", False)) else 0
        p_done = 1 if (st.session_state.get(f"saved_task_{skill}_project", False) or st.session_state.get(f"task_{skill}_project", False)) else 0
        r_done = 1 if (st.session_state.get(f"saved_task_{skill}_reading", False) or st.session_state.get(f"task_{skill}_reading", False)) else 0
        skill_score = c_done + p_done + r_done
        
        status_color = "#16A34A" if skill_score == 3 else ("#C2652A" if skill_score > 0 else "#7d736a")
        status_text = "Completed" if skill_score == 3 else f"{skill_score} / 3 Completed"
        
        st.markdown(f"""
        <div style='background: #FFFFFF; border: 1px solid #E8DFD5; border-radius: 8px; padding: 1.1rem 1.4rem; margin-bottom: 0.85rem; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 3px rgba(38,33,28,0.03);'>
            <div>
                <strong style='color: #26211C; font-size: 1.05rem; font-family: "Manrope", sans-serif;'>{skill}</strong><br>
                <span style='color: #4a423a; font-size: 0.86rem; font-weight: 500;'>Courses, projects, and readings tracked</span>
            </div>
            <div style='font-family: "JetBrains Mono", monospace; font-size: 0.95rem; font-weight: 700; color: {status_color};'>
                {status_text}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Navigation Footer ─────────────────────────────────────────────────────────
st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/3_Career_Roadmap.py", label="Back to Career Roadmap")
with col2:
    st.page_link("Home.py", label="Go to Dashboard")