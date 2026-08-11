from  dotenv import load_dotenv
load_dotenv()

from langchain_mistralai import ChatMistralAI

import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")



from langchain_core.prompts import PromptTemplate

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
-Basic information: {basic_info}
 
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
        "basic_info"
    ],
    template=RESUME_PROMPT_TEMPLATE
)




name=input("Enter your full name: ")
job_role=input("Enter your target job role: ")
skills=input("Enter your skills  ")
experience_years=input("Enter your years of experience: ")
education=input("Enter your education details: ")
certifications=input("Enter your certifications (if any, comma-separated): ")
basic_info=input("Enter your basic information: ")

final_prompt=RESUME_PROMPT_TEMPLATE.format(
    name=name,
    job_role=job_role,
    experience_years=experience_years,
    skills=skills,
    education=education,
    work_experience=experience_years,
    certifications=certifications,
    extra_notes=None,
    basic_info=basic_info
)




model= ChatMistralAI(model="mistral-small-latest", timeout=30)
response =model.invoke(final_prompt)
print(response.content)
