import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import random

# Expanded movie data
movies = {
    "Action": ["Mad Max: Fury Road 🔥", "John Wick 💥", "The Dark Knight 🦇"],
    "Romance": ["La La Land 🎶", "Pride & Prejudice 💕", "The Notebook 😢"],
    "Sci-Fi": ["Interstellar 🌌", "Inception 🌀", "The Matrix 🧠"],
    "Comedy": ["Superbad 😂", "The Grand Budapest Hotel 🏨", "Bridesmaids 💐"],
    "Thriller": ["Gone Girl 🕵️‍♀️", "Shutter Island 🧩", "Parasite 🐛"],
    "Horror": ["Hereditary 👹", "The Conjuring 👻", "Get Out 🚪"],
    "Fantasy": ["Harry Potter 🧙", "Pan's Labyrinth 🐉", "The Hobbit 🏔️"],
    "Drama": ["The Shawshank Redemption 🧱", "Forrest Gump 🏃", "Moonlight 🌙"],
    "Documentary": ["13th 📚", "Free Solo 🧗", "My Octopus Teacher 🐙"]
}

# Casual follow-up questions
follow_ups = [
    "Want another creepy pick from this genre?",
    "Feeling brave enough to try a horror next?",
    "Should I throw in a surprise recommendation?",
    "Would you like to rate this one?",
    "Want something light-hearted instead?",
    "Need a tearjerker or a thriller?",
    "Should I go deeper into this genre?",
    "Want to explore something totally different?"
]

# UI setup
root = tk.Tk()
root.title("Creepy Me 👻")
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

def recommend_movie(genre):
    genre = genre.strip().capitalize()
    if genre in movies:
        rec = random.choice(movies[genre])
        follow_up = random.choice(follow_ups)
        return f"🎬 I recommend: {rec}\n💬 {follow_up}"
    else:
        return "😕 I don't know that genre. Try Action, Romance, Sci-Fi, Comedy, Thriller, Horror, Fantasy, Drama, or Documentary!"

def send_message(event=None):
    msg = user_input.get()
    if msg:
        chat_display.config(state=tk.NORMAL)
        chat_display.insert(tk.END, f"🧑 You: {msg}\n")
        response = recommend_movie(msg)
        chat_display.insert(tk.END, f"🤖 Creepy Me: {response}\n\n")
        chat_display.config(state=tk.DISABLED)
        chat_display.yview(tk.END)  # Auto-scroll
        user_input.delete(0, tk.END)

# Bind Enter key
user_input.bind("<Return>", send_message)

root.mainloop()