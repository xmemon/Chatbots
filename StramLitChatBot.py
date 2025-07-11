# streamlit_app.py
# pip install streamlit google-genai

import os
import streamlit as st
from google import genai
from google.genai import types

# import google.generativeai as genai
# from google.generativeai import types


# Load your API key securely (recommended) or hardcode for testing only

# Initialize client
client = genai.Client(api_key="AIzaSyAXog-lK5PI060Pm2FvcTHxMHHuJezJRNs")
model = 'gemini-2.0-flash'

# Streamlit App Setup
st.set_page_config(page_title="Gemini Chatbot", layout="wide")
st.title("🧠 Test Instantiate Gemini Chatbot")

# Initialize session state for history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Text input box
user_input = st.chat_input("How can I help you?")

if user_input:
    # Append user message
    st.session_state.chat_history.append(types.Content(
        role="user",
        parts=[types.Part(text=user_input)]
    ))

    # Display user message in chat UI
    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate model response
    generate_content_config = types.GenerateContentConfig(response_mime_type="text/plain")
    response_text = ""

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=st.session_state.chat_history,
        config=generate_content_config,
    ):
        if chunk.text:
            response_text += chunk.text

    # Append model reply
    st.session_state.chat_history.append(types.Content(
        role="model",
        parts=[types.Part(text=response_text)]
    ))

    # Display model response in chat UI
    with st.chat_message("assistant"):
        st.markdown(response_text)

# Show full history above input
if st.session_state.chat_history:
    st.divider()
    st.markdown("### 💬 Full Conversation")
    for turn in st.session_state.chat_history:
        if turn.role == "user":
            st.markdown(f"*You:* {turn.parts[0].text}")
        elif turn.role == "model":
            st.markdown(f"*Gemini:* {turn.parts[0].text}")
