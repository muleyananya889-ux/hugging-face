# Hugging Face AI Application

A complete web application that integrates with Hugging Face models to provide AI-powered responses.

## Features
- Integration with Hugging Face models (DeepSeek, Kimi, etc.)
- Modern web interface
- API key management
- Real-time responses
- Model selection

## Setup Instructions

1. **Hugging Face Account Setup**
   - Create account at [huggingface.co](https://huggingface.co)
   - Verify email and enable 2FA
   - Generate API token from Settings > Access Tokens

2. **Model Selection**
   - Browse models at [huggingface.co/models](https://huggingface.co/models)
   - Recommended models:
     - `deepseek-ai/DeepSeek-R1` - Advanced reasoning
     - `microsoft/DialoGPT-medium` - Conversational AI
     - `sentence-transformers/all-MiniLM-L6-v2` - Text embeddings

3. **Space Creation**
   - Go to [huggingface.co/spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Choose SDK: Gradio or Streamlit
   - Set visibility (Public/Private)
   - Select hardware (CPU/GPU)

4. **Deployment**
   - Upload your application files
   - Configure requirements.txt
   - Set environment variables for API keys
   - Deploy and test

5. **API Integration**
   - Use Hugging Face Inference API
   - Implement proper error handling
   - Add rate limiting and caching

6. **Frontend & Backend**
   - Modern UI with responsive design
   - RESTful API endpoints
   - Real-time communication
   - User authentication

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variables
export HF_API_KEY="your_huggingface_api_key"

# Run the application
streamlit run app.py
```

## Project Structure
```
├── app.py              # Main Streamlit application
├── backend/
│   ├── api.py          # API integration
│   └── models.py       # Model management
├── frontend/
│   ├── components.py   # UI components
│   └── styles.py       # Styling
├── requirements.txt    # Python dependencies
└── README.md          # This file
```
