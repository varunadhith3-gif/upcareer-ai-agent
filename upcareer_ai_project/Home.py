import streamlit as st
import plotly.graph_objects as go
from utils.sidebar import render_sidebar

st.set_page_config(
    page_title="UpCareer AI - Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Render sidebar (injects global CSS too) ──────────────────────────────────
render_sidebar()

# ── Additional dashboard-specific CSS ────────────────────────────────────────
st.markdown("""
<style>
/* ── Dashboard header ─────────────────────────── */
.dash-header {
    padding: 2rem 0 1.4rem 0;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 1.8rem;
}
.dash-welcome {
    font-family: 'Outfit', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.5px;
    margin: 0 0 0.25rem 0;
}
.dash-welcome span { color: #FFC107; }
.dash-role-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    background: rgba(255,193,7,0.10);
    border: 1px solid rgba(255,193,7,0.25);
    border-radius: 20px;
    padding: 0.22rem 0.75rem;
    font-size: 0.8rem;
    font-weight: 600;
    color: #FFC107;
    margin-bottom: 0.6rem;
}
.dash-disclaimer {
    font-size: 0.74rem;
    color: #666;
    font-style: italic;
    margin-top: 0.4rem;
}

/* ── Gauge & breakdown cards ──────────────────── */
.dash-card {
    background-color: #161616;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 1.6rem 1.6rem 1.2rem 1.6rem;
    margin-bottom: 1.2rem;
    transition: border-color 0.3s ease, box-shadow 0.3s ease, transform 0.25s ease;
    height: 100%;
}
.dash-card:hover {
    border-color: rgba(255,193,7,0.30);
    box-shadow: 0 6px 30px rgba(255,193,7,0.07);
    transform: translateY(-2px);
}
.dash-card-title {
    font-family: 'Outfit', sans-serif;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #A0A0A0;
    margin-bottom: 0.2rem;
}
.dash-card-role {
    font-family: 'Outfit', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 0.8rem;
}
.gauge-caption {
    font-size: 0.73rem;
    color: #666;
    text-align: center;
    margin-top: -0.6rem;
    font-style: italic;
}

/* ── Score breakdown bars ─────────────────────── */
.breakdown-title {
    font-family: 'Outfit', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: #FFFFFF;
    margin-bottom: 1.1rem;
}
.bar-row {
    margin-bottom: 1.05rem;
}
.bar-label-row {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.3rem;
}
.bar-cat-name {
    font-size: 0.84rem;
    font-weight: 600;
    color: #FFFFFF;
}
.bar-score {
    font-size: 0.84rem;
    font-weight: 700;
    color: #FFC107;
    min-width: 2.2rem;
    text-align: right;
}
.bar-track {
    background: rgba(255,255,255,0.07);
    border-radius: 20px;
    height: 6px;
    width: 100%;
    overflow: hidden;
    margin-bottom: 0.25rem;
}
.bar-fill {
    height: 100%;
    border-radius: 20px;
    background: linear-gradient(90deg, #FFC107 0%, #FFE082 100%);
    transition: width 0.8s ease;
}
.bar-desc {
    font-size: 0.71rem;
    color: #777;
    line-height: 1.4;
}
.breakdown-summary {
    margin-top: 1.1rem;
    padding-top: 0.9rem;
    border-top: 1px solid rgba(255,255,255,0.06);
    font-size: 0.8rem;
    color: #999;
    line-height: 1.6;
}

/* ── Stat cards (Present / Partial / Missing) ── */
.stat-cards-row {
    display: flex;
    gap: 1rem;
    margin-top: 0.6rem;
    margin-bottom: 1rem;
}
.stat-card {
    flex: 1;
    background: #161616;
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 14px;
    padding: 1.2rem 1.4rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: border-color 0.3s ease, box-shadow 0.3s ease, transform 0.25s ease;
}
.stat-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 22px rgba(0,0,0,0.3);
}
.stat-card.present { border-color: rgba(72,199,142,0.18); }
.stat-card.present:hover { border-color: rgba(72,199,142,0.4); }
.stat-card.partial  { border-color: rgba(255,193,7,0.18); }
.stat-card.partial:hover  { border-color: rgba(255,193,7,0.4); }
.stat-card.missing  { border-color: rgba(255,82,82,0.18); }
.stat-card.missing:hover  { border-color: rgba(255,82,82,0.4); }

.stat-dot {
    width: 12px; height: 12px;
    border-radius: 50%;
    flex-shrink: 0;
    box-shadow: 0 0 8px currentColor;
}
.stat-dot.green  { background:#48C78E; color:#48C78E; }
.stat-dot.yellow { background:#FFC107; color:#FFC107; }
.stat-dot.red    { background:#FF5252; color:#FF5252; }

.stat-info { flex: 1; }
.stat-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #888;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 0.2rem;
}
.stat-count {
    font-family: 'Outfit', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    line-height: 1;
}
.stat-count.green  { color: #48C78E; }
.stat-count.yellow { color: #FFC107; }
.stat-count.red    { color: #FF5252; }
.stat-sublabel {
    font-size: 0.71rem;
    color: #666;
    margin-top: 0.15rem;
}
</style>
""", unsafe_allow_html=True)

# ── Session-state defaults (placeholders until resume is analyzed) ───────────
_defaults = {
    "user_name":           "Alex",
    "target_role":         "Data Scientist",
    "readiness_score":     67,
    "category_scores": {
        "Skills":           74,
        "Experience":       60,
        "Projects":         72,
        "Education":        80,
        "Certifications":   50,
    },
    "skills_present":      12,
    "skills_partial":       8,
    "skills_missing":       5,
}
for k, v in _defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Convenience aliases
name        = st.session_state.user_name
role        = st.session_state.target_role
score       = st.session_state.readiness_score
cats        = st.session_state.category_scores
n_present   = st.session_state.skills_present
n_partial   = st.session_state.skills_partial
n_missing   = st.session_state.skills_missing

# ── Dashboard header ─────────────────────────────────────────────────────────
st.markdown(f"""
<div class="dash-header">
    <div class="dash-role-pill">🎯 &nbsp;Target role: {role}</div>
    <div class="dash-welcome">Welcome back, <span>{name}</span> 👋</div>
    <div class="dash-disclaimer">
        ℹ️ Your readiness score is an evidence-based estimate, not a prediction of hiring outcomes.
    </div>
</div>
""", unsafe_allow_html=True)

# ── Two-column layout ────────────────────────────────────────────────────────
col_left, col_right = st.columns([1, 1.55], gap="large")

# ── LEFT COLUMN — Readiness Gauge ───────────────────────────────────────────
with col_left:
    st.markdown(f"""
    <div class="dash-card">
        <div class="dash-card-title">Career Readiness Score</div>
        <div class="dash-card-role">{role}</div>
    """, unsafe_allow_html=True)

    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        number={
            "font": {"size": 52, "color": "#FFFFFF", "family": "Outfit, sans-serif"},
            "suffix": "",
        },
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
            "steps": [
                {"range": [0, 100], "color": "#272727"},
            ],
            "threshold": {
                "line": {"color": "#FFE082", "width": 3},
                "thickness": 0.85,
                "value": score,
            },
        },
        title={
            "text": "READINESS",
            "font": {"size": 13, "color": "#888888", "family": "Inter, sans-serif"},
        },
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

    st.markdown('<div class="gauge-caption">Estimate · weighted, explainable model</div>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)  # close .dash-card

# ── RIGHT COLUMN — Score Breakdown ──────────────────────────────────────────
with col_right:
    cat_meta = {
        "Skills": {
            "desc": "Overlap between your stated skills and the role's required technical stack.",
            "icon": "🛠️",
        },
        "Experience": {
            "desc": "Relevance and seniority of past roles, industries, and years of professional work.",
            "icon": "💼",
        },
        "Projects": {
            "desc": "Depth, recency, and domain relevance of portfolio projects and open-source contributions.",
            "icon": "🗂️",
        },
        "Education": {
            "desc": "Degree level and field alignment with the target discipline.",
            "icon": "🎓",
        },
        "Certifications": {
            "desc": "Industry-recognised certifications that validate specific technical competencies.",
            "icon": "📜",
        },
    }

    bars_html = ""
    for cat, cat_score in cats.items():
        pct = cat_score
        meta = cat_meta.get(cat, {"desc": "", "icon": "•"})
        bar_block = (
            "<div style='margin-bottom:1.05rem;'>"
            "<div style='display:flex;justify-content:space-between;align-items:baseline;margin-bottom:0.3rem;'>"
            "<span style='font-size:0.84rem;font-weight:600;color:#FFFFFF;'>{icon}&nbsp; {cat}</span>"
            "<span style='font-size:0.84rem;font-weight:700;color:#FFC107;min-width:2.2rem;text-align:right;'>{score}</span>"
            "</div>"
            "<div style='background:rgba(255,255,255,0.07);border-radius:20px;height:6px;width:100%;overflow:hidden;margin-bottom:0.25rem;'>"
            "<div style='height:100%;border-radius:20px;background:linear-gradient(90deg,#FFC107 0%,#FFE082 100%);width:{pct}%;'></div>"
            "</div>"
            "<div style='font-size:0.71rem;color:#777;line-height:1.4;'>{desc}</div>"
            "</div>"
        ).format(icon=meta["icon"], cat=cat, score=cat_score, pct=pct, desc=meta["desc"])
        bars_html += bar_block

    # Dynamic standing description based on score tier
    if score >= 80:
        standing_note = (
            "With a readiness score of <strong>{s}/100</strong>, {n}'s profile is well-aligned "
            "with the <em>{r}</em> role. Minor gaps in certifications can be bridged quickly with "
            "targeted learning, leaving the profile competitive for most job descriptions."
        ).format(s=score, n=name, r=role)
    elif score >= 55:
        standing_note = (
            "{n}'s profile shows solid fundamentals for a <em>{r}</em> position "
            "(score <strong>{s}/100</strong>), with clear growth areas in experience depth and certifications. "
            "A focused 2\u20133 month upskilling sprint targeting the partial-gap skills could meaningfully "
            "raise this score and improve interview conversion rates."
        ).format(s=score, n=name, r=role)
    else:
        standing_note = (
            "At <strong>{s}/100</strong>, {n}'s profile is at an early stage relative to the "
            "<em>{r}</em> requirements. Prioritise closing the critical skill gaps and building "
            "2\u20133 portfolio projects in the target domain to accelerate readiness."
        ).format(s=score, n=name, r=role)

    breakdown_html = (
        "<div style='background-color:#161616;border:1px solid rgba(255,255,255,0.06);"
        "border-radius:16px;padding:1.6rem 1.6rem 1.2rem 1.6rem;margin-bottom:1.2rem;'>"
        "<div style='font-family:Outfit,sans-serif;font-size:1.15rem;font-weight:700;"
        "color:#FFFFFF;margin-bottom:1.1rem;'>Score breakdown</div>"
        + bars_html
        + "<div style='margin-top:1.1rem;padding-top:0.9rem;"
        "border-top:1px solid rgba(255,255,255,0.06);"
        "font-size:0.8rem;color:#999;line-height:1.6;'>"
        + standing_note
        + "</div></div>"
    )
    st.markdown(breakdown_html, unsafe_allow_html=True)

# ── Stat cards row ───────────────────────────────────────────────────────────
st.markdown(f"""
<div class="stat-cards-row">
    <div class="stat-card present">
        <div class="stat-dot green"></div>
        <div class="stat-info">
            <div class="stat-label">Present</div>
            <div class="stat-count green">{n_present}</div>
            <div class="stat-sublabel">Mastered skills matched</div>
        </div>
    </div>
    <div class="stat-card partial">
        <div class="stat-dot yellow"></div>
        <div class="stat-info">
            <div class="stat-label">Partial</div>
            <div class="stat-count yellow">{n_partial}</div>
            <div class="stat-sublabel">Partial-gap skills to strengthen</div>
        </div>
    </div>
    <div class="stat-card missing">
        <div class="stat-dot red"></div>
        <div class="stat-info">
            <div class="stat-label">Missing</div>
            <div class="stat-count red">{n_missing}</div>
            <div class="stat-sublabel">Critical skills not yet demonstrated</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
