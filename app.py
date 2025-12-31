import os
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

st.title("🤖 Smart LLM Chatbot (Fixed!)")

api_key = st.secrets.get("OPENAI_API_KEY", "")
if not api_key:
    api_key = st.sidebar.text_input("OpenAI API Key", type="password")

if not api_key:
    st.error("Add OPENAI_API_KEY to Secrets! https://platform.openai.com/api-keys")
    st.stop()

os.environ["OPENAI_API_KEY"] = api_key

@st.cache_resource
def get_chain():
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    memory = ConversationBufferMemory(return_messages=True)
    return ConversationChain(llm=llm, memory=memory)

chain = get_chain()

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask anything!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = chain.invoke({"input": prompt})
        content = response["response"]
        st.markdown(content)
        st.session_state.messages.append({"role": "assistant", "content": content})
