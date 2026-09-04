import streamlit as st
import plotly.graph_objects as go
import google.generativeai as genai
import json
from utils.sidebar import render_sidebar

st.set_page_config(
    page_title="UpCareer AI - Skill Gap Report",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

def _badge(score: int) -> tuple[str, str]:
    if score >= 80: return "Strong", "#48C78E"
    elif score >= 60: return "Good", "#FFC107"
    elif score >= 40: return "Fair", "#FF9800"
    else: return "Early Stage", "#FF5252"

# ── 1. AGENT TOOL: Dynamic Score Recalculation ────────────────────────────────
def evaluate_role_fit(resume_text, target_role):
    """Calls Gemini to recalculate scores based on the new target role."""
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-pro')
    
    prompt = f"""
    You are an expert AI Career Coach. Analyze the following resume against the industry requirements for a {target_role}.
    Return ONLY a valid JSON object with this exact structure (do not include markdown formatting or backticks):
    {{
        "readiness_score": 75,
        "category_scores": {{"Skills": 80, "Experience": 70, "Projects": 60, "Education": 90, "Certifications": 50}}
    }}
    Resume text: {resume_text}
    """
    try:
        response = model.generate_content(prompt)
        clean_json = response.text.replace("```json", "").replace("```", "").strip()
        return json.loads(clean_json)
    except Exception as e:
        return None

# ── 2. SMART STATE CHECK ──────────────────────────────────────────────────────
has_data = st.session_state.get("analysis_complete", False)
role = st.session_state.get("target_role", "Target Role")
resume_text = st.session_state.get("resume_text", "")

# If the user changed the role, force the Agent to recalculate before rendering the page!
if has_data and resume_text and st.session_state.get("last_evaluated_role") != role:
    with st.spinner(f"Agent analyzing skill gaps for {role}..."):
        new_data = evaluate_role_fit(resume_text, role)
        if new_data:
            st.session_state["readiness_score"] = new_data["readiness_score"]
            st.session_state["category_scores"] = new_data["category_scores"]
            st.session_state["last_evaluated_role"] = role
            st.rerun() # Refresh the page with the new numbers

# Pull live variables for UI
score          = st.session_state.get("readiness_score", 0)
cats           = st.session_state.get("category_scores", {})
user_name      = st.session_state.get("user_name", "Candidate")
match_results  = st.session_state.get("match_results", {})
evaluated      = match_results.get("evaluated", {"mastered": [], "partial": [], "missing": []})
skill_scores   = match_results.get("skill_scores", {})
jd_skills      = match_results.get("jd_skills", [])

badge_label, badge_color = _badge(score)

# ── 3. RENDER UI ──────────────────────────────────────────────────────────────
hdr_left, hdr_right = st.columns([3, 1], gap="small")

with hdr_left:
    st.markdown(
        "<div style='padding:1.8rem 0 0.3rem 0;'>"
        "<div style='display:inline-flex;align-items:center;gap:0.4rem; background:rgba(255,193,7,0.10);border:1px solid rgba(255,193,7,0.25); border-radius:20px;padding:0.22rem 0.75rem;font-size:0.8rem;font-weight:600; color:#FFC107;margin-bottom:0.5rem;'>🎯 &nbsp;Skill Gap Analysis</div>"
        "<div style='font-family:Outfit,sans-serif;font-size:2rem;font-weight:800; color:#FFFFFF;letter-spacing:-0.5px;margin:0 0 0.3rem 0;'>Skill Gap Report</div>"
        f"<div style='font-size:0.84rem;color:#888;line-height:1.6;'><strong style='color:#DDD;'>{role}</strong> &nbsp;·&nbsp; Live AI evaluation enabled.</div></div>",
        unsafe_allow_html=True,
    )

with hdr_right:
    st.markdown("<div style='padding-top:2.4rem;'>", unsafe_allow_html=True)
    if has_data:
        st.markdown(
            f"<div style='display:inline-block;background:{badge_color}22; border:1px solid {badge_color}55;border-radius:20px;padding:0.3rem 0.9rem; font-size:0.82rem;font-weight:700;color:{badge_color}; margin-bottom:0.6rem;text-align:center;width:100%;'>● &nbsp;{badge_label}</div>",
            unsafe_allow_html=True,
        )
        if st.button("⬇ Export PDF", key="export_pdf_btn", use_container_width=True):
            try:
                from utils.exporter import generate_skill_gap_pdf
                pdf_bytes = generate_skill_gap_pdf({"role": role, "score": score, "badge": badge_label, "user_name": user_name, "category_scores": cats, "evaluated": evaluated, "skill_scores": skill_scores})
                st.download_button(label="📄 Download report.pdf", data=pdf_bytes, file_name=f"UpCareer_{role.replace(' ', '_')}.pdf", mime="application/pdf")
            except Exception as e:
                st.error(f"Export failed: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<hr style='border:none;border-top:1px solid rgba(255,255,255,0.06); margin:0.2rem 0 1.6rem 0;'>", unsafe_allow_html=True)

if not has_data:
    st.markdown(
        "<div style='background:#161616;border:1px solid rgba(255,255,255,0.06); border-radius:16px;padding:3.5rem 2rem;text-align:center;margin-top:1rem;'>"
        "<div style='font-size:3rem;margin-bottom:1rem;'>📋</div>"
        "<div style='font-family:Outfit,sans-serif;font-size:1.3rem;font-weight:700; color:#FFFFFF;margin-bottom:0.5rem;'>No analysis yet</div>"
        "<div style='font-size:0.85rem;color:#777;max-width:420px;margin:0 auto 1.4rem auto; line-height:1.6;'>Upload your resume and click <strong style='color:#FFC107;'>Analyze resume</strong> to generate your live report.</div></div>",
        unsafe_allow_html=True,
    )
    st.page_link("pages/1_Resume_Analysis.py", label="📄 Go to Resume Analysis", icon=None)
    st.stop()

col_gauge, col_breakdown = st.columns([1, 1.55], gap="large")

with col_gauge:
    st.markdown(
        "<div style='background:#161616;border:1px solid rgba(255,255,255,0.06); border-radius:16px;padding:1.5rem 1.6rem 0.8rem 1.6rem;'>"
        "<div style='font-family:Outfit,sans-serif;font-size:0.78rem;font-weight:700; letter-spacing:0.08em;text-transform:uppercase;color:#A0A0A0; margin-bottom:0.2rem;'>Career Readiness Score</div>"
        f"<div style='font-family:Outfit,sans-serif;font-size:1.1rem;font-weight:700; color:#FFFFFF;margin-bottom:0.6rem;'>{role}</div>",
        unsafe_allow_html=True,
    )

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"font": {"size": 52, "color": "#FFFFFF", "family": "Outfit, sans-serif"}},
        gauge={
            "axis": {"range": [0, 100], "tickwidth": 0, "tickcolor": "rgba(0,0,0,0)", "showticklabels": False},
            "bar": {"color": "#FFC107", "thickness": 0.72},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [{"range": [0, 100], "color": "#272727"}],
            "threshold": {"line": {"color": "#48C78E", "width": 4}, "thickness": 0.85, "value": score},
        },
        domain={"x": [0, 1], "y": [0, 1]},
    ))
    fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=260, margin=dict(t=30, b=10, l=20, r=20))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.markdown("<div style='font-size:0.73rem;color:#555;text-align:center; margin-top:-0.6rem;font-style:italic;padding-bottom:1rem;'>Live estimate updated via AI Agent</div></div>", unsafe_allow_html=True)

