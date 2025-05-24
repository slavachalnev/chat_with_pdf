# Smart Manual Assistant

A Streamlit-based application that allows users to upload PDF technical manuals and ask questions about repairs and maintenance using Google's Gemini AI.

## Setup

1. Clone the repository:
```bash
git clone git@github.com:slavachalnev/chat_with_pdf.git
cd chat_with_pdf
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set your Google API key:
```bash
export GOOGLE_API_KEY="your_api_key_here"
```

## Running the Application

```bash
streamlit run app.py
```

The application will open in your web browser. Upload a PDF manual and start asking questions about repairs and maintenance!