import os
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory

st.title("🤖 FREE Groq Chatbot - Modern LCEL!")

# Free Groq key: console.groq.com/keys
api_key = st.secrets.get("GROQ_API_KEY", "")
if not api_key:
    api_key = st.sidebar.text_input("Groq API Key", type="password")

if not api_key:
    st.stop()

os.environ["GROQ_API_KEY"] = api_key

@st.cache_resource
def get_llm():
    return ChatGroq(model="llama3-8b-8192", temperature=0.7)

llm = get_llm()

# LCEL Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant."),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

# Simple chain
chain = prompt | llm

if "session_history" not in st.session_state:
    st.session_state.session_history = ChatMessageHistory()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt_input := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt_input})
    with st.chat_message("user"):
        st.markdown(prompt_input)

    with st.chat_message("assistant"):
        # LCEL invoke with history
        response = chain.invoke(
            {"input": prompt_input, "history": st.session_state.session_history.messages}
        )
        resp_content = response.content
        st.markdown(resp_content)
        st.session_state.messages.append({"role": "assistant", "content": resp_content})

    # Update history
    st.session_state.session_history.add_user_message(prompt_input)
    st.session_state.session_history.add_ai_message(resp_content)
