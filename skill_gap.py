required_skills = [
"python",
"sql",
"machine learning",
"statistics",
"data visualization",
"powerbi",
"tableau"
]

def detect_skill_gap(found_skills):

    missing = []

    for skill in required_skills:
        if skill not in found_skills:
            missing.append(skill)

    return missing