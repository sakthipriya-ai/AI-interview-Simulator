import pdfplumber
import docx

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from ats_scoring import ats_score
from job_recommender import recommend_jobs
from skill_gap import detect_skill_gap

# Load model
model = SentenceTransformer("all-MiniLM-L6-v2")

job_description = """
Python SQL data analysis machine learning statistics
PowerBI Tableau
"""

skills_db = [
"python","java","sql","machine learning","deep learning",
"flask","django","docker","aws","cloud",
"pandas","numpy","tensorflow","powerbi","tableau"
]


# -------- Extract Resume Text --------
def extract_text(filepath):

    text = ""

    if filepath.endswith(".pdf"):
        with pdfplumber.open(filepath) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text

    elif filepath.endswith(".docx"):
        doc = docx.Document(filepath)
        for para in doc.paragraphs:
            text += para.text

    return text.lower()


# -------- Resume Analyzer --------
def analyze_resume(filepath):

    resume_text = extract_text(filepath)

    # -------- AI Similarity --------
    embeddings = model.encode([resume_text, job_description])
    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    # -------- Skill Detection --------
    found_skills = []
    for skill in skills_db:
        if skill in resume_text:
            found_skills.append(skill)

    # -------- Other Analysis --------
    missing_skills = detect_skill_gap(found_skills)
    recommended_jobs = recommend_jobs(found_skills)

    # -------- ATS Score FIX --------
    ats_result = ats_score(resume_text)

    # Handle tuple or single value safely
    if isinstance(ats_result, tuple):
        ats = float(ats_result[0])
        ats_feedback = ats_result[1] if len(ats_result) > 1 else ""
    else:
        ats = float(ats_result)
        ats_feedback = ""

    # -------- Scores --------
    ai_score = float(similarity) * 100
    skill_score = float(len(found_skills) * 5)

    score = (ai_score * 0.6) + (skill_score * 0.2) + (ats * 0.2)
    score = round(score, 2)

    if score > 100:
        score = 100

    # -------- Feedback --------
    feedback = ""

    feedback += "\nSkills detected:\n"
    feedback += ", ".join(found_skills) if found_skills else "None"

    feedback += "\n\nMissing Skills:\n"
    feedback += ", ".join(missing_skills) if missing_skills else "None"

    feedback += "\n\nRecommended Jobs:\n"
    feedback += ", ".join(recommended_jobs) if recommended_jobs else "None"

    feedback += f"\n\nATS Score: {ats}"

    if ats_feedback:
      feedback += "\n\nATS Feedback:\n"

    if isinstance(ats_feedback, list):
        feedback += ", ".join(ats_feedback)
    else:
        feedback += str(ats_feedback)
    return score, feedback, found_skills, missing_skills