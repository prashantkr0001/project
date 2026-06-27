import streamlit as st
from utils.resume_parser import extract_text
from utils.styles import apply_custom_css, status_badge, section_header

apply_custom_css()

st.markdown("<h1>Job Description</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Paste or upload a job description to screen candidates against</p>', unsafe_allow_html=True)

jd_text = st.session_state.get("jd_text")
current_file = st.session_state.get("jd_filename")

if jd_text and current_file:
    word_count = len(jd_text.split())
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#002a1a,#003322);border:1px solid #00cc8866;
                border-radius:10px;padding:0.8rem 1rem;margin-bottom:1rem;
                display:flex;justify-content:space-between;align-items:center;">
        <div>
            <span style="color:#00cc88;">Current JD:</span>
            <span style="color:#e0e0ff;font-weight:600;">{current_file}</span>
            <span style="color:#8888bb;margin-left:1rem;">{word_count} words</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<h2 style="font-size:1.2rem;margin-top:0;">Paste Job Description</h2>', unsafe_allow_html=True)
input_text = st.text_area(
    "Paste the job description text here:",
    height=200,
    value=jd_text if jd_text and not current_file else "",
    label_visibility="collapsed",
)

st.markdown('<h2 style="font-size:1.2rem;margin-top:1rem;">Or Upload a File</h2>', unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "Upload JD file (.txt, .pdf, .docx)",
    type=["txt", "pdf", "docx"],
    key="jd_uploader",
    label_visibility="collapsed",
)

col1, col2 = st.columns([1, 3])
with col1:
    save_clicked = st.button("Save Job Description", type="primary", use_container_width=True)
with col2:
    if jd_text:
        if st.button("Clear", type="secondary", use_container_width=True):
            st.session_state.jd_text = None
            st.session_state.jd_filename = None
            st.session_state.processed = False
            st.rerun()

if save_clicked:
    if uploaded_file:
        text = extract_text(uploaded_file)
        if text.strip():
            st.session_state.jd_text = text
            st.session_state.jd_filename = uploaded_file.name
            st.session_state.processed = False
            st.rerun()
        else:
            st.error("Could not extract text from the uploaded file.")
    elif input_text.strip():
        st.session_state.jd_text = input_text.strip()
        st.session_state.jd_filename = "pasted_text.txt"
        st.session_state.processed = False
        st.rerun()
    else:
        st.warning("Please paste some text or upload a file.")

if jd_text:
    with st.expander("Preview Job Description"):
        preview = jd_text[:2000]
        st.markdown(f'<div style="color:#a0a0cc;white-space:pre-wrap;font-size:0.9rem;">{preview}{"..." if len(jd_text) > 2000 else ""}</div>', unsafe_allow_html=True)

st.divider()
st.markdown(f"""
<div style="display:flex;gap:1rem;justify-content:center;">
    <span>{status_badge('JD: ' + ('Ready' if jd_text else 'Not Set'), 'green' if jd_text else 'red')}</span>
    <span>{status_badge('Resumes: ' + str(len(st.session_state.resumes)), 'green' if st.session_state.resumes else 'yellow')}</span>
</div>
""", unsafe_allow_html=True)
