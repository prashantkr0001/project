# -*- coding: utf-8 -*-
"""
Created on Tue Jun  9 00:46:36 2026

@author: pkuma
"""

import tkinter as tk
from tkinter import messagebox
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

# Load dataset
df = pd.read_csv("Crop_recommendation.csv")

X = df.drop("label", axis=1)
y = df["label"]

# Train model
model = RandomForestClassifier(random_state=42)
model.fit(X, y)

# Prediction function
def predict_crop():
    try:
        N = float(entry_N.get())
        P = float(entry_P.get())
        K = float(entry_K.get())
        temp = float(entry_temp.get())
        humidity = float(entry_humidity.get())
        ph = float(entry_ph.get())
        rainfall = float(entry_rainfall.get())

        sample = [[N, P, K, temp, humidity, ph, rainfall]]
        result = model.predict(sample)

        result_label.config(text=f"Recommended Crop: {result[0]}")

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric values.")




# GUI Window
root = tk.Tk()
root.title("Crop Recommendation System(by Soil Nutrition Contents)")
root.geometry("400x500")

# Labels and Entry Fields
tk.Label(root, text="Nitrogen").pack()
entry_N = tk.Entry(root)
entry_N.pack()

tk.Label(root, text="Phosphorus").pack()
entry_P = tk.Entry(root)
entry_P.pack()

tk.Label(root, text="Potassium").pack()
entry_K = tk.Entry(root)
entry_K.pack()

tk.Label(root, text="Temperature").pack()
entry_temp = tk.Entry(root)
entry_temp.pack()

tk.Label(root, text="Humidity").pack()
entry_humidity = tk.Entry(root)
entry_humidity.pack()

tk.Label(root, text="pH").pack()
entry_ph = tk.Entry(root)
entry_ph.pack()

tk.Label(root, text="Rainfall").pack()
entry_rainfall = tk.Entry(root)
entry_rainfall.pack()

# Predict Button
tk.Button(root, text="Predict Crop", command=predict_crop).pack(pady=10)

# Result Label
result_label = tk.Label(root, text="", font=("Arial", 12, "bold"))
result_label.pack(pady=10)

root.mainloop()

import matplotlib.pyplot as plt

def show_plot():
    crop_counts = df['label'].value_counts()

    plt.figure(figsize=(10, 5))
    crop_counts.plot(kind='bar')
    plt.title("Number of Samples per Crop")
    plt.xlabel("Crop")
    plt.ylabel("Count")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

tk.Button(root, text="Show Dataset Plot", command=show_plot).pack(pady=10)