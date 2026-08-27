import math
from config import ALPHA

def calculate_readiness_score(skill_scores, jd_skills):
    if not jd_skills:
        return 100.0
    
    # Readiness Score = 100 * (1 - exp(-sum(alpha * P(s) / R_req(s))))
    # Assuming R_req(s) is 1.0 (max proficiency required for all listed skills)
    
    sum_val = 0.0
    for jd_skill in jd_skills:
        p_s = skill_scores.get(jd_skill, 0.0)
        sum_val += ALPHA * (p_s / 1.0)
        
    score = 100 * (1 - math.exp(-sum_val / len(jd_skills)))
    return round(score, 1)

def calculate_projected_score(skill_scores, jd_skills, roadmap_skills):
    # Simulate completion of roadmap
    projected_scores = skill_scores.copy()
    for skill in roadmap_skills:
        # After completing the roadmap, assume P(s) becomes 0.9 (mastered)
        projected_scores[skill] = max(projected_scores.get(skill, 0.0), 0.9)
        
    return calculate_readiness_score(projected_scores, jd_skills)
