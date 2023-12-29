from datetime import timedelta
import json
import streamlit as st
import streamlit_lottie as st_lottie
from model import MessageContent,ChatAssistant

with st.container():
    st.title("Poetify--your chatty friend")
    st.write("Your poetic assistant!")
conn = st.connection('chat_db', type='sql')

# View the connection contents.
#conn

with conn.session as s:
    s.execute('CREATE TABLE IF NOT EXISTS chat_history (role TEXT, content TEXT);')

chat_history = conn.query('select * from chat_history', ttl=timedelta(minutes=10))
convo = chat_history[["role","content"]]
# convo.at[0,"role"]
# convo.at[0,"content"]


#This is where the rows and columns of the dataframe are extracted
rows ,cols = convo.shape

with st.sidebar:
    st.title("Previous Conversations")
    d = st.button(':wastebasket:')
    if d:
         s.execute('DELETE FROM chat_history;')
    for i in range(rows):
        with st.chat_message(convo.at[i,"role"]):
            st.markdown(convo.at[i,"content"])


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
         s.execute(
            'INSERT INTO chat_history (role, content) VALUES (:role, :content);',
            params=dict(role="user", content=prompt))
         s.commit()
       
   
       
    if(st.session_state.chat_assistant.is_complete()):
            response  = st.session_state.chat_assistant.get_answer()
            with st.chat_message("assistant"):
                 st.markdown(response)
                 #chat_history = {"role":"assistant","content":response}
                 s.execute(
                        'INSERT INTO chat_history (role, content) VALUES (:role, :content);',
                        params=dict(role="assistant", content=response))
                 s.commit()
   
   
        

           
           
                

