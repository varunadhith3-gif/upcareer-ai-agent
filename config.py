# config.py

# Competency levels based on P(s)
THRESHOLD_MASTERED = 0.80
THRESHOLD_PARTIAL = 0.45

# Weights for P(s) formula
# P(s) = W_SIM * Sim(s, JD) + W_EXP * min(1.0, ExpMonths/24)
W_SIM = 0.7
W_EXP = 0.3

# Default timeline and bandwidth limits
DEFAULT_WEEKS = 12
DEFAULT_HOURS_PER_WEEK = 10

# Readiness Score alpha scaling
ALPHA = 1.0

# Paths
SPACY_MODEL = "en_core_web_sm"
SENTENCE_MODEL = "all-MiniLM-L6-v2"
