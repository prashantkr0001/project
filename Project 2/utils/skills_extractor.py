import re
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from .ai_model import get_embedder

SKILLS_DB = {
    "python", "java", "javascript", "typescript", "c++", "c#", "ruby", "go",
    "rust", "swift", "kotlin", "scala", "php", "html", "css", "sql",
    "react", "angular", "vue", "django", "flask", "fastapi", "spring",
    "node.js", "express", "next.js", "tailwind", "bootstrap",
    "aws", "azure", "gcp", "docker", "kubernetes", "terraform",
    "jenkins", "git", "github", "gitlab", "ci/cd", "linux",
    "machine learning", "deep learning", "nlp", "computer vision",
    "tensorflow", "pytorch", "scikit-learn", "pandas", "numpy",
    "data analysis", "data science", "data engineering",
    "tableau", "power bi", "excel", "spark", "hadoop",
    "mongodb", "postgresql", "mysql", "redis", "elasticsearch",
    "rest api", "graphql", "microservices", "agile", "scrum",
    "communication", "leadership", "project management",
    "product management", "ui/ux", "figma", "photoshop",
}


def extract_skills(text: str) -> list[str]:
    text_lower = text.lower()
    found = set()
    for skill in SKILLS_DB:
        if skill in text_lower:
            found.add(skill)
    return sorted(found)


def extract_skills_ai(text: str, jd_text: str | None = None, threshold: float = 0.65) -> list[str]:
    text_lower = text.lower()
    found = set()
    for skill in SKILLS_DB:
        if skill in text_lower:
            found.add(skill)
    if jd_text and len(found) < 5:
        embedder = get_embedder()
        jd_lower = jd_text.lower()
        jd_skills = [s for s in SKILLS_DB if s in jd_lower]
        if jd_skills:
            candidates = [s for s in SKILLS_DB if s not in found]
            if candidates:
                emb_candidates = embedder.encode(candidates, convert_to_numpy=True)
                emb_jd = embedder.encode(jd_skills, convert_to_numpy=True)
                sim = cosine_similarity(emb_candidates, emb_jd).max(axis=1)
                for i, s in enumerate(candidates):
                    if sim[i] >= threshold and s in text_lower:
                        found.add(s)
    return sorted(found)


def extract_education(text: str) -> list[str]:
    keywords = ["bachelor", "master", "phd", "b.tech", "m.tech", "b.e", "m.e",
                "mba", "bca", "mca", "degree", "university", "college",
                "b.sc", "m.sc", "b.a", "m.a", "b.com", "m.com"]
    lines = text.lower().split("\n")
    found = []
    for line in lines:
        if any(kw in line for kw in keywords):
            found.append(line.strip())
    return found[:5]


def extract_experience(text: str) -> float:
    patterns = [
        r"(\d+)\+?\s*years?\s*(?:of)?\s*experience",
        r"experience\s*(?:of)?\s*(\d+)\+?\s*years?",
        r"worked\s*(?:for|over)?\s*(\d+)\+?\s*years?",
    ]
    for pattern in patterns:
        match = re.search(pattern, text.lower())
        if match:
            return float(match.group(1))
    return 0.0
