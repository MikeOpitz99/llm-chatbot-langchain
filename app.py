import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, AIMessage

st.title("🤖 FREE Groq Chatbot - No Hassle!")

api_key = st.secrets.get("GROQ_API_KEY")
if not api_key:
    api_key = st.sidebar.text_input("Groq API Key (free: console.groq.com/keys)", type="password")

if not api_key:
    st.stop()

os.environ["GROQ_API_KEY"] = api_key

@st.cache_resource
def get_llm():
    return ChatGroq(model="llama3-8b-8192", temperature=0.7)

llm = get_llm()

if "messages" not in st.session_state:
    st.session_state.messages = []

# Show chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# New message
if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Simple prompt with history
        history = ""
        for m in st.session_state.messages[-10:]:  # Last 10 msgs
            role = "Human" if m["role"] == "user" else "Assistant"
            history += f"{role}: {m['content']}\n"

        full_prompt = f"{history}Human: {prompt}\nAssistant:"
        response = llm.invoke(full_prompt)
        content = response.content
        st.markdown(content)
        st.session_state.messages.append({"role": "assistant", "content": content})
