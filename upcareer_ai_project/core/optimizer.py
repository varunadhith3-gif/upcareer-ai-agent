import math

def generate_roadmap(ordered_skills, weekly_hours, target_weeks):
    roadmap = []
    
    # Simple heuristic: allocate 15 hours per skill on average
    HOURS_PER_SKILL = 15.0
    
    total_available_hours = weekly_hours * target_weeks
    total_needed_hours = len(ordered_skills) * HOURS_PER_SKILL
    
    # Schedule skills into weeks
    current_week = 1
    current_week_hours = 0.0
    
    milestones = []
    current_milestone_skills = []
    
    for skill in ordered_skills:
        if current_week_hours + HOURS_PER_SKILL > weekly_hours:
            # Move to next week
            if current_milestone_skills:
                milestones.append({
                    "week": current_week,
                    "skills": current_milestone_skills,
                    "project": f"Mini-project combining {', '.join(current_milestone_skills)}"
                })
            current_week += 1
            current_week_hours = 0.0
            current_milestone_skills = []
            
        current_milestone_skills.append(skill)
        current_week_hours += HOURS_PER_SKILL
        
    if current_milestone_skills:
        milestones.append({
            "week": current_week,
            "skills": current_milestone_skills,
            "project": f"Mini-project combining {', '.join(current_milestone_skills)}"
        })
        
    status = "Feasible" if current_week <= target_weeks else "Over-scheduled"
    
    return {
        "milestones": milestones,
        "status": status,
        "total_weeks_needed": current_week
    }
