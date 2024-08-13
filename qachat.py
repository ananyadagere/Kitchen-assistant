from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("API_KEY"))

model = genai.GenerativeModel("gemini-1.5-flash")
chat = model.start_chat(history=[])

def get_gemini_response(question):
    response = chat.send_message(question, stream=True)
    return response

st.set_page_config(page_title="Kitchen Companion", layout="wide", initial_sidebar_state="collapsed", page_icon="🍽️")

st.title("Your Kitchen Companion")

if 'messages' not in st.session_state:
    st.session_state.messages = []

dark_mode = st.sidebar.checkbox("Dark Mode")
if dark_mode:
    st.markdown("""
    <style>
        body, * {
            background-color: #262730;
            color: #fff;
        }
        h1, h2 {
            color: #fff;
        }
    </style>
    """, unsafe_allow_html=True)

container = st.container()

for message in st.session_state.messages:
    with container:
        if message["role"] == "user":
            st.markdown(f"**You:** {message['content']}")
        else:
            st.markdown(f"{message['content']}")

if prompt := st.chat_input("What's cookin'?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with container:
        st.markdown(f"**You:** {prompt}")
    response = get_gemini_response(prompt)
    whole_response = ""
    for chunk in response:
        whole_response += chunk.text
    st.markdown(f"{whole_response}", unsafe_allow_html=True)
    st.session_state.messages.append({"role": "bot", "content": whole_response})

st.sidebar.title("Recipe Book")
st.sidebar.markdown("---")
for message in st.session_state.messages:
    if message["role"] == "user":
        st.sidebar.markdown(f"**You:** {message['content']}")
    else:
        st.sidebar.markdown(f"{message['content']}")

st.markdown("---")
st.markdown("Cooked with ❤️ and Gemini")
