import os
import json
import requests
import streamlit as st
from dotenv import load_dotenv

# ===============================
# APP CONFIG
# ===============================
st.set_page_config(page_title="Groq vs LM Studio Chatbot")
st.title("💬 Multi-LLM Chatbot")

load_dotenv()

# ===============================
# SIDEBAR
# ===============================
st.sidebar.title("⚙️ Settings")

llm_choice = st.sidebar.radio(
    "Choose LLM Provider",
    ["Groq (Cloud)", "LM Studio (Local)"]
)

# 🆕 NEW CHAT BUTTON
if st.sidebar.button("🆕 New Chat"):
    if llm_choice == "Groq (Cloud)":
        st.session_state.groq_messages = []
    else:
        st.session_state.lm_messages = []
    st.rerun()

show_history = st.sidebar.checkbox("📜 Show Chat History", value=True)

# ===============================
# SESSION STATE
# ===============================
if "groq_messages" not in st.session_state:
    st.session_state.groq_messages = []

if "lm_messages" not in st.session_state:
    st.session_state.lm_messages = []

# ===============================
# SELECT ACTIVE HISTORY
# ===============================
if llm_choice == "Groq (Cloud)":
    messages = st.session_state.groq_messages
else:
    messages = st.session_state.lm_messages

# ===============================
# DISPLAY CHAT HISTORY
# ===============================
if show_history:
    for msg in messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# ===============================
# USER INPUT
# ===============================
user_prompt = st.chat_input("Ask anything...")

if user_prompt:
    messages.append({"role": "user", "content": user_prompt})

    with st.chat_message("user"):
        st.markdown(user_prompt)

    # ===============================
    # GROQ API
    # ===============================
    if llm_choice == "Groq (Cloud)":
        api_key = os.getenv("GROQ_API_KEY")

        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.3-70b-versatile",
            "messages": messages,
            "temperature": 0.7
        }

        response = requests.post(url, headers=headers, json=payload)
        resp = response.json()

        answer = resp["choices"][0]["message"]["content"]

    # ===============================
    # LM STUDIO API
    # ===============================
    else:
        try:
            url = "http://127.0.0.1:1234/v1/chat/completions"
            headers = {"Content-Type": "application/json"}

            payload = {
                "model": "microsoft/phi-4-mini-reasoning",
                "messages": messages,
                "temperature": 0.7
            }

            response = requests.post(url, headers=headers, json=payload, timeout=30)
            resp = response.json()

            answer = resp["choices"][0]["message"]["content"]

            if isinstance(answer, list):
                answer = answer[0]["text"]

        except requests.exceptions.ConnectionError:
            answer = "❌ LM Studio server is not running. Please start it."

    # ===============================
    # SAVE & DISPLAY RESPONSE
    # ===============================
    messages.append({"role": "assistant", "content": answer})

    with st.chat_message("assistant"):
        st.markdown(answer)
