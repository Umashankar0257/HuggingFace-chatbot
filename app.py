import streamlit as st
import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Hugging Face API
HF_TOKEN = os.getenv("HF_TOKEN")
API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

# Function to call Hugging Face
def generate_response(question, temperature, max_tokens):

    payload = {
        "inputs": question,
        "parameters": {
            "temperature": temperature,
            "max_new_tokens": max_tokens
        }
    }

    response = requests.post(API_URL, headers=headers, json=payload)
    result = response.json()

    # ✅ Handle different response formats
    if isinstance(result, list):
        return result[0].get("generated_text", "No response generated.")
    elif "error" in result:
        return f"Error from Hugging Face: {result['error']}"
    else:
        return str(result)

# Streamlit UI
st.title("Enhanced Q&A Chatbot With HuggingFace")

temperature = st.sidebar.slider("Temperature", 0.0, 1.0, 0.7)
max_tokens = st.sidebar.slider("Max Tokens", 50, 300, 150)

st.write("Go ahead and ask any question")

user_input = st.text_input("You:")

if user_input:
    response = generate_response(user_input, temperature, max_tokens)
    st.write(response)
else:
    st.write("Please provide the user input")