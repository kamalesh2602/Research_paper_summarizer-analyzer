import streamlit as st
import requests
import json

# Define the backend URL
BACKEND_URL = "http://localhost:8000"

st.set_page_config(page_title="Research Paper Analyzer", layout="wide")

st.title("📚 Research Paper Summarizer & Analyzer")
st.markdown("Upload your research papers (PDF, TXT, DOCX) and use AI to summarize, analyze, and chat with them.")

# Sidebar for Uploads
with st.sidebar:
    st.header("1. Document Ingestion")
    uploaded_files = st.file_uploader(
        "Upload Papers", 
        type=["pdf", "txt", "docx"], 
        accept_multiple_files=True
    )
    
    if st.button("Process Documents"):
        if uploaded_files:
            with st.spinner("Processing & embedding documents..."):
                files_payload = []
                for file in uploaded_files:
                    files_payload.append(
                        ("files", (file.name, file.getvalue(), file.type))
                    )
                
                try:
                    res = requests.post(f"{BACKEND_URL}/upload", files=files_payload)
                    if res.status_code == 200:
                        st.success(f"Success! {res.json().get('chunks_count')} chunks created.")
                    else:
                        st.error(f"Error: {res.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")
        else:
            st.warning("Please upload at least one file first.")

st.divider()

# Main area for Summarize, Analyze, Chat
tab1, tab2, tab3 = st.tabs(["📝 Summarize", "🔍 Analyze", "💬 Chat"])

with tab1:
    st.header("Document Summary")
    if st.button("Generate Summary"):
        with st.spinner("Summarizer Agent is working..."):
            try:
                res = requests.get(f"{BACKEND_URL}/summarize")
                if res.status_code == 200:
                    data = res.json()
                    if "error" in data:
                        st.error("Failed to generate structural summary. Raw output:")
                        st.write(data["raw"])
                    else:
                        st.subheader("Title")
                        st.write(data.get("Title", "N/A"))
                        st.subheader("Abstract")
                        st.write(data.get("Abstract", "N/A"))
                        st.subheader("Methodology")
                        st.write(data.get("Methodology", "N/A"))
                        st.subheader("Key Findings")
                        st.write(data.get("Key Findings", "N/A"))
                        st.subheader("Conclusion")
                        st.write(data.get("Conclusion", "N/A"))
                else:
                    st.error(f"Error: {res.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")

with tab2:
    st.header("Critical Analysis")
    if st.button("Generate Analysis"):
        with st.spinner("Analyzer Agent is working..."):
            try:
                res = requests.get(f"{BACKEND_URL}/analyze")
                if res.status_code == 200:
                    data = res.json()
                    if "error" in data:
                        st.error("Failed to generate structural analysis. Raw output:")
                        st.write(data["raw"])
                    else:
                        st.subheader("Strengths")
                        st.write(data.get("Strengths", "N/A"))
                        st.subheader("Weaknesses")
                        st.write(data.get("Weaknesses", "N/A"))
                        st.subheader("Novelty")
                        st.write(data.get("Novelty", "N/A"))
                        st.subheader("Limitations")
                        st.write(data.get("Limitations", "N/A"))
                        st.subheader("Suggestions")
                        st.write(data.get("Suggestions", "N/A"))
                else:
                    st.error(f"Error: {res.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")

with tab3:
    st.header("Chat with Documents")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # React to user input
    if prompt := st.chat_input("Ask a question about your documents..."):
        # Display user message in chat message container
        st.chat_message("user").markdown(prompt)
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Thinking..."):
            try:
                res = requests.post(f"{BACKEND_URL}/chat", json={"query": prompt})
                if res.status_code == 200:
                    response_text = res.json().get("response", "No response.")
                    with st.chat_message("assistant"):
                        st.markdown(response_text)
                        with st.expander("Show retrieved context"):
                            st.write(res.json().get("context_used", ""))
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                else:
                    st.error(f"Error: {res.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")
