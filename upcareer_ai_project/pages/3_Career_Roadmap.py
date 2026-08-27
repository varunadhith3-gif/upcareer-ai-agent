import streamlit as st
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
.roadmap-card {
    background: #161616;
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}
.phase-1 { border-left: 4px solid #FF5252; } 
.phase-2 { border-left: 4px solid #FFC107; } 
.phase-3 { border-left: 4px solid #48C78E; } 

.skill-badge {
    background: #252525;
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 6px;
    padding: 0.4rem 0.8rem;
    font-size: 0.85rem;
    color: #E0E0E0;
    display: inline-block;
    margin-right: 0.6rem;
    margin-bottom: 0.6rem;
    font-weight: 500;
}
.action-list {
    color: #A0A0A0;
    font-size: 0.9rem;
    line-height: 1.6;
    margin-top: 1rem;
}
[data-testid="stExpander"] {
    background: #161616 !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 12px !important;
    margin-bottom: 1rem !important;
}
.progress-text {
    font-size: 1.1rem;
    font-weight: 600;
    color: #FFC107;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding:2rem 0 1.4rem 0;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:1.8rem;'>
    <div style='display:inline-flex;align-items:center;gap:0.4rem;background:rgba(255,193,7,0.10);
        border:1px solid rgba(255,193,7,0.25);border-radius:20px;padding:0.22rem 0.75rem;
        font-size:0.8rem;font-weight:600;color:#FFC107;margin-bottom:0.6rem;'>
        🗺️ &nbsp;Step 3 of 3
    </div>
    <div style='font-family:Outfit,sans-serif;font-size:2rem;font-weight:800;color:#FFFFFF;
        letter-spacing:-0.5px;margin:0 0 0.4rem 0;'>
        Your Interactive Roadmap
    </div>
    <div style='font-size:0.84rem;color:#888;max-width:620px;line-height:1.6;'>
        Track your progress. Check off the resources below and click <strong>Save Progress</strong> to sync with your Progress Tracker.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Check if Analysis is Complete ─────────────────────────────────────────────
if not st.session_state.get("analysis_complete", False):
    st.warning("⚠️ We don't have your data yet! Please go to **Resume Analysis** to upload your resume first.")
    st.stop()

# ── Resource Database ─────────────────────────────────────────────────────────
RESOURCE_DB = {
    "Python": {
        "course": {"name": "100 Days of Code: The Complete Python Pro Bootcamp", "url": "https://www.udemy.com/course/100-days-of-code/"},
        "project": "Build a command-line task manager or a web scraper for job postings.",
        "reading": {"name": "Automate the Boring Stuff with Python", "url": "https://automatetheboringstuff.com/"}
    },
    "Machine Learning": {
        "course": {"name": "Machine Learning Specialization by Andrew Ng", "url": "https://www.coursera.org/specializations/machine-learning-introduction"},
        "project": "Build a housing price prediction model using Scikit-Learn.",
        "reading": {"name": "Introduction to Statistical Learning (Free PDF)", "url": "https://www.statlearning.com/"}
    },
    "Deep Learning": {
        "course": {"name": "Deep Learning Specialization by DeepLearning.AI", "url": "https://www.coursera.org/specializations/deep-learning"},
        "project": "Build an image classifier using a Convolutional Neural Network.",
        "reading": {"name": "Deep Learning Book by Ian Goodfellow", "url": "https://www.deeplearningbook.org/"}
    },
    "Sql": {
        "course": {"name": "PostgreSQL for Everybody (freeCodeCamp)", "url": "https://www.youtube.com/watch?v=qw--VYLpxG4"},
        "project": "Design a relational database for a mock e-commerce store and write 5 complex join queries.",
        "reading": {"name": "SQLBolt - Interactive Lessons", "url": "https://sqlbolt.com/"}
    },
    "Pandas": {
        "course": {"name": "Data Analysis with Python (freeCodeCamp)", "url": "https://www.youtube.com/watch?v=r-uOLxNrNk8"},
        "project": "Download a dataset from Kaggle and clean/analyze it to find top 3 trends.",
        "reading": {"name": "Official Pandas User Guide", "url": "https://pandas.pydata.org/docs/user_guide/index.html"}
    },
    "Docker": {
        "course": {"name": "Docker Tutorial for Beginners (TechWorld with Nana)", "url": "https://www.youtube.com/watch?v=3c-iBn73dDE"},
        "project": "Containerize a simple Python Flask API and run it locally.",
        "reading": {"name": "Docker Overview (Official Docs)", "url": "https://docs.docker.com/get-started/overview/"}
    },
    "Git": {
        "course": {"name": "Git and GitHub for Beginners (freeCodeCamp)", "url": "https://www.youtube.com/watch?v=RGOj5yH7evk"},
        "project": "Create a repository, branch off, make changes, and open a Pull Request.",
        "reading": {"name": "Pro Git Book (Free)", "url": "https://git-scm.com/book/en/v2"}
    }
}

def get_resources(skill):
    return RESOURCE_DB.get(skill, {
        "course": {"name": f"{skill} Full Course for Beginners (YouTube)", "url": f"https://www.youtube.com/results?search_query={skill.replace(' ', '+')}+full+course"},
        "project": f"Build a small, single-feature application focused entirely on using {skill}.",
        "reading": {"name": f"Official {skill} Documentation & Best Practices", "url": f"https://www.google.com/search?q={skill}+official+documentation"}
    })

# ── Fetch & Clean Data ────────────────────────────────────────────────────────
target_role = st.session_state.get("target_role", "your target role")
evaluated = st.session_state["match_results"]["evaluated"]

def extract_skill_names(skill_list):
    cleaned = []
    for s in skill_list:
        if isinstance(s, (tuple, list)):
            cleaned.append(str(s[0]).title()) 
        else:
            cleaned.append(str(s).title())
    return cleaned

missing_skills = extract_skill_names(evaluated.get("missing", []))
partial_skills = extract_skill_names(evaluated.get("partial", []))
skills_to_learn = missing_skills + partial_skills

if not skills_to_learn:
    st.success(f"🎉 Wow! You already have all the core skills for a **{target_role}**. Your roadmap is to start applying right now!")
    st.balloons()
    st.stop()

# ── Initialize Persistent Session State for Tasks ─────────────────────────────
for skill in skills_to_learn:
    for task_type in ["course", "project", "reading"]:
        state_key = f"saved_task_{skill}_{task_type}"
        if state_key not in st.session_state:
            st.session_state[state_key] = False

# ── Render Action Modules with Form/State Saving ──────────────────────────────
st.markdown(f"<h3 style='color: #FFFFFF; font-size: 1.3rem; margin-bottom: 1.5rem;'>Action Plan to become a {target_role}</h3>", unsafe_allow_html=True)

# We use a form so user checks can be explicitly committed
with st.form(key="roadmap_form"):
    
    temp_checkbox_states = {}
    
    for skill in skills_to_learn:
        priority = "🔴 Missing Skill" if skill in missing_skills else "🟡 Partial Skill"
        
        with st.expander(f"{skill}  —  {priority}", expanded=False):
            resources = get_resources(skill)
            
            st.markdown("#### 1. Take a Course")
            st.markdown(f"[{resources['course']['name']}]({resources['course']['url']})")
            temp_checkbox_states[f"saved_task_{skill}_course"] = st.checkbox(
                f"I completed the {skill} course", 
                value=st.session_state.get(f"saved_task_{skill}_course", False)
            )
            
            st.markdown("#### 2. Hands-On Project")
            st.info(f"**Mission:** {resources['project']}")
            temp_checkbox_states[f"saved_task_{skill}_project"] = st.checkbox(
                f"I built the {skill} project", 
                value=st.session_state.get(f"saved_task_{skill}_project", False)
            )
            
            st.markdown("#### 3. Reading Material")
            st.markdown(f"[{resources['reading']['name']}]({resources['reading']['url']})")
            temp_checkbox_states[f"saved_task_{skill}_reading"] = st.checkbox(
                f"I finished the {skill} reading", 
                value=st.session_state.get(f"saved_task_{skill}_reading", False)
            )

    st.markdown("<br>", unsafe_allow_html=True)
    submit_button = st.form_submit_button(label="💾 Save Progress", use_container_width=True)

if submit_button:
    # Commit form values explicitly into standard session_state keys used by the tracker
    for key, val in temp_checkbox_states.items():
        st.session_state[key] = val
        # Also map to the shorthand version for the progress calculation
        shorthand_key = key.replace("saved_", "")
        st.session_state[shorthand_key] = val
        
    st.success("✅ Progress successfully saved and synced to your Progress Tracker!")
    st.balloons()

# ── Calculate Live Progress for Top Bar ───────────────────────────────────────
total_tasks = len(skills_to_learn) * 3
completed_tasks = sum(
    1 for skill in skills_to_learn 
    for t in ["course", "project", "reading"] 
    if st.session_state.get(f"task_{skill}_{t}", False)
)
progress_pct = int((completed_tasks / total_tasks) * 100)

st.markdown(f"<div class='progress-text' style='margin-top: 2rem;'>Current Saved Progress: {progress_pct}% ({completed_tasks} of {total_tasks} tasks completed)</div>", unsafe_allow_html=True)
st.progress(progress_pct / 100.0)

# ── Navigation Footer ─────────────────────────────────────────────────────────
st.markdown("<div style='height: 1.5rem;'></div>", unsafe_allow_html=True)
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/4_Progress_Tracker.py", label="📈 View Progress Tracker Dashboard", icon=None)
with col2:
    st.page_link("Home.py", label="📊 Go to Dashboard", icon=None)