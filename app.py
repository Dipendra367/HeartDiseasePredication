import streamlit as st
import numpy as np
import pickle

# Load model and scaler
model = pickle.load(open("xgb_model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))

# Page setup
st.set_page_config(page_title="Heart Disease Predictor", layout="wide")

# ---- HEADER ----
st.markdown(
    "<h1 style='text-align: center; color: red;'>🫀 Heart Disease Risk Prediction</h1>",
    unsafe_allow_html=True
)
st.markdown("<h5 style='text-align: center;'>Mini Project – 6th Semester, Pokhara University</h5>", unsafe_allow_html=True)

# ---- ABOUT SECTION ----
with st.expander("ℹ️ About This Project"):
    st.markdown("""
This application uses a machine learning model (XGBoost + SMOTE) to predict the risk of heart disease based on user-inputted health indicators.  
The model was trained using real data from the WHO STEPS 2019 Survey (Nepal), focusing on features like cholesterol, triglycerides, BMI, diabetes, and lifestyle factors.  
This is a demo and not meant to replace clinical diagnostics.
""")

# ---- INPUT FORM ----
st.markdown("### 📋 Enter Patient Health Information")

with st.form("prediction_form"):
    col1, col2 = st.columns(2)

    with col1:
        age = st.slider("Age (years)", 10, 100, 40)
        sex = st.radio("Biological Sex", ["Male", "Female"])
        cholesterol = st.number_input("Total Cholesterol (mg/dL)", 100.0, 600.0, step=1.0)
        triglycerides = st.number_input("Triglycerides (mg/dL)", 50.0, 700.0, step=1.0)
        hdl = st.number_input("HDL Cholesterol (mg/dL)", 20.0, 100.0, step=1.0)

    with col2:
        diabetes = st.selectbox("Has Diabetes?", ["No", "Yes"])
        salt = st.slider("Salt Intake (g/day)", 0.0, 30.0, 10.0)
        smoking = st.slider("Cigarettes/Day", 0, 60, 0)
        inactivity = st.slider("Physical Inactivity (hrs/day)", 0.0, 24.0, 1.0)
        weight = st.number_input("Weight (kg)", 30.0, 150.0, 60.0)
        height = st.number_input("Height (cm)", 100.0, 220.0, 165.0)
        bmi = round(weight / ((height / 100) ** 2), 2)
        st.markdown(f"**📏 Calculated BMI:** `{bmi}`")

    submitted = st.form_submit_button("🩺 Predict Risk")

# ---- PREDICTION ----
if submitted:
    sex_encoded = 1 if sex == "Male" else 0
    diabetes_encoded = 1 if diabetes == "Yes" else 0

    input_data = np.array([[age, sex_encoded, cholesterol, triglycerides, hdl,
                            diabetes_encoded, salt, smoking, inactivity, bmi]])
    input_scaled = scaler.transform(input_data)
    prediction = model.predict(input_scaled)[0]
    proba = model.predict_proba(input_scaled)[0][1]

    st.markdown("---")
    if prediction == 1:
        st.error(f"⚠️ High Risk of Heart Disease Detected! (Probability: {proba:.2f})")
    else:
        st.success(f"✅ No Significant Risk Detected (Probability: {proba:.2f})")

# ---- HEALTH REFERENCES ----
st.markdown("---")
st.subheader("📚 Health Reference Ranges")

col1, col2 = st.columns(2)
with col1:
    with st.expander("🧪 Total Cholesterol"):
        st.markdown("""
- **Normal:** Less than 200 mg/dL  
- **Borderline High:** 200–239 mg/dL  
- **High:** 240 mg/dL and above  
> ⚠️ High cholesterol increases artery blockage risk.
""")

    with st.expander("💧 Triglycerides"):
        st.markdown("""
- **Normal:** Less than 150 mg/dL  
- **Borderline High:** 150–199 mg/dL  
- **High:** 200–499 mg/dL  
- **Very High:** 500+ mg/dL  
> ⚠️ High levels linked to heart disease & diabetes.
""")

with col2:
    with st.expander("💓 HDL (Good Cholesterol)"):
        st.markdown("""
- **Low Risky:**  
  - Men: < 40 mg/dL  
  - Women: < 50 mg/dL  
- **Ideal:** 60+ mg/dL  
> 🛡️ HDL removes bad cholesterol.
""")

    with st.expander("⚖️ BMI"):
        st.markdown(f"""
- **Underweight:** < 18.5  
- **Normal:** 18.5 – 24.9  
- **Overweight:** 25 – 29.9  
- **Obese:** ≥ 30  
> BMI is a health indicator based on weight and height.
**Your BMI:** `{bmi}`
""")

# ---- FOOTER ----
st.markdown("---")
st.markdown("### 👨‍💻 Team Members and Roles")
st.markdown("""
- **Aayush Thapa** – Data Handling & Preprocessing  
- **Dipendra Thapa** – Model Evaluation & Streamlit  
- **Narayan Adhikari** – Exploratory Data Analysis  
- **Rajeeb Kumar Singh** – Model Training & Feature Selection  
""")

st.markdown("---")
st.caption("📦 Model: XGBoost + SMOTE | 📊 Dataset: WHO STEPS Nepal 2019 | 🎓 Pokhara University – 6th Semester Project")
