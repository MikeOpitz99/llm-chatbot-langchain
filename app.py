import streamlit as st
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

st.title("?? Smart LLM Chatbot")

# Bulletproof key: Secrets > Input
api_key = st.secrets.get("OPENAI_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Paste OpenAI Key (temp for testing)", type="password")

if not api_key:
    st.error("Add OPENAI_API_KEY to Secrets tab or paste here! platform.openai.com/api-keys")
    st.stop()

llm = OpenAI(openai_api_key=api_key, temperature=0.7)
memory = ConversationBufferMemory()
conversation = ConversationChain(llm=llm, memory=memory)

# Chat UI unchanged...
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask anything!"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        response = conversation.predict(input=prompt)
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})