import streamlit as st
import pandas as pd
import pickle
import sklearn 

st.title("DIAGUIDE ~ Diabetes Prediction App")

st.write("This app predicts the likelihood of diabetes based on user input data. Please fill in the form below to get started.")

try:
    with open("models/logistic_regression_model.pkl", "rb") as f:
        model, preprocessor = pickle.load(f)
except FileNotFoundError:
    print("Model file not found. Please ensure the model is trained and saved correctly.")
    st.error("Model file not found. Please ensure the model is trained and saved correctly.")
    st.stop()
except Exception as e:
    print(f"An error occurred while loading the model: {e}")
    st.error(f"An error occurred while loading the model: {e}")
    st.stop()

questions = {
    "Age": (
        "Age Category",
        "18-24",
        "25-29",
        "30-34",
        "35-39",
        "40-44",
        "45-49",
        "50-54",
        "55-59",
        "60-64",
        "65-69",
        "70-74",
        "75-79",
        "80 or older",
    ),
    "Sex" : ("Sex", "Female", "Male"),
    "HighChol": ("High Cholesterol", "High", "Low"),  # Changed default to "No"
    "CholCheck": ("Cholesterol Check in 5 Years", "Yes", "No"),  # Changed default to "Yes"
    "Mass": ("Mass (pounds)", 100, 300, 150),
    "Height": ("Height (inches)", 60, 80, 65),
    "Smoker": ("Smoked at least 5 packs (100 cigarets) in your life", "Yes", "No"),  # Changed default to "No"
    "Stroke": ("Ever Had a Stroke", "Yes", "No"),  # Changed default to "No"
    "HeartDiseaseorAttack": ("Ever Had Heart Disease or Heart Attack", "Yes", "No"),  # Changed default to "No"
    "PhysActivity": ("Physical Activity", "Yes", "No"),  # Changed default to "Yes"
    "Fruits": ("Consume Fruits 1 or more times per day", "Yes", "No"),  # Changed default to "Yes"
    "Veggies": ("Consume Vegetables 1 or more times per day", "Yes", "No"),  # Changed default to "Yes"
    "HvyAlcoholConsump": ("Heavy Alcohol Consumption", "Yes", "No"),  # Changed default to "No"
    "AnyHealthcare": ("Any Healthcare Coverage", "Yes", "No"),  # Changed default to "Yes"
    "GenHlth": (
        "How Would You Rate Your General Health",
        "Excellent",  
        "Very Good",
        "Good",
        "Fair",
        "Poor",
    ),
    "MentHlth": ("Number of days with bad mental health in past 30 days", 0, 30, 0),
    "PhysHlth": ("Number of days with bad physical health in past 30 days", 0, 30, 0),
    "DiffWalk": ("Difficulty Walking", "Yes", "No"),
    # "Education": (
    #     "Education Level",
    #     "Never attended school",
    #     "Elementary",
    #     "High school graduate",
    #     "Some high school",
    #     "College graduate",
    #     "Some college",
    # ),
    # "Income": (
    #     "Income Level (yearly income in USD)",
    #     "<=$10,000",
    #     "$10,000-$15,000",
    #     "$15,000-$20,000",
    #     "$20,000-$25,000",
    #     "$25,000-$35,000",
    #     "$35,000-$50,000",
    #     "$50,000-$75,000",
    #     ">=$75,000",
    # ),
    "HighBP": ("High Blood Pressure", "Yes", "No"),
    "NoDocbcCost": ("Was there a time in the past 12 months when you needed to see a doctor but could not because of cost?", "Yes", "No")

}

def show_question():
    key = list(questions.keys())[st.session_state.current_question]
    
    st.subheader(questions[key][0])
    
    if key in ["Mass", "Height", "MentHlth", "PhysHlth"]:
        user_input = st.slider("", questions[key][1], questions[key][2], questions[key][3], key=key)
    elif key in ["GenHlth", "Education", "Income", "Age"]:
        user_input = st.selectbox("", options=questions[key][1:], index=0, key=key)
    elif key in ["HighChol", "CholCheck", "Smoker", "Stroke", "HeartDiseaseorAttack", "PhysActivity", "Fruits", "Veggies", "HvyAlcoholConsump", "AnyHealthcare", "DiffWalk"]:
        user_input = st.radio("", options=[questions[key][1], questions[key][2]], index=0, key=key)
    else:
        user_input = st.radio("", options=[questions[key][1], questions[key][2]], index=0, key=key)
    
    st.session_state.user_inputs[key] = user_input
    
    if st.button("Next", key=questions[key][0]+ "button"):
        st.session_state.current_question += 1
        if st.session_state.current_question < len(questions):
            show_question()
        else:
            st.session_state.current_question = 0
            st.success("Thank you for your input!")
            st.session_state.submit_button_pressed = True
            st.balloons()
            
