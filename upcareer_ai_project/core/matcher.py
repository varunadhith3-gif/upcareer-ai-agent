from sentence_transformers import SentenceTransformer, util
from config import SENTENCE_MODEL, THRESHOLD_MASTERED, THRESHOLD_PARTIAL, W_SIM, W_EXP

model = SentenceTransformer(SENTENCE_MODEL)

def compute_similarity_matrix(candidate_skills, jd_skills):
    if not candidate_skills or not jd_skills:
        return {}
    
    # Embeddings
    cand_embeddings = model.encode(candidate_skills, convert_to_tensor=True)
    jd_embeddings = model.encode(jd_skills, convert_to_tensor=True)
    
    # Cosine similarities
    cosine_scores = util.cos_sim(jd_embeddings, cand_embeddings)
    
    # For each JD skill, find the best matching candidate skill
    match_results = {}
    for i, jd_skill in enumerate(jd_skills):
        best_score = float(cosine_scores[i].max())
        match_results[jd_skill] = best_score
        
    return match_results

def evaluate_skills(candidate_data, jd_skills):
    candidate_skills = candidate_data.get("skills", [])
    exp_months = candidate_data.get("experience_months", 0)
    
    match_results = compute_similarity_matrix(candidate_skills, jd_skills)
    
    evaluated = {
        "mastered": [],
        "partial": [],
        "missing": []
    }
    
    exp_factor = min(1.0, exp_months / 24.0)
    
    skill_scores = {}
    for jd_skill in jd_skills:
        sim_score = match_results.get(jd_skill, 0.0)
        # P(s) formula
        p_s = (W_SIM * sim_score) + (W_EXP * exp_factor)
        
        # In case sim_score was 0, they don't get free points for experience
        if sim_score < 0.2:
            p_s = sim_score
            
        skill_scores[jd_skill] = p_s
        
        if p_s >= THRESHOLD_MASTERED:
            evaluated["mastered"].append((jd_skill, p_s))
        elif p_s >= THRESHOLD_PARTIAL:
            evaluated["partial"].append((jd_skill, p_s))
        else:
            evaluated["missing"].append((jd_skill, p_s))
            
    return evaluated, skill_scores
