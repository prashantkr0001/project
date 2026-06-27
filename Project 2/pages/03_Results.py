import streamlit as st
import pandas as pd
import time
from utils.matcher import rank_resumes
from utils.visualizer import plot_score_comparison, plot_skill_heatmap, plot_top_skills
from utils.styles import apply_custom_css, status_badge

apply_custom_css()

st.markdown("<h1>Results</h1>", unsafe_allow_html=True)
st.markdown('<p class="subtitle">Ranked candidates and interactive visualizations</p>', unsafe_allow_html=True)

if not st.session_state.jd_text:
    st.markdown("""
    <div class="card">
        <div class="card-title">Job Description Missing</div>
        <div class="card-meta">Please add a job description first.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

if len(st.session_state.resumes) == 0:
    st.markdown("""
    <div class="card">
        <div class="card-title">No Resumes Uploaded</div>
        <div class="card-meta">Please upload resumes first.</div>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

results = st.session_state.results
jd_text = st.session_state.jd_text

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1a1a3e,#16213e);border:1px solid #2a2a5e;
                border-radius:12px;padding:1rem;text-align:center;box-shadow:0 4px 15px rgba(0,0,0,0.3);">
        <div style="color:#8888bb;font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;">Candidates</div>
        <div style="color:#e0e0ff;font-size:1.6rem;font-weight:700;">{len(st.session_state.resumes)}</div>
    </div>""", unsafe_allow_html=True)
with col2:
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1a1a3e,#16213e);border:1px solid #2a2a5e;
                border-radius:12px;padding:1rem;text-align:center;box-shadow:0 4px 15px rgba(0,0,0,0.3);">
        <div style="color:#8888bb;font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;">JD Words</div>
        <div style="color:#e0e0ff;font-size:1.6rem;font-weight:700;">{len(jd_text.split())}</div>
    </div>""", unsafe_allow_html=True)
