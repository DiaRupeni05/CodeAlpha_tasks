import tkinter as tk
from tkinter import messagebox, scrolledtext
from deep_translator import GoogleTranslator
import speech_recognition as sr
import pyperclip

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

# Languages
languages = GoogleTranslator().get_supported_languages()
languages_display = ["Auto Detect"] + languages

# UI
root = tk.Tk()
root.title("Colorful Translator")
root.geometry("700x500")
root.config(bg="#222831")

# Title
tk.Label(root, text="🌍 Modern Translator", font=("Arial Black", 18), bg="#222831", fg="#FFD369").pack(pady=10)

# Language selectors
frame_lang = tk.Frame(root, bg="#222831")
frame_lang.pack()

source_lang = tk.StringVar(value="Auto Detect")
target_lang = tk.StringVar(value="english")

tk.OptionMenu(frame_lang, source_lang, *languages_display).config(bg="#FFD369", fg="black", font=("Arial", 10))
tk.OptionMenu(frame_lang, target_lang, *languages).config(bg="#FFD369", fg="black", font=("Arial", 10))

src_menu = tk.OptionMenu(frame_lang, source_lang, *languages_display)
src_menu.config(bg="#FFD369", fg="black")
src_menu.grid(row=0, column=0, padx=5)

tgt_menu = tk.OptionMenu(frame_lang, target_lang, *languages)
tgt_menu.config(bg="#FFD369", fg="black")
tgt_menu.grid(row=0, column=1, padx=5)

# Input box
input_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=5, bg="#393E46", fg="white", font=("Arial", 12))
input_text.pack(pady=10)

# Buttons frame
frame_buttons = tk.Frame(root, bg="#222831")
frame_buttons.pack()

tk.Button(frame_buttons, text="🎤 Speak", command=speak_to_text, bg="#00ADB5", fg="white", font=("Arial", 10)).grid(row=0, column=0, padx=5)
tk.Button(frame_buttons, text="📋 Paste", command=paste_input, bg="#00ADB5", fg="white", font=("Arial", 10)).grid(row=0, column=1, padx=5)
tk.Button(frame_buttons, text="➡ Translate", command=translate_text, bg="#FFD369", fg="black", font=("Arial Black", 10)).grid(row=0, column=2, padx=5)

# Output box
output_text = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=5, bg="#393E46", fg="white", font=("Arial", 12))
output_text.pack(pady=10)

# Copy button
tk.Button(root, text="📄 Copy", command=copy_output, bg="#00ADB5", fg="white", font=("Arial", 10)).pack()

root.mainloop()
