
import re

SKILLS = [
    "python",
    "java",
    "c++",
    "machine learning",
    "deep learning",
    "html",
    "css",
    "javascript",
    "sql",
    "flask",
    "django",
    "data science",
    "excel",
    "pandas",
    "numpy",
    "scikit-learn",
    "communication",
    "teamwork"
]

def extract_skills(text):

    text = text.lower()
    found_skills = []

    for skill in SKILLS:
        pattern = r'(?<!\w)' + re.escape(skill) + r'(?!\w)'

        if re.search(pattern, text):
            found_skills.append(skill)

    return found_skills


def find_missing_skills(resume_skills, job_skills):

    matched = []

    missing = []

    for skill in job_skills:

        if skill in resume_skills:
            matched.append(skill)
        else:
            missing.append(skill)

    return matched, missing
