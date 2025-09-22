import streamlit as st
import requests
import random
import time

st.title("ChatBot")

# -------------------
# Initialize chat messages
# -------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hi! What’s on your mind?"}]

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------
# Chat input
# -------------------
if prompt := st.chat_input("Type your message"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Send user input to backend
    url = "http://127.0.0.1:8000/query"
    question = {"query": prompt}

    with st.spinner("Waiting for chatbot response..."):
        try:
            response = requests.post(url, json=question)
            response_data = response.json()

            if response.status_code == 200:
                st.success("Here is your answer")
            else:
                st.error(f"POST request failed with status code: {response.status_code}")
                st.write(response.text)
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred during the request: {e}")
            response_data = {"answer": "Empty Response"}

    # Display assistant response
    assistant_response = response_data.get("answer", "Empty Response")
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        if assistant_response == "Empty Response":
            message_placeholder.markdown("Sorry, no response available.")
        else:
            message_placeholder.markdown(assistant_response)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})

# -------------------
# File uploader
# -------------------
uploaded_file = st.file_uploader("Upload a file")
if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    files = {'file': (uploaded_file.name, file_bytes, uploaded_file.type)}

    with st.spinner("Uploading file..."):
        try:
            response = requests.post("http://127.0.0.1:8000/file", files=files)
            if response.status_code == 200:
                st.success("File uploaded successfully!")
            else:
                st.error(f"POST request failed with status code: {response.status_code}")
                st.write(response.text)
        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred during the request: {e}")
