import tkinter as tk
from tkinter import font
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
import string
import random

nltk.download('stopwords')

# FAQ data
faq_data = {
    "What is your return policy?": "You can return any item within 30 days of purchase.",
    "How do I track my order?": "Use the tracking link sent to your email after shipping.",
    "Do you offer international shipping?": "Yes, we ship to over 50 countries worldwide.",
    "What payment methods do you accept?": "We accept credit cards, PayPal, and UPI.",
    "What is your name?": "My name is Chatbot AI.",
    "How are you?": "I'm functioning perfectly, thanks for asking!",
    "What can you do?": "I can answer your questions and help you explore our services.",
    "Where are you from?": "I live in the cloud, always ready to assist!"
}

# Contextual follow-up mapping
follow_up_map = {
    "What is your return policy?": ["Need help starting a return?", "Want to know about refunds?"],
    "How do I track my order?": ["Didn't receive a tracking link?", "Want to check delivery time?"],
    "Do you offer international shipping?": ["Which country are you shipping to?", "Need customs info?"],
    "What payment methods do you accept?": ["Having trouble with payment?", "Want to add a new method?"],
    "What is your name?": ["Want to know what I can do?", "Curious how I was built?"],
    "How are you?": ["Want to know my capabilities?", "Need help with something?"],
    "What can you do?": ["Want to explore services?", "Need help navigating the site?"],
    "Where are you from?": ["Want to know how I work?", "Curious about cloud tech?"]
}

# Preprocessing
def preprocess(text):
    stop_words = set(stopwords.words('english'))
    text = text.lower()
    text = ''.join([c for c in text if c not in string.punctuation])
    tokens = text.split()
    tokens = [word for word in tokens if word not in stop_words]
    return ' '.join(tokens)

questions = list(faq_data.keys())
answers = list(faq_data.values())
processed_questions = [preprocess(q) for q in questions]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(processed_questions)

def get_answer(user_input):
    user_input_processed = preprocess(user_input)
    user_vec = vectorizer.transform([user_input_processed])
    similarity = cosine_similarity(user_vec, X)
    best_match = similarity.argmax()
    return answers[best_match], questions[best_match]

# GUI setup
root = tk.Tk()
root.title("Chatbot AI 💬")
root.geometry("650x600")
root.configure(bg="#1c1c1c")

# Fonts
title_font = font.Font(family="Segoe UI", size=18, weight="bold")
chat_font = font.Font(family="Segoe UI", size=12)
entry_font = font.Font(family="Segoe UI", size=12)

# Header
header = tk.Label(root, text="Chatbot AI 🤖", bg="#1c1c1c", fg="#a3c47c", font=title_font)
header.pack(pady=10)

# Chat log frame
chat_frame = tk.Frame(root, bg="#1c1c1c")
chat_scrollbar = tk.Scrollbar(chat_frame)
chat_log = tk.Text(chat_frame, height=20, width=80, font=chat_font, bg="#2a2a2a", fg="#e0e0e0", yscrollcommand=chat_scrollbar.set, wrap=tk.WORD, bd=0, padx=10, pady=10)
chat_scrollbar.config(command=chat_log.yview)
chat_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
chat_log.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
chat_frame.pack(padx=10, pady=10)

# Entry and button
entry_frame = tk.Frame(root, bg="#1c1c1c")
entry = tk.Entry(entry_frame, width=50, font=entry_font, bg="#3a3a3a", fg="#ffffff", bd=0, relief=tk.FLAT)
entry.insert(0, "Ask me anything...")
entry.bind("<FocusIn>", lambda e: entry.delete(0, tk.END))
entry.pack(side=tk.LEFT, padx=10, pady=10, ipady=6)

send_button = tk.Button(entry_frame, text="➤", command=lambda: send_message(), bg="#a3c47c", fg="#1c1c1c", font=("Segoe UI", 14, "bold"), padx=12, pady=6, bd=0, relief=tk.FLAT, activebackground="#b8d68c")
send_button.pack(side=tk.LEFT, padx=5)
entry_frame.pack()

# Helper to show follow-up in oval bubble
def show_follow_up(text):
    bubble_canvas = tk.Canvas(chat_frame, width=500, height=50, bg="#1c1c1c", highlightthickness=0)
    bubble_canvas.pack(pady=5)
    bubble_canvas.create_oval(10, 10, 490, 40, fill="#a3c47c", outline="#a3c47c")
    bubble_canvas.create_text(250, 25, text=text, fill="#1c1c1c", font=("Segoe UI", 11, "bold"))

# Message handler
def send_message():
    user_input = entry.get().strip()
    if user_input == "":
        return
    chat_log.insert(tk.END, "🧑 You: " + user_input + "\n", "user")
    response, matched_question = get_answer(user_input)
    chat_log.insert(tk.END, "🤖 Chatbot AI: " + response + "\n", "bot")

    # Get relevant follow-up
    follow_ups = follow_up_map.get(matched_question, ["Can I assist you further?"])
    follow_up = random.choice(follow_ups)
    show_follow_up(follow_up)

    chat_log.insert(tk.END, "\n", "bot")
    chat_log.see(tk.END)
    entry.delete(0, tk.END)

# Tag styles
chat_log.tag_config("user", foreground="#ffffff", font=chat_font)
chat_log.tag_config("bot", foreground="#a3c47c", font=chat_font)

root.mainloop()


