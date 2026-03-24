"""
Deployment script for Hugging Face Spaces
This script helps deploy the application to Hugging Face Spaces
"""

import os
import json
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List

class SpaceDeployer:
    """Handles deployment to Hugging Face Spaces"""
    
    def __init__(self, space_name: str, space_type: str = "streamlit"):
        self.space_name = space_name
        self.space_type = space_type
        self.required_files = [
            "app.py",
            "requirements.txt",
            "README.md"
        ]
        
    def create_space_structure(self) -> bool:
        """Create the basic structure for Hugging Face Space"""
        try:
            # Create necessary directories
            os.makedirs("backend", exist_ok=True)
            os.makedirs("frontend", exist_ok=True)
            
            # Create __init__.py files
            Path("backend/__init__.py").touch()
            Path("frontend/__init__.py").touch()
            
            print("✅ Space structure created successfully")
            return True
            
        except Exception as e:
            print(f"❌ Error creating space structure: {str(e)}")
            return False
    
    def generate_space_config(self) -> Dict[str, Any]:
        """Generate configuration for Hugging Face Space"""
        if self.space_type == "streamlit":
            return {
                "title": "Hugging Face AI Assistant",
                "emoji": "🤖",
                "colorFrom": "blue",
                "colorTo": "purple",
                "sdk": "streamlit",
                "sdk_version": "1.28.0",
                "app_file": "app.py",
                "pinned": False,
                "license": "mit",
                "python_version": "3.9"
            }
        elif self.space_type == "gradio":
            return {
                "title": "Hugging Face AI Assistant",
                "emoji": "🤖",
                "colorFrom": "blue",
                "colorTo": "purple",
                "sdk": "gradio",
                "sdk_version": "4.0.0",
                "app_file": "app.py",
                "pinned": False,
                "license": "mit",
                "python_version": "3.9"
            }
        else:
            raise ValueError(f"Unsupported space type: {self.space_type}")
    
    def create_space_readme(self) -> str:
        """Create README for Hugging Face Space"""
        return f"""
---
title: Hugging Face AI Assistant
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: streamlit
sdk_version: 1.28.0
app_file: app.py
pinned: false
license: mit
python_version: 3.9
---

# Hugging Face AI Assistant

A modern web application that integrates with Hugging Face models to provide AI-powered responses.

## Features

- 🤖 Multiple AI model support (DeepSeek, GPT-2, BLOOM, LLaMA, etc.)
- 💬 Real-time chat interface
- ⚙️ Adjustable model parameters
- 📊 Usage statistics and analytics
- 🎨 Modern, responsive UI
- 🔐 Secure API key management

## How to Use

1. **Enter your Hugging Face API key** in the sidebar
2. **Select a model** from the available options
3. **Adjust parameters** like temperature and max length
4. **Start chatting** with the AI assistant

## Available Models

- **DeepSeek-R1**: Advanced reasoning capabilities
- **DialoGPT Medium**: Optimized for conversation
- **GPT-2**: Classic text generation
- **BLOOM**: Multilingual support
- **LLaMA 2 7B Chat**: Meta's conversational model

## Model Parameters

- **Temperature**: Controls randomness (0.1-2.0)
- **Max Length**: Maximum response length
- **Top P**: Nucleus sampling parameter
- **Repetition Penalty**: Reduces repetitive responses

## API Integration

This application uses the Hugging Face Inference API to communicate with models. You need:

1. A Hugging Face account
2. An API token from [huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)

## Technical Stack

- **Frontend**: Streamlit
- **Backend**: Python with Hugging Face Transformers
- **API**: Hugging Face Inference API
- **Styling**: Custom CSS with responsive design

## Deployment

This application is designed to run on Hugging Face Spaces. To deploy:

1. Create a new Space at [huggingface.co/spaces](https://huggingface.co/spaces)
2. Upload these files
3. Set your API token as a secret environment variable
4. The app will automatically deploy

## Environment Variables

- `HF_API_KEY`: Your Hugging Face API key
- `HF_MODEL`: Default model to use

## Contributing

Feel free to submit issues and enhancement requests!

## License

MIT License - see LICENSE file for details
"""
    
    def create_gradio_app(self) -> str:
        """Create a Gradio version of the app"""
        return '''
import gradio as gr
import os
import requests
from dotenv import load_dotenv
import json
from typing import Dict, Any

load_dotenv()

class HuggingFaceAPI:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://api-inference.huggingface.co/models"
        
    def query_model(self, model_name: str, inputs: str, parameters: Dict[str, Any] = None):
        if parameters is None:
            parameters = {
                "max_length": 2048,
                "temperature": 0.7,
                "do_sample": True,
                "top_p": 0.9
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
                data = response.json()
                if isinstance(data, list) and len(data) > 0:
                    generated_text = data[0].get("generated_text", "")
                    if generated_text.startswith(inputs):
                        return generated_text[len(inputs):].strip()
                    return generated_text.strip()
                return "Sorry, I couldn't generate a response."
            else:
                return f"Error: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"Error: {str(e)}"

def get_api_key():
    return os.getenv("HF_API_KEY", "")

def chat_fn(message, history, model_name, temperature, max_length, api_key):
    if not api_key:
        return "Please enter your Hugging Face API key."
    
    hf_api = HuggingFaceAPI(api_key)
    
    parameters = {
        "max_length": max_length,
        "temperature": temperature,
        "do_sample": True,
        "top_p": 0.9
    }
    
    # Map model names to IDs
    model_map = {
        "DeepSeek-R1": "deepseek-ai/DeepSeek-R1",
        "DialoGPT Medium": "microsoft/DialoGPT-medium",
        "GPT-2": "gpt2",
        "BLOOM": "bigscience/bloom",
        "LLaMA 2 7B Chat": "meta-llama/Llama-2-7b-chat-hf"
    }
    
    model_id = model_map.get(model_name, model_name)
    
    response = hf_api.query_model(model_id, message, parameters)
    return response

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🤖 Hugging Face AI Assistant")
    
    with gr.Row():
        with gr.Column(scale=2):
            chatbot = gr.Chatbot(height=500)
            msg = gr.Textbox(
                label="Your Message",
                placeholder="Type your message here...",
                lines=2
            )
            
        with gr.Column(scale=1):
            gr.Markdown("### ⚙️ Configuration")
            
            api_key = gr.Textbox(
                label="Hugging Face API Key",
                type="password",
                placeholder="Enter your HF API key...",
                value=get_api_key()
            )
            
            model_name = gr.Dropdown(
                choices=["DeepSeek-R1", "DialoGPT Medium", "GPT-2", "BLOOM", "LLaMA 2 7B Chat"],
                label="Select Model",
                value="DeepSeek-R1"
            )
            
            temperature = gr.Slider(
                minimum=0.1,
                maximum=2.0,
                value=0.7,
                step=0.1,
                label="Temperature"
            )
            
            max_length = gr.Slider(
                minimum=50,
                maximum=4096,
                value=2048,
                step=50,
                label="Max Length"
            )
    
    def respond(message, chat_history, model_name, temperature, max_length, api_key):
        if not message.strip():
            return "", chat_history
        
        bot_message = chat_fn(message, chat_history, model_name, temperature, max_length, api_key)
        chat_history.append((message, bot_message))
        return "", chat_history
    
    msg.submit(
        respond,
        [msg, chatbot, model_name, temperature, max_length, api_key],
        [msg, chatbot]
    )

if __name__ == "__main__":
    demo.launch()
'''
    
    def verify_deployment_readiness(self) -> List[str]:
        """Check if the project is ready for deployment"""
        issues = []
        
        # Check required files
        for file in self.required_files:
            if not os.path.exists(file):
                issues.append(f"Missing required file: {file}")
        
        # Check if app.py is valid
        if os.path.exists("app.py"):
            try:
                with open("app.py", 'r') as f:
                    content = f.read()
                    if "streamlit" not in content and "gradio" not in content:
                        issues.append("app.py should contain Streamlit or Gradio code")
            except Exception as e:
                issues.append(f"Error reading app.py: {str(e)}")
        
        # Check requirements.txt
        if os.path.exists("requirements.txt"):
            try:
                with open("requirements.txt", 'r') as f:
                    requirements = f.read()
                    if "streamlit" not in requirements and "gradio" not in requirements:
                        issues.append("requirements.txt should include streamlit or gradio")
            except Exception as e:
                issues.append(f"Error reading requirements.txt: {str(e)}")
        
        return issues
    
    def create_deployment_package(self) -> bool:
        """Create a deployment package"""
        try:
            # Update README for Space
            with open("README.md", 'w') as f:
                f.write(self.create_space_readme())
            
            print("✅ README.md updated for Space deployment")
            
            # Verify everything is ready
            issues = self.verify_deployment_readiness()
            if issues:
                print("❌ Deployment issues found:")
                for issue in issues:
                    print(f"  - {issue}")
                return False
            
            print("✅ Project is ready for deployment!")
            return True
            
        except Exception as e:
            print(f"❌ Error creating deployment package: {str(e)}")
            return False
    
    def print_deployment_instructions(self):
        """Print instructions for deploying to Hugging Face Spaces"""
        print("""
🚀 DEPLOYMENT INSTRUCTIONS

1. CREATE YOUR SPACE:
   - Go to https://huggingface.co/spaces
   - Click "Create new Space"
   - Choose a name for your space
   - Select SDK: Streamlit
   - Set visibility (Public/Private)
   - Choose hardware (CPU is fine for start)

2. UPLOAD YOUR FILES:
   - Upload all files from this directory
   - Make sure to include:
     ✓ app.py
     ✓ requirements.txt
     ✓ README.md
     ✓ backend/ directory
     ✓ frontend/ directory

3. SET ENVIRONMENT VARIABLES:
   - Go to your Space settings
   - Add Repository Secret: HF_API_KEY
   - Set your Hugging Face API key as the value

4. DEPLOY:
   - The Space will automatically build and deploy
   - Wait for the build to complete
   - Your app will be available at the Space URL

5. TEST YOUR APP:
   - Enter your API key in the sidebar
   - Select a model
   - Start chatting!

📝 TIPS:
- Use GPU for faster responses with large models
- Monitor your API usage to avoid rate limits
- Keep your API key secure and never commit it to git
- Consider using a model-specific API key for better security

🔗 USEFUL LINKS:
- Hugging Face Spaces: https://huggingface.co/spaces
- API Tokens: https://huggingface.co/settings/tokens
- Models: https://huggingface.co/models
- Documentation: https://huggingface.co/docs/hub/spaces
""")

def main():
    """Main deployment function"""
    print("🚀 Hugging Face Space Deployment Helper")
    print("=" * 50)
    
    # Get space name from user
    space_name = input("Enter your desired Space name: ").strip()
    if not space_name:
        space_name = "hf-ai-assistant"
        print(f"Using default name: {space_name}")
    
    # Create deployer
    deployer = SpaceDeployer(space_name)
    
    # Create space structure
    print("\n📁 Creating Space structure...")
    if not deployer.create_space_structure():
        print("❌ Failed to create space structure")
        return
    
    # Create deployment package
    print("\n📦 Creating deployment package...")
    if not deployer.create_deployment_package():
        print("❌ Failed to create deployment package")
        return
    
    # Print instructions
    print("\n📋 Deployment Instructions:")
    deployer.print_deployment_instructions()
    
    print(f"\n✅ Your Space '{space_name}' is ready for deployment!")
    print("🌐 Follow the instructions above to deploy to Hugging Face Spaces")

if __name__ == "__main__":
    main()
