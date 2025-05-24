# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Application Overview

This is a Streamlit-based Smart Manual Assistant application that allows users to upload PDF technical manuals and ask questions about repairs and maintenance using Google's Gemini AI.

### Key Architecture Components

- **Main Application**: `app.py` - Single-file Streamlit application with two-column layout
- **AI Integration**: Uses Google Gemini AI via the `google-genai` library for document analysis and Q&A
- **File Processing**: Uploads PDFs to Gemini File API for persistent document context
- **Chat Interface**: Maintains conversation history with system instructions for repair-focused responses

### Core Functionality Flow

1. User uploads PDF manual via Streamlit file uploader
2. File is temporarily saved and uploaded to Gemini File API
3. Chat interface processes user questions with full document context
4. System instruction configures AI as an "expert equipment technician"
5. Responses include page citations and step-by-step repair guidance

## Development Commands

### Running the Application
```bash
streamlit run app.py
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Environment Setup
Required environment variable:
```bash
export GOOGLE_API_KEY="your_api_key_here"
```

## Important Implementation Details

- **Session State Management**: Uses `st.session_state` to maintain uploaded file, chat history, and Gemini file references
- **File Handling**: Creates temporary files for Gemini upload, automatically cleans up after processing
- **Error Handling**: Comprehensive try-catch blocks for file processing and AI response generation
- **AI Model**: Currently configured to use `gemini-2.5-flash-preview-05-20`
- **System Instruction**: Pre-configured to focus on repair/maintenance guidance with page citations