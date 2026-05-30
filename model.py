import pandas as pd

from sklearn.model_selection import train_test_split

from sklearn.linear_model import LinearRegression

from sklearn.metrics import mean_absolute_error

from sklearn.metrics import r2_score

# =========================
# LOAD DATASETS
# =========================

exercise_df = pd.read_csv(
    'dataset/exercise.csv'
)

calories_df = pd.read_csv(
    'dataset/calories.csv'
)

# =========================
# MERGE DATASETS
# =========================

df = exercise_df.merge(

    calories_df,

    on='User_ID'

)

print()

print("Merged Dataset")

print(df.head())

# =========================
# ENCODE GENDER
# =========================

df['Gender'] = df['Gender'].map({

    'male': 0,
    'female': 1

})

# =========================
# FEATURES
# =========================

X = df[[

    'Gender',
    'Age',
    'Height',
    'Weight',
    'Duration',
    'Heart_Rate',
    'Body_Temp'

]]

# =========================
# TARGET
# =========================

y = df['Calories']

# =========================
# TRAIN TEST SPLIT
# =========================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42

)

# =========================
# MODEL
# =========================

model = LinearRegression()

# =========================
# TRAIN MODEL
# =========================

model.fit(

    X_train,
    y_train

)

# =========================
# PREDICTIONS
# =========================

predictions = model.predict(

    X_test

)

# =========================
# EVALUATION
# =========================

mae = mean_absolute_error(

    y_test,
    predictions

)

r2 = r2_score(

    y_test,
    predictions

)

print()

print("MODEL TRAINED SUCCESSFULLY")

print()

print("Mean Absolute Error:")
print(mae)

print()

print("R2 Score:")
print(r2)

# =========================
# SAMPLE PREDICTION
# =========================

sample = [[

    0,      # male
    25,     # age
    175,    # height
    70,     # weight
    30,     # duration
    95,     # heart rate
    40      # body temp

]]

prediction = model.predict(sample)

print()

print("Predicted Calories Burned:")

print(int(prediction[0]))