import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage
from langchain_core.prompts import ChatMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


from dotenv import load_dotenv
load_dotenv()
if "chat_history" not in st.session_state:
    st.session_state.chat_history=[]

st.set_page_config(page_title="My Chatbot",page_icon="")
st.header("My own chatbot")
#Get response from openai
def get_response(query,chat_history):
    template="""
        You are a helpful assisstant.answer the following questions
        chat history:{chat_history}
        user question:{user_question}
        """
    prompt=ChatMessagePromptTemplate.from_template(template)
    llm=ChatOpenAI()
    chain= prompt | llm | StrOutputParser()
    return chain.invoke({
        "chat_history":chat_history,
        "user_question":query
    })

#print history conversation
for message in st.session_state.chat_history:
    if isinstance(message,HumanMessage):
        with st.chat_message("Human"):
            st.markdown(message.content)
    else:
        with st.chat_message("AI"):
            st.markdown(message.content)        
#userinput
user_query=st.chat_input("Type Your Message")
if user_query is not None and user_query!="":
    st.session_state.chat_history.append(HumanMessage(user_query))
    with st.chat_message("human"):
        st.markdown(user_query)

    with st.chat_message("AI"):
        ai_response=get_response(user_query,st.session_state.chat_history)
        st.markdown(ai_response)
    st.session_state.chat_history.append(AIMessage(ai_response))        