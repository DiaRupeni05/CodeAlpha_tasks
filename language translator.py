from tkinter import *
from tkinter import ttk, messagebox
from deep_translator import GoogleTranslator

# ---------- Translator Setup ----------
translator_instance = GoogleTranslator(source='auto', target='english')
languages = translator_instance.get_supported_languages(as_dict=True)
lang_list = list(languages.keys())

# ---------- Main Window ----------
root = Tk()
root.title("🌐 Modern Translator")
root.geometry("750x550")
root.config(bg="#f3f4f6")
root.resizable(False, False)

# ---------- Styles ----------
style = ttk.Style()
style.theme_use("clam")

style.configure("TButton",
                font=("Segoe UI", 10, "bold"),
                padding=8,
                background="#14b8a6",
                foreground="white")
style.map("TButton",
          background=[("active", "#0d9488")])

style.configure("TCombobox",
                padding=6,
                font=("Segoe UI", 10))

# ---------- Functions ----------
def copy_to_clipboard(text_widget):
    text = text_widget.get("1.0", END).strip()
    if text:
        root.clipboard_clear()
        root.clipboard_append(text)
        messagebox.showinfo("Copied ✅", "Text copied to clipboard!")
    else:
        messagebox.showwarning("Warning", "No text to copy.")

def translate_text():
    try:
        src_lang = source_lang.get()
        tgt_lang = target_lang.get()
        text_to_translate = input_text.get("1.0", END).strip()

        if not text_to_translate:
            messagebox.showwarning("⚠️ Warning", "Please enter text to translate.")
            return

        translated_text = GoogleTranslator(
            source=languages[src_lang] if src_lang != "Auto Detect" else 'auto',
            target=languages[tgt_lang]
        ).translate(text_to_translate)

        output_text.delete("1.0", END)
        output_text.insert(END, translated_text)

    except Exception as e:
        messagebox.showerror("❌ Error", f"Translation failed!\n{e}")

# ---------- Header ----------
header_frame = Frame(root, bg="#14b8a6", height=70)
header_frame.pack(fill="x")

Label(header_frame, text="🌐 Modern Translator",
      font=("Segoe UI", 20, "bold"),
      bg="#14b8a6", fg="white").pack(pady=15)

# ---------- Language Selection ----------
lang_frame = Frame(root, bg="#f3f4f6")
lang_frame.pack(pady=15)

source_lang = ttk.Combobox(lang_frame, values=["Auto Detect"] + lang_list, state="readonly", width=25)
source_lang.set("Auto Detect")
source_lang.grid(row=0, column=0, padx=10)

target_lang = ttk.Combobox(lang_frame, values=lang_list, state="readonly", width=25)
target_lang.set("english")
target_lang.grid(row=0, column=1, padx=10)

# ---------- Input Card ----------
input_card = Frame(root, bg="white", bd=0, relief=FLAT)
input_card.pack(padx=20, pady=10, fill="x")

Label(input_card, text="Enter Text", font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w", padx=10, pady=5)

input_frame = Frame(input_card, bg="white")
input_frame.pack(fill="x", padx=10, pady=(0, 10))

input_text = Text(input_frame, height=6, font=("Segoe UI", 10), bd=1, relief=GROOVE, wrap=WORD)
input_text.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
ttk.Button(input_frame, text="📋 Copy", command=lambda: copy_to_clipboard(input_text)).grid(row=0, column=1)

# ---------- Translate Button ----------
ttk.Button(root, text="🔄 Translate", command=translate_text).pack(pady=15)

# ---------- Output Card ----------
output_card = Frame(root, bg="white", bd=0, relief=FLAT)
output_card.pack(padx=20, pady=10, fill="x")

Label(output_card, text="Translated Text", font=("Segoe UI", 11, "bold"), bg="white").pack(anchor="w", padx=10, pady=5)

output_frame = Frame(output_card, bg="white")
output_frame.pack(fill="x", padx=10, pady=(0, 10))

output_text = Text(output_frame, height=6, font=("Segoe UI", 10), bd=1, relief=GROOVE, wrap=WORD)
output_text.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
ttk.Button(output_frame, text="📋 Copy", command=lambda: copy_to_clipboard(output_text)).grid(row=0, column=1)

root.mainloop()
