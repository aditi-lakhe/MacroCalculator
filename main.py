import streamlit as st
import pandas as pd

#Load kaggle dataset 
@st.cache_data
def Load_Data():
    df=pd.read_csv("Indian_Food_Nutrition_Processed.csv")

    df=df.rename(columns={
        df.columns[0]: 'Dish',
        df.columns[1]: 'Calories',
        df.columns[2]: 'Carbs',
        df.columns[3]: 'Protein',
        df.columns[4]: 'Fats'
    })

    cols_to_fix = ['Calories', 'Carbs', 'Protein', 'Fats']
    for col in cols_to_fix:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
    return df

df=Load_Data()

# User_Inputs
st.sidebar.header("👤 Your Profile")
age = st.sidebar.slider("Age", min_value=10, max_value=100, value=25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
weight = st.sidebar.slider("Weight (kg)", 30, 200, 70)
height = st.sidebar.slider("Height (cm)", 100, 250, 170)
goal = st.sidebar.selectbox("Goal", ["Weight Loss", "Maintain", "Weight Gain"])

#Macro Calculation Logic
def calculate_macros(weight, height, age, gender, goal):
    # Calculate BMR
    if gender == "Male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161
    
    # TDEE Calculation based on goal
    if goal == "Weight Loss":
        tdee = bmr * 1.2 - 500
    elif goal == "Weight Gain":
        tdee = bmr * 1.2 + 500
    else:
        tdee = bmr * 1.2
        
    # Standard Macro Split: 50% Carbs, 25% Protein, 25% Fat
    carbs = (tdee * 0.5) / 4
    protein = (tdee * 0.25) / 4
    fats = (tdee * 0.25) / 9
    
    return round(tdee ,3), round(carbs,3), round(protein,3), round(fats,3) ,weight

calories, carbs, protein, fats = calculate_macros(weight, height, age, gender, goal)

#Display Results
st.title("🥗Macro Calculator and Indian Food Suggester")
st.write(f"### Your Daily Target: **{calories} kcal**")

col1, col2, col3 = st.columns(3)
col1.metric("Carbs", f"{carbs}g")
col2.metric("Protein", f"{protein}g")
col3.metric("Fats", f"{fats}g")

# Food Recommendation Logic
st.divider()
st.subheader("🍲 Recommended Indian Dishes for You")
st.write("Based on your protein and calorie needs:")

# Filter dishes that are within a reasonable range per 100g
# High protein filter for those gaining weight, low calorie for loss


if goal == "Weight Loss":
    recommendations = df[(df['Calories'] <= calories-400) & (df['Calories']>40) & (df['Protein']==1.4*weight)].sort_values(by='Protein', ascending=False)

elif goal == "Weight Gain":
    recommendations = df[(df['Calories'] <= calories+400) & (df['Calories']>40) & (df['Protein']==2.2*weight)].sort_values(by='Protein', ascending=False)

else:
    recommendations = df[(df['Calories'] <= calories) & (df['Calories']>40) & (df['Protein']==1.4*weight)].sort_values(by='Protein', ascending=False)

# Display top 10 matches
st.dataframe(recommendations[['Dish(per 100 gm)', 'Calories', 'Protein', 'Carbs', 'Fats']].head(10))

