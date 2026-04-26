import streamlit as st
import pandas as pd
import random

#Load kaggle dataset 
st.set_page_config(layout="wide")
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
st.sidebar.image("https://images.pexels.com/photos/7462811/pexels-photo-7462811.jpeg",width=500)
header=st.sidebar.subheader("YOU PROFILE")
age = st.sidebar.slider("Age", min_value=10, max_value=100, value=25)
gender = st.sidebar.selectbox("Gender", ["Male", "Female"])
weight = st.sidebar.slider("Weight (kg)", 30, 150, 50)
height = st.sidebar.slider("Height (cm)", 100, 200, 170)
activity = st.sidebar.selectbox("Activity Level", ["Sedentary", "Light", "Moderate" , "Active"])
goal = st.sidebar.selectbox("Goal", ["Weight Loss", "Maintain", "Weight Gain"])
if st.sidebar.button("Generate Plan"):
    st.sidebar.success("Plan Ready!")
    st.sidebar.balloons()
with st.sidebar.expander("ABOUT PROJECT"):
    st.write("""
We are a team of students working on a mini project focused on building a smart and user-friendly nutrition tool. Our application, the Macro Calculator and Indian Food Suggester, is designed to help users understand their daily nutritional needs and make better food choices based on Indian cuisine.

This project combines health awareness with simple technology, making it easier for users to calculate their daily calorie requirements and get suitable food recommendations.
    """)
with st.sidebar.expander("ABOUT THE TEAM"):
    st.write("""
Team Contributions:

             
Aditi Lakhe – Development and core functionality
             
Tanishka Bodke – User Interface design and layout
             
Arpita Hande – Documentation
             
Gargee Bhatkhande – Documentation and User Interface 

""")
with st.sidebar.expander("GOAL OF THE PROJECT"):
    st.write("""To create an accessible and practical tool that promotes healthier eating habits in a simple and intuitive way.

This mini project reflects our collaborative effort, where each member contributed their skills to build a complete and meaningful application.
""")
st.sidebar.image("https://images.pexels.com/photos/33143861/pexels-photo-33143861.jpeg", width=500)


#Macro Calculation Logic
def calculate_macros(weight, height, age, gender, goal):
    # Calculate BMR
    if gender == "Male":
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    
    # TDEE Calculation activity level
    if activity == "Sedentary":
        tdee = bmr * 1.2
    elif activity == "Light":
        tdee = bmr * 1.375
    elif activity == "Moderate":
        tdee = bmr * 1.55
    else:
        tdee = bmr * 1.725
        
    # Standard Macro Split: 50% Carbs, 25% Protein, 25% Fat
    carbs = (tdee * 0.5) / 4
    protein = (tdee * 0.25) / 4
    fats = (tdee * 0.25) / 9
    
    return round(tdee ,2), round(carbs,2), round(protein,2), round(fats,2)

calories, carbs, protein, fats = calculate_macros(weight, height, age, gender, goal)

#Display Results
st.title("MACROS CALCULATOR AND INDIAN FOOD SUGGESTER")
st.subheader(f"YOUR DAILY TARGET::{calories}KCAL")
#st.write(f"### Your Daily Target: **{calories} kcal**")
col1, col2, col3 = st.columns(3)
col1.metric("Carbs", f"{carbs}g")
col2.metric("Protein", f"{protein}g")
col3.metric("Fats", f"{fats}g")
col4,col5,col6=st.columns(3)
with col4:
    st.image("https://images.pexels.com/photos/37199356/pexels-photo-37199356.jpeg",width=700)
with col5:
    st.image("https://images.pexels.com/photos/7646673/pexels-photo-7646673.jpeg",width=700)
with col6:
    st.image("https://images.pexels.com/photos/19964370/pexels-photo-19964370.jpeg",width=700)

# Food Recommendation Logic
st.divider()
st.subheader(" Recommended Indian Dishes for You")
st.write("Based on your protein and calorie needs:")



if goal == "Weight Loss":
    calorie_target = calories - 500
elif goal == "Weight Gain":
    calorie_target = calories + 500
else:
    calorie_target = calories

recommendations = []
calorie_count = calorie_target

# Shuffle dataset once instead of random each time
df_shuffled = df.sample(frac=1).reset_index(drop=True)

for _, dish in df_shuffled.iterrows():
    if dish['Calories'] <= calorie_count:
        recommendations.append(dish)
        calorie_count -= dish['Calories']
    
    if calorie_count <= 0:
        break

# Convert list → DataFrame
recommendations_df = pd.DataFrame(recommendations)

# Display
st.dataframe(recommendations_df[['Dish', 'Calories', 'Protein', 'Carbs', 'Fats']].head(10))