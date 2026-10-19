"""
mentor_tools.py  -  Intent detection & backend state bridge for AI Career Mentor.

This module does NOT touch the Amazon Bedrock / Nova Micro invocation path.
It provides two independent capabilities:
  1.  detect_career_change_intent()  - pure-text heuristic that returns the
      requested new role (if any) from the mentor's reply or the user's message.
  2.  apply_career_change()  - re-runs the same evaluation pipeline used by
      2_Skill_Gap_Report.py and pushes the results into st.session_state so that
      the Career Roadmap, Progress Tracker, and Dashboard all reflect the change
      instantly on the next page visit (no manual page reset required).
"""

from __future__ import annotations

import re
import json
import streamlit as st

# -- Canonical role list (must stay in sync with 1_Resume_Analysis.py) ----------
SUPPORTED_ROLES: list[str] = [
    "Software Engineer",
    "Data Scientist",
    "Full Stack Developer",
    "Machine Learning Engineer",
    "Data Engineer",
    "Cloud Architect",
    "DevOps Engineer",
    "Cybersecurity Analyst",
]

# Lowercase aliases -> canonical name (extend freely)
_ROLE_ALIASES: dict[str, str] = {
    "software engineer":         "Software Engineer",
    "swe":                       "Software Engineer",
    "backend engineer":          "Software Engineer",
    "backend developer":         "Software Engineer",
    "data scientist":            "Data Scientist",
    "ml scientist":              "Data Scientist",
    "full stack developer":      "Full Stack Developer",
    "full stack":                "Full Stack Developer",
    "fullstack developer":       "Full Stack Developer",
    "fullstack":                 "Full Stack Developer",
    "machine learning engineer": "Machine Learning Engineer",
    "ml engineer":               "Machine Learning Engineer",
    "mle":                       "Machine Learning Engineer",
    "ai engineer":               "Machine Learning Engineer",
    "data engineer":             "Data Engineer",
    "cloud architect":           "Cloud Architect",
    "solutions architect":       "Cloud Architect",
    "cloud engineer":            "Cloud Architect",
    "devops engineer":           "DevOps Engineer",
    "devops":                    "DevOps Engineer",
    "site reliability engineer": "DevOps Engineer",
    "sre":                       "DevOps Engineer",
    "cybersecurity analyst":     "Cybersecurity Analyst",
    "security analyst":          "Cybersecurity Analyst",
    "cybersecurity":             "Cybersecurity Analyst",
    "information security":      "Cybersecurity Analyst",
}

# Intent trigger phrases searched in user / assistant text
_CHANGE_TRIGGERS: list[str] = [
    r"switch(?:ing)?\s+(?:my\s+)?(?:career\s+)?(?:path|role|target|goal)\s+to",
    r"change(?:d)?\s+(?:my\s+)?(?:career\s+)?(?:path|role|target|goal)\s+to",
    r"update(?:d)?\s+(?:my\s+)?(?:career\s+)?(?:path|role|target|goal)\s+to",
    r"pivot(?:ing)?\s+to",
    r"transition(?:ing)?\s+to",
    r"become\s+(?:a\s+|an\s+)?",
    r"pursuing\s+(?:a\s+|an\s+)?",
    r"now\s+targ[e]ting",
    r"new\s+(?:career\s+)?(?:path|role|target|goal)\s+(?:is\s+)?",
    r"set\s+(?:my\s+)?(?:career\s+)?(?:path|role|target|goal)\s+to",
    r"want\s+to\s+be(?:come)?\s+(?:a\s+|an\s+)?",
    r"interested\s+in\s+(?:becoming\s+)?(?:a\s+|an\s+)?",
    r"roadmap\s+for\s+(?:a\s+|an\s+)?",
    r"update\s+(?:my\s+)?roadmap\s+(?:for|to)",
    r"regenerate\s+(?:my\s+)?roadmap\s+(?:for|to|as)",
    r"switching\s+to",
    r"move\s+to\s+(?:a\s+|an\s+)?",
    r"moving\s+to\s+(?:a\s+|an\s+)?",
]

_TRIGGER_RE = re.compile(
    "|".join(f"(?:{t})" for t in _CHANGE_TRIGGERS),
    re.IGNORECASE,
)


def _extract_role(text: str) -> str | None:
    """Return the canonical role name if any role alias is found in *text*."""
    text_lower = text.lower()
    # Longest alias first so "machine learning engineer" beats "machine learning"
    for alias in sorted(_ROLE_ALIASES, key=len, reverse=True):
        if alias in text_lower:
            return _ROLE_ALIASES[alias]
    return None


