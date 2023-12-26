import streamlit as st
from model import MessageContent,ChatAssistant
st.title("Chatify--your chatty friend")

instructions:str = """You are a poetic assistant, skilled in responding to 
                      the questions from all fields of life with a poetic flair"""
# if "chat_assistant" not in st.session_state:
#     st.session_state.chat_assistant = ChatAssistant()tate

if "messages" not in st.session_state:
     st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

# if "chat_assistant" in st.session_state: 
#     for m in st.session_state.chat_assistant.get_message_history():
#         with st.chat_message(m.role):
#             st.markdown(m.content)

if prompt := st.chat_input("Please Ask a Question"):
    with st.chat_message("user"):
         st.markdown(prompt)
         st.session_state.chat_assistant = ChatAssistant(prompt,instructions)
         st.session_state.messages.append({"role":"user","content":prompt})
  
        
       
    response  = st.session_state.chat_assistant.get_answer()
    st.session_state.messages.append({"role":"assistant","content":response})
    with st.chat_message("assistant"):
        st.markdown(response)
           
           
                

