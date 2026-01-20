import streamlit as st
from google import genai
from google.genai import types
import os

# 1. Setup Page Config
st.set_page_config(page_title="Financial Data Bot", page_icon="📈")
st.title("🤖 Financial Data Analysis Bot")
st.markdown("Ask questions about your **holdings** and **trades** using AI-powered code execution.")

# 2. Securely get API Key
api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")
if not api_key:
    st.info("Please enter your Gemini API Key in the sidebar to continue.", icon="🗝️")
    st.stop()

client = genai.Client(api_key=api_key)

# 3. Load Multiple Data Files
@st.cache_resource
def upload_data_files():
    files_to_upload = ['holdings.csv', 'trades.csv']
    uploaded_file_objects = []
    
    try:
        for file_name in files_to_upload:
            # This looks for the files in the same folder as app.py
            if os.path.exists(file_name):
                file_obj = client.files.upload(file=file_name)
                uploaded_file_objects.append(file_obj)
            else:
                st.warning(f"File {file_name} not found in directory. Please add it to your repo.")
        return uploaded_file_objects
    except Exception as e:
        st.error(f"Error uploading data to Gemini: {e}")
        return None

# Get the list of file objects for the chat
data_files = upload_data_files()

def chat_with_data(query):
    system_prompt = (
        "You are a specialized Financial Data Bot. You have access to two files: 'holdings.csv' and 'trades.csv'. "
        "1. Use the code_execution tool to analyze data across BOTH files to find answers. "
        "2. For holdings questions, refer to 'holdings.csv'. For transaction/history questions, refer to 'trades.csv'. "
        "3. When calculating totals, sum ALL relevant rows in the dataframes. "
        "4. IF THE ANSWER IS NOT FOUND, respond with: 'Sorry, I cannot find that information in the provided data.' "
        "5. Do not use outside knowledge."
    )

    tools_config = [{'code_execution': {}}]

    # We pass the list of files [holdings, trades] in the contents
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        config=types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=tools_config,
            temperature=0.0
        ),
        contents=data_files + [query]
    )
    return response.text

# 4. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ex: What was my total profit from trades in January?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing holdings and trades..."):
            answer = chat_with_data(prompt)
            st.markdown(answer)
    
    st.session_state.messages.append({"role": "assistant", "content": answer})