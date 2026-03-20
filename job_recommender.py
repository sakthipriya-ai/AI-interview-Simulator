job_roles = {

"Data Scientist":["python","machine learning","pandas"],

"Backend Developer":["python","flask","sql"],

"Frontend Developer":["html","css","javascript","react"],

"AI Engineer":["python","tensorflow","machine learning"]

}

def recommend_jobs(skills):

    recommended = []

    for role, required in job_roles.items():

        for skill in skills:

            if skill in required:
                recommended.append(role)
                break

    return recommended
