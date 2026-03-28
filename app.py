import streamlit as st
import pdfplumber
import io
from model import analyze_resume

st.set_page_config(
    page_title="CareerAI — Resume Analyzer",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600&display=swap');

#MainMenu, footer, header { visibility: hidden; }
section.main > div { padding-top: 0rem; }
* { font-family: 'Inter', sans-serif; }

.stApp { background: #f0f6ff; color: #0f172a; }

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #e2eaf6; }
::-webkit-scrollbar-thumb { background: #93c5fd; border-radius: 2px; }

.hero-wrap { text-align: center; padding: 44px 20px 32px; }
.hero-eyebrow { font-size: 11px; font-weight: 600; letter-spacing: 3px; color: #2563eb; text-transform: uppercase; margin-bottom: 14px; }
.hero-title { font-family: 'Syne', sans-serif; font-size: 52px; font-weight: 800; line-height: 1.05; background: linear-gradient(135deg, #1e40af 0%, #2563eb 60%, #38bdf8 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin: 0 0 14px; }
.hero-sub { font-size: 16px; color: #64748b; max-width: 460px; margin: 0 auto 24px; line-height: 1.6; }
.stat-row { display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }
.stat-pill { background: #fff; border: 1px solid #bfdbfe; border-radius: 100px; padding: 5px 14px; font-size: 12px; color: #64748b; box-shadow: 0 1px 4px rgba(37,99,235,0.07); }
.stat-pill span { color: #2563eb; font-weight: 600; }

.divider { border: none; border-top: 1px solid #bfdbfe; margin: 28px 0; }

.section-header { font-family: 'Syne', sans-serif; font-size: 13px; font-weight: 700; color: #1e40af; letter-spacing: 1px; text-transform: uppercase; margin-bottom: 12px; padding-bottom: 8px; border-bottom: 2px solid #bfdbfe; }

.card { background: #fff; border: 1px solid #bfdbfe; border-radius: 14px; padding: 22px 24px; margin-bottom: 16px; box-shadow: 0 2px 12px rgba(37,99,235,0.06); }

div[data-baseweb="select"] > div { background: #f8faff !important; border: 1px solid #bfdbfe !important; border-radius: 10px !important; color: #0f172a !important; font-size: 14px !important; }
textarea { background: #f8faff !important; border: 1px solid #bfdbfe !important; border-radius: 10px !important; color: #1e293b !important; font-size: 14px !important; line-height: 1.7 !important; }
textarea:focus { border-color: #2563eb !important; box-shadow: 0 0 0 3px rgba(37,99,235,0.10) !important; }

[data-testid="stFileUploader"] { background: #f8faff; border: 2px dashed #bfdbfe; border-radius: 12px; padding: 8px; }
[data-testid="stFileUploader"]:hover { border-color: #2563eb; }

[data-baseweb="tab-list"] { background: #f0f6ff !important; border-radius: 10px; padding: 4px; gap: 4px; }
[data-baseweb="tab"] { border-radius: 8px !important; font-size: 13px !important; font-weight: 500 !important; color: #64748b !important; }
[aria-selected="true"] { background: #fff !important; color: #2563eb !important; box-shadow: 0 1px 4px rgba(37,99,235,0.12) !important; }

.stButton > button { width: 100%; background: linear-gradient(135deg, #2563eb, #38bdf8); color: white; border: none; border-radius: 10px; padding: 13px 20px; font-family: 'Syne', sans-serif; font-size: 15px; font-weight: 700; letter-spacing: 0.5px; transition: opacity 0.2s; margin-top: 4px; }
.stButton > button:hover { opacity: 0.88; }

.score-ring { width: 110px; height: 110px; border-radius: 50%; display: flex; flex-direction: column; align-items: center; justify-content: center; border: 3px solid; margin: 0 auto 12px; }
.score-ring.excellent { border-color: #16a34a; background: rgba(22,163,74,0.07); }
.score-ring.good      { border-color: #2563eb; background: rgba(37,99,235,0.07); }
.score-ring.average   { border-color: #d97706; background: rgba(217,119,6,0.07); }
.score-ring.weak      { border-color: #dc2626; background: rgba(220,38,38,0.07); }
.score-num { font-family: 'Syne', sans-serif; font-size: 32px; font-weight: 800; line-height: 1; }
.score-ring.excellent .score-num { color: #16a34a; }
.score-ring.good      .score-num { color: #2563eb; }
.score-ring.average   .score-num { color: #d97706; }
.score-ring.weak      .score-num { color: #dc2626; }
.score-label { font-size: 10px; color: #94a3b8; letter-spacing: 1px; text-transform: uppercase; margin-top: 2px; }
.score-verdict { font-family: 'Syne', sans-serif; font-size: 17px; font-weight: 700; color: #0f172a; margin-bottom: 4px; text-align: center; }
.score-sub { font-size: 12px; color: #64748b; text-align: center; }

.chip-wrap { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px; }
.chip { padding: 4px 12px; border-radius: 100px; font-size: 12px; font-weight: 500; }
.chip-found   { background: #dcfce7; color: #15803d; border: 1px solid #bbf7d0; }
.chip-missing { background: #fee2e2; color: #b91c1c; border: 1px solid #fecaca; }
.chip-bonus   { background: #dbeafe; color: #1d4ed8; border: 1px solid #bfdbfe; }

.sub-label { font-size: 10px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; color: #94a3b8; margin: 14px 0 6px; }

.suggestion { display: flex; gap: 10px; align-items: flex-start; padding: 10px 14px; background: #f0f6ff; border: 1px solid #bfdbfe; border-radius: 10px; margin-bottom: 8px; font-size: 13px; color: #334155; line-height: 1.5; }
.suggestion-dot { width: 6px; height: 6px; border-radius: 50%; background: #2563eb; flex-shrink: 0; margin-top: 5px; }

.seniority-badge { display: inline-block; padding: 4px 14px; border-radius: 100px; font-size: 12px; font-weight: 600; background: #ede9fe; color: #5b21b6; border: 1px solid #c4b5fd; }

.progress-wrap { margin: 8px 0 4px; }
.progress-label { display: flex; justify-content: space-between; font-size: 12px; color: #64748b; margin-bottom: 5px; }
.progress-bg { background: #dbeafe; border-radius: 4px; height: 5px; }
.progress-fill { height: 5px; border-radius: 4px; }

.empty-state { text-align: center; padding: 48px 20px; background: #fff; border: 1px solid #bfdbfe; border-radius: 14px; box-shadow: 0 2px 12px rgba(37,99,235,0.06); }

.footer { text-align: center; padding: 28px 0 16px; font-size: 12px; color: #94a3b8; }
.footer span { color: #2563eb; }
</style>
""", unsafe_allow_html=True)

# ── HERO ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
    <div class="hero-eyebrow">AI-Powered Career Tool</div>
    <h1 class="hero-title">CareerAI</h1>
    <p class="hero-sub">Upload your resume PDF or paste text — get instant skill analysis and career insights</p>
    <div class="stat-row">
        <div class="stat-pill"><span>6</span> Job Roles</div>
        <div class="stat-pill"><span>TF-IDF</span> NLP Engine</div>
        <div class="stat-pill"><span>PDF</span> Support</div>
        <div class="stat-pill"><span>Instant</span> Results</div>
    </div>
</div>
<hr class="divider">
""", unsafe_allow_html=True)

# ── LAYOUT ────────────────────────────────────────────────────────────
left, right = st.columns([1, 1.2], gap="large")

# ── LEFT PANEL ────────────────────────────────────────────────────────
with left:
    st.markdown('<div class="section-header">Configure Analysis</div>', unsafe_allow_html=True)

    # Role
    role = st.selectbox(
        "Target Role",
        ["Software Developer", "Data Analyst", "Machine Learning Engineer",
         "Frontend Developer", "Backend Developer", "DevOps Engineer"],
        help="Select the role you are targeting"
    )

    # Resume input
    tab_pdf, tab_text = st.tabs(["  Upload PDF  ", "  Paste Text  "])

    resume_text = ""

    with tab_pdf:
        st.markdown("<br>", unsafe_allow_html=True)
        uploaded_file = st.file_uploader(
            "Drop your resume PDF here",
            type=["pdf"],
            label_visibility="collapsed"
        )
        if uploaded_file:
            try:
                with pdfplumber.open(io.BytesIO(uploaded_file.read())) as pdf:
                    extracted = "\n".join(
                        page.extract_text() or "" for page in pdf.pages
                    ).strip()
                if extracted:
                    resume_text = extracted
                    st.success(f"PDF read successfully — {len(resume_text.split())} words found")
                else:
                    st.error("No text found. Make sure your PDF is not a scanned image.")
            except Exception as e:
                st.error(f"Could not read PDF: {e}")

    with tab_text:
        typed = st.text_area(
            "Resume text",
            height=220,
            placeholder="Paste your full resume here — skills, experience, education, projects...",
            label_visibility="collapsed"
        )
        if typed.strip():
            resume_text = typed

    if resume_text.strip():
        ca, cb = st.columns(2)
        ca.metric("Words", len(resume_text.split()))
        cb.metric("Characters", len(resume_text))

    analyze = st.button("Analyze Resume →", use_container_width=True)

# ── RIGHT PANEL ───────────────────────────────────────────────────────
with right:
    st.markdown('<div class="section-header">Analysis Results</div>', unsafe_allow_html=True)

    if not analyze:
        st.markdown("""
        <div class="empty-state">
            <div style="font-size:36px; color:#bfdbfe; margin-bottom:14px;">◎</div>
            <div style="font-family:'Syne',sans-serif; font-size:17px; font-weight:700; color:#1e40af; margin-bottom:8px;">Ready to analyze</div>
            <div style="font-size:13px; color:#64748b; line-height:1.6;">Upload a PDF or paste your resume,<br>select a role, then click Analyze.</div>
        </div>
        """, unsafe_allow_html=True)

    elif not resume_text.strip():
        st.warning("Please upload a PDF or paste resume text first.")

    else:
        result = analyze_resume(resume_text, role)

        if not result:
            st.error("Analysis failed. Please try again.")
        else:
            score         = result["score"]
            keyword_score = result["keyword_score"]
            tfidf_score   = result["tfidf_score"]
            found         = result["found_required"]
            missing       = result["missing_required"]
            bonus         = result["found_bonus"]
            suggestions   = result["suggestions"]
            seniority     = result["seniority"]

            if score >= 80:
                ring_class, verdict, verdict_sub = "excellent", "Excellent Match", "Your profile strongly aligns with this role"
            elif score >= 60:
                ring_class, verdict, verdict_sub = "good",      "Good Match",      "Solid foundation — close a few skill gaps"
            elif score >= 40:
                ring_class, verdict, verdict_sub = "average",   "Partial Match",   "Some key skills need attention"
            else:
                ring_class, verdict, verdict_sub = "weak",      "Needs Work",      "Significant skill gaps detected"

            # Score card
            st.markdown(f"""
            <div class="card" style="text-align:center; padding:24px;">
                <div class="score-ring {ring_class}">
                    <div class="score-num">{score}</div>
                    <div class="score-label">/ 100</div>
                </div>
                <div class="score-verdict">{verdict}</div>
                <div class="score-sub">{verdict_sub}</div>
                <div style="margin-top:12px;">
                    <span class="seniority-badge">Detected Level: {seniority}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Metrics
            c1, c2, c3 = st.columns(3)
            c1.metric("Keyword Match", f"{keyword_score}%")
            c2.metric("TF-IDF Score",  f"{tfidf_score}%")
            c3.metric("Skills Found",  f"{len(found)}/{len(found)+len(missing)}")

            # Progress bars
            st.markdown(f"""
            <div class="card" style="padding:18px 22px;">
                <div class="progress-wrap">
                    <div class="progress-label"><span>Skill Coverage</span><span>{keyword_score}%</span></div>
                    <div class="progress-bg"><div class="progress-fill" style="width:{keyword_score}%; background:linear-gradient(90deg,#2563eb,#38bdf8);"></div></div>
                </div>
                <div class="progress-wrap" style="margin-top:12px;">
                    <div class="progress-label"><span>Semantic Similarity</span><span>{tfidf_score}%</span></div>
                    <div class="progress-bg"><div class="progress-fill" style="width:{tfidf_score}%; background:linear-gradient(90deg,#7c3aed,#a78bfa);"></div></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Skills
            st.markdown('<div class="card">', unsafe_allow_html=True)
            if found:
                st.markdown(f"""
                <div class="sub-label">Matched Skills</div>
                <div class="chip-wrap">{"".join(f'<span class="chip chip-found">{s}</span>' for s in found)}</div>
                """, unsafe_allow_html=True)
            if missing:
                st.markdown(f"""
                <div class="sub-label">Missing Skills</div>
                <div class="chip-wrap">{"".join(f'<span class="chip chip-missing">{s}</span>' for s in missing)}</div>
                """, unsafe_allow_html=True)
            if bonus:
                st.markdown(f"""
                <div class="sub-label">Bonus Skills</div>
                <div class="chip-wrap">{"".join(f'<span class="chip chip-bonus">{s}</span>' for s in bonus)}</div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

            # Suggestions
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.markdown('<div class="sub-label">AI Recommendations</div>', unsafe_allow_html=True)
            for s in suggestions:
                st.markdown(f"""
                <div class="suggestion"><div class="suggestion-dot"></div><div>{s}</div></div>
                """, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────
st.markdown("""
<hr class="divider">
<div class="footer">
    CareerAI © 2026 — Built with <span>Python · Scikit-learn · pdfplumber · Streamlit</span>
</div>
""", unsafe_allow_html=True)