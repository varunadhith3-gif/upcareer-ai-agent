import streamlit as st
from utils.sidebar import render_sidebar

st.set_page_config(
    page_title="UpCareer AI - Progress Tracker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

# ── Page-level CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
.tracker-card { background: #161616; border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 1.6rem; margin-bottom: 1.2rem; }
.metric-container { display: flex; gap: 1.5rem; margin-top: 1rem; }
.metric-box { flex: 1; background: #1C1C1C; border: 1px solid rgba(255,193,7,0.2); border-radius: 10px; padding: 1.2rem; text-align: center; }
.metric-value { font-family: 'Outfit', sans-serif; font-size: 2.2rem; font-weight: 800; color: #FFC107; }
.metric-label { font-size: 0.75rem; color: #888; text-transform: uppercase; letter-spacing: 0.06em; margin-top: 0.3rem; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding:2rem 0 1.4rem 0;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:1.8rem;'>
    <div style='display:inline-flex;align-items:center;gap:0.4rem;background:rgba(255,193,7,0.10); border:1px solid rgba(255,193,7,0.25);border-radius:20px;padding:0.22rem 0.75rem; font-size:0.8rem;font-weight:600;color:#FFC107;margin-bottom:0.6rem;'>
        📈 &nbsp;Activity Overview
    </div>
    <div style='font-family:Outfit,sans-serif;font-size:2rem;font-weight:800;color:#FFFFFF; letter-spacing:-0.5px;margin:0 0 0.4rem 0;'>
        Progress Tracker
    </div>
    <div style='font-size:0.84rem;color:#888;max-width:620px;line-height:1.6;'>
        Monitor your upskilling momentum and track completed milestones across your target roadmap.
    </div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.get("analysis_complete", False):
    st.warning("⚠️ No active profile data found! Please head to **Resume Analysis** and run your first report.")
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
st.markdown('<div class="tracker-card">', unsafe_allow_html=True)
st.markdown(f"<h3 style='color: #FFFFFF; margin-top: 0;'>Target: {target_role}</h3>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #AAA; font-size: 0.9rem;'>Overall completion status across your identified skill gaps.</p>", unsafe_allow_html=True)

st.progress(progress_pct / 100.0)

st.markdown(f"""
<div class="metric-container">
    <div class="metric-box">
        <div class="metric-value">{progress_pct}%</div>
        <div class="metric-label">Roadmap Complete</div>
    </div>
    <div class="metric-box">
        <div class="metric-value" style="color: #48C78E;">{completed_tasks}</div>
        <div class="metric-label">Tasks Finished</div>
    </div>
    <div class="metric-box">
        <div class="metric-value" style="color: #FF5252;">{total_tasks - completed_tasks}</div>
        <div class="metric-label">Tasks Remaining</div>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Detailed Activity Breakdown ───────────────────────────────────────────────
st.markdown("### 📋 Milestone Checklist")
st.write("A breakdown of your learning milestones by skill module:")

if not skills_to_learn:
    st.success("🎉 You have no pending skill gaps to track! You are fully prepared.")
else:
    for skill in skills_to_learn:
        c_done = 1 if (st.session_state.get(f"saved_task_{skill}_course", False) or st.session_state.get(f"task_{skill}_course", False)) else 0
        p_done = 1 if (st.session_state.get(f"saved_task_{skill}_project", False) or st.session_state.get(f"task_{skill}_project", False)) else 0
        r_done = 1 if (st.session_state.get(f"saved_task_{skill}_reading", False) or st.session_state.get(f"task_{skill}_reading", False)) else 0
        skill_score = c_done + p_done + r_done
        
        status_color = "#48C78E" if skill_score == 3 else ("#FFC107" if skill_score > 0 else "#666")
        status_text = "Completed 🟢" if skill_score == 3 else f"{skill_score} / 3 Completed"
        
        st.markdown(f"""
        <div style='background: #161616; border: 1px solid rgba(255,255,255,0.06); border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 0.8rem; display: flex; justify-content: space-between; align-items: center;'>
            <div>
                <strong style='color: #FFF; font-size: 1rem;'>{skill}</strong><br>
                <span style='color: #888; font-size: 0.78rem;'>Courses, projects, and readings tracked</span>
            </div>
            <div style='font-family: Outfit, sans-serif; font-size: 1.1rem; font-weight: 700; color: {status_color};'>
                {status_text}
            </div>
        </div>
        """, unsafe_allow_html=True)

# ── Navigation Footer ─────────────────────────────────────────────────────────
st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/3_Career_Roadmap.py", label="🗺️ Back to Career Roadmap", icon=None)
with col2:
    st.page_link("Home.py", label="📊 Go to Dashboard", icon=None)