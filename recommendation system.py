import tkinter as tk
from tkinter import ttk

# 🧠 Recommendation dataset
recommendations = {
    "action movie": ["🎬 Mad Max: Fury Road", "🦸 Avengers: Endgame", "🚗 Fast & Furious 9"],
    "romantic movie": ["💖 The Notebook", "🌹 Titanic", "🎥 La La Land"],
    "sci-fi movie": ["👽 Interstellar", "🚀 The Martian", "🧠 Inception"],
    "comedy movie": ["😂 Superbad", "🤣 The Hangover", "🎭 The Grand Budapest Hotel"],
    "horror movie": ["👻 The Conjuring", "🩸 Hereditary", "🧟‍♂️ Train to Busan"],
    "animated movie": ["🐉 How to Train Your Dragon", "🦁 The Lion King", "🎨 Soul"],
    "self-help book": ["📖 Atomic Habits", "🧠 The Power of Now", "💡 Deep Work"],
    "fiction book": ["📚 The Alchemist", "🧙‍♂️ Harry Potter", "🕵️‍♂️ Sherlock Holmes"],
    "non-fiction book": ["📘 Sapiens", "💼 Shoe Dog", "🧬 The Gene"],
    "fantasy book": ["🐉 Eragon", "🧝‍♀️ Lord of the Rings", "🧙‍♂️ Mistborn"],
    "python course": ["🐍 Codecademy Python", "📘 Automate the Boring Stuff", "🎓 Coursera Python for Everybody"],
    "machine learning course": ["🤖 Andrew Ng ML", "📊 Fast.ai", "🧠 Kaggle Learn"],
    "smartphone": ["📱 iPhone 14", "📱 Samsung Galaxy S23", "📱 Google Pixel 7"],
    "laptop": ["💻 MacBook Pro", "💻 Dell XPS 13", "💻 Lenovo ThinkPad"],
    "anime": ["🍜 Naruto", "🌀 Attack on Titan", "👊 Jujutsu Kaisen"],
    "dessert": ["🍰 Cheesecake", "🍪 Chocolate Chip Cookies", "🍫 Brownies"],
    "vegan meal": ["🥗 Buddha Bowl", "🌮 Jackfruit Tacos", "🍛 Lentil Curry"]
}

# 💡 Follow-up suggestions
follow_ups = {key: [f"Want more {key}s?", f"Looking for similar {key}s?"] for key in recommendations}

# 🎨 UI Setup
root = tk.Tk()
root.title("Recommender Genie 🧞")
root.geometry("540x640")
root.configure(bg="#121212")

chat_frame = tk.Frame(root, bg="#121212")
chat_frame.pack(padx=10, pady=10, fill="both", expand=True)

canvas = tk.Canvas(chat_frame, bg="#121212", highlightthickness=0)
scrollbar = ttk.Scrollbar(chat_frame, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, bg="#121212")

scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# 💬 Message handling
def send_query(event=None):
    user_text = entry.get().strip().lower()
    if user_text == "":
        return
    entry.delete(0, tk.END)
    add_message("🧑 You", user_text, "#1e88e5")
    root.after(500, lambda: show_recommendations(user_text))

def show_recommendations(query):
    matched = None
    for key in recommendations:
        if key in query:
            matched = key
            break
    if matched:
        recs = recommendations[matched]
        add_message("🧞 Genie", f"Here are some {matched} recommendations:", "#43a047")
        for item in recs:
            add_message("✨", item, "#2e7d32")
        if matched in follow_ups:
            suggest_label = tk.Label(scrollable_frame, text="💡 You could ask:", bg="#121212", fg="#aaaaaa",
                                     font=("Helvetica", 10), anchor="w", padx=10)
            suggest_label.pack(fill="x", padx=10, pady=(5,0))
            for s in follow_ups[matched]:
                btn = tk.Button(scrollable_frame, text=s, font=("Helvetica", 10),
                                bg="#37474f", fg="#ffffff", activebackground="#455a64",
                                relief="flat", cursor="hand2", command=lambda s=s: entry.insert(0, s))
                btn.pack(padx=20, pady=2, anchor="w")
    else:
        add_message("🧞 Genie", "Hmm... I don't have recommendations for that yet. Try asking about movies, books, or tech!", "#d81b60")

def add_message(sender, text, color):
    bubble = tk.Label(scrollable_frame, text=f"{sender}: {text}", wraplength=400,
                      justify="left", bg=color, fg="white", font=("Helvetica", 12),
                      padx=10, pady=8, anchor="w")
    bubble.pack(fill="x", pady=5, padx=10, anchor="w")

# 📝 Input field
entry = tk.Entry(root, font=("Helvetica", 14), bg="#212121", fg="#ffffff", insertbackground="#ffffff")
entry.pack(padx=10, pady=(0,10), fill="x")
entry.bind("<Return>", send_query)

# 🚀 Send button
send_btn = tk.Button(root, text="Get Recommendations", font=("Helvetica", 12, "bold"),
                     bg="#43a047", fg="white", activebackground="#388e3c",
                     padx=10, pady=5, command=send_query, cursor="hand2")
send_btn.pack(pady=(0,10))

# 🧠 Footer
footer = tk.Label(root, text="Recommender Genie 🧞 | Powered by Dia", font=("Helvetica", 9),
                  bg="#121212", fg="#777777")
footer.pack(side="bottom", pady=5)

root.mainloop()