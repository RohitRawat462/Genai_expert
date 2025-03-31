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
        "messages": chat_history + [{"role": "user", "content": user_message}],
        "temperature": 0.7
    }
    
    response = requests.post(GROQ_API_URL, headers=headers, data=json.dumps(data))
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code}, {response.text}"  # More detailed error

    print(response.status_code)
    print(response.text)

# Streamlit UI
st.set_page_config(page_title="GenAI Expert Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 Generative AI Expert Chatbot")
st.write("Ask anything about AI, ML, Generative AI, and the latest AI trends!")

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
