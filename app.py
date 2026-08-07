from utils.pdf_reader import extract_text
from utils.preprocess import preprocess_text
from utils.matcher import calculate_similarity
from utils.skill_extractor import extract_skills

# Read Resume
resume = extract_text("data/resume.pdf")

# Read Job Description
with open("data/job.txt", "r", encoding="utf-8") as file:
    job = file.read()

# Preprocess
clean_resume = preprocess_text(resume)
clean_job = preprocess_text(job)

# Match Score
score = calculate_similarity(clean_resume, clean_job)

# Extract Skills
resume_skills = extract_skills(clean_resume)
job_skills = extract_skills(clean_job)

missing_skills = job_skills - resume_skills

print("=" * 40)
print(f"Resume Match Score : {score:.2f}%")
print("=" * 40)

print("\nResume Skills")
print(sorted(resume_skills))

print("\nJob Skills")
print(sorted(job_skills))

print("\nMissing Skills")
print(sorted(missing_skills))