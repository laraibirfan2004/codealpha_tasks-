import pandas as pd
import gradio as gr
import nltk
import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# NLTK resources
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

# Load dataset
df = pd.read_csv("Ecommerce_FAQs.csv")

# Preprocessing function
def preprocess_text(text):
    stop_words = set(nltk.corpus.stopwords.words("english"))
    tokens = nltk.word_tokenize(text.lower())
    tokens = [word for word in tokens if word not in stop_words and word not in string.punctuation]
    return " ".join(tokens)

print(df.columns)

df["Processed_Question"] = df["prompt"].apply(preprocess_text)

# Vectorization
vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(df["Processed_Question"])

# Chatbot function
def chatbot_response(user_input):
    if not user_input.strip():
        return "Please enter a valid question."

    user_input_processed = preprocess_text(user_input)
    user_vector = vectorizer.transform([user_input_processed])

    similarity_scores = cosine_similarity(user_vector, faq_vectors)
    best_match_idx = np.argmax(similarity_scores)

    best_match_score = similarity_scores[0, best_match_idx]
    if best_match_score > 0.3:
        return df.iloc[best_match_idx]["response"]
    else:
        return "I'm sorry, I couldn't find an answer to your question. Please try rephrasing."

# Gradio UI
iface = gr.Interface(
    fn=chatbot_response,
    inputs=gr.Textbox(label="Ask me a question"),
    outputs=gr.Textbox(label="Chatbot Response"),
    title="E-commerce FAQ Chatbot",
    description="Ask a question related to e-commerce and get an instant response.",
)

# Run the chatbot
if __name__ == "__main__":
    iface.launch()

