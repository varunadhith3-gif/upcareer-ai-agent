import streamlit as st
import os
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go  # type: ignore

from config import DEFAULT_WEEKS, DEFAULT_HOURS_PER_WEEK
from core.parser import parse_document
from core.extractor import extract_entities, extract_jd_skills
from core.matcher import evaluate_skills
from core.ontology_dag import resolve_prerequisites, build_skill_dag
from core.optimizer import generate_roadmap
from core.scorer import calculate_readiness_score, calculate_projected_score
from utils.exporter import generate_roadmap_pdf

st.set_page_config(page_title="UpCareer AI Agent", layout="wide")

custom_css = """
<style>
/* Modern Dark Theme */
[data-testid="stAppViewContainer"] {
    background-color: #0d1117;
    color: #c9d1d9;
    font-family: 'Inter', sans-serif;
}
[data-testid="stSidebar"] {
    background-color: #161b22;
    border-right: 1px solid #30363d;
}
.stButton>button {
    background: linear-gradient(135deg, #6e40c9, #3b82f6);
    color: white;
    border: none;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    font-weight: 600;
    transition: all 0.3s ease;
}
.stButton>button:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(110, 64, 201, 0.4);
}
h1, h2, h3 {
    color: #58a6ff !important;
}
.skill-card {
    background-color: #1c2128;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
}
.skill-title {
    font-size: 1.2rem;
    font-weight: bold;
    color: #e6edf3;
    margin-bottom: 0.5rem;
}
.skill-status {
    font-size: 0.9rem;
    font-weight: 600;
}
.status-mastered { color: #3fb950; }
.status-partial { color: #d29922; }
.status-critical { color: #f85149; }
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

st.title("UpCareer AI: Career Mentor & Roadmap Generator")

# Sidebar
with st.sidebar:
    st.title("🛠️ Configuration")
    st.markdown("Configure your career roadmap parameters below.")
    st.divider()
    
    st.subheader("📄 Upload Profile")
    resume_file = st.file_uploader("Upload Resume (PDF/DOCX/TXT)", type=['pdf', 'docx', 'txt'])
    
    st.divider()
    st.subheader("🎯 Target Job Description")
    use_sample = st.checkbox("Use Sample JDs", value=False)
    if use_sample:
        jd_choice = st.selectbox("Select Sample", ["Software Engineer", "Data Scientist"])
        if jd_choice == "Software Engineer":
            with open("sample_data/jd_se.txt", "r") as f:
                jd_text_input = f.read()
        else:
            with open("sample_data/jd_ds.txt", "r") as f:
                jd_text_input = f.read()
        
        jd_text = st.text_area("Job Description", jd_text_input, height=200)
    else:
        jd_text = st.text_area("Paste Job Description Here", height=200)
        
    st.divider()
    st.subheader("⏱️ Constraints")
    target_weeks = st.slider("Target Timeframe (Weeks)", min_value=1, max_value=24, value=DEFAULT_WEEKS)
    weekly_hours = st.slider("Weekly Study Hours", min_value=2, max_value=40, value=DEFAULT_HOURS_PER_WEEK)
    
    st.divider()
    process_btn = st.button("🚀 Generate Roadmap", type="primary", use_container_width=True)

if process_btn:
    if not resume_file and not use_sample:
        st.error("Please upload a resume or select a sample.")
    elif not jd_text:
        st.error("Please provide a Job Description.")
    else:
        with st.spinner("Analyzing profile and computing roadmap..."):
            
            # 1. Parse Input
            if resume_file:
                resume_text = parse_document(resume_file, resume_file.name)
            else:
                # Use sample resume matching JD choice
                if jd_choice == "Software Engineer":
                    with open("sample_data/resume_se.txt", "r") as f:
                        resume_text = f.read()
                else:
                    with open("sample_data/resume_ds.txt", "r") as f:
                        resume_text = f.read()
                        
            # 2. Extract Entities
            candidate_data = extract_entities(resume_text)
            jd_skills = extract_jd_skills(jd_text)
            
            if not jd_skills:
                st.error("Could not extract any standard skills from JD.")
                st.stop()
                
            # 3. Match Skills
            evaluated, skill_scores = evaluate_skills(candidate_data, jd_skills)
            
            # 4. Resolve Prerequisites
            missing_skills = [s for s, _ in evaluated["missing"]]
            acquired_skills = [s for s, _ in evaluated["mastered"]] + [s for s, _ in evaluated["partial"]]
            
            ordered_backlog = resolve_prerequisites(missing_skills, acquired_skills)
            
            # 5. Optimize Roadmap
            roadmap = generate_roadmap(ordered_backlog, weekly_hours, target_weeks)
            
            # 6. Scorer
            current_score = calculate_readiness_score(skill_scores, jd_skills)
            projected_score = calculate_projected_score(skill_scores, jd_skills, ordered_backlog)
            
            # ----- Render Dashboard -----
            st.success("Analysis Complete!")
            
            def create_gauge(score, title):
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number",
                    value = score,
                    title = {'text': title, 'font': {'size': 20, 'color': '#58a6ff'}},
                    gauge = {
                        'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                        'bar': {'color': "#6e40c9"},
                        'bgcolor': "rgba(0,0,0,0)",
                        'borderwidth': 2,
                        'bordercolor': "#30363d",
                        'steps': [
                            {'range': [0, 50], 'color': '#f85149'},
                            {'range': [50, 80], 'color': '#d29922'},
                            {'range': [80, 100], 'color': '#3fb950'}],
                    }
                ))
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font={'color': "#c9d1d9", 'family': "Inter"},
                    height=300,
                    margin=dict(l=20, r=20, t=50, b=20)
                )
                return fig
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.plotly_chart(create_gauge(current_score, "Current Readiness Score"), use_container_width=True)
                
            with col2:
                st.plotly_chart(create_gauge(projected_score, "Projected Score After Roadmap"), use_container_width=True)

            st.divider()
            
            st.subheader("Skill Gap Analysis")
            
            all_skills = []
            for s, p in evaluated["mastered"]: all_skills.append({"Skill": s, "Status": "Mastered", "Icon": "✅", "Class": "status-mastered"})
            for s, p in evaluated["partial"]: all_skills.append({"Skill": s, "Status": "Partial Gap", "Icon": "⚠️", "Class": "status-partial"})
            for s, p in evaluated["missing"]: all_skills.append({"Skill": s, "Status": "Critical Gap", "Icon": "❌", "Class": "status-critical"})
            
            # Display as cards in columns
            cols = st.columns(3)
            for i, skill in enumerate(all_skills):
                col = cols[i % 3]
                card_html = f"""
                <div class="skill-card">
                    <div class="skill-title">{skill['Skill']}</div>
                    <div class="skill-status {skill['Class']}">
                        {skill['Icon']} {skill['Status']}
                    </div>
                </div>
                """
                col.markdown(card_html, unsafe_allow_html=True)
            
            st.divider()
            
            # Roadmap
            st.subheader("Personalized Roadmap")
            st.write(f"**Status:** {roadmap['status']}")
            
            for ms in roadmap["milestones"]:
                with st.expander(f"Week {ms['week']}"):
                    st.write(f"**Skills to Learn:** {', '.join(ms['skills'])}")
                    st.write(f"**Project:** {ms['project']}")
                    
            # Export to PDF
            pdf_path = generate_roadmap_pdf(roadmap)
            with open(pdf_path, "rb") as f:
                st.download_button("Download Roadmap PDF", f, file_name="UpCareer_Roadmap.pdf", mime="application/pdf")
            
            st.divider()
            
            # DAG Visual (pyvis)
            st.subheader("Prerequisite Skill DAG")
            G_full = build_skill_dag()
            # subgraph of relevant skills
            relevant = set(jd_skills + ordered_backlog + acquired_skills)
            # Find ancestors of relevant
            G = G_full.subgraph([n for n in G_full.nodes() if n in relevant])
            
            net = Network(height="400px", width="100%", directed=True)
            for node in G.nodes():
                color = "green" if node in acquired_skills else ("red" if node in ordered_backlog else "gray")
                net.add_node(node, label=node, color=color)
                
            for edge in G.edges():
                net.add_edge(edge[0], edge[1])
                
            try:
                path = "/tmp" if os.name != "nt" else "C:\\Windows\\Temp"
                net.save_graph(f"{path}/graph.html")
                HtmlFile = open(f"{path}/graph.html", 'r', encoding='utf-8')
                source_code = HtmlFile.read() 
                components.html(source_code, height=450)
            except Exception as e:
                st.warning("Could not render DAG visualization.")
                st.write(list(G.edges()))
