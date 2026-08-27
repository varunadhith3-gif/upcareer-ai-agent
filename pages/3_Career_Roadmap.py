import streamlit as st
import time
from utils.sidebar import render_sidebar

st.set_page_config(
    page_title="UpCareer AI - Career Roadmap",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

# ── Page-level CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
.roadmap-card { background: #161616; border: 1px solid rgba(255,255,255,0.08); border-radius: 12px; padding: 1.5rem; margin-bottom: 1.5rem; }
.phase-1 { border-left: 4px solid #FF5252; } 
.phase-2 { border-left: 4px solid #FFC107; } 
.phase-3 { border-left: 4px solid #48C78E; } 
.skill-badge { background: #252525; border: 1px solid rgba(255,255,255,0.15); border-radius: 6px; padding: 0.4rem 0.8rem; font-size: 0.85rem; color: #E0E0E0; display: inline-block; margin-right: 0.6rem; margin-bottom: 0.6rem; font-weight: 500; }
[data-testid="stExpander"] { background: #161616 !important; border: 1px solid rgba(255,255,255,0.08) !important; border-radius: 12px !important; margin-bottom: 1rem !important; }
.progress-text { font-size: 1.1rem; font-weight: 600; color: #FFC107; margin-bottom: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding:2rem 0 1.4rem 0;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:1.8rem;'>
    <div style='display:inline-flex;align-items:center;gap:0.4rem;background:rgba(255,193,7,0.10); border:1px solid rgba(255,193,7,0.25);border-radius:20px;padding:0.22rem 0.75rem; font-size:0.8rem;font-weight:600;color:#FFC107;margin-bottom:0.6rem;'>
        🗺️ &nbsp;Step 3 of 3
    </div>
    <div style='font-family:Outfit,sans-serif;font-size:2rem;font-weight:800;color:#FFFFFF; letter-spacing:-0.5px;margin:0 0 0.4rem 0;'>
        Your Interactive Roadmap
    </div>
    <div style='font-size:0.84rem;color:#888;max-width:620px;line-height:1.6;'>
        Track your progress. Check off resources and click <strong>Save Progress</strong> to sync with your tracker and dashboard.
    </div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.get("analysis_complete", False):
    st.warning("⚠️ We don't have your data yet! Please go to **Resume Analysis** to upload your resume first.")
    st.stop()

# ── Resource Database ─────────────────────────────────────────────────────────
RESOURCE_DB = {
    "Python": {"course": {"name": "100 Days of Code: Python Bootcamp", "url": "https://www.udemy.com/"}, "project": "Build a command-line task manager or web scraper.", "reading": {"name": "Automate the Boring Stuff", "url": "https://automatetheboringstuff.com/"}},
    "Machine Learning": {"course": {"name": "Machine Learning by Andrew Ng", "url": "https://www.coursera.org/"}, "project": "Build a housing price prediction model.", "reading": {"name": "Introduction to Statistical Learning", "url": "https://www.statlearning.com/"}},
    "Sql": {"course": {"name": "PostgreSQL for Everybody", "url": "https://www.youtube.com/"}, "project": "Design an e-commerce database with 5 join queries.", "reading": {"name": "SQLBolt - Interactive Lessons", "url": "https://sqlbolt.com/"}}
}

def get_resources(skill):
    return RESOURCE_DB.get(skill, {
        "course": {"name": f"{skill} Full Course for Beginners", "url": f"https://www.youtube.com/results?search_query={skill.replace(' ', '+')}+full+course"},
        "project": f"Build a small application focused entirely on using {skill}.",
        "reading": {"name": f"Official {skill} Documentation", "url": f"https://www.google.com/search?q={skill}+official+documentation"}
    })

# ── Fetch & Secure Permanent Roadmap Skills List ──────────────────────────────
target_role = st.session_state.get("target_role", "your target role")
evaluated = st.session_state["match_results"]["evaluated"]

def extract_skill_names(skill_list):
    return [str(s[0]).title() if isinstance(s, (tuple, list)) else str(s).title() for s in skill_list]

# Cache the initial skills to learn so they never disappear when graduated
if "roadmap_skills" not in st.session_state:
    missing_init = extract_skill_names(evaluated.get("missing", []))
    partial_init = extract_skill_names(evaluated.get("partial", []))
    st.session_state["roadmap_skills"] = missing_init + partial_init

skills_to_learn = st.session_state["roadmap_skills"]

if not skills_to_learn:
    st.success(f"🎉 Wow! You already have all the core skills for a **{target_role}**. Start applying!")
    st.stop()

if "_base_skills_score" not in st.session_state:
    st.session_state["_base_skills_score"] = st.session_state.get("category_scores", {}).get("Skills", 0)

for skill in skills_to_learn:
    for task_type in ["course", "project", "reading"]:
        if f"saved_task_{skill}_{task_type}" not in st.session_state:
            st.session_state[f"saved_task_{skill}_{task_type}"] = False

# ── Top Level Progress Metrics ────────────────────────────────────────────────
total_tasks = max(len(skills_to_learn) * 3, 1)
completed_tasks = sum(1 for skill in skills_to_learn for t in ["course", "project", "reading"] if st.session_state.get(f"saved_task_{skill}_{t}", False))
progress_pct = int((completed_tasks / total_tasks) * 100)

st.markdown(f"<div class='progress-text'>Current Saved Progress: {progress_pct}% ({completed_tasks} of {total_tasks} tasks completed)</div>", unsafe_allow_html=True)
st.progress(progress_pct / 100.0)

# ── Render Action Modules ────────────────────────────────────────────────     
st.markdown(f"<h3 style='color: #FFFFFF; font-size: 1.3rem; margin-bottom: 1.5rem; margin-top: 2rem;'>Action Plan to become a {target_role}</h3>", unsafe_allow_html=True)

with st.form(key="roadmap_form"):
    temp_checkbox_states = {}
    
    for skill in skills_to_learn:
        # Check if completed
        c_status = st.session_state.get(f"saved_task_{skill}_course", False)
        p_status = st.session_state.get(f"saved_task_{skill}_project", False)
        r_status = st.session_state.get(f"saved_task_{skill}_reading", False)
        is_fully_done = c_status and p_status and r_status
        
        priority = "🟢 Completed" if is_fully_done else "🔴 Action Required"
        
        with st.expander(f"{skill}  —  {priority}", expanded=False):
            resources = get_resources(skill)
            
            st.markdown("#### 1. Take a Course")
            st.markdown(f"[{resources['course']['name']}]({resources['course']['url']})")
            temp_checkbox_states[f"saved_task_{skill}_course"] = st.checkbox(f"I completed the {skill} course", value=c_status)
            
            st.markdown("#### 2. Hands-On Project")
            st.info(f"**Mission:** {resources['project']}")
            temp_checkbox_states[f"saved_task_{skill}_project"] = st.checkbox(f"I built the {skill} project", value=p_status)
            
            st.markdown("#### 3. Reading Material")
            st.markdown(f"[{resources['reading']['name']}]({resources['reading']['url']})")
            temp_checkbox_states[f"saved_task_{skill}_reading"] = st.checkbox(f"I finished the {skill} reading", value=r_status)

    st.markdown("<br>", unsafe_allow_html=True)
    submit_button = st.form_submit_button(label="💾 Save Progress & Update Dashboard", use_container_width=True)

if submit_button:
    for key, val in temp_checkbox_states.items():
        st.session_state[key] = val
        st.session_state[key.replace("saved_", "")] = val
        
    # Skill Migration Logic
    mastered_list = list(evaluated.get("mastered", []))
    partial_list = list(evaluated.get("partial", []))
    missing_list = list(evaluated.get("missing", []))

    def get_skill_name(s):
        return str(s[0]).title() if isinstance(s, (list, tuple)) else str(s).title()

    for skill in skills_to_learn:
        c_done = temp_checkbox_states.get(f"saved_task_{skill}_course", False)
        p_done = temp_checkbox_states.get(f"saved_task_{skill}_project", False)
        r_done = temp_checkbox_states.get(f"saved_task_{skill}_reading", False)
        
        if c_done and p_done and r_done:
            partial_list = [s for s in partial_list if get_skill_name(s) != skill]
            missing_list = [s for s in missing_list if get_skill_name(s) != skill]
            if not any(get_skill_name(s) == skill for s in mastered_list):
                mastered_list.append((skill, 0.95))

    st.session_state["match_results"]["evaluated"]["mastered"] = mastered_list
    st.session_state["match_results"]["evaluated"]["partial"] = partial_list
    st.session_state["match_results"]["evaluated"]["missing"] = missing_list
    
    st.session_state["skills_present"] = len(mastered_list)
    st.session_state["skills_partial"] = len(partial_list)
    st.session_state["skills_missing"] = len(missing_list)

    # Dynamic Scoring
    new_completed = sum(1 for val in temp_checkbox_states.values() if val is True)
    bonus_points = int((new_completed / total_tasks) * 45)
    new_skills_score = min(100, st.session_state["_base_skills_score"] + bonus_points)
    
    updated_cats = dict(st.session_state.get("category_scores", {}))
    updated_cats["Skills"] = new_skills_score
    st.session_state["category_scores"] = updated_cats
    
    weights = {
        "Data Scientist":          {"Skills": 0.35, "Experience": 0.25, "Projects": 0.20, "Education": 0.12, "Certifications": 0.08},
        "Software Engineer":       {"Skills": 0.30, "Experience": 0.30, "Projects": 0.22, "Education": 0.10, "Certifications": 0.08},
        "Embedded Systems Engineer":{"Skills": 0.35, "Experience": 0.30, "Projects": 0.20, "Education": 0.10, "Certifications": 0.05},
        "Product Manager":         {"Skills": 0.25, "Experience": 0.35, "Projects": 0.18, "Education": 0.12, "Certifications": 0.10},
        "ML Engineer":             {"Skills": 0.35, "Experience": 0.25, "Projects": 0.22, "Education": 0.10, "Certifications": 0.08},
    }.get(target_role, {"Skills": 0.35, "Experience": 0.25, "Projects": 0.20, "Education": 0.12, "Certifications": 0.08})
    
    new_readiness = int(round(
        (updated_cats.get("Skills", 0) * weights["Skills"]) +
        (updated_cats.get("Experience", 0) * weights["Experience"]) +
        (updated_cats.get("Projects", 0) * weights["Projects"]) +
        (updated_cats.get("Education", 0) * weights["Education"]) +
        (updated_cats.get("Certifications", 0) * weights["Certifications"])
    ))
    
    st.session_state["readiness_score"] = max(0, min(100, new_readiness))
        
    st.success("✅ Progress saved and synced across dashboard & tracker! Reloading...")
    time.sleep(1.2)
    st.rerun()

# ── Navigation Footer ─────────────────────────────────────────────────────────
st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/4_Progress_Tracker.py", label="📈 View Progress Tracker", icon=None)
with col2:
    st.page_link("Home.py", label="📊 Go to Dashboard", icon=None)