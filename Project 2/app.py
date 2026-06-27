import streamlit as st
from utils.ai_model import get_embedder, get_model_info
from utils.styles import apply_custom_css, status_badge, section_header

st.set_page_config(page_title="Resume Screening AI", layout="wide")
apply_custom_css()

if "jd_text" not in st.session_state:
    st.session_state.jd_text = None
if "jd_filename" not in st.session_state:
    st.session_state.jd_filename = None
if "resumes" not in st.session_state:
    st.session_state.resumes = []
if "results" not in st.session_state:
    st.session_state.results = []
if "processed" not in st.session_state:
    st.session_state.processed = False

with st.spinner("Loading AI model (all-MiniLM-L6-v2)..."):
    get_embedder()
    model_info = get_model_info()
    st.session_state.model_info = model_info

st.markdown("<h1>Resume Screening & Ranking System</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">AI-powered candidate ranking using semantic embeddings and NLP</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
jd_status_val = "Ready" if st.session_state.jd_text else "Not Set"
resume_count = len(st.session_state.resumes)
results_status = "Ready" if st.session_state.processed else "Pending"

with col1:
    jd_dot = "green" if st.session_state.jd_text else "red"
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1a1a3e,#16213e);border:1px solid #2a2a5e;
                border-radius:12px;padding:1rem;text-align:center;box-shadow:0 4px 15px rgba(0,0,0,0.3);">
        <div style="color:#8888bb;font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;">Job Description</div>
        <div style="margin-top:0.5rem;">{status_badge(jd_status_val, jd_dot)}</div>
    </div>""", unsafe_allow_html=True)

with col2:
    r_dot = "green" if resume_count > 0 else "red"
    r_status = f"{resume_count} Uploaded" if resume_count > 0 else "None"
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1a1a3e,#16213e);border:1px solid #2a2a5e;
                border-radius:12px;padding:1rem;text-align:center;box-shadow:0 4px 15px rgba(0,0,0,0.3);">
        <div style="color:#8888bb;font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;">Resumes</div>
        <div style="margin-top:0.5rem;">{status_badge(r_status, r_dot)}</div>
    </div>""", unsafe_allow_html=True)

with col3:
    res_dot = "green" if st.session_state.processed else "yellow"
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1a1a3e,#16213e);border:1px solid #2a2a5e;
                border-radius:12px;padding:1rem;text-align:center;box-shadow:0 4px 15px rgba(0,0,0,0.3);">
        <div style="color:#8888bb;font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;">Results</div>
        <div style="margin-top:0.5rem;">{status_badge(results_status, res_dot)}</div>
    </div>""", unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1a1a3e,#16213e);border:1px solid #2a2a5e;
                border-radius:12px;padding:1rem;text-align:center;box-shadow:0 4px 15px rgba(0,0,0,0.3);">
        <div style="color:#8888bb;font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;">AI Model</div>
        <div style="color:#e0e0ff;font-size:1.1rem;font-weight:600;margin-top:0.4rem;">all-MiniLM-L6-v2</div>
    </div>""", unsafe_allow_html=True)

st.divider()

if not st.session_state.jd_text:
    st.markdown("""
    <div class="card">
        <div class="card-title">Getting Started</div>
        <div class="card-meta">Follow these steps to screen candidates:</div>
        <ol style="color:#a0a0cc;margin-top:0.5rem;line-height:1.8;">
            <li><strong style="color:#667eea;">1.</strong> Add a <strong>Job Description</strong> → navigate to the <em>Job Description</em> page</li>
            <li><strong style="color:#667eea;">2.</strong> <strong>Upload Resumes</strong> → go to the <em>Upload Resumes</em> page</li>
            <li><strong style="color:#667eea;">3.</strong> View <strong>Results</strong> → run the AI pipeline on the <em>Results</em> page</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
elif len(st.session_state.resumes) == 0:
    st.markdown("""
    <div class="card">
        <div class="card-title">Job Description Ready</div>
        <div class="card-meta">JD is set. Now upload resumes to begin screening.</div>
        <p style="color:#8888bb;margin-top:0.5rem;">Navigate to the <strong>Upload Resumes</strong> page to add candidate resumes.</p>
    </div>
    """, unsafe_allow_html=True)
elif not st.session_state.processed:
    st.markdown("""
    <div class="card">
        <div class="card-title">Ready to Analyze</div>
        <div class="card-meta">Resumes are uploaded. Run the AI pipeline to see results.</div>
        <p style="color:#8888bb;margin-top:0.5rem;">Go to the <strong>Results</strong> page and click <em>Run AI Pipeline</em>.</p>
    </div>
    """, unsafe_allow_html=True)
else:
    top = st.session_state.results[0] if st.session_state.results else None
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Pipeline Complete</div>
        <div class="card-meta">All candidates ranked. View detailed results on the Results page.</div>
        <p style="color:#00cc88;margin-top:0.5rem;">Top candidate: <strong>{top['name']}</strong> — {top['overall_score']}% overall</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.markdown('<p style="color:#3a3a6e;font-size:0.8rem;text-align:center;">Built with sentence-transformers, scikit-learn, Streamlit, and Plotly</p>', unsafe_allow_html=True)
