import tkinter as tk
from tkinter import ttk, scrolledtext
from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression
import random

# Simulated historical temperature data (days vs. temperature)
days = np.array([1, 2, 3, 4, 5, 6, 7]).reshape(-1, 1)
temps = np.array([30, 32, 31, 33, 35, 34, 36])

# Train regression model
model = LinearRegression()
model.fit(days, temps)

# Casual follow-up prompts
follow_ups = [
    "Want to see the forecast for next weekend?",
    "Should I show a weekly trend?",
    "Curious how this prediction works?",
    "Want to compare with another city?",
    "Need a weather joke to lighten the mood?",
    "Should I plot this trend next?",
    "Want to know the coldest day in the dataset?",
    "Feeling the heat or craving the chill?"
]

# UI setup
root = tk.Tk()
root.title("Frost ❄️")
root.geometry("500x600")
root.configure(bg="#1e1e2f")

style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", foreground="#ffffff", background="#3e3e5e", font=("Helvetica", 10, "bold"))
style.configure("TLabel", foreground="#ffffff", background="#1e1e2f", font=("Helvetica", 12))
style.configure("TEntry", fieldbackground="#2e2e3f", foreground="#ffffff")

# Chat display
chat_display = scrolledtext.ScrolledText(root, wrap=tk.WORD, bg="#2e2e3f", fg="#ffffff", font=("Helvetica", 11))
chat_display.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
chat_display.config(state=tk.DISABLED)

# Input field
user_input = tk.Entry(root, font=("Helvetica", 12), bg="#3e3e5e", fg="#ffffff", insertbackground="#ffffff")
user_input.pack(padx=10, pady=10, fill=tk.X)

def date_to_day_offset(date_str):
    try:
        input_date = datetime.strptime(date_str.strip(), "%Y-%m-%d")
        today = datetime.today()
        delta = (input_date - today).days
        return delta + 8  # Assuming day 8 is tomorrow
    except ValueError:
        return None

def predict_temperature_from_date(date_str):
    offset = date_to_day_offset(date_str)
    if offset is None or offset < 1:
        return "⚠️ Please enter a valid future date in YYYY-MM-DD format."
    prediction = model.predict(np.array([[offset]]))[0]
    follow_up = random.choice(follow_ups)
    return f"📅 Forecast for {date_str}:\n🌡️ Predicted temperature: {prediction:.1f}°C\n💬 {follow_up}"

def send_message(event=None):
    msg = user_input.get()
    if msg:
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"🧑 You: {msg}\n")
        response = predict_temperature_from_date(msg)
        chat_display.insert(tk.END, f"🤖 Frost: {response}\n\n")
        chat_display.config(state=tk.DISABLED)
        chat_display.yview(tk.END)  # Auto-scroll
        user_input.delete(0, tk.END)

# Bind Enter key
user_input.bind("<Return>", send_message)

root.mainloop()