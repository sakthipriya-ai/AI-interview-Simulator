import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# Load AI model
model = SentenceTransformer('all-MiniLM-L6-v2')


def load_questions():

    with open("questions.json", "r") as file:
        data = json.load(file)

    return data


def evaluate_answer(user_answer, correct_answer):

    sentences = [user_answer, correct_answer]

    embeddings = model.encode(sentences)

    similarity = cosine_similarity(
        [embeddings[0]],
        [embeddings[1]]
    )[0][0]

    score = round(similarity * 10, 2)

    if score >= 8:
        feedback = "Excellent answer. Very close to expected response."

    elif score >= 6:
        feedback = "Good answer but you can improve explanation."

    elif score >= 4:
        feedback = "Average answer. Try adding more technical details."

    else:
        feedback = "Answer needs improvement. Review the concept."

    return score, feedback