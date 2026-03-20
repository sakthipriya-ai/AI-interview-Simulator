from flask import Flask, render_template, request, redirect, session, jsonify
import sqlite3
import random
import os

from ai_engine import evaluate_answer, load_questions
from database import create_database
from resume_analyzer import analyze_resume
from chatbot_engine import get_chatbot_reply

app = Flask(__name__)
app.secret_key = "secret"

create_database()

questions = load_questions()

current_question = ""
current_answer = ""

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------------- LANDING PAGE ----------------
@app.route("/")
def home():
    return render_template("landing.html")

@app.route("/login")
def login():
    return render_template("login.html")

# ---------------- SIGNUP ----------------
@app.route("/signup")
def signup():
    return render_template("signup.html")


# ---------------- REGISTER ----------------
@app.route("/register", methods=["POST"])
def register():

    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users(username,email,password) VALUES(?,?,?)",
        (username, email, password)
    )

    conn.commit()
    conn.close()

    return redirect("/")


# ---------------- LOGIN ----------------

@app.route("/login", methods=["GET", "POST"])
def login_user():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("users.db")
        cur = conn.cursor()

        cur.execute(
            "SELECT * FROM users WHERE email=? AND password=?",
            (email, password)
        )

        user = cur.fetchone()
        conn.close()

        if user:
            session["user"] = user[1]
            return redirect("/dashboard")

        return "Invalid login"

    return render_template("login.html")


# ---------------- DASHBOARD ----------------

@app.route("/dashboard")
def dashboard():

    if "user" not in session:
        return redirect("/")

    # ✅ CONNECT DATABASE (IMPORTANT FIX)
    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT score FROM interview_history WHERE username=?",
        (session["user"],)
    )

    data = cur.fetchall()
    conn.close()

    # ✅ CLEAN SCORES (VERY IMPORTANT)
    scores = []

    for row in data:
        value = row[0]

        # Fix byte values
        if isinstance(value, bytes):
            try:
                value = int.from_bytes(value, "little")
            except:
                continue

        # Convert safely
        try:
            value = float(value)
        except:
            continue

        # Ignore invalid values
        if value > 100 or value < 0:
            continue

        scores.append(value)

    # ✅ CALCULATE AVERAGE
    if scores:
        avg_score = int(sum(scores) / len(scores))
    else:
        avg_score = 0

    # ✅ SEND TO HTML
    return render_template(
        "dashboard.html",
        user=session["user"],
        scores=scores,
        avg_score=avg_score
    )

# --------------nt_question)-- START INTERVIEW ----------------
@app.route("/interview", methods=["POST"])
def interview():

    global current_question, current_answer

    role = request.form.get("role")

    if role not in questions:
        return "Invalid role selected"

    q = random.choice(questions[role])

    current_question = q["question"]
    current_answer = q["answer"]

    return render_template("interview.html", question=current_question)


# ---------------- SUBMIT ANSWER ----------------
@app.route("/submit", methods=["POST"])
def submit():

    user_answer = request.form["answer"]

    score, feedback = evaluate_answer(user_answer, current_answer)

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO interview_history(username,score) VALUES(?,?)",
        (session["user"], score)
    )

    conn.commit()
    conn.close()

    return render_template(
        "result.html",
        score=score,
        feedback=feedback
    )


# ---------------- RESUME PAGE ----------------
@app.route("/resume")
def resume_page():

    if "user" not in session:
        return redirect("/")

    return render_template("resume.html")


# ---------------- RESUME ANALYSIS ----------------
@app.route("/analyze", methods=["POST"])
def analyze():

    if "user" not in session:
        return redirect("/")

    if "resume" not in request.files:
        return "No file uploaded"

    file = request.files["resume"]

    if file.filename == "":
        return "No selected file"

    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    try:
        score, feedback, found_skills, missing_skills = analyze_resume(filepath)
    except Exception as e:
        return f"Error in resume analysis: {str(e)}"

    return render_template(
    "resume.html",
    score=score,
    feedback=feedback,
    skills=found_skills,
    missing=missing_skills
)

# ---------------- ANALYTICS PAGE ----------------
@app.route("/analytics")
def analytics():

    if "user" not in session:
        return redirect("/")

    conn = sqlite3.connect("users.db")
    cur = conn.cursor()

    cur.execute(
        "SELECT score FROM interview_history WHERE username=?",
        (session["user"],)
    )

    scores = cur.fetchall()
    conn.close()

    score_list = [s[0] for s in scores]

    return render_template(
        "analytics.html",
        scores=score_list
    )


# ---------------- CHATBOT PAGE ----------------
@app.route("/chatbot")
def chatbot():
    return render_template("chatbot.html")


# ---------------- CHATBOT API ----------------
@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json["message"]
    user = session.get("user", "guest")

    reply = get_chatbot_reply(user, user_message)

    return jsonify({"reply": reply})

@app.route("/reset_chat")
def reset_chat():
    from chatbot_engine import user_memory
    user = session.get("user", "guest")
    user_memory.pop(user, None)
    return "Chat reset successful"

# ---------------- LOGOUT ----------------
@app.route("/logout")
def logout():

    session.pop("user", None)

    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)


