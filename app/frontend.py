import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
import requests
import random
import time
st.title("ChatBot")

# with open('config.yaml') as file:
#     config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

st.title("🔐 Login")
name, authentication_status, username = authenticator.login("main")


if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name}*')
    
st.write("Welcome to our RAG Based Chatbot")
# if prompt := st.chat_input("Hiii what's on your mind")
if "messages" not in st.session_state:
    st.session_state.messages = [{"role":"assistant" , "content":"Hii what on your mind ?"}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("what is up ?"):
    with st.chat_message("user"):
        st.session_state.messages.append({"role":"user","content":prompt})    
        st.markdown(prompt)

    url = "http://127.0.0.1:8000/query"
    question = {"query":prompt}
# @st.cache_data
    with st.spinner("Waiting for chatbot response..."):
        try:
            # Make the POST request
            response = requests.post(url, json=question)
            response_data = response.json()



            # Check if the request was successful
            if response.status_code == 200:  # 201 Created for successful POST
                st.success("Here Is your Answer")
                # st.write("Response Status Code:", response.status_code)
                # st.write("Response Body:")
                # st.json(response.json())  # Display the JSON response
            else:
                st.error(f"POST request failed with status code: {response.status_code}")
                st.write("Response Body:")
                st.write(response.text)

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred during the request: {e}")

    with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            # assistant_response = random.choice(
            # [
            #     "Hello there! How can I assist you today?",
            #     "Hi, human! Is there anything I can help you with?",
            #     "Do you need help?",
            # ]
    # with st.spinner("Wait for it...", show_time=True):
            assistant_response = response_data["answer"]
            if(assistant_response == "Empty Response"):
                message_placeholder.markdown("Sorry No Response about this")
        # ) 
            # for chunk in assistant_response:
            #     full_response += chunk + " "
            #     time.sleep(0.05)
            else:
                #  message_placeholder.markdown(assistant_response + "▌")
                message_placeholder.markdown(assistant_response)          
    # st.session_state.messages.append({"role":"assistant","content":assistant_response})  
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})  

uploaded_file =st.file_uploader("Upload a File Through Here")
if uploaded_file is not None:
    file_bytes = uploaded_file.read()
        
        # Example 1: Sending as multipart form-data
    files = {'file': (uploaded_file.name, file_bytes, uploaded_file.type)}
    with st.spinner("Waiting for chatbot response..."):
        try:
            # Make the POST request
            response = requests.post("http://127.0.0.1:8000/file", files=files)
        



            # Check if the request was successful
            if response.status_code == 200:  # 201 Created for successful POST
                st.success("POST request successful!")
                st.write("Response Status Code:", response.status_code)
                # st.write("Response Body:")
                # st.json(response.json())  # Display the JSON response
            else:
                st.error(f"POST request failed with status code: {response.status_code}")
                st.write("Response Body:")
                st.write(response.text)

        except requests.exceptions.RequestException as e:
            st.error(f"An error occurred during the request: {e}")



elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
