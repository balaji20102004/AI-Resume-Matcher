import streamlit as st
import tempfile
import plotly.express as px

from utils.pdf_reader import extract_text
from utils.preprocess import preprocess_text
from utils.bert_matcher import calculate_similarity
from utils.skill_extractor import extract_skills

# ---------------- PAGE CONFIG ---------------- #

st.set_page_config(
    page_title="AI Resume Matcher",
    page_icon="📄",
    layout="wide"
)

# ---------------- WINDOWS 11 THEME ---------------- #

st.markdown("""
<style>

.stApp{
    background: linear-gradient(135deg,#0f172a,#1e3a8a,#312e81);
    background-attachment: fixed;
}

.main > div{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
    padding:30px;
    border-radius:20px;
    border:1px solid rgba(255,255,255,0.15);
}

section[data-testid="stSidebar"]{
    background: rgba(255,255,255,0.08);
    backdrop-filter: blur(20px);
}

.stButton>button{
    width:100%;
    height:3em;
    border-radius:12px;
    background:#2563eb;
    color:white;
    border:none;
    font-weight:bold;
}

.stButton>button:hover{
    background:#1d4ed8;
}

div[data-testid="metric-container"]{
    background:rgba(255,255,255,0.08);
    padding:20px;
    border-radius:15px;
    border:1px solid rgba(255,255,255,0.15);
}

</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ---------------- #

with st.sidebar:

    st.title("🤖 AI Resume Matcher")

    st.markdown("---")

    st.subheader("Features")

    st.write("✅ Resume Upload")
    st.write("✅ ATS Match Score")
    st.write("✅ Skill Extraction")
    st.write("✅ Dashboard")
    st.write("✅ Charts")

    st.markdown("---")

    st.subheader("Developer")

    st.write("KV Balaji")

# ---------------- HEADER ---------------- #

st.title("📄 AI Resume Matcher")

st.caption("Analyze Resume using NLP & Machine Learning")

st.divider()

# ---------------- INPUT ---------------- #

uploaded_resume = st.file_uploader(
    "Upload Resume (PDF)",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description",
    height=220
)

# ---------------- ANALYZE BUTTON ---------------- #

if st.button("🚀 Analyze Resume"):

    if uploaded_resume is None:
        st.error("Please upload a resume.")
        st.stop()

    if job_description.strip() == "":
        st.error("Please paste a Job Description.")
        st.stop()

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        tmp.write(uploaded_resume.read())
        resume_path = tmp.name

    resume = extract_text(resume_path)

    clean_resume = preprocess_text(resume)
    clean_job = preprocess_text(job_description)

    score = calculate_similarity(
        clean_resume,
        clean_job
    )

    resume_skills = extract_skills(clean_resume)
    job_skills = extract_skills(clean_job)

    missing_skills = job_skills - resume_skills

    matched_skills = resume_skills & job_skills

    
      # ---------------- DASHBOARD ---------------- #

    st.divider()

    card1, card2, card3 = st.columns(3)

    with card1:
        st.metric(
            "🎯 Match Score",
            f"{score:.2f}%"
        )

    with card2:
        st.metric(
            "✅ Resume Skills",
            len(resume_skills)
        )

    with card3:
        st.metric(
            "❌ Missing Skills",
            len(missing_skills)
        )

    st.divider()

    # ---------------- SCORE ---------------- #

    st.subheader("📊 Resume Match Score")

    st.progress(float(min(score / 100, 1.0)))

    if score >= 80:
        st.success("Excellent Match ✅")

    elif score >= 60:
        st.info("Good Match 👍")

    elif score >= 40:
        st.warning("Average Match ⚠️")

    else:
        st.error("Poor Match ❌")

    # ---------------- SKILLS ---------------- #

    left, right = st.columns(2)

    with left:

        st.subheader("✅ Resume Skills")

        if resume_skills:

            for skill in sorted(resume_skills):
                st.success(skill)

        else:
            st.warning("No skills detected.")

    with right:

        st.subheader("❌ Missing Skills")

        if missing_skills:

            for skill in sorted(missing_skills):
                st.error(skill)

        else:
            st.success("No missing skills.")  

                # ---------------- PIE CHART ---------------- #

    st.divider()

    st.subheader("📈 Skill Distribution")

    fig = px.pie(
        names=["Matched Skills", "Missing Skills"],
        values=[
            len(matched_skills),
            len(missing_skills)
        ],
        hole=0.45,
        title="Matched vs Missing Skills"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ---------------- BAR CHART ---------------- #

    st.subheader("📊 Skills Overview")

    fig2 = px.bar(
        x=["Matched", "Missing"],
        y=[
            len(matched_skills),
            len(missing_skills)
        ],
        color=["Matched", "Missing"],
        labels={
            "x": "Category",
            "y": "Skills Count"
        }
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

    # ---------------- RECOMMENDATIONS ---------------- #

    st.divider()

    st.subheader("💡 Recommendations")

    if missing_skills:

        st.warning(
            "Consider adding the following skills to improve your ATS score:"
        )

        for skill in sorted(missing_skills):
            st.write(f"✅ Learn or mention **{skill.title()}**")

    else:

        st.success(
            "Excellent! Your resume already contains all detected job skills."
        )

    st.divider()

    st.caption("🚀 AI Resume Matcher | Built using Python, Streamlit & NLP")