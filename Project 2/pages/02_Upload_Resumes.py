import streamlit as st
from utils.resume_parser import extract_text, extract_email, extract_phone, extract_name
from utils.skills_extractor import extract_skills, extract_education, extract_experience
from utils.styles import apply_custom_css, status_badge, section_header

apply_custom_css()

st.markdown("<h1>Upload Resumes</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Upload resume files (PDF, DOCX, TXT) to screen against the job description</p>', unsafe_allow_html=True)

if not st.session_state.jd_text:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Job Description Required</div>
        <div class="card-meta">Please set a job description first before uploading resumes.</div>
        <p style="color:#8888bb;margin-top:0.5rem;">Navigate to the <strong>Job Description</strong> page to add one.</p>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

resumes = st.session_state.resumes
uploaded_files = st.file_uploader(
    "Choose resume files",
    type=["pdf", "docx", "txt"],
    accept_multiple_files=True,
    key="resume_uploader",
    label_visibility="collapsed",
)

if uploaded_files:
    existing_names = {r["filename"] for r in resumes}
    new_files = [f for f in uploaded_files if f.name not in existing_names]

    if new_files:
        with st.spinner(f"Processing {len(new_files)} new resume(s)..."):
            for f in new_files:
                text = extract_text(f)
                resumes.append({
                    "filename": f.name,
                    "text": text,
                    "name": extract_name(text),
                    "email": extract_email(text),
                    "phone": extract_phone(text),
                    "skills": extract_skills(text),
                    "education": extract_education(text),
                    "experience": extract_experience(text),
                })
        st.session_state.resumes = resumes
        st.session_state.processed = False
        st.rerun()

if resumes:
    st.markdown(f"""
    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.5rem;">
        <span style="color:#e0e0ff;font-size:1.1rem;font-weight:600;">
            Uploaded Resumes
            <span style="color:#8888bb;font-size:0.85rem;font-weight:400;margin-left:0.5rem;">({len(resumes)} total)</span>
        </span>
    </div>
    """, unsafe_allow_html=True)

    for i, r in enumerate(resumes):
        skill_tags = "".join(f'<span class="badge">{s}</span>' for s in r["skills"][:8])
        if len(r["skills"]) > 8:
            skill_tags += f'<span class="badge" style="background:transparent;">+{len(r["skills"])-8}</span>'

        edu_text = r["education"][0].title() if r["education"] else "Not specified"

        st.markdown(f"""
        <div class="card">
            <div style="display:flex;justify-content:space-between;align-items:start;">
                <div>
                    <div class="card-title">{r['name']}</div>
                    <div class="card-meta">{r['filename']} — {r['experience']} yrs exp</div>
                </div>
                <div style="text-align:right;font-size:0.8rem;color:#667eea;font-weight:600;">
                    #{i+1}
                </div>
            </div>
            <div style="display:flex;gap:1.5rem;margin:0.5rem 0;font-size:0.85rem;color:#8888bb;">
                <span>✉ {r['email']}</span>
                <span>📞 {r['phone']}</span>
                <span>🎓 {edu_text}</span>
            </div>
            <div style="margin-top:0.3rem;">{skill_tags}</div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("Clear All Resumes", type="secondary", use_container_width=True):
        st.session_state.resumes = []
        st.session_state.results = []
        st.session_state.processed = False
        st.rerun()
else:
    st.markdown("""
    <div class="card" style="text-align:center;padding:2rem;">
        <div style="font-size:3rem;margin-bottom:0.5rem;">📄</div>
        <div class="card-title">No Resumes Yet</div>
        <div class="card-meta">Upload PDF, DOCX, or TXT files above to get started.</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()
st.markdown(f"""
<div style="display:flex;gap:1rem;justify-content:center;">
    <span>{status_badge('Resumes: ' + str(len(resumes)), 'green' if resumes else 'yellow')}</span>
    <span>{status_badge('JD: Ready', 'green')}</span>
</div>
""", unsafe_allow_html=True)
