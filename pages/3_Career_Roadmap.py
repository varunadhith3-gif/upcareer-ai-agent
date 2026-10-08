import streamlit as st
import json
import os
from utils.sidebar import render_sidebar

st.set_page_config(
    page_title="UpCareer AI - Career Roadmap",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

st.markdown("""
<div style='padding:2rem 0 1.4rem 0;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:1.8rem;'>
    <div style='display:inline-flex;align-items:center;gap:0.4rem;background:rgba(72,199,142,0.10);
        border:1px solid rgba(72,199,142,0.25);border-radius:20px;padding:0.22rem 0.75rem;
        font-size:0.8rem;font-weight:600;color:#48C78E;margin-bottom:0.6rem;'>
        🗺️ &nbsp;Personalized Milestone Engine
    </div>
    <div style='font-family:Outfit,sans-serif;font-size:2rem;font-weight:800;color:#FFFFFF;
        letter-spacing:-0.5px;margin:0 0 0.4rem 0;'>
        Career Roadmap & Action Plan
    </div>
    <div style='font-size:0.84rem;color:#888;max-width:650px;line-height:1.6;'>
        Step-by-step milestones tailored to bridge your skill gaps and target your desired role.
    </div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.get("analysis_complete", False):
    st.warning("⚠️ No resume profile found! Please run your analysis on the **Resume Analysis** page first.")
    st.stop()

target_role = st.session_state.get("target_role", "Software Engineer")
match_results = st.session_state.get("match_results", {})
evaluated = match_results.get("evaluated", {"missing": [], "partial": [], "mastered": []})

# Helper function to map skills directly to verified professional platform courses (Udemy/Coursera)
def get_verified_course_link(skill_name: str) -> tuple[str, str]:
    skill_lower = skill_name.lower().strip()
    
    course_directory = {
        "docker": ("Docker Mastery: with Kubernetes + Swarm (Udemy)", "https://www.udemy.com/course/docker-mastery/"),
        "kubernetes": ("Certified Kubernetes Administrator (CKA) with Practice Tests (Udemy)", "https://www.udemy.com/course/certified-kubernetes-administrator-course/"),
        "system design": ("System Design Interview Guide for Software Architecture (Udemy)", "https://www.udemy.com/course/system-design-interview-guide-architectures/"),
        "ci/cd pipelines": ("DevOps Tools: Git, Jenkins, Ansible, Docker, Kubernetes (Udemy)", "https://www.udemy.com/course/devops-prerequisite-course/"),
        "microservices": ("Microservices Architecture - Practical Implementation (Udemy)", "https://www.udemy.com/course/microservices-architecture-and-design-patterns/"),
        "data structures & algorithms": ("Data Structures and Algorithms Specialization (Coursera)", "https://www.coursera.org/specializations/data-structures-algorithms"),
        "cloud computing (aws/gcp)": ("AWS Certified Solutions Architect Associate (Udemy)", "https://www.udemy.com/course/aws-certified-solutions-architect-associate-saa-c03/"),
        "linux/unix": ("Linux Administration Bootcamp: Go from Beginner to Advanced (Udemy)", "https://www.udemy.com/course/linux-administration-bootcamp/")
    }
    
    if skill_lower in course_directory:
        return course_directory[skill_lower]
    
    formatted_query = skill_name.replace(" ", "+")
    return (f"Complete {skill_name} Course & Practice (Udemy)", f"https://www.udemy.com/topic/{formatted_query.lower()}/")

missing_skills = evaluated.get("missing", [])
if not missing_skills:
    st.success("🎉 Outstanding! You have no missing critical skills for your target role.")
else:
    st.markdown(f"### Action Plan for Target Role: **{target_role}**")
    study_bandwidth = st.session_state.get("study_bandwidth", 10)
    hours_per_skill = max(1, study_bandwidth // len(missing_skills))
    st.info(f"⏱️ Based on your **{study_bandwidth} hours/week** study bandwidth, aim to spend about **{hours_per_skill} hours/week** on each skill module below.")
    st.markdown("Complete the modules below for each identified skill gap:")

    if "roadmap_progress" not in st.session_state:
        st.session_state["roadmap_progress"] = {}

    temp_checkbox_states = {}

    for item in missing_skills:
        skill = item[0] if isinstance(item, (tuple, list)) else item
        
        with st.expander(f"📌 {skill} — Action Required", expanded=False):
            # Retrieve checkbox completion states
            c_key = f"saved_task_{skill}_course"
            p_key = f"saved_task_{skill}_project"
            r_key = f"saved_task_{skill}_reading"
            
            c_status = st.session_state["roadmap_progress"].get(c_key, False)
            p_status = st.session_state["roadmap_progress"].get(p_key, False)
            r_status = st.session_state["roadmap_progress"].get(r_key, False)

            # 1. Take a Course (Using direct verified Udemy/Coursera links)
            course_title, course_url = get_verified_course_link(skill)
            st.markdown("#### 1. Take a Course")
            st.markdown(f"[{course_title}]({course_url})")
            temp_checkbox_states[c_key] = st.checkbox(f"I completed the {skill} course", value=c_status, key=c_key)

            st.divider()

            # 2. Hands-On Project
            st.markdown("#### 2. Hands-On Project")
            st.info(f"**Mission**: Build a small application or component focused entirely on implementing {skill} in a real-world scenario.")
            temp_checkbox_states[p_key] = st.checkbox(f"I built the {skill} project", value=p_status, key=p_key)

            st.divider()

            # 3. Reading Material
            st.markdown("#### 3. Reading Material")
            st.markdown(f"[{skill} Official Documentation & Guides](https://www.google.com/search?q={skill.replace(' ', '+')}+documentation)")
            temp_checkbox_states[r_key] = st.checkbox(f"I finished the {skill} reading", value=r_status, key=r_key)

    # Save progress action button
    if st.button("💾 Save Progress & Update Roadmap", type="primary"):
        for k, v in temp_checkbox_states.items():
            st.session_state["roadmap_progress"][k] = v
        st.toast("✅ Roadmap progress saved successfully!", icon="🎉")