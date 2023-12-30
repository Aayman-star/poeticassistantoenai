from datetime import timedelta
import json
import streamlit as st
import streamlit_lottie as st_lottie
from model import MessageContent,ChatAssistant
import sqlite3

with st.container():
    st.title("Poetify--your chatty friend")
    st.write("Your poetic assistant!")


conn = st.connection('chat_db', type='sql')

with conn.session as s:
    st.markdown(f"s is a {type(s)}")
    s.execute('CREATE TABLE IF NOT EXISTS chat_history (role TEXT, content TEXT);')
    s.execute('DELETE FROM chat_history;')
    

def add_conversation(role:str,content:str)->None:
     s.execute(
            'INSERT INTO chat_history (role, content) VALUES (:role, :content);',
            params=dict(role=role, content=content))
     s.commit()

def delete_conversation()->None:
     with conn.session as s:
        s.execute('DELETE FROM chat_history;');
        s.commit();

def display_chathistory():
     chat_history = conn.query('select * from chat_history;')
     convo = chat_history[["role","content"]]
     rows ,cols = convo.shape
     for i in range(rows):
        with st.chat_message(convo.at[i,"role"]):
            st.markdown(convo.at[i,"content"])

def display_dataframe():
      chat_history = conn.query('select * from chat_history;')
      convo = chat_history[["role","content"]]
      convo
  #ttl=timedelta(minutes=1)

# convo.at[0,"role"]
# 
# convo.at[0,"content"]


#This is where the rows and columns of the dataframe are extracted

display_dataframe()
with st.sidebar:
    st.title("Previous Conversations")
    d = st.button(':wastebasket:')
    if d:
        x = st.sidebar.checkbox('Are you sure you want to delete the coversation history?')
        if x:
           delete_conversation()
           display_chathistory()
   
    display_chathistory()


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
         #chat_history = {"role":"user","content":prompt}
         add_conversation("user",prompt)
 
       
   
    with st.spinner('Searching for answer'):
        if(st.session_state.chat_assistant.is_complete()):
                response  = st.session_state.chat_assistant.get_answer()
                
                with st.chat_message("assistant"):
                        st.markdown(response)
                        add_conversation("assistant",response)
                
   