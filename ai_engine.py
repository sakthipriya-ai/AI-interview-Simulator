import json


# -------- Load Questions --------
def load_questions():
    with open("questions.json", "r") as file:
        data = json.load(file)
    return data


# -------- Evaluate Answer (LIGHTWEIGHT VERSION) --------
def evaluate_answer(user_answer, correct_answer):

    # Convert to lowercase
    user_answer = user_answer.lower()
    correct_answer = correct_answer.lower()

    # Split into words
    correct_words = correct_answer.split()
    user_words = user_answer.split()

    # Count matching words
    match_count = 0
    for word in correct_words:
        if word in user_words:
            match_count += 1

    # Calculate similarity safely
    if len(correct_words) > 0:
        similarity = match_count / len(correct_words)
    else:
        similarity = 0

    # Score out of 10
    score = round(similarity * 10, 2)

    # Feedback
    if score >= 8:
        feedback = "Excellent answer. Very close to expected response."
    elif score >= 6:
        feedback = "Good answer but you can improve explanation."
    elif score >= 4:
        feedback = "Average answer. Try adding more technical details."
    else:
        feedback = "Answer needs improvement. Review the concept."

    return score, feedback
