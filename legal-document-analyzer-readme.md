# Legal Document Analyzer

## Overview
The Legal Document Analyzer is an AI-powered application that helps users understand, analyze, and extract important information from legal documents. Built with Streamlit and powered by Google's Gemini AI, this tool offers three primary functions:

1. **Document Summarization**: Concisely outlines the key points and overall purpose of legal documents
2. **Risk Detection**: Identifies potential issues, ambiguities, and liabilities within the text
3. **Key Clause Highlighting**: Extracts and explains critical sections and clauses

## Features
- **Multiple Document Format Support**: Upload documents in PDF, DOCX, or TXT formats
- **Interactive Chat Interface**: Ask specific questions about your documents
- **Three Analysis Modes**: Summarize, detect risks, or highlight key clauses with a single click
- **Conversation History**: Maintain separate chat sessions for different documents
- **User-Friendly Interface**: Clean, intuitive design with sidebar navigation

## Technical Details
- **Frontend**: Streamlit
- **AI Backend**: Google's Generative AI (Gemini Pro)
- **Document Processing**: PyPDF2 for PDF files, python-docx for Word documents

## Installation

### Prerequisites
- Python 3.8+
- Gemini API key from [Google AI Studio](https://makersuite.google.com/)

### Setup Instructions

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/legal-document-analyzer.git
   cd legal-document-analyzer
   ```

2. Install required dependencies:
   ```bash
   pip install streamlit google-generativeai pypdf2 python-docx pandas
   ```

3. Set up your Gemini API key:
   
   Option 1: Create a Streamlit secrets file `.streamlit/secrets.toml`:
   ```toml
   GEMINI_API_KEY = "your-api-key-here"
   ```
   
   Option 2: Enter the API key when prompted by the application

4. Run the application:
   ```bash
   streamlit run app.py
   ```

## Usage Guide

1. **Upload Document**: Use the sidebar to upload your legal document
2. **Select Analysis Type**: Choose one of the three analysis buttons:
   - 📄 Summarize Document
   - ⚠️ Detect Risks 
   - 🔍 Highlight Key Clauses
3. **Chat Interface**: Ask follow-up questions about the document using the chat input
4. **Manage Conversations**: Create new chats or switch between previous sessions using the sidebar

## Example Use Cases

- Contract review and analysis before signing
- Quick understanding of complex legal agreements
- Identifying potential issues in terms of service
- Academic research on legal documents
- Legal document preparation and review

## Limitations

- Document size: Very large documents may be truncated due to API token limits
- AI analysis: While powerful, the AI-generated insights should supplement, not replace, professional legal advice
- Language support: Currently optimized for documents in English

## Future Improvements

- Multi-language support
- Document comparison functionality
- Enhanced document parsing for more complex layouts
- Template-specific analysis for common legal document types
- Export functionality for analysis results

## Disclaimer

This application is designed to assist with understanding legal documents but is not a substitute for professional legal advice. Always consult with a qualified legal professional for important legal matters.
