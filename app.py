import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.chains import ConversationChain  # FIXED: _community
from langchain_community.memory import ConversationBufferMemory  # FIXED

st.title("🤖 FREE Groq Chatbot - Fixed Imports!")

api_key = st.secrets.get("GROQ_API_KEY", "")
if not api_key:
    api_key = st.sidebar.text_input("Groq Key (console.groq.com/keys)", type="password")

if not api_key:
    st.info("Get free Groq key!")
    st.stop()

os.environ["GROQ_API_KEY"] = api_key

@st.cache_resource
def get_chain():
    llm = ChatGroq(model="llama3-8b-8192", temperature=0.7)
    memory = ConversationBufferMemory(return_messages=True)
    return ConversationChain(llm=llm, memory=memory)

chain = get_chain()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = chain.invoke({"input": prompt})
        content = response["response"]
        st.markdown(content)
        st.session_state.messages.append({"role": "assistant", "content": content})
