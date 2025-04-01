import streamlit as st
import requests
import json

# Groq API Configuration
GROQ_API_KEY = "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"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_groq_response(user_message, chat_history):
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    data = {
        "model": "llama-3.3-70b-versatile",  # Update this with the correct model name
        "messages":[{"role": "system", "content": """You are a Generative AI Expert with deep knowledge in Artificial Intelligence, Machine Learning, and Generative AI. 
  You provide expert-level answers on topics such as NLP, transformers, diffusion models, AI trends, model fine-tuning, and ethical AI. 
  If a user asks about anything outside these topics, politely refuse to answer and guide them back to AI-related discussions. please answer my question based on max_tokens set on api."""},]
    + chat_history + [{"role": "user", "content": user_message}], 
  "temperature": 0.7,  # Controls randomness (lower = more deterministic)
  "top_p": 0.9,  # Nucleus sampling (alternative to temperature)
 # "max_tokens": 512, # Limits response length
  "frequency_penalty": 0.0,  # Reduces repetition (higher = less repetition)
  "presence_penalty": 0.6,  # Encourages new topics in response
    }
    
    response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"  # More detailed error


# Streamlit UI Config
st.set_page_config(page_title="GenAI Expert", page_icon="🤖", layout="wide")

# Centered Header
st.markdown(
    """
    <div style="text-align: center;">
        <h1>🤖 Generative AI Expert</h1>
        <p>Ask anything about AI, ML, Generative AI, and the latest AI trends!</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Session State for chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! I'm your Generative AI expert. How can I help you today?"}]

# Display previous messages
for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.chat_message("user").write(msg["content"])
    else:
        st.chat_message("assistant").write(msg["content"])

# User input
user_input = st.chat_input("Type your question here...")
if user_input:
    # Append user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # Get AI response
    response = get_groq_response(user_input, st.session_state["messages"])
    st.session_state["messages"].append({"role": "assistant", "content": response})
    st.chat_message("assistant").write(response)
