import streamlit as st
import requests
import time
import random

st.title("Career Advisor for Computing Science")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Function to send user message to Rasa server and get response
def send_message(message):
    url = "http://localhost:5005/webhooks/rest/webhook"  # Replace with your Rasa server URL
    payload = {"sender": "user", "message": message}
    response = requests.post(url, json=payload)
    return response.json()

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("You:"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    rasa_response = send_message(prompt)
    # Display assistant response in chat message container
    for response in rasa_response:
        with st.chat_message("assistant"):
            st.markdown(response["text"])
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response["text"]})