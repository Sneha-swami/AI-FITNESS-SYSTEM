from flask import Flask, render_template, request, redirect, session
import sqlite3
import pandas as pd
from flask_bcrypt import Bcrypt
from sklearn.linear_model import LinearRegression

app = Flask(__name__)
app.secret_key = "fitness_secret_key"
bcrypt = Bcrypt(app)

# =========================
# LOAD DATASETS
# =========================

exercise_df = pd.read_csv("dataset/exercise.csv")
calories_df = pd.read_csv("dataset/calories.csv")

df = exercise_df.merge(calories_df, on="User_ID")

df["Gender"] = df["Gender"].map({
    "male": 0,
    "female": 1
})

X = df[[
    "Gender",
    "Age",
    "Height",
    "Weight",
    "Duration",
    "Heart_Rate",
    "Body_Temp"
]]

y = df["Calories"]

model = LinearRegression()
model.fit(X, y)


# =========================
# HELPER FUNCTIONS
# =========================

def calculate_fitness_score(bmi, calories, duration):
    score = 100

    if bmi < 18.5:
        score -= 25
    elif bmi < 25:
        score -= 0
    elif bmi < 30:
        score -= 15
    else:
        score -= 30

    if calories < 100:
        score -= 15
    elif calories < 250:
        score -= 5

    if duration < 10:
        score -= 15
    elif duration < 30:
        score -= 5

    return max(score, 0)


def get_score_status(score):
    if score >= 85:
        return "Excellent"
    elif score >= 70:
        return "Good"
    elif score >= 50:
        return "Average"
    else:
        return "Needs Improvement"


# =========================
# HOME PAGE
# =========================

@app.route("/")
def home():
    if "user" not in session:
        return redirect("/login")

    return render_template("index.html")


# =========================
# PREDICTION ROUTE
# =========================

@app.route("/predict", methods=["POST"])
def predict():
    if "user" not in session:
        return redirect("/login")

    username = session["user"]

    gender = request.form["gender"]
    age = int(request.form["age"])
    height = float(request.form["height"])
    weight = float(request.form["weight"])
    duration = int(request.form["duration"])
    heart_rate = int(request.form["heart_rate"])
    body_temp = float(request.form["body_temp"])
    goal = request.form["goal"]

    gender_value = 0 if gender == "male" else 1

    bmi = round(
        weight / ((height / 100) ** 2),
        2
    )

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"

    prediction = model.predict([[
        gender_value,
        age,
        height,
        weight,
        duration,
        heart_rate,
        body_temp
    ]])

    calories = int(prediction[0])

    fitness_score = calculate_fitness_score(
        bmi,
        calories,
        duration
    )

    score_status = get_score_status(fitness_score)

    bmi_percentage = min(
        round((bmi / 40) * 100, 2),
        100
    )

    if goal == "Weight Loss":
        workout = """
• HIIT Training
• Running
• Cycling
• Fat Burn Cardio
• Calorie Deficit Diet
"""

    elif goal == "Muscle Gain":
        workout = """
• Strength Training
• Push Pull Legs Split
• High Protein Diet
• Heavy Compound Exercises
• Progressive Overload
"""

    else:
        workout = """
• Balanced Workout
• Yoga & Flexibility
• Moderate Cardio
• Healthy Lifestyle
"""

    conn = sqlite3.connect("fitness.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO users (
        username,
        age,
        height,
        weight,
        bmi,
        category,
        goal,
        calories
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        username,
        age,
        height,
        weight,
        bmi,
        category,
        goal,
        calories
    ))

    conn.commit()
    conn.close()

    result = {
        "bmi": bmi,
        "category": category,
        "calories": calories,
        "workout": workout,
        "fitness_score": fitness_score,
        "score_status": score_status,
        "bmi_percentage": bmi_percentage,
        "goal": goal,
        "duration": duration
    }

    return render_template(
        "index.html",
        result=result
    )


# =========================
# HISTORY PAGE
# =========================

@app.route("/history")
def history():
    if "user" not in session:
        return redirect("/login")

    username = session["user"]

    conn = sqlite3.connect("fitness.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    data = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        data=data
    )


# =========================
# ANALYTICS PAGE
# =========================

@app.route("/analytics")
def analytics():
    if "user" not in session:
        return redirect("/login")

    username = session["user"]

    conn = sqlite3.connect("fitness.db")

    data = pd.read_sql_query(
        "SELECT * FROM users WHERE username = ?",
        conn,
        params=(username,)
    )

    conn.close()

    if len(data) == 0:
        stats = {
            "users": 0,
            "avg_bmi": 0,
            "avg_calories": 0,
            "predictions": 0
        }
    else:
        stats = {
            "users": len(data),
            "avg_bmi": round(data["bmi"].mean(), 2),
            "avg_calories": round(data["calories"].mean(), 2),
            "predictions": len(data)
        }

    return render_template(
        "analytics.html",
        stats=stats
    )


# =========================
# CHATBOT PAGE
# =========================

@app.route("/chatbot", methods=["GET", "POST"])
def chatbot():
    if "user" not in session:
        return redirect("/login")

    bot_response = ""
    user_message = ""

    if request.method == "POST":
        user_message = request.form["message"]
        message = user_message.lower()

        if "weight loss" in message:
            bot_response = """
For weight loss:

• Maintain calorie deficit
• Do cardio regularly
• Increase protein intake
• Avoid sugary drinks
• Sleep properly
"""

        elif "muscle gain" in message:
            bot_response = """
For muscle gain:

• Eat high protein diet
• Do strength training
• Progressive overload
• Compound exercises
• Proper recovery
"""

        elif "bmi" in message:
            bot_response = """
BMI Categories:

• Underweight < 18.5
• Normal = 18.5 - 24.9
• Overweight = 25 - 29.9
• Obese > 30
"""

        elif "diet" in message:
            bot_response = """
Healthy Diet Tips:

• Eat whole foods
• Drink more water
• Avoid junk food
• Include protein & fiber
• Eat balanced meals
"""

        elif "workout" in message:
            bot_response = """
Workout Tips:

• Warm up properly
• Train consistently
• Focus on form
• Stay hydrated
• Rest adequately
"""

        else:
            bot_response = """
I can help with:

• Weight loss
• Muscle gain
• BMI
• Diet plans
• Workout advice
• Calories & fitness tips
"""

    return render_template(
        "chatbot.html",
        user_message=user_message,
        bot_response=bot_response
    )


# =========================
# SIGNUP PAGE
# =========================

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        hashed_password = bcrypt.generate_password_hash(
            password
        ).decode("utf-8")

        try:
            conn = sqlite3.connect("fitness.db")
            cursor = conn.cursor()

            cursor.execute("""
            INSERT INTO auth_users (
                username,
                email,
                password
            )
            VALUES (?, ?, ?)
            """, (
                username,
                email,
                hashed_password
            ))

            conn.commit()
            conn.close()

            return redirect("/login")

        except sqlite3.IntegrityError:
            return "Email or username already exists. Please login or use another email."

    return render_template("signup.html")


# =========================
# LOGIN PAGE
# =========================

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = sqlite3.connect("fitness.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM auth_users WHERE email = ?",
            (email,)
        )

        user = cursor.fetchone()
        conn.close()

        if user:
            stored_password = user[3]

            if bcrypt.check_password_hash(
                stored_password,
                password
            ):
                session["user"] = user[1]
                return redirect("/")

    return render_template("login.html")


# =========================
# LOGOUT
# =========================

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/login")


# =========================
# RUN APP
# =========================

if __name__ == "__main__":
    app.run(debug=True)