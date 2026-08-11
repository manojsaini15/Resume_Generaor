import streamlit as st
from dotenv import load_dotenv

load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import PromptTemplate

# ---------------------------------------------------------------------------
# Prompt template (same one from your script)
# ---------------------------------------------------------------------------
RESUME_PROMPT_TEMPLATE = """You are an expert resume writer and career coach.
Generate a professional, ATS-friendly resume based on the details below.

Candidate Details:
- Full Name: {name}
- Target Job Role: {job_role}
- Years of Experience: {experience_years}
- Skills: {skills}
- Education: {education}
- Work Experience: {work_experience}
- Certifications: {certifications}
- Summary/Objective (optional notes from candidate): {extra_notes}

Instructions:
1. Write a compelling 2-3 line professional summary tailored to the target job role.
2. List skills in a clean, categorized format (Technical Skills, Soft Skills).
3. Present work experience in reverse-chronological order with 2-4 bullet points
   per role, each starting with a strong action verb and quantifying impact
   where possible.
4. Include an Education section.
5. Include a Certifications section if certifications are provided.
6. Keep formatting clean using plain text section headers (no markdown symbols
   like ** or #), suitable for direct use in a .docx or .pdf resume.
7. Do not invent facts not present in the candidate details; only elaborate
   on wording and structure.
 dont add things from your side
 
Return the final resume as clean, well-structured plain text and word document with ats friendly formatting.
"""

prompt = PromptTemplate(
    input_variables=[
        "name",
        "job_role",
        "experience_years",
        "skills",
        "education",
        "work_experience",
        "certifications",
        "extra_notes",
    ],
    template=RESUME_PROMPT_TEMPLATE,
)

# ---------------------------------------------------------------------------
# Page setup
# ---------------------------------------------------------------------------
st.set_page_config(page_title="AI Resume Builder", page_icon="📄", layout="wide")

st.title("📄 AI Resume Builder")
st.caption("Fill in your details and let AI draft an ATS-friendly resume for you.")

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

left, right = st.columns([1, 1.2], gap="large")

# ---------------------------------------------------------------------------
# Left column: input form
# ---------------------------------------------------------------------------
with left:
    with st.form("resume_form"):
        st.subheader("Candidate Details")

        name = st.text_input("Full Name *", placeholder="e.g. Manoj Saini")
        job_role = st.text_input("Target Job Role *", placeholder="e.g. Data Analyst")

        col1, col2 = st.columns(2)
        with col1:
            experience_years = st.text_input("Years of Experience *", placeholder="e.g. 2")
        with col2:
            certifications = st.text_input("Certifications (comma-separated)", placeholder="e.g. PL-300, AWS CCP")

        skills = st.text_area(
            "Skills *",
            placeholder="e.g. Python, SQL, Power BI, Data Visualization, Communication",
            height=80,
        )

        education = st.text_area(
            "Education *",
            placeholder="e.g. B.Tech in CSE, Arya College of Engineering, 2022-2026",
            height=80,
        )

        work_experience = st.text_area(
            "Work Experience",
            placeholder="Describe roles, companies, dates, and responsibilities/achievements",
            height=150,
        )

        extra_notes = st.text_area(
            "Extra Notes (optional)",
            placeholder="Anything else you'd like included, e.g. career goals",
            height=80,
        )

        model_name = st.selectbox(
            "Model",
            ["mistral-small-latest", "mistral-large-latest", "mistral-medium-latest"],
            index=0,
        )

        submitted = st.form_submit_button("✨ Generate Resume", use_container_width=True)

    if submitted:
        missing = [
            label
            for label, val in [
                ("Full Name", name),
                ("Target Job Role", job_role),
                ("Years of Experience", experience_years),
                ("Skills", skills),
                ("Education", education),
            ]
            if not val.strip()
        ]
        if missing:
            st.error(f"Please fill in required fields: {', '.join(missing)}")
        else:
            final_prompt = prompt.format(
                name=name,
                job_role=job_role,
                experience_years=experience_years,
                skills=skills,
                education=education,
                work_experience=work_experience or "Not provided",
                certifications=certifications or "None",
                extra_notes=extra_notes or "None",
            )
            with st.spinner("Generating your resume..."):
                try:
                    model = ChatMistralAI(model=model_name, timeout=30)
                    response = model.invoke(final_prompt)
                    st.session_state.resume_text = response.content
                except Exception as e:
                    st.error(f"Something went wrong while generating the resume: {e}")

# ---------------------------------------------------------------------------
# Right column: output
# ---------------------------------------------------------------------------
with right:
    st.subheader("Generated Resume")
    if st.session_state.resume_text:
        st.text_area("Resume Preview", st.session_state.resume_text, height=500)
        st.download_button(
            "⬇️ Download as .txt",
            data=st.session_state.resume_text,
            file_name=f"{(name or 'resume').replace(' ', '_')}_resume.txt",
            mime="text/plain",
            use_container_width=True,
        )
    else:
        st.info("Fill in the form on the left and click **Generate Resume** to see the result here.")