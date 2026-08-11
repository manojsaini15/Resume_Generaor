import streamlit as st
from dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import PromptTemplate

# Prompt template (kept identical to your original)
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
 
Return the final resume as clean, well-structured plain text.
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
        "extra_notes"
    ],
    template=RESUME_PROMPT_TEMPLATE
)

st.set_page_config(page_title="Resume Generator", layout="centered")

st.title("Resume Generator UI")
st.write("Fill in the candidate details and click Generate to create an ATS-friendly resume.")

with st.form("resume_form"):
    name = st.text_input("Full name", value="")
    job_role = st.text_input("Target job role", value="")
    experience_years = st.text_input("Years of experience", value="")
    skills = st.text_area("Skills (comma-separated or grouped)", value="")
    education = st.text_area("Education details", value="")
    work_experience = st.text_area("Work experience (list roles, dates, bullets)", value="")
    certifications = st.text_input("Certifications (comma-separated)", value="")
    extra_notes = st.text_area("Summary / Objective / Extra notes (optional)", value="")
    submit = st.form_submit_button("Generate Resume")

if submit:
    if not name or not job_role:
        st.error("Please provide at least Full name and Target job role.")
    else:
        # Build final prompt using the PromptTemplate
        final_prompt = RESUME_PROMPT_TEMPLATE.format(
            name=name,
            job_role=job_role,
            experience_years=experience_years,
            skills=skills,
            education=education,
            work_experience=work_experience,
            certifications=certifications,
            extra_notes=extra_notes or ""
        )

        st.info("Sending prompt to model. This may take a few seconds.")
        try:
            model = ChatMistralAI(model="mistral-small-latest", timeout=60)
            with st.spinner("Generating resume..."):
                response = model.invoke(final_prompt)
            # response.content is expected to contain the text
            resume_text = getattr(response, "content", None) or str(response)
            st.subheader("Generated Resume")
            st.code(resume_text, language=None)
            # Optionally allow user to copy
            st.download_button("Download as .txt", resume_text, file_name=f"{name.replace(' ', '_')}_resume.txt", mime="text/plain")
        except Exception as e:
            st.error(f"Model invocation failed: {e}")
