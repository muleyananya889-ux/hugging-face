import streamlit as st
import os
from dotenv import load_dotenv
import requests
import json
from typing import Dict, Any
import time

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Hugging Face AI Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        border-left: 4px solid #2196f3;
    }
    .assistant-message {
        background-color: #f3e5f5;
        border-left: 4px solid #9c27b0;
    }
    .model-card {
        padding: 1rem;
        border: 1px solid #ddd;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
    .sidebar-section {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

class HuggingFaceAPI:
    """Handles communication with Hugging Face Inference API"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api-inference.huggingface.co/models"
        
    def get_available_models(self) -> Dict[str, str]:
        """Returns a dictionary of available models"""
        return {
            "DeepSeek-R1": "deepseek-ai/DeepSeek-R1",
            "DialoGPT Medium": "microsoft/DialoGPT-medium", 
            "GPT-2": "gpt2",
            "BLOOM": "bigscience/bloom",
            "LLaMA 2 7B": "meta-llama/Llama-2-7b-chat-hf"
        }
    
    def query_model(self, model_name: str, inputs: str, parameters: Dict[str, Any] = None) -> Dict[str, Any]:
        """Query a specific model with the given inputs"""
        if parameters is None:
            parameters = {
                "max_length": 2048,
                "temperature": 0.7,
                "do_sample": True,
                "top_p": 0.9,
                "top_k": 50
            }
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        try:
            response = requests.post(
                f"{self.api_url}/{model_name}",
                headers=headers,
                json={"inputs": inputs, "parameters": parameters},
                timeout=30
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {
                    "success": False, 
                    "error": f"API Error: {response.status_code} - {response.text}"
                }
                
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": f"Request Error: {str(e)}"}

def main():
    """Main application function"""
    
    # Header
    st.markdown('<h1 class="main-header">🤖 Hugging Face AI Assistant</h1>', unsafe_allow_html=True)
    
    # Sidebar for configuration
    with st.sidebar:
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.header("⚙️ Configuration")
        
        # API Key input
        api_key = st.text_input(
            "Hugging Face API Key",
            type="password",
            placeholder="Enter your HF API key...",
            help="Get your API key from huggingface.co/settings/tokens"
        )
        
        # Model selection
        hf_api = HuggingFaceAPI(api_key) if api_key else None
        available_models = hf_api.get_available_models() if hf_api else {}
        
        selected_model = st.selectbox(
            "Select Model",
            options=list(available_models.keys()),
            help="Choose the AI model to use for responses"
        )
        
        # Parameters
        st.subheader("Model Parameters")
        temperature = st.slider("Temperature", 0.1, 2.0, 0.7, 0.1)
        max_length = st.slider("Max Length", 50, 4096, 2048, 50)
        top_p = st.slider("Top P", 0.1, 1.0, 0.9, 0.1)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Model information
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.header("📊 Model Info")
        if selected_model in available_models:
            st.info(f"**Model ID:** `{available_models[selected_model]}`")
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 Chat Interface")
        
        # Initialize chat history
        if "messages" not in st.session_state:
            st.session_state.messages = []
        
        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])
        
        # Chat input
        if prompt := st.chat_input("Type your message here..."):
            if not api_key:
                st.error("Please enter your Hugging Face API key in the sidebar!")
                return
            
            # Add user message to chat history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)
            
            # Generate assistant response
            with st.chat_message("assistant"):
                message_placeholder = st.empty()
                full_response = ""
                
                # Query the model
                model_id = available_models[selected_model]
                parameters = {
                    "max_length": max_length,
                    "temperature": temperature,
                    "top_p": top_p,
                    "do_sample": True
                }
                
                with st.spinner("Thinking..."):
                    result = hf_api.query_model(model_id, prompt, parameters)
                
                if result["success"]:
                    # Extract the generated text
                    if isinstance(result["data"], list) and len(result["data"]) > 0:
                        generated_text = result["data"][0].get("generated_text", "")
                        # Remove the original prompt from the response
                        if generated_text.startswith(prompt):
                            full_response = generated_text[len(prompt):].strip()
                        else:
                            full_response = generated_text
                    else:
                        full_response = "Sorry, I couldn't generate a response."
                else:
                    full_response = f"Error: {result['error']}"
                
                message_placeholder.markdown(full_response)
            
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
    
    with col2:
        st.header("📈 Quick Actions")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", type="secondary"):
            st.session_state.messages = []
            st.rerun()
        
        # Example prompts
        st.subheader("💡 Example Prompts")
        example_prompts = [
            "Explain quantum computing in simple terms",
            "Write a short story about a robot discovering emotions",
            "What are the benefits of renewable energy?",
            "Create a poem about artificial intelligence",
            "Explain the concept of machine learning"
        ]
        
        for prompt in example_prompts:
            if st.button(prompt, key=f"example_{prompt[:20]}"):
                st.session_state.messages.append({"role": "user", "content": prompt})
                st.rerun()
        
        # Statistics
        st.subheader("📊 Session Stats")
        if st.session_state.messages:
            user_messages = len([m for m in st.session_state.messages if m["role"] == "user"])
            assistant_messages = len([m for m in st.session_state.messages if m["role"] == "assistant"])
            
            col_stats1, col_stats2 = st.columns(2)
            with col_stats1:
                st.metric("User Messages", user_messages)
            with col_stats2:
                st.metric("AI Responses", assistant_messages)

if __name__ == "__main__":
    main()
