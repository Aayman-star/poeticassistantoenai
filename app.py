import json
import streamlit as st
import streamlit_lottie as st_lottie
from model import MessageContent,ChatAssistant

with st.container():
    st.title("Poetify--your chatty friend")
    st.write("Your poetic assistant!")

# def load_animation(filepath:str):
#     with open(filepath) as f:
#         return json.load(f)

# chatbot_1 = load_animation('Animation.json')

# st_lottie(chatbot_1)

instructions:str = """You are a poetic assistant, skilled in responding to 
                      the questions from all fields of life with a poetic flair"""
name : str = 'Poetic Assistant'
if "chat_assistant" not in st.session_state:
    st.session_state.chat_assistant = ChatAssistant(name,instructions)

if "messages" not in st.session_state:
     st.session_state.messages = []

for m in st.session_state.chat_assistant.get_message_history():
    with st.chat_message(m.role):
        st.markdown(m.msgstring)



if prompt := st.chat_input("Please Ask a Question"):
    with st.chat_message("user"):
         st.markdown(prompt)
         st.session_state.chat_assistant.askquestion(prompt)
       
   
       
    if(st.session_state.chat_assistant.is_complete()):
            response  = st.session_state.chat_assistant.get_answer()
            with st.chat_message("assistant"):
                 st.markdown(response)
   
   
        

           
           
                

