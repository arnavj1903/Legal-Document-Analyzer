import streamlit as st
import google.generativeai as genai
import os
import tempfile
import uuid
from datetime import datetime
import pandas as pd
import json
from PyPDF2 import PdfReader
import docx

# Configure page settings
st.set_page_config(
    page_title="Legal Document Analyzer",
    page_icon="⚖️",
    layout="wide"
)

# Initialize session state variables if they don't exist
if 'chats' not in st.session_state:
    st.session_state.chats = {}
if 'current_chat_id' not in st.session_state:
    st.session_state.current_chat_id = None
if 'document_content' not in st.session_state:
    st.session_state.document_content = None
if 'document_name' not in st.session_state:
    st.session_state.document_name = None

# Function to configure the Gemini API
def configure_gemini_api():
    api_key = st.secrets.get("GEMINI_API_KEY", None)
    if api_key is None:
        api_key = st.text_input("Enter your Gemini API Key:", type="password")
        if not api_key:
            st.warning("Please enter a valid Gemini API key to continue.")
            st.stop()
    
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-pro')

# Function to process different document types
def process_document(uploaded_file):
    file_extension = uploaded_file.name.split('.')[-1].lower()
    content = ""
    
    if file_extension == 'pdf':
        pdf_reader = PdfReader(uploaded_file)
        for page in pdf_reader.pages:
            content += page.extract_text() + "\n"
    
    elif file_extension in ['docx', 'doc']:
        doc = docx.Document(uploaded_file)
        for para in doc.paragraphs:
            content += para.text + "\n"
    
    elif file_extension == 'txt':
        content = uploaded_file.getvalue().decode('utf-8')
    
    else:
        st.error(f"Unsupported file format: {file_extension}")
        return None
    
    return content

# Function to create a new chat
def create_new_chat():
    chat_id = str(uuid.uuid4())
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    st.session_state.chats[chat_id] = {
        "title": f"Chat {len(st.session_state.chats) + 1}",
        "created_at": current_time,
        "messages": []
    }
    
    return chat_id

# Function to save chat message
def save_message(chat_id, role, content):
    if chat_id not in st.session_state.chats:
        chat_id = create_new_chat()
    
    st.session_state.chats[chat_id]["messages"].append({
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })

# Function to summarize the document
def summarize_document(model, document_content):
    prompt = f"""
    Please provide a comprehensive summary of the following legal document. Focus on:
    1. The main purpose of the document
    2. The key parties involved
    3. Main obligations and rights
    4. Important dates and deadlines
    5. Structure of the document

    Document content:
    {document_content[:30000]}  # Limiting to prevent token overflow
    """
    
    response = model.generate_content(prompt)
    return response.text

# Function to detect risks in the document
def detect_risks(model, document_content):
    prompt = f"""
    Analyze the following legal document for potential risks and issues. Please identify:
    1. Vague or ambiguous clauses
    2. Unfavorable terms or conditions
    3. Missing provisions or protections
    4. Compliance concerns
    5. Liability risks
    6. Termination risks
    7. Any other potential legal issues

    Document content:
    {document_content[:30000]}  # Limiting to prevent token overflow
    """
    
    response = model.generate_content(prompt)
    return response.text

# Function to highlight key clauses
def highlight_key_clauses(model, document_content):
    prompt = f"""
    Review the following legal document and identify the most important clauses. For each key clause:
    1. Provide the section number/name
    2. Summarize what the clause covers
    3. Explain why this clause is significant
    4. Mention any potential negotiation points or considerations

    Document content:
    {document_content[:30000]}  # Limiting to prevent token overflow
    """
    
    response = model.generate_content(prompt)
    return response.text

# Setting up the sidebar
with st.sidebar:
    st.title("Legal Document Analyzer")
    
    # Document upload section
    st.header("Upload Document")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "docx", "doc", "txt"])
    
    if uploaded_file is not None:
        st.session_state.document_name = uploaded_file.name
        document_content = process_document(uploaded_file)
        
        if document_content:
            st.session_state.document_content = document_content
            st.success(f"Document processed: {uploaded_file.name}")
            
            # If this is the first document upload, create a new chat
            if st.session_state.current_chat_id is None:
                st.session_state.current_chat_id = create_new_chat()
                st.session_state.chats[st.session_state.current_chat_id]["title"] = f"Analysis of {uploaded_file.name}"
    
    # Chat history section
    st.header("Chat History")
    
    # Button to create a new chat
    if st.button("New Chat"):
        st.session_state.current_chat_id = create_new_chat()
    
    # Display existing chats
    for chat_id, chat_data in st.session_state.chats.items():
        if st.sidebar.button(f"{chat_data['title']}", key=f"chat_{chat_id}"):
            st.session_state.current_chat_id = chat_id

# Main content area
if st.session_state.current_chat_id is not None:
    current_chat = st.session_state.chats[st.session_state.current_chat_id]
    
    # Display current document being analyzed
    if st.session_state.document_name:
        st.info(f"Current document: {st.session_state.document_name}")
    
    # Chat title
    st.header(current_chat["title"])
    
    # Display chat messages
    for message in current_chat["messages"]:
        if message["role"] == "user":
            st.chat_message("user").write(message["content"])
        else:
            st.chat_message("assistant").write(message["content"])
    
    # Analysis buttons
    if st.session_state.document_content:
        col1, col2, col3 = st.columns(3)
        
        model = configure_gemini_api()
        
        with col1:
            if st.button("📄 Summarize Document"):
                with st.spinner("Generating summary..."):
                    summary = summarize_document(model, st.session_state.document_content)
                    save_message(st.session_state.current_chat_id, "user", "Please summarize this document.")
                    save_message(st.session_state.current_chat_id, "assistant", summary)
                    st.rerun()
        
        with col2:
            if st.button("⚠️ Detect Risks"):
                with st.spinner("Analyzing risks..."):
                    risks = detect_risks(model, st.session_state.document_content)
                    save_message(st.session_state.current_chat_id, "user", "Please identify risks in this document.")
                    save_message(st.session_state.current_chat_id, "assistant", risks)
                    st.rerun()
        
        with col3:
            if st.button("🔍 Highlight Key Clauses"):
                with st.spinner("Identifying key clauses..."):
                    clauses = highlight_key_clauses(model, st.session_state.document_content)
                    save_message(st.session_state.current_chat_id, "user", "Please highlight key clauses in this document.")
                    save_message(st.session_state.current_chat_id, "assistant", clauses)
                    st.rerun()
    
    # Chatbot interface
    user_input = st.chat_input("Ask a question about the document...")
    
    if user_input:
        if not st.session_state.document_content:
            st.error("Please upload a document first.")
        else:
            # Display user message
            st.chat_message("user").write(user_input)
            save_message(st.session_state.current_chat_id, "user", user_input)
            
            # Generate response
            with st.spinner("Thinking..."):
                model = configure_gemini_api()
                prompt = f"""
                Based on the following legal document, please answer this question:
                {user_input}
                
                Document content:
                {st.session_state.document_content[:30000]}
                """
                
                response = model.generate_content(prompt)
                
                # Display assistant response
                st.chat_message("assistant").write(response.text)
                save_message(st.session_state.current_chat_id, "assistant", response.text)

else:
    st.header("Legal Document Analyzer")
    st.write("Upload a document and start a new chat to begin analysis.")
    
    # Create a new chat if none exists
    if not st.session_state.chats:
        st.info("Start by uploading a document in the sidebar.")

# Add some styling
st.markdown("""
<style>
    .stButton button {
        width: 100%;
        border-radius: 5px;
        font-weight: bold;
    }
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
</style>
""", unsafe_allow_html=True)