with col_breakdown:
    cat_meta = {"Skills": "🛠️", "Experience": "💼", "Projects": "🗂️", "Education": "🎓", "Certifications": "📜"}
    bars_html = ""
    for cat, cat_score in cats.items():
        icon = cat_meta.get(cat, "•")
        bar_block = (
            "<div style='margin-bottom:1.05rem;'>"
            "<div style='display:flex;justify-content:space-between;align-items:baseline;margin-bottom:0.3rem;'>"
            "<span style='font-size:0.84rem;font-weight:600;color:#FFFFFF;'>{icon}&nbsp; {cat}</span>"
            "<span style='font-size:0.84rem;font-weight:700;color:#FFC107;'>{score}</span>"
            "</div>"
            "<div style='background:rgba(255,255,255,0.07);border-radius:20px;height:6px; width:100%;overflow:hidden;margin-bottom:0.25rem;'>"
            "<div style='height:100%;border-radius:20px; background:linear-gradient(90deg,#FFC107 0%,#48C78E 100%);width:{pct}%;'></div>"
            "</div></div>"
        ).format(icon=icon, cat=cat, score=cat_score, pct=cat_score)
        bars_html += bar_block

    breakdown_html = (
        "<div style='background:#161616;border:1px solid rgba(255,255,255,0.06); border-radius:16px;padding:1.5rem 1.6rem 1.2rem 1.6rem;'>"
        "<div style='font-family:Outfit,sans-serif;font-size:1.15rem;font-weight:700; color:#FFFFFF;margin-bottom:1.1rem;'>Score breakdown</div>"
        + bars_html + "</div>"
    )
    st.markdown(breakdown_html, unsafe_allow_html=True)

# ── Footer nav ────────────────────────────────────────────────────────────────
st.markdown("<div style='height:1.2rem;'></div>", unsafe_allow_html=True)
fc1, fc2, fc3 = st.columns(3)
with fc1: st.page_link("Home.py", label="📊 Dashboard", icon=None)
with fc2: st.page_link("pages/1_Resume_Analysis.py", label="📄 Re-run Analysis", icon=None)
with fc3: st.page_link("pages/3_Career_Roadmap.py", label="🗺️ Career Roadmap", icon=None)