def detect_career_change_intent(user_message: str, assistant_reply: str) -> str | None:
    """
    Scan both the user message and the assistant reply for a career-change intent.

    Returns the canonical new role name if a change is detected, otherwise None.
    The current session role is excluded so we only return *different* targets.
    """
    combined = f"{user_message}\n{assistant_reply}"

    # Only look for role extraction if a trigger phrase is present
    if not _TRIGGER_RE.search(combined):
        return None

    role = _extract_role(combined)
    if not role:
        return None

    current_role = st.session_state.get("target_role", "")
    if role == current_role:
        return None  # No actual change

    return role


# -- Offline skill-gap fallback (mirrors 2_Skill_Gap_Report.py) -----------------

def _offline_match_results(resume_text: str, target_role: str) -> dict:
    """Generate rule-based match_results when the AI API is unavailable."""
    text_lower = resume_text.lower()
    common = ["python", "java", "c++", "sql", "html", "css",
              "javascript", "react", "git", "pandas", "numpy", "linux"]
    found = [[s.title(), 0.9] for s in common if s in text_lower]

    role_missing_map: dict[str, list] = {
        "Data Scientist":            [["PyTorch", 0.1], ["TensorFlow", 0.1], ["Statistics", 0.1],
                                      ["Scikit-Learn", 0.1], ["NLP", 0.1], ["Deep Learning", 0.1],
                                      ["MLOps", 0.1]],
        "Data Engineer":             [["Apache Spark", 0.1], ["Airflow", 0.1], ["Kafka", 0.1],
                                      ["Data Warehousing", 0.1], ["ETL Pipelines", 0.1],
                                      ["BigQuery", 0.1], ["Scala", 0.1]],
        "Cybersecurity Analyst":     [["Network Security", 0.1], ["Penetration Testing", 0.1],
                                      ["Wireshark", 0.1], ["SIEM Tools", 0.1],
                                      ["Cryptography", 0.1], ["Firewalls", 0.1], ["IAM", 0.1]],
        "Cloud Architect":           [["AWS/Azure", 0.1], ["Terraform", 0.1], ["Kubernetes", 0.1],
                                      ["IAM", 0.1], ["Networking", 0.1],
                                      ["Serverless", 0.1], ["Cost Optimization", 0.1]],
        "Machine Learning Engineer": [["PyTorch", 0.1], ["Transformers", 0.1],
                                      ["Computer Vision", 0.1], ["Model Deployment", 0.1],
                                      ["TensorFlow", 0.1], ["Fine-tuning", 0.1]],
        "DevOps Engineer":           [["Docker", 0.1], ["Kubernetes", 0.1], ["Terraform", 0.1],
                                      ["CI/CD Pipelines", 0.1], ["Ansible", 0.1],
                                      ["Monitoring", 0.1], ["Linux", 0.1]],
        "Full Stack Developer":      [["Node.js", 0.1], ["TypeScript", 0.1], ["React", 0.1],
                                      ["REST APIs", 0.1], ["Docker", 0.1],
                                      ["PostgreSQL", 0.1], ["GraphQL", 0.1]],
    }
    missing = role_missing_map.get(
        target_role,
        [["Docker", 0.1], ["Kubernetes", 0.1], ["System Design", 0.1],
         ["CI/CD Pipelines", 0.1], ["Microservices", 0.1], ["Redis", 0.1], ["GraphQL", 0.1]],
    )
    return {
        "evaluated": {
            "mastered": found[:2] if found else [["Python", 0.9]],
            "partial":  found[2:] if len(found) > 2 else [["SQL", 0.5]],
            "missing":  missing,
        }
    }


def _compute_scores(match_res: dict, target_role: str) -> dict:
    """Recompute readiness score and category scores from match_results."""
    evaluated = match_res.get("evaluated", {})
    m   = len(evaluated.get("mastered", []))
    p   = len(evaluated.get("partial",  []))
    mis = len(evaluated.get("missing",  []))

    role_hash = sum(ord(c) for c in target_role)
    raw   = 28 + (m * 5) + (p * 2) - (mis * 1.1) + (role_hash % 16) - 8
    score = max(22, min(65, int(round(raw))))

    cats = {
        "Skills":         max(25, min(65, score + (role_hash % 6))),
        "Experience":     max(15, min(45, score - 6)),
        "Projects":       max(30, min(68, score + 5)),
        "Education":      75,
        "Certifications": max(10, min(40, score - 10)),
    }
    return {
        "readiness_score": score,
        "category_scores": cats,
        "skills_present":  m,
        "skills_partial":  p,
        "skills_missing":  mis,
    }


