import tkinter as tk
from tkinter import messagebox, scrolledtext
from deep_translator import GoogleTranslator
import speech_recognition as sr
import pyperclip
import pyttsx3

# Initialize translation history
translation_history = []
is_dark = True  # Start with dark theme

# Translation function
def translate_text():
    try:
        text = input_text.get("1.0", tk.END).strip()
        if not text:
            messagebox.showwarning("Warning", "Please enter some text")
            return

        src = source_lang.get()
        tgt = target_lang.get()

        if src == "Auto Detect":
            translated = GoogleTranslator(source='auto', target=tgt).translate(text)
        else:
            translated = GoogleTranslator(source=src, target=tgt).translate(text)

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated)

        translation_history.append((text, translated))
        update_history()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Speech recognition function
def speak_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        messagebox.showinfo("Speak", "Please speak now...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            input_text.insert(tk.END, text)
        except sr.UnknownValueError:
            messagebox.showerror("Error", "Sorry, could not understand audio")
        except sr.RequestError:
            messagebox.showerror("Error", "Speech recognition service error")

# Copy to clipboard
def copy_output():
    pyperclip.copy(output_text.get("1.0", tk.END).strip())
    messagebox.showinfo("Copied", "Translated text copied to clipboard!")

# Paste from clipboard
def paste_input():
    input_text.insert(tk.END, pyperclip.paste())

# Speak translated output
def speak_output():
    engine = pyttsx3.init()
    engine.say(output_text.get("1.0", tk.END).strip())
    engine.runAndWait()

# Update translation history
def update_history():
    history_box.delete("1.0", tk.END)
    for i, (src, tgt) in enumerate(translation_history[-5:], 1):
        history_box.insert(tk.END, f"{i}. {src[:30]}... → {tgt[:30]}...\n")

# Theme toggle
def toggle_theme():
    global is_dark
    is_dark = not is_dark
    bg = "#0F0F0F" if is_dark else "#F8FAF8"
    fg = "#F1F5F9" if is_dark else "#2F4F4F"
    accent = "#6B8E23"
    box_bg = "#1E1E1E" if is_dark else "#FFFFFF"

    root.config(bg=bg)
    title.config(bg=bg, fg=accent)
    frame_lang.config(bg=bg)
    frame_buttons.config(bg=bg)
    input_text.config(bg=box_bg, fg=fg)
    output_text.config(bg=box_bg, fg=fg)
    history_box.config(bg=box_bg, fg=fg)
    theme_btn.config(bg=accent, fg="white")
    speak_btn.config(bg=accent, fg="white")
    paste_btn.config(bg=accent, fg="white")
    translate_btn.config(bg=accent, fg="white")
    speak_output_btn.config(bg=accent, fg="white")
    copy_btn.config(bg=accent, fg="white")
    history_label.config(bg=bg, fg=accent)

# Languages
languages = GoogleTranslator().get_supported_languages()
languages_display = ["Auto Detect"] + languages

# UI Setup
root = tk.Tk()
root.title("Language Translator")
root.geometry("780x680")
root.config(bg="#0F0F0F")

# Title
title = tk.Label(root, text="🌿 Language Translator", font=("Segoe UI", 20, "bold"), bg="#0F0F0F", fg="#6B8E23")
title.pack(pady=15)

# Language selectors
frame_lang = tk.Frame(root, bg="#0F0F0F")
frame_lang.pack(pady=5)

source_lang = tk.StringVar(value="Auto Detect")
target_lang = tk.StringVar(value="english")

def styled_optionmenu(var, options):
    menu = tk.OptionMenu(frame_lang, var, *options)
    menu.config(bg="#1E1E1E", fg="#F1F5F9", font=("Segoe UI", 10), relief="flat", highlightthickness=0)
    menu["menu"].config(bg="#1E1E1E", fg="white")
    return menu

styled_optionmenu(source_lang, languages_display).grid(row=0, column=0, padx=10)
styled_optionmenu(target_lang, languages).grid(row=0, column=1, padx=10)

# Input box
input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=6, bg="#1E1E1E", fg="#F1F5F9", font=("Segoe UI", 12), relief="flat", borderwidth=5)
input_text.pack(pady=10)

# Buttons frame
frame_buttons = tk.Frame(root, bg="#0F0F0F")
frame_buttons.pack(pady=5)

def oval_button(master, text, command):
    return tk.Button(master, text=text, command=command, bg="#6B8E23", fg="white",
                     font=("Segoe UI", 10, "bold"), relief="flat", padx=20, pady=8,
                     bd=0, highlightthickness=0)

speak_btn = oval_button(frame_buttons, "🟢 Mic", speak_to_text)
speak_btn.grid(row=0, column=0, padx=5)

paste_btn = oval_button(frame_buttons, "🟩 Paste", paste_input)
paste_btn.grid(row=0, column=1, padx=5)

translate_btn = oval_button(frame_buttons, "➡ Translate", translate_text)
translate_btn.grid(row=0, column=2, padx=5)

# Output box
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=6, bg="#1E1E1E", fg="#F1F5F9", font=("Segoe UI", 12), relief="flat", borderwidth=5)
output_text.pack(pady=10)

# Copy and Speak Output
copy_btn = oval_button(root, "🟩 Copy", copy_output)
copy_btn.pack(pady=5)

speak_output_btn = oval_button(root, "🟢 Speak", speak_output)
speak_output_btn.pack(pady=5)

# Translation History
history_label = tk.Label(root, text="🕘 Translation History", font=("Segoe UI", 10, "bold"), bg="#0F0F0F", fg="#6B8E23")
history_label.pack()
history_box = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=4, bg="#1E1E1E", fg="#F1F5F9", font=("Segoe UI", 10), relief="flat")
history_box.pack(pady=5)

# Theme Toggle
theme_btn = oval_button(root, "🟢 Theme", toggle_theme)
theme_btn.pack(pady=5)

root.mainloop()
