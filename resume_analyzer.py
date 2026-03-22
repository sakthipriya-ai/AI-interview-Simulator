def analyze_resume(filepath):

    resume_text = extract_text(filepath)

    # -------- Skill Detection --------
    found_skills = []
    for skill in skills_db:
        if skill in resume_text:
            found_skills.append(skill)

    # -------- Missing Skills --------
    missing_skills = [s for s in skills_db if s not in found_skills]

    # -------- Recommended Jobs --------
    if "python" in found_skills:
        recommended_jobs = ["Software Engineer", "Backend Developer"]
    elif "machine learning" in found_skills:
        recommended_jobs = ["Data Scientist", "ML Engineer"]
    else:
        recommended_jobs = ["Junior Developer", "IT Support"]

    # -------- Score --------
    score = len(found_skills) * 7
    if score > 100:
        score = 100

    # -------- Feedback --------
    feedback = ""

    feedback += "Skills detected:\n"
    feedback += ", ".join(found_skills) if found_skills else "None"

    feedback += "\n\nMissing Skills:\n"
    feedback += ", ".join(missing_skills) if missing_skills else "None"

    feedback += "\n\nRecommended Jobs:\n"
    feedback += ", ".join(recommended_jobs)

    return score, feedback, found_skills, missing_skills
