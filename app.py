import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage  # For history

st.title("🤖 talk to a robot for FREE?? - Perfect!")

api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Groq API Key (gsk_... from console.groq.com/keys)", type="password")

if not api_key:
    st.info("📱 Get free key & paste!")
    st.stop()

os.environ["GROQ_API_KEY"] = api_key

@st.cache_resource
def get_llm():
    return ChatGroq(model="llama3-8b-8192", temperature=0.7)  # Confirmed model

llm = ChatGroq(model="llama-3.1-8b-instant", temperature=0.7) 

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
        # FIXED: List of messages (Groq format)
        history = []
        for m in st.session_state.messages[:-1]:  # All but last (current prompt)
            if m["role"] == "user":
                history.append(HumanMessage(content=m["content"]))
            else:
                history.append(AIMessage(content=m["content"]))

        # Invoke with history + current
        response = llm.invoke(history + [HumanMessage(content=prompt)])
        content = response.content
        st.markdown(content)
        st.session_state.messages.append({"role": "assistant", "content": content})
