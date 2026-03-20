import re

skills_db = [
"python","java","sql","machine learning",
"data analysis","flask","django",
"html","css","javascript","react",
"pandas","numpy","tensorflow"
]

def ats_score(resume_text):

    resume_text = resume_text.lower()

    found_skills = []

    for skill in skills_db:
        if skill in resume_text:
            found_skills.append(skill)

    score = int((len(found_skills) / len(skills_db)) * 100)

    return score, found_skills