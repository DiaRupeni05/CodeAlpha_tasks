import streamlit as st
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# FAQ dataset
faqs = {
    "What is tokenization?": "Tokenization is splitting text into individual units like words or phrases.",
    "How does tokenization work?": "It uses rules or models to break text into tokens.",
    "What is text preprocessing?": "Preprocessing includes cleaning, tokenizing, and normalizing text.",
    "What are tokens in NLP?": "Tokens are the smallest units of text used for analysis.",
    "What features does the product offer?": "Our product includes real-time analytics, customizable dashboards, and secure cloud storage.",
    "Is there a free trial available?": "Yes, we offer a 14-day free trial with access to all premium features.",
    "How do I reset my password?": "Click 'Forgot Password' on the login page and follow the instructions sent to your email.",
    "What platforms is the product compatible with?": "Our product works on Windows, macOS, iOS, and Android.",
    "How do I contact customer support?": "You can reach our support team via chat, email, or phone 24/7.",
    "Can I integrate this with other tools?": "Yes, we support integrations with Slack, Zapier, Google Workspace, and more.",
    "What pricing plans are available?": "We offer Basic, Pro, and Enterprise plans tailored to different business needs.",
    "How do I cancel my subscription?": "Go to your account settings and click 'Cancel Subscription'. You’ll retain access until the end of your billing cycle.",
    "Is my data secure?": "Absolutely. We use end-to-end encryption and comply with GDPR and ISO standards.",
    "Can I export my data?": "Yes, you can export your data in CSV or JSON format from the dashboard."
}

# Follow-up questions for every FAQ
related_questions = {
    "What is tokenization?": [
        "Why is tokenization important?",
        "What are common tokenization tools?",
        "Is tokenization language-specific?"
    ],
    "How does tokenization work?": [
        "Can tokenization handle punctuation?",
        "What libraries support tokenization?",
        "Is tokenization rule-based or model-based?"
    ],
    "What is text preprocessing?": [
        "What steps are involved in preprocessing?",
        "Why is preprocessing necessary?",
        "How does preprocessing affect model accuracy?"
    ],
    "What are tokens in NLP?": [
        "Are tokens always words?",
        "Can tokens include punctuation?",
        "How are tokens used in machine learning?"
    ],
    "What features does the product offer?": [
        "Can I customize the dashboard?",
        "Does it support real-time analytics?",
        "Is cloud storage included?"
    ],
    "Is there a free trial available?": [
        "What happens after the trial ends?",
        "Do I need a credit card for the trial?",
        "Can I extend the trial period?"
    ],
    "How do I reset my password?": [
        "I didn’t receive the reset email. What should I do?",
        "Can I change my password from the dashboard?",
        "Is two-factor authentication available?"
    ],
    "What platforms is the product compatible with?": [
        "Does it work on mobile devices?",
        "Is there a web version?",
        "Are updates automatic across platforms?"
    ],
    "How do I contact customer support?": [
        "Is support available 24/7?",
        "Can I chat with a live agent?",
        "Is there a support email?"
    ],
    "Can I integrate this with other tools?": [
        "Is there an API available?",
        "How do I connect it to Slack?",
        "Are integrations secure?"
    ],
    "What pricing plans are available?": [
        "What’s included in the Pro plan?",
        "Can I switch plans anytime?",
        "Are there any hidden fees?"
    ],
    "How do I cancel my subscription?": [
        "Will I get a refund?",
        "Can I pause my subscription?",
        "What happens to my data after cancellation?"
    ],
    "Is my data secure?": [
        "Do you comply with GDPR?",
        "What encryption methods are used?",
        "Can I delete my data permanently?"
    ],
    "Can I export my data?": [
        "What formats are supported?",
        "Is export available for all plans?",
        "Can I schedule automatic exports?"
    ]
}

# Vectorize FAQ questions
faq_keys = list(faqs.keys())
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(faq_keys)

# Streamlit UI setup
st.set_page_config(page_title="Chatbot FAQ", layout="centered")
st.title("💬 Chatbot FAQ")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Input box
user_input = st.text_input("Ask your question:", key="faq_input")

# Process input
if user_input:
    user_vector = vectorizer.transform([user_input])
    similarity = cosine_similarity(user_vector, faq_vectors)
    best_match_idx = similarity.argmax()
    best_question = faq_keys[best_match_idx]
    response = faqs[best_question]

    # Save to history
    st.session_state.chat_history.append((user_input, response))

# Display chat history
st.markdown("### 🗂️ Chat History")
for q, a in st.session_state.chat_history:
    st.markdown(f"**You asked:** {q}\n\n**Copilot replied:** {a}")

# Suggested questions
if user_input:
    st.markdown("### 🔍 You might also ask:")
    suggestions = related_questions.get(best_question, [])
    for q in suggestions:
        if st.button(q):
            st.session_state.faq_input = q
            st.experimental_rerun()