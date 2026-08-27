import streamlit as st
import plotly.graph_objects as go
from utils.sidebar import render_sidebar

st.set_page_config(
    page_title="UpCareer AI - Skill Gap Report",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

render_sidebar()

# ── Helpers ───────────────────────────────────────────────────────────────────
def _badge(score: int) -> tuple[str, str]:
    """Return (label, hex_color) for the readiness badge."""
    if score >= 80:
        return "Strong",     "#48C78E"
    elif score >= 60:
        return "Good",       "#FFC107"
    elif score >= 40:
        return "Fair",       "#FF9800"
    else:
        return "Early Stage","#FF5252"

def _card_html(flex_items: list[str]) -> str:
    """Wrap items in a dark inline-styled card div."""
    inner = "".join(flex_items)
    return (
        "<div style='background:#161616;border:1px solid rgba(255,255,255,0.06);"
        "border-radius:16px;padding:1.5rem 1.6rem;margin-bottom:1.1rem;'>"
        + inner + "</div>"
    )

# ── Check if analysis has been run ────────────────────────────────────────────
analysis_complete = st.session_state.get("analysis_complete", False)
match_results     = st.session_state.get("match_results", {})
has_data = analysis_complete and bool(match_results)

# ── Pull values from session_state ────────────────────────────────────────────
role           = st.session_state.get("target_role", "Target Role")
score          = st.session_state.get("readiness_score", 0)
cats           = st.session_state.get("category_scores", {})
user_name      = st.session_state.get("user_name", "Candidate")
evaluated      = match_results.get("evaluated", {"mastered": [], "partial": [], "missing": []})
skill_scores   = match_results.get("skill_scores", {})
jd_skills      = match_results.get("jd_skills", [])

badge_label, badge_color = _badge(score)

# ═════════════════════════════════════════════════════════════════════════════
# HEADER ROW  (title + badge + export button)
# ═════════════════════════════════════════════════════════════════════════════
hdr_left, hdr_right = st.columns([3, 1], gap="small")

with hdr_left:
    st.markdown(
        "<div style='padding:1.8rem 0 0.3rem 0;'>"
        "<div style='display:inline-flex;align-items:center;gap:0.4rem;"
        "background:rgba(255,193,7,0.10);border:1px solid rgba(255,193,7,0.25);"
        "border-radius:20px;padding:0.22rem 0.75rem;font-size:0.8rem;font-weight:600;"
        "color:#FFC107;margin-bottom:0.5rem;'>🎯 &nbsp;Skill Gap Analysis</div>"
        "<div style='font-family:Outfit,sans-serif;font-size:2rem;font-weight:800;"
        "color:#FFFFFF;letter-spacing:-0.5px;margin:0 0 0.3rem 0;'>Skill Gap Report</div>"
        f"<div style='font-size:0.84rem;color:#888;line-height:1.6;'>"
        f"<strong style='color:#DDD;'>{role}</strong> &nbsp;·&nbsp; "
        "every requirement matched semantically against evidence in your resume."
        "</div></div>",
        unsafe_allow_html=True,
    )

with hdr_right:
    st.markdown("<div style='padding-top:2.4rem;'>", unsafe_allow_html=True)

    # Status badge
    if has_data:
        st.markdown(
            f"<div style='display:inline-block;background:{badge_color}22;"
            f"border:1px solid {badge_color}55;border-radius:20px;padding:0.3rem 0.9rem;"
            f"font-size:0.82rem;font-weight:700;color:{badge_color};"
            "margin-bottom:0.6rem;text-align:center;width:100%;'>"
            f"● &nbsp;{badge_label}</div>",
            unsafe_allow_html=True,
        )

    # Export PDF button
    if has_data:
        if st.button("⬇ Export PDF", key="export_pdf_btn", use_container_width=True):
            try:
                from utils.exporter import generate_skill_gap_pdf
                pdf_bytes = generate_skill_gap_pdf({
                    "role":             role,
                    "score":            score,
                    "badge":            badge_label,
                    "user_name":        user_name,
                    "category_scores":  cats,
                    "evaluated":        evaluated,
                    "skill_scores":     skill_scores,
                })
                st.download_button(
                    label="📄 Download report.pdf",
                    data=pdf_bytes,
                    file_name=f"UpCareer_SkillGap_{role.replace(' ', '_')}.pdf",
                    mime="application/pdf",
                    key="dl_pdf_btn",
                )
            except Exception as e:
                st.error(f"Export failed: {e}")

    st.markdown("</div>", unsafe_allow_html=True)

# Divider
st.markdown(
    "<hr style='border:none;border-top:1px solid rgba(255,255,255,0.06);"
    "margin:0.2rem 0 1.6rem 0;'>",
    unsafe_allow_html=True,
)

# ═════════════════════════════════════════════════════════════════════════════
# EMPTY STATE
# ═════════════════════════════════════════════════════════════════════════════
if not has_data:
    st.markdown(
        "<div style='background:#161616;border:1px solid rgba(255,255,255,0.06);"
        "border-radius:16px;padding:3.5rem 2rem;text-align:center;margin-top:1rem;'>"
        "<div style='font-size:3rem;margin-bottom:1rem;'>📋</div>"
        "<div style='font-family:Outfit,sans-serif;font-size:1.3rem;font-weight:700;"
        "color:#FFFFFF;margin-bottom:0.5rem;'>No analysis yet</div>"
        "<div style='font-size:0.85rem;color:#777;max-width:420px;margin:0 auto 1.4rem auto;"
        "line-height:1.6;'>Upload your resume and click <strong style='color:#FFC107;'>"
        "Analyze resume</strong> on the Resume Analysis page to generate your personalised "
        "skill gap report.</div>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.page_link("pages/1_Resume_Analysis.py", label="📄 Go to Resume Analysis", icon=None)
    st.stop()

# ═════════════════════════════════════════════════════════════════════════════
# GAUGE + SCORE BREAKDOWN  (two columns)
# ═════════════════════════════════════════════════════════════════════════════
col_gauge, col_breakdown = st.columns([1, 1.55], gap="large")

# ── LEFT: Readiness Gauge ────────────────────────────────────────────────────
with col_gauge:
    st.markdown(
        "<div style='background:#161616;border:1px solid rgba(255,255,255,0.06);"
        "border-radius:16px;padding:1.5rem 1.6rem 0.8rem 1.6rem;'>"
        "<div style='font-family:Outfit,sans-serif;font-size:0.78rem;font-weight:700;"
        "letter-spacing:0.08em;text-transform:uppercase;color:#A0A0A0;"
        "margin-bottom:0.2rem;'>Career Readiness Score</div>"
        f"<div style='font-family:Outfit,sans-serif;font-size:1.1rem;font-weight:700;"
        f"color:#FFFFFF;margin-bottom:0.6rem;'>{role}</div>",
        unsafe_allow_html=True,
    )

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={"font": {"size": 52, "color": "#FFFFFF", "family": "Outfit, sans-serif"}},
        gauge={
            "axis": {
                "range": [0, 100],
                "tickwidth": 0,
                "tickcolor": "rgba(0,0,0,0)",
                "showticklabels": False,
            },
            "bar": {"color": "#FFC107", "thickness": 0.72},
            "bgcolor": "rgba(0,0,0,0)",
            "borderwidth": 0,
            "steps": [{"range": [0, 100], "color": "#272727"}],
            "threshold": {
                "line": {"color": "#FFE082", "width": 3},
                "thickness": 0.85,
                "value": score,
            },
        },
        title={"text": "READINESS",
               "font": {"size": 13, "color": "#888888", "family": "Inter, sans-serif"}},
        domain={"x": [0, 1], "y": [0, 1]},
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        height=260,
        margin=dict(t=30, b=10, l=20, r=20),
        font=dict(color="#FFFFFF"),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    st.markdown(
        "<div style='font-size:0.73rem;color:#555;text-align:center;"
        "margin-top:-0.6rem;font-style:italic;padding-bottom:1rem;'>"
        "Estimate · weighted, explainable model</div>"
        "</div>",   # closes card div
        unsafe_allow_html=True,
    )

# ── RIGHT: Score Breakdown ────────────────────────────────────────────────────
with col_breakdown:
    cat_meta = {
        "Skills":           {"icon": "🛠️", "desc": "Overlap between your skills and the role's required stack."},
        "Experience":       {"icon": "💼", "desc": "Relevance and seniority of past roles and years worked."},
        "Projects":         {"icon": "🗂️", "desc": "Depth and domain relevance of portfolio projects."},
        "Education":        {"icon": "🎓", "desc": "Degree level and field alignment with the discipline."},
        "Certifications":   {"icon": "📜", "desc": "Industry-recognised certifications validating competencies."},
    }

    bars_html = ""
    for cat, cat_score in cats.items():
        meta = cat_meta.get(cat, {"icon": "•", "desc": ""})
        bar_block = (
            "<div style='margin-bottom:1.05rem;'>"
            "<div style='display:flex;justify-content:space-between;align-items:baseline;margin-bottom:0.3rem;'>"
            "<span style='font-size:0.84rem;font-weight:600;color:#FFFFFF;'>{icon}&nbsp; {cat}</span>"
            "<span style='font-size:0.84rem;font-weight:700;color:#FFC107;'>{score}</span>"
            "</div>"
            "<div style='background:rgba(255,255,255,0.07);border-radius:20px;height:6px;"
            "width:100%;overflow:hidden;margin-bottom:0.25rem;'>"
            "<div style='height:100%;border-radius:20px;"
            "background:linear-gradient(90deg,#FFC107 0%,#FFE082 100%);width:{pct}%;'></div>"
            "</div>"
            "<div style='font-size:0.71rem;color:#777;line-height:1.4;'>{desc}</div>"
            "</div>"
        ).format(icon=meta["icon"], cat=cat, score=cat_score, pct=cat_score, desc=meta["desc"])
        bars_html += bar_block

    if score >= 80:
        summary = (
            "With a readiness score of <strong>{s}/100</strong>, your profile is well-aligned with the "
            "<em>{r}</em> role. Minor certification gaps can be bridged quickly with targeted learning."
        ).format(s=score, r=role)
    elif score >= 55:
        summary = (
            "Your profile shows solid fundamentals for <em>{r}</em> (score <strong>{s}/100</strong>). "
            "A focused 2–3 month upskilling sprint on the partial-gap skills could meaningfully raise "
            "your interview conversion rate."
        ).format(s=score, r=role)
    else:
        summary = (
            "At <strong>{s}/100</strong>, your profile is at an early stage relative to <em>{r}</em> requirements. "
            "Prioritise the critical skill gaps and build 2–3 domain-specific portfolio projects."
        ).format(s=score, r=role)

    breakdown_html = (
        "<div style='background:#161616;border:1px solid rgba(255,255,255,0.06);"
        "border-radius:16px;padding:1.5rem 1.6rem 1.2rem 1.6rem;'>"
        "<div style='font-family:Outfit,sans-serif;font-size:1.15rem;font-weight:700;"
        "color:#FFFFFF;margin-bottom:1.1rem;'>Score breakdown</div>"
        + bars_html
        + "<div style='margin-top:1rem;padding-top:0.9rem;"
        "border-top:1px solid rgba(255,255,255,0.06);"
        "font-size:0.8rem;color:#999;line-height:1.6;'>"
        + summary + "</div></div>"
    )
    st.markdown(breakdown_html, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# SKILL STATUS SUMMARY CARDS
# ═════════════════════════════════════════════════════════════════════════════
n_mastered = len(evaluated["mastered"])
n_partial  = len(evaluated["partial"])
n_missing  = len(evaluated["missing"])

st.markdown(
    "<div style='font-family:Outfit,sans-serif;font-size:1.05rem;font-weight:700;"
    "color:#FFFFFF;margin:1.6rem 0 0.8rem 0;'>Skill status summary</div>",
    unsafe_allow_html=True,
)

stat_html = (
    "<div style='display:flex;gap:1rem;margin-bottom:1.4rem;'>"

    "<div style='flex:1;background:#161616;border:1px solid rgba(72,199,142,0.20);"
    "border-radius:14px;padding:1.2rem 1.4rem;display:flex;align-items:center;gap:1rem;'>"
    "<div style='width:12px;height:12px;border-radius:50%;background:#48C78E;"
    "box-shadow:0 0 8px #48C78E;flex-shrink:0;'></div>"
    "<div>"
    "<div style='font-size:0.75rem;font-weight:600;color:#888;text-transform:uppercase;"
    "letter-spacing:0.06em;margin-bottom:0.2rem;'>Present</div>"
    "<div style='font-family:Outfit,sans-serif;font-size:2rem;font-weight:800;"
    "color:#48C78E;line-height:1;'>{m}</div>"
    "<div style='font-size:0.71rem;color:#555;margin-top:0.15rem;'>"
    "Mastered · P(s) ≥ 0.80</div>"
    "</div></div>"

    "<div style='flex:1;background:#161616;border:1px solid rgba(255,193,7,0.20);"
    "border-radius:14px;padding:1.2rem 1.4rem;display:flex;align-items:center;gap:1rem;'>"
    "<div style='width:12px;height:12px;border-radius:50%;background:#FFC107;"
    "box-shadow:0 0 8px #FFC107;flex-shrink:0;'></div>"
    "<div>"
    "<div style='font-size:0.75rem;font-weight:600;color:#888;text-transform:uppercase;"
    "letter-spacing:0.06em;margin-bottom:0.2rem;'>Partial</div>"
    "<div style='font-family:Outfit,sans-serif;font-size:2rem;font-weight:800;"
    "color:#FFC107;line-height:1;'>{p}</div>"
    "<div style='font-size:0.71rem;color:#555;margin-top:0.15rem;'>"
    "Partial gap · 0.45 ≤ P(s) &lt; 0.80</div>"
    "</div></div>"

    "<div style='flex:1;background:#161616;border:1px solid rgba(255,82,82,0.20);"
    "border-radius:14px;padding:1.2rem 1.4rem;display:flex;align-items:center;gap:1rem;'>"
    "<div style='width:12px;height:12px;border-radius:50%;background:#FF5252;"
    "box-shadow:0 0 8px #FF5252;flex-shrink:0;'></div>"
    "<div>"
    "<div style='font-size:0.75rem;font-weight:600;color:#888;text-transform:uppercase;"
    "letter-spacing:0.06em;margin-bottom:0.2rem;'>Missing</div>"
    "<div style='font-family:Outfit,sans-serif;font-size:2rem;font-weight:800;"
    "color:#FF5252;line-height:1;'>{x}</div>"
    "<div style='font-size:0.71rem;color:#555;margin-top:0.15rem;'>"
    "Critical gap · P(s) &lt; 0.45</div>"
    "</div></div>"

    "</div>"
).format(m=n_mastered, p=n_partial, x=n_missing)

st.markdown(stat_html, unsafe_allow_html=True)

# ═════════════════════════════════════════════════════════════════════════════
# DETAILED SKILL TABLE
# ═════════════════════════════════════════════════════════════════════════════
st.markdown(
    "<div style='font-family:Outfit,sans-serif;font-size:1.05rem;font-weight:700;"
    "color:#FFFFFF;margin:0.4rem 0 0.8rem 0;'>Skill detail</div>",
    unsafe_allow_html=True,
)

# Flatten all skills into one list ordered: mastered → partial → missing
all_rows = (
    [(sk, p, "Mastered") for sk, p in evaluated["mastered"]] +
    [(sk, p, "Partial")  for sk, p in evaluated["partial"]]  +
    [(sk, p, "Missing")  for sk, p in evaluated["missing"]]
)

if all_rows:
    # Table header
    table_html = (
        "<div style='background:#161616;border:1px solid rgba(255,255,255,0.06);"
        "border-radius:16px;overflow:hidden;'>"

        # Header row
        "<div style='display:grid;grid-template-columns:2fr 1fr 1fr 2fr;"
        "padding:0.65rem 1.2rem;background:#1A1A1A;"
        "border-bottom:1px solid rgba(255,255,255,0.06);'>"
        "<span style='font-size:0.73rem;font-weight:700;color:#666;"
        "text-transform:uppercase;letter-spacing:0.06em;'>Skill</span>"
        "<span style='font-size:0.73rem;font-weight:700;color:#666;"
        "text-transform:uppercase;letter-spacing:0.06em;'>Status</span>"
        "<span style='font-size:0.73rem;font-weight:700;color:#666;"
        "text-transform:uppercase;letter-spacing:0.06em;'>P(s)</span>"
        "<span style='font-size:0.73rem;font-weight:700;color:#666;"
        "text-transform:uppercase;letter-spacing:0.06em;'>Note</span>"
        "</div>"
    )

    STATUS_META = {
        "Mastered": {"color": "#48C78E", "note": "Evidence found in resume"},
        "Partial":  {"color": "#FFC107", "note": "Partial evidence — needs strengthening"},
        "Missing":  {"color": "#FF5252", "note": "Not found in resume — critical gap"},
    }

    for i, (skill, p_score, status) in enumerate(all_rows):
        row_bg = "#181818" if i % 2 == 0 else "#161616"
        meta   = STATUS_META[status]

        table_html += (
            "<div style='display:grid;grid-template-columns:2fr 1fr 1fr 2fr;"
            "padding:0.6rem 1.2rem;background:{bg};"
            "border-bottom:1px solid rgba(255,255,255,0.04);align-items:center;'>"

            "<span style='font-size:0.84rem;font-weight:500;color:#E0E0E0;'>{skill}</span>"

            "<span style='display:flex;align-items:center;gap:0.4rem;'>"
            "<span style='width:8px;height:8px;border-radius:50%;background:{color};"
            "box-shadow:0 0 5px {color};flex-shrink:0;display:inline-block;'></span>"
            "<span style='font-size:0.82rem;font-weight:600;color:{color};'>{status}</span>"
            "</span>"

            "<span style='font-family:\"Courier New\",monospace;font-size:0.82rem;"
            "color:#AAA;'>{score:.2f}</span>"

            "<span style='font-size:0.78rem;color:#666;'>{note}</span>"
            "</div>"
        ).format(
            bg=row_bg, skill=skill, color=meta["color"],
            status=status, score=p_score, note=meta["note"],
        )

    table_html += "</div>"   # close card
    st.markdown(table_html, unsafe_allow_html=True)

else:
    st.markdown(
        "<div style='background:#161616;border:1px solid rgba(255,255,255,0.06);"
        "border-radius:14px;padding:2rem;text-align:center;color:#555;"
        "font-size:0.85rem;'>No skill matches found — the resume may not contain "
        "recognisable technical keywords.</div>",
        unsafe_allow_html=True,
    )

# ── Footer nav ────────────────────────────────────────────────────────────────
st.markdown("<div style='height:1.2rem;'></div>", unsafe_allow_html=True)
fc1, fc2, fc3 = st.columns(3)
with fc1:
    st.page_link("Home.py",                        label="📊 Dashboard",         icon=None)
with fc2:
    st.page_link("pages/1_Resume_Analysis.py",     label="📄 Re-run Analysis",   icon=None)
with fc3:
    st.page_link("pages/3_Career_Roadmap.py",      label="🗺️ Career Roadmap",   icon=None)

