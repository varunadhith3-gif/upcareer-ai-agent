from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
import os
import io

def generate_roadmap_pdf(roadmap, output_path="roadmap.pdf"):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "UpCareer AI - Personalized Career Roadmap")
    
    c.setFont("Helvetica", 12)
    y_pos = height - 80
    
    c.drawString(50, y_pos, f"Status: {roadmap['status']} | Total Weeks: {roadmap['total_weeks_needed']}")
    y_pos -= 30
    
    for milestone in roadmap["milestones"]:
        if y_pos < 50:
            c.showPage()
            c.setFont("Helvetica", 12)
            y_pos = height - 50
            
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y_pos, f"Week {milestone['week']}")
        y_pos -= 20
        
        c.setFont("Helvetica", 11)
        skills_str = ", ".join(milestone['skills'])
        c.drawString(70, y_pos, f"Skills to Learn: {skills_str}")
        y_pos -= 15
        
        c.drawString(70, y_pos, f"Project: {milestone['project']}")
        y_pos -= 30
        
    c.save()
    return output_path


def generate_skill_gap_pdf(report_data: dict) -> bytes:
    """
    Generate an in-memory PDF skill gap report and return raw bytes.

    report_data keys:
        role          str   – target role name
        score         int   – overall readiness score 0-100
        badge         str   – 'Strong' | 'Good' | 'Fair' | 'Early Stage'
        category_scores dict – {category: score}
        evaluated     dict  – {mastered: [...], partial: [...], missing: [...]}
        skill_scores  dict  – {skill: float}
        user_name     str   – candidate name (optional)
    """
    buf = io.BytesIO()
    c = canvas.Canvas(buf, pagesize=letter)
    width, height = letter

    # ── Palette ───────────────────────────────────────────────────────────────
    COLOR_BG      = colors.HexColor("#0D0D0D")
    COLOR_CARD    = colors.HexColor("#161616")
    COLOR_YELLOW  = colors.HexColor("#FFC107")
    COLOR_GREEN   = colors.HexColor("#48C78E")
    COLOR_RED     = colors.HexColor("#FF5252")
    COLOR_GRAY    = colors.HexColor("#A0A0A0")
    COLOR_WHITE   = colors.white

    def new_page():
        c.showPage()
        # dark background
        c.setFillColor(COLOR_BG)
        c.rect(0, 0, width, height, fill=1, stroke=0)

    # Background
    c.setFillColor(COLOR_BG)
    c.rect(0, 0, width, height, fill=1, stroke=0)

    role       = report_data.get("role", "Unknown Role")
    score      = report_data.get("score", 0)
    badge      = report_data.get("badge", "")
    user_name  = report_data.get("user_name", "Candidate")
    evaluated  = report_data.get("evaluated", {"mastered": [], "partial": [], "missing": []})
    skill_scores = report_data.get("skill_scores", {})
    cat_scores = report_data.get("category_scores", {})

    # ── Header ────────────────────────────────────────────────────────────────
    c.setFillColor(COLOR_YELLOW)
    c.rect(0, height - 70, width, 70, fill=1, stroke=0)

    c.setFillColor(COLOR_BG)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(40, height - 42, "UpCareer AI")
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 58, "Skill Gap Report")

    c.setFillColor(COLOR_BG)
    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(width - 40, height - 42, role)
    c.setFont("Helvetica", 9)
    c.drawRightString(width - 40, height - 56, f"Readiness: {score}/100  ·  {badge}")

    y = height - 95

    # ── Candidate + score row ─────────────────────────────────────────────────
    c.setFillColor(COLOR_WHITE)
    c.setFont("Helvetica-Bold", 13)
    c.drawString(40, y, f"{user_name}'s Skill Gap Report")
    y -= 22

    c.setFillColor(COLOR_GRAY)
    c.setFont("Helvetica", 9)
    c.drawString(40, y, f"Target role: {role}   ·   Overall readiness score: {score}/100   ·   Status: {badge}")
    y -= 24

    # ── Category score bars ───────────────────────────────────────────────────
    c.setFillColor(COLOR_YELLOW)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y, "Score Breakdown")
    y -= 14

    BAR_WIDTH = 300
    BAR_H = 8
    for cat, cs in cat_scores.items():
        pct = cs / 100.0
        # track
        c.setFillColor(colors.HexColor("#272727"))
        c.rect(40, y, BAR_WIDTH, BAR_H, fill=1, stroke=0)
        # fill
        c.setFillColor(COLOR_YELLOW)
        c.rect(40, y, BAR_WIDTH * pct, BAR_H, fill=1, stroke=0)
        # label
        c.setFillColor(COLOR_WHITE)
        c.setFont("Helvetica", 8)
        c.drawString(40 + BAR_WIDTH + 8, y + 1, f"{cat}: {cs}")
        y -= 16
        if y < 60:
            new_page()
            y = height - 60

    y -= 10

    # ── Skill table ───────────────────────────────────────────────────────────
    c.setFillColor(COLOR_YELLOW)
    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, y, "Skill Status Detail")
    y -= 4

    # Table header
    c.setFillColor(colors.HexColor("#1E1E1E"))
    c.rect(40, y - 14, width - 80, 16, fill=1, stroke=0)
    c.setFillColor(COLOR_GRAY)
    c.setFont("Helvetica-Bold", 8)
    c.drawString(44, y - 10, "Skill")
    c.drawString(250, y - 10, "Status")
    c.drawString(360, y - 10, "Score")
    c.drawString(430, y - 10, "Note")
    y -= 18

    all_skills = (
        [(sk, p, "Mastered") for sk, p in evaluated.get("mastered", [])] +
        [(sk, p, "Partial")  for sk, p in evaluated.get("partial",  [])] +
        [(sk, p, "Missing")  for sk, p in evaluated.get("missing",  [])]
    )

    for i, (skill, p_score, status) in enumerate(all_skills):
        if y < 60:
            new_page()
            y = height - 60

        row_bg = colors.HexColor("#141414") if i % 2 == 0 else colors.HexColor("#181818")
        c.setFillColor(row_bg)
        c.rect(40, y - 11, width - 80, 14, fill=1, stroke=0)

        # Status color
        dot_color = COLOR_GREEN if status == "Mastered" else (COLOR_YELLOW if status == "Partial" else COLOR_RED)
        c.setFillColor(dot_color)
        c.circle(247, y - 4, 3, fill=1, stroke=0)

        c.setFillColor(COLOR_WHITE)
        c.setFont("Helvetica", 8)
        c.drawString(44,  y - 8, skill[:32])
        c.drawString(255, y - 8, status)
        c.drawString(360, y - 8, f"{p_score:.2f}")

        note = "Evidence found" if status == "Mastered" else ("Partial evidence" if status == "Partial" else "Not found in resume")
        c.setFillColor(COLOR_GRAY)
        c.drawString(430, y - 8, note)

        y -= 15

    # ── Footer ────────────────────────────────────────────────────────────────
    c.setFillColor(COLOR_GRAY)
    c.setFont("Helvetica", 7)
    c.drawString(40, 30, "Generated by UpCareer AI  ·  Score is an evidence-based estimate, not a hiring prediction.")
    c.drawRightString(width - 40, 30, f"upcareer.ai")

    c.save()
    buf.seek(0)
    return buf.read()
