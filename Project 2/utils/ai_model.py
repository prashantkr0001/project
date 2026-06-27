import streamlit as st

@st.cache_resource
def get_embedder():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")


@st.cache_resource
def get_model_info() -> dict:
    return {
        "model": "all-MiniLM-L6-v2",
        "type": "Sentence Transformer",
        "dimensions": 384,
        "source": "HuggingFace / sentence-transformers",
        "description": "Semantic embedding model for text similarity. Maps resumes and job descriptions to 384-dim vectors capturing semantic meaning.",
    }