with col3:
    status = "Complete" if st.session_state.processed else "Pending"
    s_dot = "green" if st.session_state.processed else "yellow"
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#1a1a3e,#16213e);border:1px solid #2a2a5e;
                border-radius:12px;padding:1rem;text-align:center;box-shadow:0 4px 15px rgba(0,0,0,0.3);">
        <div style="color:#8888bb;font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;">Pipeline</div>
        <div style="margin-top:0.5rem;">{status_badge(status, s_dot)}</div>
    </div>""", unsafe_allow_html=True)

if st.session_state.processed:
    if st.button("Re-run AI Pipeline", type="primary", use_container_width=False):
        st.session_state.processed = False
        st.rerun()
else:
    run = st.button("Run AI Pipeline", type="primary", use_container_width=True)
    if run:
        with st.spinner("Running AI pipeline across all resumes..."):
            start = time.time()
            resumes_data = [
                {"text": r["text"], **{k: r[k] for k in r if k != "text"}}
                for r in st.session_state.resumes
            ]
            results = rank_resumes(resumes_data, jd_text)
            st.session_state.results = results
            st.session_state.processed = True
            elapsed = time.time() - start
        st.success(f"Processed {len(results)} resumes in {elapsed:.2f}s")
        st.rerun()

if st.session_state.processed and st.session_state.results:
    results = st.session_state.results
    all_skills = sorted(set(s for r in results for s in r["matched_skills"]))

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Rankings", "Comparison", "Skill Matrix", "Details", "AI Pipeline"]
    )

    with tab1:
        df = pd.DataFrame(results)[
            ["name", "email", "phone", "overall_score", "semantic_score",
             "tfidf_score", "skill_score", "experience"]
        ]
        df.columns = ["Name", "Email", "Phone", "Overall %", "Semantic %",
                      "TF-IDF %", "Skills %", "Exp (yrs)"]
        df = df.sort_values("Overall %", ascending=False)

        for idx, row in df.iterrows():
            medal = ""
            if idx == 0: medal = "🥇"
            elif idx == 1: medal = "🥈"
            elif idx == 2: medal = "🥉"
            st.markdown(f"""
            <div class="card" style="display:flex;justify-content:space-between;align-items:center;padding:0.8rem 1.2rem;">
                <div>
                    <span style="font-size:1.2rem;margin-right:0.5rem;">{medal}</span>
                    <span style="color:#e0e0ff;font-weight:600;">{row['Name']}</span>
                    <span style="color:#8888bb;margin-left:0.8rem;">{row['Email']}</span>
                </div>
                <div style="display:flex;align-items:center;gap:1.5rem;">
                    <div style="text-align:center;">
                        <div style="color:#667eea;font-size:1.3rem;font-weight:700;">{row['Overall %']}%</div>
                        <div style="color:#8888bb;font-size:0.65rem;text-transform:uppercase;">Overall</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:#a0a0cc;font-size:0.9rem;">{row['Semantic %']}%</div>
                        <div style="color:#8888bb;font-size:0.65rem;text-transform:uppercase;">Semantic</div>
                    </div>
                    <div style="text-align:center;">
                        <div style="color:#a0a0cc;font-size:0.9rem;">{row['Skills %']}%</div>
                        <div style="color:#8888bb;font-size:0.65rem;text-transform:uppercase;">Skills</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("Download Rankings as CSV", csv, "rankings.csv", "text/csv")

    with tab2:
        fig = plot_score_comparison(results)
        st.plotly_chart(fig, use_container_width=True)
        if all_skills:
            freq = {s: sum(1 for r in results if s in r["matched_skills"])
                    for s in all_skills}
            fig2 = plot_top_skills(freq)
            st.plotly_chart(fig2, use_container_width=True)

    with tab3:
        if all_skills:
            fig3 = plot_skill_heatmap(results, all_skills)
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No skills matched across candidates.")

    with tab4:
        for i, r in enumerate(results):
            medal = ""
            if i == 0: medal = "🥇 "
            elif i == 1: medal = "🥈 "
            elif i == 2: medal = "🥉 "
            with st.expander(f"{medal}{r['name']} — Score: {r['overall_score']}%"):
                c1, c2 = st.columns([1, 1])
                with c1:
                    st.markdown(f"**Email:** {r['email']}")
                    st.markdown(f"**Phone:** {r['phone']}")
                    st.markdown(f"**Experience:** {r['experience']} years")
                with c2:
                    st.markdown(f"**Semantic Score:** {r['semantic_score']}%")
                    st.markdown(f"**TF-IDF Score:** {r['tfidf_score']}%")
                    st.markdown(f"**Skill Score:** {r['skill_score']}%")
                matched = ", ".join(r["matched_skills"]) if r["matched_skills"] else "None"
                st.markdown(f"**Matched Skills:** {matched}")
                if r["missing_skills"]:
                    st.markdown(f"**Missing Skills:** {', '.join(r['missing_skills'])}")
                if r["education"]:
                    st.markdown("**Education:**")
                    for edu in r["education"]:
                        st.markdown(f"- {edu.title()}")

    with tab5:
        model_info = st.session_state.get("model_info", {})
        st.markdown(f"""
        <div class="card">
            <div class="card-title">AI/ML Pipeline</div>
            <div style="color:#a0a0cc;margin:0.5rem 0;">
                <strong>Model:</strong> <code style="color:#667eea;">{model_info.get('model', 'all-MiniLM-L6-v2')}</code><br>
                <strong>Type:</strong> {model_info.get('type', 'Sentence Transformer')}<br>
                <strong>Dimensions:</strong> {model_info.get('dimensions', 384)}<br>
                <strong>Source:</strong> {model_info.get('source', 'HuggingFace')}
            </div>
            <div style="margin-top:1rem;">
                <div style="color:#e0e0ff;font-weight:600;margin-bottom:0.3rem;">Pipeline Steps</div>
                <ol style="color:#a0a0cc;line-height:1.8;padding-left:1.2rem;">
                    <li><strong style="color:#667eea;">Text Extraction</strong> — Extract raw text from PDF/DOCX/TXT</li>
                    <li><strong style="color:#667eea;">NLP Parsing</strong> — Regex + pattern matching for name, email, phone, education, experience</li>
                    <li><strong style="color:#667eea;">Skill Extraction</strong> — Keyword matching against 75+ skill database</li>
                    <li><strong style="color:#667eea;">Semantic Embedding</strong> — Encode resume and JD into 384-dim vectors using all-MiniLM-L6-v2</li>
                    <li><strong style="color:#667eea;">Chunked Similarity</strong> — Compare resume sections against JD sections (max-pooled cosine similarity)</li>
                    <li><strong style="color:#667eea;">TF-IDF Baseline</strong> — Traditional bag-of-words similarity as secondary signal</li>
                    <li><strong style="color:#667eea;">Weighted Scoring</strong> — Overall = 50% (70% semantic + 30% TF-IDF) + 50% skill match</li>
                    <li><strong style="color:#667eea;">Ranking</strong> — Sort candidates by overall score descending</li>
                </ol>
            </div>
        </div>
        """, unsafe_allow_html=True)

elif not st.session_state.processed:
    st.markdown("""
    <div class="card" style="text-align:center;padding:2rem;">
        <div style="font-size:3rem;margin-bottom:0.5rem;">⚡</div>
        <div class="card-title">Ready to Analyze</div>
        <div class="card-meta">Click the <strong>Run AI Pipeline</strong> button above to start.</div>
    </div>
    """, unsafe_allow_html=True)
