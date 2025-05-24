import streamlit as st
import os
from google import genai
from google.genai import types
import tempfile
import pathlib

# Configure the page
st.set_page_config(
    page_title="Smart Manual Assistant",
    page_icon="🔧",
    layout="wide"
)

# Initialize Gemini client
@st.cache_resource
def init_gemini():
    # You'll need to set your API key as an environment variable
    # export GOOGLE_API_KEY="your_api_key_here"
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        st.error("Please set your GOOGLE_API_KEY environment variable")
        st.stop()
    
    client = genai.Client(api_key=api_key)
    return client

client = init_gemini()

# Title and description
st.title("🔧 Smart Manual Assistant")
st.markdown("Upload a technical manual and ask questions about repairs and maintenance.")

# Create two columns
col1, col2 = st.columns([1, 2])

# Left column - PDF Upload/Selection
with col1:
    st.header("📁 Select Manual")
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Upload PDF Manual",
        type=['pdf'],
        help="Upload a technical manual (up to 50MB)"
    )
    
    # Store uploaded file info in session state
    if uploaded_file is not None:
        if 'current_file' not in st.session_state or st.session_state.current_file != uploaded_file.name:
            st.session_state.current_file = uploaded_file.name
            st.session_state.gemini_file = None
            st.session_state.messages = []
        
        # Upload to Gemini File API
        if st.session_state.gemini_file is None:
            with st.spinner(f"Processing {uploaded_file.name}..."):
                try:
                    # Create temporary file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = pathlib.Path(tmp_file.name)
                    
                    # Upload to Gemini File API
                    gemini_file = client.files.upload(file=tmp_path)
                    st.session_state.gemini_file = gemini_file
                    
                    # Clean up temp file
                    os.unlink(tmp_path)
                    
                    st.success(f"✅ {uploaded_file.name} processed successfully!")
                    
                except Exception as e:
                    st.error(f"Error processing file: {str(e)}")
        else:
            st.success(f"✅ {uploaded_file.name} ready for questions!")

# Right column - Chat Interface
with col2:
    st.header("💬 Ask Questions")
    
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input - process if there's a new message
    if prompt := st.chat_input("Ask about repairs, maintenance, troubleshooting..."):
        if 'gemini_file' not in st.session_state or st.session_state.gemini_file is None:
            st.error("Please upload a PDF manual first!")
        else:
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            # Generate response
            with st.spinner("Analyzing manual..."):
                try:
                    # System instruction for repair focus
                    system_instruction = """You are an expert equipment technician and repair specialist. 
                    You have access to this technical service manual. When answering questions about repairs, maintenance, and troubleshooting:
                    
                    - Always cite specific page numbers when referencing procedures (e.g., "See page 45")
                    - Provide step-by-step instructions when applicable
                    - Mention any safety warnings or precautions from the manual
                    - If you're unsure about something, say so rather than guessing
                    - Focus on practical repair and maintenance guidance
                    - Answer directly and conversationally"""
                    
                    # Build conversation history
                    contents = []
                    
                    # Always include the file first
                    contents.append(st.session_state.gemini_file)
                    
                    # Add the system instruction
                    contents.append(types.Content(
                        role="user",
                        parts=[types.Part(text=system_instruction)]
                    ))
                    contents.append(types.Content(
                        role="model", 
                        parts=[types.Part(text="I understand. As an expert equipment technician, I'm here to provide accurate, practical guidance from this manual. When you ask about a specific repair, maintenance, or troubleshooting topic, I will provide step-by-step instructions, citing manual page numbers and relevant safety information.")]
                    ))
                    
                    # Add conversation history
                    for msg in st.session_state.messages[:-1]:  # Exclude the last message we just added
                        contents.append(types.Content(
                            role="user" if msg["role"] == "user" else "model",
                            parts=[types.Part(text=msg["content"])]
                        ))
                    
                    # Add current prompt
                    contents.append(types.Content(
                        role="user",
                        parts=[types.Part(text=prompt)]
                    ))
                    
                    response = client.models.generate_content(
                        model="gemini-2.5-flash-preview-05-20",
                        contents=contents
                    )
                    
                    response_text = response.text
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response_text})
                    
                    # Rerun to display the new messages
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error generating response: {str(e)}")
                    st.session_state.messages.append({"role": "assistant", "content": f"Sorry, I encountered an error: {str(e)}"})
                    st.rerun()

# Sidebar with instructions
with st.sidebar:
    st.header("📋 How to Use")
    st.markdown("""
    1. **Upload** a PDF technical manual
    2. **Wait** for processing (may take a moment)
    3. **Ask** questions about:
       - Troubleshooting procedures
       - Repair instructions
       - Maintenance schedules
       - Part specifications
       - Safety procedures
    
    **Example questions:**
    - "How do I troubleshoot hydraulic pressure loss?"
    - "What's the procedure for changing engine oil?"
    - "Where is the fuel filter located?"
    - "What are the torque specifications for the cylinder head?"
    """)
    
    st.header("⚠️ Important Notes")
    st.markdown("""
    - Files are stored securely for 48 hours
    - Maximum file size: 50MB
    - Always follow safety procedures
    - Verify critical information with official sources
    """)
    
    # Clear chat button
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()