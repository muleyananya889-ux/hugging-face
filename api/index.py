"""
Vercel serverless function - simplified version
"""

import json
import os

def handler(request):
    """Vercel serverless function handler"""
    
    # Handle CORS
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    try:
        # Parse request
        method = request.method if hasattr(request, 'method') else 'GET'
        
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        if method == 'GET':
            # Return simple HTML page
            html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hugging Face AI Assistant</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .chat-container { max-height: 500px; overflow-y: auto; }
        .user-message { background: #e3f2fd; border-radius: 18px 18px 4px 18px; margin-left: auto; max-width: 70%; }
        .assistant-message { background: #f3e5f5; border-radius: 18px 18px 18px 4px; margin-right: auto; max-width: 70%; }
        .loading { display: inline-block; width: 20px; height: 20px; border: 3px solid #f3f3f3; border-top: 3px solid #3498db; border-radius: 50%; animation: spin 1s linear infinite; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
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
                    <input type="password" id="apiKey" placeholder="Enter HF API Key" class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                </div>
                
                <div class="bg-gray-50 p-4 rounded-lg">
                    <h3 class="font-semibold mb-2">🤖 Model</h3>
                    <select id="model" class="w-full p-2 border rounded focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <option value="deepseek-ai/DeepSeek-R1">DeepSeek-R1</option>
                        <option value="microsoft/DialoGPT-medium">DialoGPT Medium</option>
                        <option value="gpt2">GPT-2</option>
                        <option value="bigscience/bloom">BLOOM</option>
                    </select>
                </div>
                
                <div class="bg-gray-50 p-4 rounded-lg">
                    <h3 class="font-semibold mb-2">⚙️ Temperature</h3>
                    <input type="range" id="temperature" min="0.1" max="2.0" step="0.1" value="0.7" class="w-full">
                    <span id="tempValue" class="text-sm text-gray-600">0.7</span>
                </div>
            </div>
            
            <div class="chat-container bg-gray-50 rounded-lg p-4 mb-4" id="chatContainer">
                <div class="text-center text-gray-500 py-8">
                    <div class="text-4xl mb-4">💬</div>
                    <p>Start a conversation with AI assistant!</p>
                    <p class="text-sm mt-2">Enter your Hugging Face API key above to begin.</p>
                </div>
            </div>
            
            <div class="flex gap-2">
                <input type="text" id="messageInput" placeholder="Type your message here..." class="flex-1 p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500">
                <button onclick="sendMessage()" id="sendButton" class="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-3 rounded-lg hover:opacity-90 transition disabled:opacity-50">
                    Send
                </button>
            </div>
            
            <div class="mt-4 text-center">
                <button onclick="clearChat()" class="text-gray-500 hover:text-gray-700 transition">🗑️ Clear Chat</button>
            </div>
            
            <div class="mt-6 text-center text-sm text-gray-500">
                <p>Need an API key? Get one at <a href="https://huggingface.co/settings/tokens" target="_blank" class="text-blue-600 hover:underline">Hugging Face</a></p>
            </div>
        </div>
    </div>

    <script>
        let isLoading = false;
        
        document.getElementById('temperature').addEventListener('input', function(e) {
            document.getElementById('tempValue').textContent = e.target.value;
        });
        
        document.getElementById('messageInput').addEventListener('keypress', function(e) {
            if (e.key === 'Enter' && !isLoading) {
                sendMessage();
            }
        });
        
        async function sendMessage() {
            if (isLoading) return;
            
            const messageInput = document.getElementById('messageInput');
            const message = messageInput.value.trim();
            
            if (!message) {
                alert('Please enter a message');
                return;
            }
            
            const apiKey = document.getElementById('apiKey').value;
            if (!apiKey) {
                alert('Please enter your Hugging Face API key');
                return;
            }
            
            isLoading = true;
            document.getElementById('sendButton').disabled = true;
            
            addMessage('user', message);
            messageInput.value = '';
            
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'text-center py-2';
            loadingDiv.innerHTML = '<div class="loading"></div> <span class="ml-2">Thinking...</span>';
            document.getElementById('chatContainer').appendChild(loadingDiv);
            
            try {
                const response = await fetch('/api', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: message,
                        apiKey: apiKey,
                        model: document.getElementById('model').value,
                        temperature: parseFloat(document.getElementById('temperature').value)
                    })
                });
                
                const data = await response.json();
                loadingDiv.remove();
                
                if (data.success) {
                    addMessage('assistant', data.response);
                } else {
                    addMessage('assistant', '❌ Error: ' + data.error);
                }
            } catch (error) {
                loadingDiv.remove();
                addMessage('assistant', '❌ Network Error: ' + error.message);
            } finally {
                isLoading = false;
                document.getElementById('sendButton').disabled = false;
            }
        }
        
        function addMessage(role, content) {
            const chatContainer = document.getElementById('chatContainer');
            const messageDiv = document.createElement('div');
            messageDiv.className = 'p-3 mb-3 rounded-lg ' + (role === 'user' ? 'user-message' : 'assistant-message');
            messageDiv.innerHTML = '<div class="font-semibold mb-1">' + (role === 'user' ? '👤 You' : '🤖 Assistant') + '</div><div>' + content + '</div>';
            
            const welcomeMsg = chatContainer.querySelector('.text-center.text-gray-500');
            if (welcomeMsg) {
                welcomeMsg.remove();
            }
            
            chatContainer.appendChild(messageDiv);
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        
        function clearChat() {
            const chatContainer = document.getElementById('chatContainer');
            chatContainer.innerHTML = '<div class="text-center text-gray-500 py-8"><div class="text-4xl mb-4">💬</div><p>Start a conversation with AI assistant!</p><p class="text-sm mt-2">Enter your Hugging Face API key above to begin.</p></div>';
        }
    </script>
</body>
</html>
            '''
            
            return {
                'statusCode': 200,
                'headers': {**headers, 'Content-Type': 'text/html'},
                'body': html_content
            }
        
        elif method == 'POST':
            # Handle API request
            try:
                # Get request body
                body = request.body if hasattr(request, 'body') else '{}'
                if isinstance(body, bytes):
                    body = body.decode('utf-8')
                
                data = json.loads(body) if body else {}
                message = data.get('message', '').strip()
                api_key = data.get('apiKey', '').strip()
                model = data.get('model', 'deepseek-ai/DeepSeek-R1')
                temperature = data.get('temperature', 0.7)
                
                if not message or not api_key:
                    return {
                        'statusCode': 400,
                        'headers': headers,
                        'body': json.dumps({'success': False, 'error': 'Message and API key required'})
                    }
                
                # Import requests here to avoid dependency issues
                import requests
                
                headers_hf = {'Authorization': f'Bearer {api_key}'}
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
                    headers=headers_hf,
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
                        
                        return {
                            'statusCode': 200,
                            'headers': headers,
                            'body': json.dumps({'success': True, 'response': clean_response})
                        }
                    else:
                        return {
                            'statusCode': 200,
                            'headers': headers,
                            'body': json.dumps({'success': False, 'error': 'No response generated'})
                        }
                else:
                    return {
                        'statusCode': 200,
                        'headers': headers,
                        'body': json.dumps({'success': False, 'error': f'API Error: {response.status_code}'})
                    }
                    
            except Exception as e:
                return {
                    'statusCode': 500,
                    'headers': headers,
                    'body': json.dumps({'success': False, 'error': str(e)})
                }
        
        else:
            return {
                'statusCode': 405,
                'headers': headers,
                'body': json.dumps({'error': 'Method not allowed'})
            }
            
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': headers,
            'body': json.dumps({'error': f'Server error: {str(e)}'})
        }
