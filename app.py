import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
import os
#Load company Knowledge
with open("company_knowledge.txt","r")as file:
    company_knowlege=file.read()
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
st.title("24/7 AI Support Agent🤖")
st.caption("Powered by LLM + Custom Business Knowlege")
uploaded_file = st.file_uploader("Upload your business FAQ", type="txt")
if st.button("Clear Conversations"):
    st.session_state.messages = []
    st.rerun ()
business_info = ""
if uploaded_file is not None:
    business_info = uploaded_file.read().decode("utf-8")
    if business_info == "":
        st.warning("Please upload a business FAQ file to activate the AI support agent.")
        st.stop()
# Store chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
# Show previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])
#User input
prompt = st.chat_input("Ask a question about our business....")
if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)
        system_prompt ={
            "role": "system",
            "content":"""
            You are an AI customer support agent for an ecommerce company.
            Use the company knowlege belowto answer all questions
            {company_knowledge}
            Rules:
            -Be friendly and professional
            -Only give answers based on the knowledge provided
            -Refund policy is 30 days
            -If you dont know something, say you will escalate to human support
            """
        }
        messages = [system_prompt] + st.session_state.messages
        response = client.chat.completions.create(
            model = "gpt-4.1-mini",
            messages=messages
        )
        reply = response.choices[0].message.content
        st.session_state.messages.append(
            {"role": "assistant", "content":reply}
        )
        with st.chat_message("assistant"):
            st.write(reply)