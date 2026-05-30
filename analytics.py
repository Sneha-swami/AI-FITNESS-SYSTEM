import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect("fitness.db")

df = pd.read_sql_query(
    "SELECT * FROM users",
    conn
)

conn.close()

# BMI Distribution

plt.figure(figsize=(8,5))

df["bmi"].hist(bins=20)

plt.title("BMI Distribution")

plt.xlabel("BMI")

plt.ylabel("Count")

plt.savefig("static/bmi_chart.png")

plt.close()

# Calories Distribution

plt.figure(figsize=(8,5))

df["calories"].hist(bins=20)

plt.title("Calories Burned")

plt.savefig("static/calories_chart.png")

plt.close()

# Goal Distribution

goal_counts = df["goal"].value_counts()

plt.figure(figsize=(6,6))

goal_counts.plot(kind="pie", autopct="%1.1f%%")

plt.ylabel("")

plt.savefig("static/goals_chart.png")

plt.close()

# Age vs Calories

plt.figure(figsize=(8,5))

plt.scatter(

    df["age"],
    df["calories"]

)

plt.xlabel("Age")

plt.ylabel("Calories")

plt.title("Age vs Calories")

plt.savefig("static/scatter_chart.png")

plt.close()

print("Charts Generated")