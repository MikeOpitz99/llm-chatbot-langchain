import streamlit as st
from langchain.llms import OpenAI
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory

st.title("?? Smart LLM Chatbot")

# Get OpenAI API key from user (or use env var)
api_key = st.sidebar.text_input("OpenAI API Key", type="password")
if api_key:
    llm = OpenAI(openai_api_key=api_key, temperature=0.7)
    memory = ConversationBufferMemory()
    conversation = ConversationChain(llm=llm, memory=memory)
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    if prompt := st.chat_input("Ask me anything!"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        with st.chat_message("assistant"):
            response = conversation.predict(input=prompt)
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})