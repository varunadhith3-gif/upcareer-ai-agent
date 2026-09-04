import io
import math
import streamlit as st
from utils.sidebar import render_sidebar

st.set_page_config(
    page_title="UpCareer AI - Resume Analysis",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

# ── Page-level CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* Upload zone */
[data-testid="stFileUploader"] {
    background: #161616 !important;
    border: 2px dashed rgba(255,193,7,0.30) !important;
    border-radius: 14px !important;
    padding: 0.5rem !important;
    transition: border-color 0.3s ease !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: rgba(255,193,7,0.65) !important;
}
/* Text area */
[data-testid="stTextArea"] textarea {
    background: #1C1C1C !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #E0E0E0 !important;
    font-size: 0.83rem !important;
    font-family: 'Inter', monospace !important;
    resize: vertical !important;
}
[data-testid="stTextArea"] textarea:focus {
    border-color: rgba(255,193,7,0.5) !important;
    box-shadow: 0 0 0 2px rgba(255,193,7,0.12) !important;
}
/* Selectbox */
[data-testid="stSelectbox"] > div > div {
    background: #1C1C1C !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 10px !important;
    color: #FFFFFF !important;
}
/* Analyze button */
.analyze-btn > button {
    background: linear-gradient(135deg, #FFC107 0%, #FFD54F 100%) !important;
    color: #0D0D0D !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1.5rem !important;
    width: 100% !important;
    transition: opacity 0.2s ease, transform 0.15s ease !important;
    box-shadow: 0 4px 18px rgba(255,193,7,0.25) !important;
}
.analyze-btn > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Role → JD skill templates ─────────────────────────────────────────────────
ROLE_JD_SKILLS = {
    "Data Scientist": [
        "Python", "Machine Learning", "Deep Learning", "Natural Language Processing",
        "Pandas", "Numpy", "Scikit-Learn", "Tensorflow", "Pytorch", "Statistics",
        "Sql", "Data Analysis", "Linear Algebra", "Mlops", "Transformers",
    ],
    "Software Engineer": [
        "Python", "Java", "C++", "Data Structures", "Algorithms", "System Design",
        "Rest Apis", "Docker", "Kubernetes", "Sql", "Git", "Aws", "Ci/Cd",
    ],
    "Embedded Systems Engineer": [
        "C++", "Python", "Git", "System Design", "Algorithms", "Data Structures",
    ],
    "Product Manager": [
        "Data Analysis", "Statistics", "Rest Apis", "Git", "Sql",
    ],
    "ML Engineer": [
        "Python", "Machine Learning", "Deep Learning", "Tensorflow", "Pytorch",
        "Mlops", "Docker", "Kubernetes", "Aws", "Transformers", "Scikit-Learn",
        "Statistics", "Sql", "Git", "Ci/Cd",
    ],
}

ROLE_CATEGORY_WEIGHTS = {
    "Data Scientist":          {"Skills": 0.35, "Experience": 0.25, "Projects": 0.20, "Education": 0.12, "Certifications": 0.08},
    "Software Engineer":       {"Skills": 0.30, "Experience": 0.30, "Projects": 0.22, "Education": 0.10, "Certifications": 0.08},
    "Embedded Systems Engineer":{"Skills": 0.35, "Experience": 0.30, "Projects": 0.20, "Education": 0.10, "Certifications": 0.05},
    "Product Manager":         {"Skills": 0.25, "Experience": 0.35, "Projects": 0.18, "Education": 0.12, "Certifications": 0.10},
    "ML Engineer":             {"Skills": 0.35, "Experience": 0.25, "Projects": 0.22, "Education": 0.10, "Certifications": 0.08},
}

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style='padding:2rem 0 1.4rem 0;border-bottom:1px solid rgba(255,255,255,0.06);margin-bottom:1.8rem;'>
    <div style='display:inline-flex;align-items:center;gap:0.4rem;background:rgba(255,193,7,0.10);
        border:1px solid rgba(255,193,7,0.25);border-radius:20px;padding:0.22rem 0.75rem;
        font-size:0.8rem;font-weight:600;color:#FFC107;margin-bottom:0.6rem;'>
        📄 &nbsp;Step 1 of 3
    </div>
    <div style='font-family:Outfit,sans-serif;font-size:2rem;font-weight:800;color:#FFFFFF;
        letter-spacing:-0.5px;margin:0 0 0.4rem 0;'>
        Resume Analysis
    </div>
    <div style='font-size:0.84rem;color:#888;max-width:620px;line-height:1.6;'>
        Upload a resume or paste its text, pick your target role, and the agent pipeline will
        extract your profile and match it against role requirements.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Two-column layout ─────────────────────────────────────────────────────────
col_left, col_right = st.columns([1.1, 1], gap="large")

# ══════════════════════════════════════════════════════════════════════════════
# LEFT COLUMN — Upload + text area
# ══════════════════════════════════════════════════════════════════════════════
with col_left:
    st.markdown(
        "<div style='font-family:Outfit,sans-serif;font-size:1.05rem;font-weight:700;"
        "color:#FFFFFF;margin-bottom:0.7rem;'>📂 Upload your resume</div>",
        unsafe_allow_html=True,
    )

    # 1. State lock for uploader visibility
    if "uploader_visible" not in st.session_state:
        st.session_state["uploader_visible"] = (st.session_state.get("_last_uploaded_name") is None)

    if st.session_state["uploader_visible"]:
        uploaded_file = st.file_uploader(
            label="Resume file",
            type=["pdf", "docx", "txt"],
            accept_multiple_files=False,
            label_visibility="collapsed",
            key="resume_file_upload",
            help="Accepted formats: PDF, DOCX, TXT · max one file",
        )

        if not uploaded_file:
            st.markdown(
                "<div style='text-align:center;color:#666;font-size:0.78rem;margin-top:-0.4rem;"
                "margin-bottom:0.6rem;'>☁️ Drag and drop your resume, or click to browse"
                "<br><span style='color:#444;'>Accepted formats: PDF · DOCX · TXT &nbsp;·&nbsp; max one file</span></div>",
                unsafe_allow_html=True,
            )
        else:
            # File just uploaded
            file_bytes = io.BytesIO(uploaded_file.read())
            try:
                from core.parser import parse_document
                extracted_raw = parse_document(file_bytes, filename=uploaded_file.name)
                st.session_state["resume_text_area"] = extracted_raw
                st.session_state["_last_uploaded_name"] = uploaded_file.name
                st.session_state["uploader_visible"] = False # Lock the UI
                st.rerun() # Refresh to show locked state
            except Exception as exc:
                st.error(f"⚠️ Could not parse file: {exc}")
    else:
        # 2. File is already loaded in memory
        st.markdown(
            f"<div style='background:rgba(72,199,142,0.1); border:1px solid rgba(72,199,142,0.3); border-radius:10px; padding:0.8rem 1rem; margin-bottom:1rem;'>"
            f"<div style='color:#48C78E; font-size:0.85rem; font-weight:600;'>✅ Currently loaded:</div>"
            f"<div style='color:#FFF; font-weight:700; font-size:1rem; margin-top:0.2rem;'>{st.session_state['_last_uploaded_name']}</div>"
            f"</div>",
            unsafe_allow_html=True
        )
        if st.button("🔄 Upload a New Resume", use_container_width=True):
            st.session_state["uploader_visible"] = True
            st.rerun()

    # ── Editable text area ────────────────────────────────────────────────────
    st.markdown(
        "<div style='font-family:Outfit,sans-serif;font-size:0.82rem;font-weight:600;"
        "color:#A0A0A0;text-transform:uppercase;letter-spacing:0.06em;"
        "margin:1.1rem 0 0.35rem 0;'>Extracted resume text (editable)</div>",
        unsafe_allow_html=True,
    )

    st.text_area(
        label="Resume text",
        height=320,
        placeholder="Extracted text appears here — or paste your resume text directly.",
        label_visibility="collapsed",
        key="resume_text_area", # Automatically syncs with st.session_state
    )

# ══════════════════════════════════════════════════════════════════════════════
# RIGHT COLUMN — Role selector, JD, Analyze button
# ══════════════════════════════════════════════════════════════════════════════
with col_right:

    # ── Target role ───────────────────────────────────────────────────────────
    st.markdown(
        "<div style='font-family:Outfit,sans-serif;font-size:1.05rem;font-weight:700;"
        "color:#FFFFFF;margin-bottom:0.7rem;'>🎯 Target role</div>",
        unsafe_allow_html=True,
    )

    role_options = list(ROLE_JD_SKILLS.keys())
    default_role = st.session_state.get("target_role", "Data Scientist")
    default_idx  = role_options.index(default_role) if default_role in role_options else 0

    selected_role = st.selectbox(
        label="Target role",
        options=role_options,
        index=default_idx,
        label_visibility="collapsed",
        key="role_selectbox",
    )
    st.session_state["target_role"] = selected_role

    # ── JD paste area ─────────────────────────────────────────────────────────
    st.markdown(
        "<div style='font-family:Outfit,sans-serif;font-size:0.82rem;font-weight:600;"
        "color:#A0A0A0;text-transform:uppercase;letter-spacing:0.06em;"
        "margin:1.1rem 0 0.35rem 0;'>Job description <span style=\"color:#555;font-weight:400;"
        "text-transform:none;letter-spacing:0;\">(optional)</span></div>",
        unsafe_allow_html=True,
    )

    st.text_area(
        label="Job description",
        height=180,
        placeholder="Paste a specific job posting to match against it instead of the generic role template.",
        label_visibility="collapsed",
        key="jd_text_area",
    )

    st.markdown("<div style='height:0.6rem;'></div>", unsafe_allow_html=True)

    # ── Analyze button ────────────────────────────────────────────────────────
    st.markdown('<div class="analyze-btn">', unsafe_allow_html=True)
    analyze_clicked = st.button("⚡  Analyze resume", key="analyze_btn", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(
        "<div style='font-size:0.72rem;color:#555;margin-top:0.7rem;line-height:1.5;'>"
        "🔒 Your resume text is processed only to generate your own analysis, stays private "
        "to your account, and can be deleted from Profile &amp; Settings."
        "</div>",
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════════════════════════════════
# ANALYSIS PIPELINE
# ══════════════════════════════════════════════════════════════════════════════
if analyze_clicked:
    resume_text_final = st.session_state.get("resume_text_area", "").strip()

    if not resume_text_final:
        st.warning("⚠️ Please upload a resume file or paste resume text before analyzing.")
    else:
        with st.spinner("🔍 Running analysis pipeline…"):
            try:
                # ── Step 1: Extract entities from resume ──────────────────────
                from core.extractor import extract_entities, extract_jd_skills
                candidate_data = extract_entities(resume_text_final)

                # ── Step 2: Determine JD skill list ───────────────────────────
                jd_text_final = st.session_state.get("jd_text_area", "").strip()
                if jd_text_final:
                    jd_skills = extract_jd_skills(jd_text_final)
                    if not jd_skills:                           
                        jd_skills = ROLE_JD_SKILLS.get(selected_role, [])
                else:
                    jd_skills = ROLE_JD_SKILLS.get(selected_role, [])

                # ── Step 3: Match skills ───────────────────────────────────────
                from core.matcher import evaluate_skills
                evaluated, skill_scores = evaluate_skills(candidate_data, jd_skills)

                # ── Step 4 & 5: Advanced Scoring with Asymptotic Decay ────────
                weights = ROLE_CATEGORY_WEIGHTS.get(
                    selected_role,
                    {"Skills": 0.35, "Experience": 0.25, "Projects": 0.20,
                     "Education": 0.12, "Certifications": 0.08},
                )

                n_jd       = max(len(jd_skills), 1)
                n_mastered = len(evaluated["mastered"])
                n_partial  = len(evaluated["partial"])
                n_missing  = len(evaluated["missing"])

                # Skills: Ratio of mastered/partial to required
                skill_ratio = (n_mastered + (0.4 * n_partial)) / n_jd
                skill_cat_score = int(round(min(100, skill_ratio * 100)))

                # Experience: Asymptotic curve (k = 0.045)
                exp_months = candidate_data.get("experience_months", 0)
                exp_cat_score = int(round(100 * (1 - math.exp(-0.045 * exp_months))))

                # Projects: Asymptotic curve (k = 0.25)
                proj_keywords = ["project", "built", "developed", "deployed", "github", "portfolio", "led", "architected"]
                proj_hits = sum(1 for kw in proj_keywords if kw in resume_text_final.lower())
                proj_cat_score = int(round(100 * (1 - math.exp(-0.25 * proj_hits))))

                # Education: Asymptotic curve (k = 0.6)
                edu_keywords = ["bachelor", "master", "phd", "b.tech", "m.tech", "b.e", "degree", "university", "college"]
                edu_hits = sum(1 for kw in edu_keywords if kw in resume_text_final.lower())
                edu_cat_score = int(round(100 * (1 - math.exp(-0.6 * edu_hits))))

                # Certifications: Asymptotic curve (k = 0.8)
                cert_keywords = ["certified", "certification", "certificate", "aws", "gcp", "azure", "coursera", "udemy"]
                cert_hits = sum(1 for kw in cert_keywords if kw in resume_text_final.lower())
                cert_cat_score = int(round(100 * (1 - math.exp(-0.8 * cert_hits))))

                category_scores = {
                    "Skills":           skill_cat_score,
                    "Experience":       exp_cat_score,
                    "Projects":         proj_cat_score,
                    "Education":        edu_cat_score,
                    "Certifications":   cert_cat_score,
                }

                # Compute True Weighted Readiness Score
                readiness = int(round(
                    (skill_cat_score * weights["Skills"]) +
                    (exp_cat_score * weights["Experience"]) +
                    (proj_cat_score * weights["Projects"]) +
                    (edu_cat_score * weights["Education"]) +
                    (cert_cat_score * weights["Certifications"])
                ))
                readiness = max(0, min(100, readiness))

                # ── Step 6: Persist everything to session_state ───────────────
                st.session_state.update({
                    "target_role":       selected_role,
                    "readiness_score":   readiness,
                    "category_scores":   category_scores,
                    "extracted_skills":  candidate_data.get("skills", []),
                    "match_results":     {
                        "evaluated":     evaluated,
                        "skill_scores":  skill_scores,
                        "jd_skills":     jd_skills,
                    },
                    "candidate_data":    candidate_data,
                    "skills_present":    n_mastered,
                    "skills_partial":    n_partial,
                    "skills_missing":    n_missing,
                    "analysis_complete": True,
                })

            except Exception as exc:
                st.error(f"❌ Pipeline error: {exc}")
                st.stop()

# Render results persistently across page reloads!
if st.session_state.get("analysis_complete"):
    evaluated   = st.session_state["match_results"]["evaluated"]
    n_mastered  = len(evaluated["mastered"])
    n_partial   = len(evaluated["partial"])
    n_missing   = len(evaluated["missing"])
    readiness   = st.session_state["readiness_score"]
    selected_role_state = st.session_state["target_role"]

    # Success banner
    st.markdown(
        "<div style='background:rgba(72,199,142,0.08);border:1px solid rgba(72,199,142,0.25);"
        "border-radius:14px;padding:1.2rem 1.4rem;margin-top:1.4rem;'>"
        "<div style='font-family:Outfit,sans-serif;font-size:1.05rem;font-weight:700;"
        "color:#48C78E;margin-bottom:0.4rem;'>✅ Analysis complete!</div>"
        "<div style='font-size:0.82rem;color:#999;line-height:1.6;'>"
        f"Readiness score: <strong style='color:#FFC107;'>{readiness}/100</strong> &nbsp;·&nbsp; "
        f"Role: <strong style='color:#FFF;'>{selected_role_state}</strong>"
        "</div></div>",
        unsafe_allow_html=True,
    )

    # Three mini stat cards
    stat_html = (
        "<div style='display:flex;gap:0.8rem;margin-top:1rem;'>"

        "<div style='flex:1;background:#161616;border:1px solid rgba(72,199,142,0.22);"
        "border-radius:12px;padding:1rem 1.1rem;'>"
        "<div style='font-size:0.72rem;font-weight:600;color:#888;text-transform:uppercase;"
        "letter-spacing:0.06em;margin-bottom:0.2rem;'>Present</div>"
        "<div style='font-family:Outfit,sans-serif;font-size:1.8rem;font-weight:800;"
        "color:#48C78E;line-height:1;'>{m}</div>"
        "<div style='font-size:0.7rem;color:#555;margin-top:0.15rem;'>Mastered skills</div>"
        "</div>"

        "<div style='flex:1;background:#161616;border:1px solid rgba(255,193,7,0.22);"
        "border-radius:12px;padding:1rem 1.1rem;'>"
        "<div style='font-size:0.72rem;font-weight:600;color:#888;text-transform:uppercase;"
        "letter-spacing:0.06em;margin-bottom:0.2rem;'>Partial</div>"
        "<div style='font-family:Outfit,sans-serif;font-size:1.8rem;font-weight:800;"
        "color:#FFC107;line-height:1;'>{p}</div>"
        "<div style='font-size:0.7rem;color:#555;margin-top:0.15rem;'>Gap skills</div>"
        "</div>"

        "<div style='flex:1;background:#161616;border:1px solid rgba(255,82,82,0.22);"
        "border-radius:12px;padding:1rem 1.1rem;'>"
        "<div style='font-size:0.72rem;font-weight:600;color:#888;text-transform:uppercase;"
        "letter-spacing:0.06em;margin-bottom:0.2rem;'>Missing</div>"
        "<div style='font-family:Outfit,sans-serif;font-size:1.8rem;font-weight:800;"
        "color:#FF5252;line-height:1;'>{x}</div>"
        "<div style='font-size:0.7rem;color:#555;margin-top:0.15rem;'>Critical gaps</div>"
        "</div>"

        "</div>"
    ).format(m=n_mastered, p=n_partial, x=n_missing)
    st.markdown(stat_html, unsafe_allow_html=True)

    # Navigation buttons
    st.markdown("<div style='height:0.8rem;'></div>", unsafe_allow_html=True)
    nav_col1, nav_col2 = st.columns(2)
    with nav_col1:
        st.page_link("Home.py", label="📊 View Dashboard", icon=None)
    with nav_col2:
        st.page_link("pages/2_Skill_Gap_Report.py", label="🎯 Skill Gap Report", icon=None)