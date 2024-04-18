import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import streamlit as st
from platforms.vectara_platform.vectara import request_vectara
from models.vectara_gpt import request_vectara_gpt
from models.together_ai import mistral_response

models = ['Vectara', 'Together AI (Mistral-7b-v0.2)', 'Vectara + Open AI (GPT-3.5-turbo)']
option = st.selectbox('Which model you want to select?', ('Vectara', 'Together AI (Mistral-7b-v0.2)', 'Vectara + Open AI (GPT-3.5-turbo)'))
st.title("Advanced RAG Hackathon")

idx = 0
for index, item in enumerate(models):
    if option == item:
        idx = index
        break

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [[],[],[]]

# Display chat messages from history on app rerun
for message in st.session_state.messages[idx]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input(placeholder="Write your query here....."):
    # Add user message to chat history
    st.session_state.messages[idx].append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        
    with st.spinner("Looking into your queries, please wait...."):
        with st.chat_message("assistant"):
            if option == 'Vectara':
                res = request_vectara(prompt)
                res = res['responseSet'][0]['summary'][0]['text']
            elif option == 'Together AI (Mistral-7b-v0.2)':
                res = mistral_response(prompt)
            else:
                res = request_vectara_gpt(prompt)
            response = st.markdown(res)
    st.session_state.messages[idx].append({"role": "assistant", "content": res})