"""
Vercel serverless function for Hugging Face AI Assistant
"""

import json
import os
from http.server import BaseHTTPRequestHandler

class handler(BaseHTTPRequestHandler):
    """Vercel serverless handler"""
    
    def do_GET(self):
        """Handle GET requests"""
        try:
            # Set environment variables
            api_key = os.environ.get('HF_API_KEY', '')
            model = os.environ.get('HF_MODEL', 'deepseek-ai/DeepSeek-R1')
            
            # Return HTML page
            html_content = f'''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hugging Face AI Assistant</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .gradient-bg {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }}
        .chat-container {{
            max-height: 500px;
            overflow-y: auto;
        }}
        .user-message {{
            background: #e3f2fd;
            border-radius: 18px 18px 4px 18px;
            margin-left: auto;
            max-width: 70%;
        }}
        .assistant-message {{
            background: #f3e5f5;
            border-radius: 18px 18px 18px 4px;
            margin-right: auto;
            max-width: 70%;
        }}
    </style>
</head>
<body class="gradient-bg min-h-screen">
    <div class="container mx-auto px-4 py-8">
        <div class="bg-white rounded-2xl shadow-2xl p-6 max-w-4xl mx-auto">
            <h1 class="text-3xl font-bold text-center mb-8 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                🤖 Hugging Face AI Assistant
            </h1>
            
            <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
                <div class="bg-gray-50 p-4 rounded-lg">
                    <h3 class="font-semibold mb-2">🔑 API Key</h3>
                    <input type="password" id="apiKey" placeholder="Enter HF API Key" 
                           class="w-full p-2 border rounded" value="{api_key}">
                </div>
                
                <div class="bg-gray-50 p-4 rounded-lg">
                    <h3 class="font-semibold mb-2">🤖 Model</h3>
                    <select id="model" class="w-full p-2 border rounded">
                        <option value="deepseek-ai/DeepSeek-R1">DeepSeek-R1</option>
                        <option value="microsoft/DialoGPT-medium">DialoGPT Medium</option>
                        <option value="gpt2">GPT-2</option>
                        <option value="bigscience/bloom">BLOOM</option>
                    </select>
                </div>
                
                <div class="bg-gray-50 p-4 rounded-lg">
                    <h3 class="font-semibold mb-2">⚙️ Temperature</h3>
                    <input type="range" id="temperature" min="0.1" max="2.0" step="0.1" value="0.7" 
                           class="w-full">
                    <span id="tempValue">0.7</span>
                </div>
            </div>
            
            <div class="chat-container bg-gray-50 rounded-lg p-4 mb-4" id="chatContainer">
                <div class="text-center text-gray-500 py-8">
                    <div class="text-4xl mb-4">💬</div>
                    <p>Start a conversation with the AI assistant!</p>
                </div>
            </div>
            
            <div class="flex gap-2">
                <input type="text" id="messageInput" placeholder="Type your message here..." 
                       class="flex-1 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                <button onclick="sendMessage()" 
                        class="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg hover:opacity-90 transition">
                    Send
                </button>
            </div>
            
            <div class="mt-4 text-center">
                <button onclick="clearChat()" class="text-gray-500 hover:text-gray-700">
                    🗑️ Clear Chat
                </button>
            </div>
        </div>
    </div>

    <script>
        let chatHistory = [];
        
        // Update temperature display
        document.getElementById('temperature').addEventListener('input', function(e) {{
            document.getElementById('tempValue').textContent = e.target.value;
        }});
        
        // Send message on Enter
        document.getElementById('messageInput').addEventListener('keypress', function(e) {{
            if (e.key === 'Enter') {{
                sendMessage();
            }}
        }});
        
        async function sendMessage() {{
            const messageInput = document.getElementById('messageInput');
            const message = messageInput.value.trim();
            
            if (!message) return;
            
            const apiKey = document.getElementById('apiKey').value;
            if (!apiKey) {{
                alert('Please enter your Hugging Face API key');
                return;
            }}
            
            // Add user message to chat
            addMessage('user', message);
            messageInput.value = '';
            
            // Show loading
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'text-center py-2';
            loadingDiv.innerHTML = '<div class="inline-block animate-spin rounded-full h-4 w-4 border-b-2 border-blue-600"></div> Thinking...';
            document.getElementById('chatContainer').appendChild(loadingDiv);
            
            try {{
                const response = await fetch('/api/chat', {{
                    method: 'POST',
                    headers: {{
                        'Content-Type': 'application/json',
                    }},
                    body: JSON.stringify({{
                        message: message,
                        apiKey: apiKey,
                        model: document.getElementById('model').value,
                        temperature: parseFloat(document.getElementById('temperature').value)
                    }})
                }});
                
                const data = await response.json();
                
                // Remove loading
                loadingDiv.remove();
                
                if (data.success) {{
                    addMessage('assistant', data.response);
                }} else {{
                    addMessage('assistant', `Error: ${{data.error}}`);
                }}
                
            }} catch (error) {{
                loadingDiv.remove();
                addMessage('assistant', `Error: ${{error.message}}`);
            }}
        }}
        
        function addMessage(role, content) {{
            const chatContainer = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = `p-3 mb-3 rounded-lg ${{role === 'user' ? 'user-message' : 'assistant-message'}}`;
            messageDiv.innerHTML = `
                <div class="font-semibold mb-1">${{role === 'user' ? '👤 You' : '🤖 Assistant'}}</div>
                <div>${{content}}</div>
            `;
            
            // Remove welcome message if it exists
            const welcomeMsg = chatContainer.querySelector('.text-center.text-gray-500');
            if (welcomeMsg) {{
                welcomeMsg.remove();
            }}
            
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }}
        
        function clearChat() {{
            const chatContainer = document.getElementById('chatContainer');
            chatContainer.innerHTML = `
                <div class="text-center text-gray-500 py-8">
                    <div class="text-4xl mb-4">💬</div>
                    <p>Start a conversation with the AI assistant!</p>
                </div>
            `;
            chatHistory = [];
        }}
    </script>
</body>
</html>
            '''
            
            self.send_response(200, html_content)
            
        except Exception as e:
            error_response = f'Error: {str(e)}'
            self.send_response(500, error_response)
    
    def do_POST(self):
        """Handle POST requests for chat API"""
        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            # Parse JSON data
            data = json.loads(post_data.decode('utf-8'))
            message = data.get('message', '')
            api_key = data.get('apiKey', '')
            model = data.get('model', 'deepseek-ai/DeepSeek-R1')
            temperature = data.get('temperature', 0.7)
            
            if not api_key:
                response_data = {'success': False, 'error': 'API key is required'}
                self.send_json_response(400, response_data)
                return
            
            # Call Hugging Face API
            import requests
            
            headers = {'Authorization': f'Bearer {api_key}'}
            payload = {
                'inputs': message,
                'parameters': {
                    'max_length': 2048,
                    'temperature': temperature,
                    'do_sample': True,
                    'top_p': 0.9
                }
            }
            
            response = requests.post(
                f'https://api-inference.huggingface.co/models/{model}',
                headers=headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if isinstance(result, list) and len(result) > 0:
                    generated_text = result[0].get('generated_text', '')
                    if generated_text.startswith(message):
                        clean_response = generated_text[len(message):].strip()
                    else:
                        clean_response = generated_text.strip()
                    
                    response_data = {'success': True, 'response': clean_response}
                else:
                    response_data = {'success': False, 'error': 'No response generated'}
            else:
                response_data = {'success': False, 'error': f'API Error: {response.status_code}'}
            
            self.send_json_response(200, response_data)
            
        except Exception as e:
            response_data = {'success': False, 'error': str(e)}
            self.send_json_response(500, response_data)
    
    def send_response(self, status_code, content):
        """Send HTML response"""
        self.send_response_only(status_code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))
    
    def send_json_response(self, status_code, data):
        """Send JSON response"""
        self.send_response_only(status_code)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))
