import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

import streamlit as st
from platforms.vectara_platform.vectara import request_vectara_sop, request_vectara_sop_and_chat_history
from models.vectara_gpt import request_vectara_gpt_sop, request_vectara_gpt_sop_and_chat_history
from models.crag import request_crag_sop, request_crag_sop_and_chat_history
from models.together_ai import request_mistral_sop, request_mistral_sop_and_chat_history


approches = ['Vectara SOP only',
             'Vectara  SOP + Chat History',
             'Vectara + Open AI (GPT-3.5-turbo) SOP Only',
             'Vectara + Open AI (GPT-3.5-turbo) SOP + Chat History',
             'Together AI (Mistral-7b-v0.2) SOP only',
             'Together AI (Mistral-7b-v0.2) SOP + Chat History',
             'Vectara + GPT3.5 & Mixtral-8x7B-Instruct-v0.1 (CRAG) SOP only',
             'Vectara + GPT3.5 & Mixtral-8x7B-Instruct-v0.1 (CRAG) SOP + Chat History'
            ]
option = st.selectbox('Which approach do you want to select?',
                      (
                          'Vectara SOP only',
                          'Vectara  SOP + Chat History',
                          'Vectara + Open AI (GPT-3.5-turbo) SOP Only',
                          'Vectara + Open AI (GPT-3.5-turbo) SOP + Chat History',
                          'Together AI (Mistral-7b-v0.2) SOP only',
                          'Together AI (Mistral-7b-v0.2) SOP + Chat History',
                          'Vectara + GPT3.5 & Mixtral-8x7B-Instruct-v0.1 (CRAG) SOP only',
                          'Vectara + GPT3.5 & Mixtral-8x7B-Instruct-v0.1 (CRAG) SOP + Chat History'
                        )
                      )


st.title("Vectara Advanced RAG Hackathon")

idx = 0
for index, item in enumerate(approches):
    if option == item:
        idx = index
        break

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [[],[],[],[],[],[],[],[]]

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

            if option == 'Vectara SOP only':
                res = request_vectara_sop(prompt)
                res = res['responseSet'][0]['summary'][0]['text']
            elif option == 'Vectara  SOP + Chat History':
                res = request_vectara_sop_and_chat_history(prompt)
                res = res['responseSet'][0]['summary'][0]['text']
            elif option == 'Vectara + Open AI (GPT-3.5-turbo) SOP Only':
                res = request_vectara_gpt_sop(prompt)
            elif option == 'Vectara + Open AI (GPT-3.5-turbo) SOP + Chat History':
                res = request_vectara_gpt_sop_and_chat_history(prompt)
            elif option == 'Together AI (Mistral-7b-v0.2) SOP only':
                res = request_mistral_sop(prompt)
            elif option == 'Together AI (Mistral-7b-v0.2) SOP + Chat History':
                res = request_mistral_sop_and_chat_history(prompt)
            elif option == 'Vectara + GPT3.5 & Mixtral-8x7B-Instruct-v0.1 (CRAG) SOP only':
                res = request_crag_sop(prompt)
            else: #option == 'Vectara + GPT3.5 & Mixtral-8x7B-Instruct-v0.1 (CRAG) SOP + Chat History':
                res = request_crag_sop_and_chat_history(prompt)

            response = st.markdown(res)

    st.session_state.messages[idx].append({"role": "assistant", "content": res})