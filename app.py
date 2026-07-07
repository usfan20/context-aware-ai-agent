import streamlit as st
from groq import Groq  # Switch from openai to groq

st.set_page_config(page_title="Safex Solutions Support Bot", page_icon="🛡️", layout="centered")
st.markdown("<h2 style='text-align: center; color: #1E3A8A;'>🛡️ Safex Solutions AI Assistant</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Official FAQ and Support Agent</p>", unsafe_allow_html=True)
st.divider()

# Paste your free Groq API key here
try:
    api_key = st.secrets["GROQ_API_KEY"]
except Exception:
    api_key = "PASTE_YOUR_KEY_HERE_ONLY_FOR_LOCAL_TESTING"

client = Groq(api_key=api_key)

@st.cache_data
def load_safex_data():
    try:
        with open("website_context.txt", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Error: website_context.txt file missing."

safex_knowledge = load_safex_data()

SAFEX_SYSTEM_PROMPT = f"""
You are the official corporate AI assistant for Safex Solutions. Assist users using ONLY the Safex Solutions Knowledge Base below.
KNOWLEDGE BASE:
{safex_knowledge}

RULES:
1. If found in context, answer professionally.
2. If about Safex but missing, say: "Please contact support@safexsolutions.com".
3. If completely unrelated, answer via general fallback knowledge but prefix with: "(Note: Answering via general knowledge fallback)".
"""

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "system", "content": SAFEX_SYSTEM_PROMPT}]

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

if user_input := st.chat_input("How can I assist you today?"):
    with st.chat_message("user"):
        st.markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        response_box = st.empty()
        ai_response = ""
        
        # Using openai/gpt-oss-20b which is incredibly fast and free on Groq
        stream = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=st.session_state.messages,
            stream=True,
            temperature=0.15
        )
        for chunk in stream:
            if chunk.choices[0].delta.content:
                ai_response += chunk.choices[0].delta.content
                response_box.markdown(ai_response + "▌")
        response_box.markdown(ai_response)
        
    st.session_state.messages.append({"role": "assistant", "content": ai_response})