if "user_inputs" not in st.session_state:
    st.session_state.user_inputs = {}
if "current_question" not in st.session_state:
    st.session_state.current_question = 0
if "submit_button_pressed" not in st.session_state:
    st.session_state.submit_button_pressed = False
if "risk_calculated" not in st.session_state:
    st.session_state.risk_calculated = False

if st.session_state.current_question < len(questions):
    show_question()
    
if st.session_state.submit_button_pressed:
    # print(st.session_state.user_inputs)
    input_data = pd.DataFrame([st.session_state.user_inputs])
    st.write(input_data)
    # RADIO
    input_data["Sex"] = input_data["Sex"].map({"Female": 0, "Male": 1})
    input_data["HighChol"] = input_data["HighChol"].map({"High": 1, "Low": 0})
    input_data["CholCheck"] = input_data["CholCheck"].map({"Yes": 1, "No": 0})
    input_data["Smoker"] = input_data["Smoker"].map({"Yes": 1, "No": 0})
    input_data["Stroke"] = input_data["Stroke"].map({"Yes": 1, "No": 0})
    input_data["HeartDiseaseorAttack"] = input_data["HeartDiseaseorAttack"].map({"Yes": 1, "No": 0})
    input_data["PhysActivity"] = input_data["PhysActivity"].map({"Yes": 1, "No": 0})
    input_data["Fruits"] = input_data["Fruits"].map({"Yes": 1, "No": 0})
    input_data["Veggies"] = input_data["Veggies"].map({"Yes": 1, "No": 0})
    input_data["HvyAlcoholConsump"] = input_data["HvyAlcoholConsump"].map({"Yes": 1, "No": 0})
    input_data["AnyHealthcare"] = input_data["AnyHealthcare"].map({"Yes": 1, "No": 0})
    input_data["DiffWalk"] = input_data["DiffWalk"].map({"Yes": 1, "No": 0})
    # SELECT
    input_data["GenHlth"] = input_data["GenHlth"].map(
        {
            "Excellent": 1,
            "Very Good": 2,
            "Good": 3,
            "Fair": 4,
            "Poor": 5,
        }
    )
    # input_data["Education"] = input_data["Education"].map(
    #     {
    #         "Never attended school": 1,
    #         "Elementary": 2,
    #         "Some high school": 3,
    #         "High school graduate": 4,
    #         "Some college": 5,
    #         "College graduate": 6,
    #     }
    # )
    # input_data["Income"] = input_data["Income"].map(
    #     {
    #         " <=$10,000": 1,
    #         " $10,000-$15,000": 2,
    #         " $15,000-$20,000": 3,
    #         " $20,000-$25,000": 4,
    #         " $25,000-$35,000": 5,
    #         " $35,000-$50,000": 6,
    #         " $50,000-$75,000": 7,
    #         ">= $75,000": 8,
    #     }
    # )
    input_data["Age"] = input_data["Age"].map(
        {
            "18-24": 1,
            "25-29": 2,
            "30-34": 3,
            "35-39": 4,
            "40-44": 5,
            "45-49": 6,
            "50-54": 7,
            "55-59": 8,
            "60-64": 9,
            "65-69": 10,
            "70-74": 11,
            "75-79": 12,
            "80 or older": 13,
        }
    )
    # NUMERIC
    input_data["BMI"] = (input_data["Mass"]*0.45359237) / ((input_data["Height"] * 0.0254) ** 2)
    input_data.drop(columns=["Mass", "Height"])
    input_data["BMI"] = input_data["BMI"].round(2)
    
    input_data["MentHlth"] = input_data["MentHlth"].astype(int)
    input_data["PhysHlth"] = input_data["PhysHlth"].astype(int)
    
    try:
        processed_data = preprocessor.transform(input_data)
    except Exception as e:
        st.error(
            f"Error: An error occurred during preprocessing.  This may be due to the input data not matching the format the model expects.  Please check your answers. Error Details: {e}"
        )
        st.stop()
    
    try:
        prediction = model.predict_proba(processed_data)[:, 1]
        risk_per = prediction[0] * 100
        st.session_state.risk_calculated = True
    except Exception as e:
        st.error(
            f"Error: An error occurred during prediction.  This may be due to the input data not matching the format the model expects.  Please check your answers. Error Details: {e}"
        )
        st.stop()
    st.session_state.user_inputs = {}
    st.session_state.current_question = 0

if st.session_state.risk_calculated:
    st.subheader("Diabetes Risk Assessment Result")
    st.write(f"Your estimated risk of diabetes is: {risk_per:.2f}%")

    # Interpretation of risk
    if risk_per < 15:
        st.write("Based on your answers, your risk is low.")
    elif risk_per < 30:
        st.write("Based on your answers, your risk is moderate.")
    else:
        st.write(
            "Based on your answers, your risk is elevated. It is recommended to consult with a healthcare professional."
        )