def apply_career_change(new_role: str) -> bool:
    """
    Re-evaluate the stored resume text against *new_role* and push all
    derived state into st.session_state - exactly what Skill Gap Report does
    when the user changes the dropdown, but callable from any page.

    Returns True on success, False if there is no resume text to evaluate.
    """
    resume_text: str = st.session_state.get("resume_text", "")
    if not resume_text.strip():
        return False

    match_res: dict | None = None

    # -- Try Gemini first (same API used by 2_Skill_Gap_Report.py) --------------
    try:
        import google.generativeai as genai  # type: ignore
        api_key = st.secrets.get("GEMINI_API_KEY", "")
        if api_key:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel("gemini-3.6-flash")
            prompt = (
                f"You are an expert technical recruiter. Rigorously evaluate this resume "
                f"against industry requirements for a {new_role}.\n"
                f"Extract technical skills into three precise lists: mastered, partial, missing.\n"
                f"Return ONLY a valid JSON object (no markdown, no backticks):\n"
                '{"match_results": {"evaluated": {"mastered": [["Python", 0.9]],'
                '"partial": [["SQL", 0.5]],"missing": [["Docker", 0.1]]}}}\n'
                f"Resume text: {resume_text}"
            )
            response = model.generate_content(prompt)
            text_res = response.text.strip()
            for fence in ("```json", "```"):
                if fence in text_res:
                    text_res = text_res.split(fence)[1].split("```")[0].strip()
                    break
            data = json.loads(text_res)
            match_res = data.get(
                "match_results",
                {"evaluated": {"mastered": [], "partial": [], "missing": []}},
            )
    except Exception:
        pass  # Fall through to offline fallback

    if match_res is None:
        match_res = _offline_match_results(resume_text, new_role)

    # -- Push all derived state -------------------------------------------------
    scores = _compute_scores(match_res, new_role)

    st.session_state["target_role"]         = new_role
    st.session_state["last_evaluated_role"] = new_role
    st.session_state["match_results"]       = match_res
    st.session_state["readiness_score"]     = scores["readiness_score"]
    st.session_state["category_scores"]     = scores["category_scores"]
    st.session_state["skills_present"]      = scores["skills_present"]
    st.session_state["skills_partial"]      = scores["skills_partial"]
    st.session_state["skills_missing"]      = scores["skills_missing"]

    # Keep Skill Gap Report dropdown in sync (role_selector widget key)
    st.session_state["role_selector"]       = new_role

    # Reset roadmap progress so stale checkbox keys don't bleed into the new role
    st.session_state["roadmap_progress"]    = {}
    st.session_state["hitl_confirmed"]      = []

    # Signal Career Roadmap page to show a recalculation notice on next visit
    st.session_state["roadmap_stale"]       = True

    return True


def build_mentor_system_prompt() -> str:
    """Build a rich, context-aware system prompt for the Nova Micro mentor."""
    role      = st.session_state.get("target_role", "a tech role")
    score     = st.session_state.get("readiness_score", "N/A")
    match_res = st.session_state.get("match_results", {})
    evaluated = match_res.get("evaluated", {})

    def _names(key: str) -> str:
        items = evaluated.get(key, [])
        names = [s[0] if isinstance(s, (list, tuple)) else str(s) for s in items]
        return ", ".join(names) if names else "none identified"

    bandwidth = st.session_state.get("study_bandwidth", 10)
    user_name = st.session_state.get("user_name", "the user")
    supported = ", ".join(SUPPORTED_ROLES)

    return (
        f"You are an expert AI Career Mentor inside the UpCareer AI platform. "
        f"You are helping {user_name}.\n\n"
        f"CURRENT PROFILE:\n"
        f"- Target role: {role}\n"
        f"- Career readiness score: {score}/100\n"
        f"- Study bandwidth: {bandwidth} hours/week\n"
        f"- Mastered skills: {_names('mastered')}\n"
        f"- Partial skills: {_names('partial')}\n"
        f"- Missing skills: {_names('missing')}\n\n"
        f"SUPPORTED ROLES (for role switching): {supported}\n\n"
        f"INSTRUCTIONS:\n"
        f"1. Give concise, actionable career guidance tailored to the profile above.\n"
        f"2. If the user asks to switch, change, pivot, or update their career path or target role, "
        f"   confirm the new role clearly in your reply using phrasing like: "
        f"   'I've updated your target role to [Role Name]' or "
        f"   'Switching your career path to [Role Name]'.\n"
        f"3. Only switch to one of the supported roles listed above.\n"
        f"4. Keep answers focused and under 300 words unless more detail is requested.\n"
        f"5. Be encouraging but realistic about skill gaps."
    )
