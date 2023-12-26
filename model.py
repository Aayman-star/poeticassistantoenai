from openai import OpenAI
from openai.types.chat.chat_completion import ChatCompletion
from dotenv import load_dotenv,find_dotenv
from typing import Any


class MessageContent:
    def __init__(self,role:str,msgstring:str| Any):
        self.role = role
        self.msgstring=msgstring


class ChatAssistant:
    def __init__(self,prompt:str,instructions:str,model="gpt-3.5-turbo-1106"):
        self.prompt :str = prompt;
        self.instructions:str = instructions;
        self.model:str = model;

        load_dotenv(find_dotenv());
        self.client : OpenAI = OpenAI();
        self.chat_assistant:ChatCompletion = self.client.chat.completions.create(
              model = self.model,
              messages= [
                {"role": "system", "content": "You are a poetic assistant, skilled in explaining complex programming with creative flair."},
                {"role": "user", "content": self.prompt}
                    ],
                    

        )
        self.messages: list[MessageContent] = []
        self.add_message(MessageContent(role="user",msgstring=prompt))
        """
        #This function will get the answer to the current question
        """
    def get_answer(self)->MessageContent:
            answer = MessageContent(role="assistant",msgstring=self.chat_assistant.choices[0].message.content)
            print("Assistant:",answer.role,"Answet",answer.msgstring)
            self.add_message(MessageContent(role="assistant",msgstring=self.chat_assistant.choices[0].message.content))
            return self.chat_assistant.choices[0].message.content
            """
            #This function creates the message history by appending the message to the list of messages
            """
    def add_message(self,message)->None:
            self.messages.append(message)

            """
            #This is the entire message history to be displayed
            """
    def get_message_history(self)->list[MessageContent]:
            return self.messages

            
