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
        "messages":[{"role": "system", "content": """You are an advanced AI mentor specializing in software development, competitive exam preparation, and knowledge assessment. Your role is to assist in:

Software Development – Provide expert guidance, code solutions, debugging help, best practices, and technology recommendations across all programming languages.

Competitive Exams & Higher Studies (NET, PhD, etc.) – Cover complete syllabus, provide conceptual explanations, create study plans, and conduct mock tests.

Active Learning & Revision – Ask topic-wise questions, simulate real exam environments, and provide structured revision strategies.

Knowledge Assessment & Rating – Evaluate responses, rate knowledge levels, and suggest improvement areas.

Job Performance Support – Help in real-world development tasks, project implementation, and career growth strategies.

Whenever I study a topic, ask me questions to test my understanding. If I struggle, provide hints before revealing the answer. During coding tasks, guide me step by step instead of giving direct answers. Ensure responses are structured, engaging, and practical. If I need revision, summarize key points concisely and suggest practice problems. Always adapt to my learning pace and focus on my weak areas.
Inshort You are DevGuru AI, an advanced AI mentor specializing in software development, competitive exam preparation, and knowledge assessment.  
        Guide users in coding, exams, revision, and job-related development tasks. Ensure structured, engaging, and practical responses."""},]
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
st.set_page_config(page_title="DevGuru AI", page_icon="🤖", layout="wide")

# Fix Header Spacing (Top Padding)
st.markdown("""
    <style>
        /* Remove default padding from Streamlit layout */
        .block-container { 
            padding-top: 0px !important;  /* Just 10px space */
        }
    </style>
""", unsafe_allow_html=True)

# Custom CSS for WhatsApp-style chat UI
st.markdown("""
    <style>
        body { margin: 0; padding: 0; font-family: Arial, sans-serif; }
        
        .header {
            text-align: center;
            font-size: 28px;
            font-weight: bold;
            color: #fff;
            background: linear-gradient(90deg, #007AFF, #4A90E2);
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 5px;
        }
        
        .subtext {
            text-align: center;
            font-size: 14px;
            color: #eaeaea;
            margin-top: -10px;
        }
        
        .chat-container {
            max-width: 600px;
            margin: auto;
            padding: 10px;
        }
        
        .chat-bubble {
            padding: 10px 15px;
            border-radius: 15px;
            margin: 5px 0;
            font-size: 14px;
            display: inline-block;
            max-width: 75%;
            word-wrap: break-word;
        }
        
        .user-msg {
            background-color: #DCF8C6;
            color: black;
            text-align: right;
            float: right;
            clear: both;
        }
        
        .bot-msg {
            background-color: #EAEAEA;
            color: black;
            text-align: left;
            float: left;
            clear: both;
        }
        
        .msg-container {
            display: flex;
            flex-direction: column;
        }
        
        .input-container {
            text-align: center;
            margin-top: 10px;
        }
        
    </style>
""", unsafe_allow_html=True)

st.markdown(
    """
    <div style="text-align: center; padding: 10px; background: linear-gradient(90deg, #007AFF, #4A90E2); border-radius: 10px;">
        <h1 style="color: white; margin-bottom: 5px;">🤖 DevGuru AI</h1>
        <p style="color: #f0f0f0; font-size: 14px;">Your AI Mentor for Coding, Competitive Exams & Job Success</p>
    </div>
    """,
    unsafe_allow_html=True
)

# Session State for Chat History
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! I'm DevGuru AI. How can I assist you today?"}]

# Chat Container
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for msg in st.session_state["messages"]:
    if msg["role"] == "user":
        st.markdown(f'<div class="chat-bubble user-msg">{msg["content"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="chat-bubble bot-msg">{msg["content"]}</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# User Input
user_input = st.chat_input("Type your message...")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    st.markdown(f'<div class="chat-bubble user-msg">{user_input}</div>', unsafe_allow_html=True)

    # Get AI response
    response = get_groq_response(user_input, st.session_state["messages"])
    st.session_state["messages"].append({"role": "assistant", "content": response})
    st.markdown(f'<div class="chat-bubble bot-msg">{response}</div>', unsafe_allow_html=True)

# Hide Streamlit Branding & Fork Button
st.markdown("""
    <style>
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display: none !important;}  
        .viewerBadge_link__qRIco {display: none !important;}
        #MainMenu {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)
