import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .skills_extractor import extract_skills
from .ai_model import get_embedder

def preprocess(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def chunk_text(text: str, chunk_size: int = 3) -> list[str]:
    sentences = re.split(r"[.!?\n]+", text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    chunks = []
    for i in range(0, len(sentences), chunk_size):
        chunk = " ".join(sentences[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)
    return chunks if chunks else [text]


def compute_semantic_similarity(text1: str, text2: str) -> float:
    embedder = get_embedder()
    chunks1 = chunk_text(text1)
    chunks2 = chunk_text(text2)
    emb1 = embedder.encode(chunks1, convert_to_numpy=True)
    emb2 = embedder.encode(chunks2, convert_to_numpy=True)
    sim_matrix = cosine_similarity(emb1, emb2)
    row_max = sim_matrix.max(axis=1)
    col_max = sim_matrix.max(axis=0)
    score = float(np.concatenate([row_max, col_max]).mean())
    return score


def compute_text_similarity(resume_text: str, jd_text: str) -> dict:
    tfidf_corpus = [preprocess(resume_text), preprocess(jd_text)]
    tfidf_vec = TfidfVectorizer(stop_words="english")
    tfidf_mat = tfidf_vec.fit_transform(tfidf_corpus)
    tfidf_score = float(cosine_similarity(tfidf_mat[0:1], tfidf_mat[1:2])[0][0])
    semantic_score = compute_semantic_similarity(resume_text, jd_text)
    combined = 0.3 * tfidf_score + 0.7 * semantic_score
    return {
        "tfidf": round(tfidf_score * 100, 1),
        "semantic": round(semantic_score * 100, 1),
        "combined": round(combined * 100, 1),
    }


def compute_skill_match(resume_text: str, jd_text: str) -> dict:
    resume_skills = set(extract_skills(resume_text))
    jd_skills = set(extract_skills(jd_text))
    matched = resume_skills & jd_skills
    missing = jd_skills - resume_skills
    score = len(matched) / len(jd_skills) * 100 if jd_skills else 0
    return {
        "matched_skills": sorted(matched),
        "missing_skills": sorted(missing),
        "skill_score": round(score, 1),
    }


def rank_resumes(resumes: list[dict], jd_text: str) -> list[dict]:
    for r in resumes:
        sim = compute_text_similarity(r["text"], jd_text)
        skill = compute_skill_match(r["text"], jd_text)
        r["similarity_score"] = sim["combined"]
        r["semantic_score"] = sim["semantic"]
        r["tfidf_score"] = sim["tfidf"]
        r["skill_score"] = skill["skill_score"]
        r["matched_skills"] = skill["matched_skills"]
        r["missing_skills"] = skill["missing_skills"]
        r["overall_score"] = round(0.5 * r["similarity_score"] + 0.5 * r["skill_score"], 1)
    return sorted(resumes, key=lambda x: x["overall_score"], reverse=True)
