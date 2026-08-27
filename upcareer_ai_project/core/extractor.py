import spacy
import re
from config import SPACY_MODEL

try:
    nlp = spacy.load(SPACY_MODEL)
except OSError:
    import subprocess
    subprocess.run(["python", "-m", "spacy", "download", SPACY_MODEL])
    nlp = spacy.load(SPACY_MODEL)

# Expanded keyword dictionary for fallback extraction
TECH_KEYWORDS = {
    "python", "java", "c++", "c#", "javascript", "typescript", "golang", "ruby", "php",
    "django", "flask", "fastapi", "spring", "react", "angular", "vue", "node.js",
    "docker", "kubernetes", "aws", "gcp", "azure", "ci/cd", "jenkins", "github actions",
    "sql", "nosql", "mysql", "postgresql", "mongodb", "redis",
    "machine learning", "deep learning", "natural language processing", "computer vision",
    "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy", "transformers", "llms",
    "data structures", "algorithms", "system design", "mlops", "data analysis", "statistics",
    "linear algebra", "rest apis", "graphql", "git"
}

def extract_entities(text):
    doc = nlp(text)
    
    extracted = {
        "skills": set(),
        "experience": [],
        "education": [],
        "certifications": []
    }
    
    lower_text = text.lower()
    
    # Simple rule-based extraction for keywords
    for kw in TECH_KEYWORDS:
        # Use regex to match whole words/phrases
        pattern = r'\b' + re.escape(kw) + r'\b'
        if re.search(pattern, lower_text):
            extracted["skills"].add(kw.title())
            
    # Extract ORG and DATE entities
    for ent in doc.ents:
        if ent.label_ == "ORG":
            # Could be education or experience depending on context, simple heuristic
            if any(word in ent.text.lower() for word in ["university", "college", "institute"]):
                extracted["education"].append(ent.text)
            elif ent.text not in extracted["experience"]:
                extracted["experience"].append(ent.text)

    # ── FIX: Isolate the "Experience" section ─────────────────────────────────
    exp_text = ""
    # Look for common work headers
    exp_match = re.search(r'\b(experience|employment|work history)\b', lower_text)
    
    if exp_match:
        # Find the next section header to know where experience stops
        next_header = re.search(r'\b(education|projects|skills|certifications|languages|summary|objective)\b', 
                                lower_text[exp_match.end():])
        if next_header:
            exp_text = lower_text[exp_match.end():exp_match.end() + next_header.start()]
        else:
            exp_text = lower_text[exp_match.end():]
    
    # Basic duration extraction heuristic applied ONLY to the experience block
    duration_matches = re.findall(r'(\d+)\s*(year|yr|month|mo)s?', exp_text)
    total_months = 0
    for val, unit in duration_matches:
        if 'year' in unit or 'yr' in unit:
            total_months += int(val) * 12
        else:
            total_months += int(val)
    
    extracted["experience_months"] = total_months
    extracted["skills"] = list(extracted["skills"])
    return extracted

def extract_jd_skills(text):
    # For JD, primarily care about extracting required skills
    doc = nlp(text)
    skills = set()
    lower_text = text.lower()
    for kw in TECH_KEYWORDS:
        pattern = r'\b' + re.escape(kw) + r'\b'
        if re.search(pattern, lower_text):
            skills.add(kw.title())
    return list(skills)