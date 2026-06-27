import streamlit as st
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import matplotlib.pyplot as plt

st.set_page_config(page_title="Crop Recommendation System", layout="centered")

@st.cache_data
def load_data():
    return pd.read_csv("Crop_recommendation.csv")

@st.cache_resource
def train_model():
    df = load_data()
    X = df.drop("label", axis=1)
    y = df["label"]
    model = RandomForestClassifier(random_state=42)
    model.fit(X, y)
    return model, df

model, df = train_model()

st.title("Crop Recommendation System")
st.markdown("Predict the best crop to grow based on soil nutrient contents.")

with st.form("input_form"):
    col1, col2 = st.columns(2)
    with col1:
        N = st.number_input("Nitrogen (N)", min_value=0.0, step=1.0)
        P = st.number_input("Phosphorus (P)", min_value=0.0, step=1.0)
        K = st.number_input("Potassium (K)", min_value=0.0, step=1.0)
        temp = st.number_input("Temperature (°C)", step=0.1)
    with col2:
        humidity = st.number_input("Humidity (%)", step=0.1)
        ph = st.number_input("pH", step=0.1)
        rainfall = st.number_input("Rainfall (mm)", step=0.1)
    submitted = st.form_submit_button("Predict Crop", type="primary")

if submitted:
    sample = [[N, P, K, temp, humidity, ph, rainfall]]
    result = model.predict(sample)[0]
    st.success(f"Recommended Crop: **{result}**")

st.markdown("---")
st.subheader("Dataset Overview")

if st.checkbox("Show sample distribution"):
    crop_counts = df["label"].value_counts()
    fig, ax = plt.subplots(figsize=(10, 5))
    crop_counts.plot(kind="bar", ax=ax)
    ax.set_title("Number of Samples per Crop")
    ax.set_xlabel("Crop")
    ax.set_ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)
