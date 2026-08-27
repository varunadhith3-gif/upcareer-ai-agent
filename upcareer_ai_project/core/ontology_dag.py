import networkx as nx

def build_skill_dag():
    G = nx.DiGraph()
    
    edges = [
        # CS Fundamentals
        ("Data Structures", "Algorithms"),
        ("Algorithms", "System Design"),
        ("Python", "Data Structures"),
        ("Java", "Data Structures"),
        ("C++", "Data Structures"),
        
        # AI/ML
        ("Linear Algebra", "Machine Learning"),
        ("Statistics", "Machine Learning"),
        ("Python", "Machine Learning"),
        ("Machine Learning", "Deep Learning"),
        ("Deep Learning", "Transformers & Llms"),
        ("Deep Learning", "Computer Vision"),
        ("Deep Learning", "Natural Language Processing"),
        
        # Data Eng & MLOps
        ("Sql", "Data Analysis"),
        ("Data Analysis", "Machine Learning"),
        ("Docker", "Kubernetes"),
        ("Kubernetes", "Mlops"),
        ("Machine Learning", "Mlops"),
        
        # Web Dev
        ("Python", "Django"),
        ("Python", "Flask"),
        ("Python", "Fastapi"),
        ("Javascript", "React"),
        ("Javascript", "Node.Js"),
        ("Rest Apis", "System Design"),
        ("Django", "Rest Apis"),
        ("Fastapi", "Rest Apis")
    ]
    
    G.add_edges_from(edges)
    return G

def resolve_prerequisites(missing_skills, acquired_skills):
    G = build_skill_dag()
    
    # Capitalize for matching
    missing_skills = [s.title() for s in missing_skills]
    acquired_skills = [s.title() for s in acquired_skills]
    
    # Find all ancestors for missing skills
    needed_skills = set(missing_skills)
    for skill in missing_skills:
        if skill in G:
            ancestors = nx.ancestors(G, skill)
            needed_skills.update(ancestors)
            
    # Remove acquired skills
    needed_skills = needed_skills - set(acquired_skills)
    
    # We want to topologically sort the subgraph of needed_skills
    subgraph = G.subgraph(needed_skills)
    
    try:
        ordered_skills = list(nx.topological_sort(subgraph))
    except nx.NetworkXUnfeasible:
        # Fallback if cycle exists (should not happen in our hardcoded DAG)
        ordered_skills = list(needed_skills)
        
    # If there are skills not in the DAG, append them at the end
    non_dag_skills = needed_skills - set(subgraph.nodes())
    ordered_skills.extend(list(non_dag_skills))
    
    return ordered_skills
