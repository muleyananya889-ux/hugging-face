"""
Simple Vercel serverless function
"""

import json

def handler(request):
    """Main handler function"""
    
    # CORS headers
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Content-Type': 'application/json'
    }
    
    try:
        # Handle different request methods
        if hasattr(request, 'method'):
            method = request.method
        else:
            method = 'GET'
        
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': headers,
                'body': ''
            }
        
        if method == 'GET':
            # Simple HTML page
            html = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HF AI Assistant</title>
    <style>
        body { font-family: Arial, sans-serif; background: linear-gradient(135deg, #667eea, #764ba2); margin: 0; padding: 20px; }
        .container { max-width: 800px; margin: 0 auto; background: white; border-radius: 10px; padding: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
        .input-group { margin-bottom: 15px; }
        input, select, button { padding: 10px; border: 1px solid #ddd; border-radius: 5px; font-size: 14px; }
        input[type="text"] { width: 70%; }
        button { background: #667eea; color: white; border: none; cursor: pointer; }
        button:hover { background: #5a6fd8; }
        .chat { height: 400px; overflow-y: auto; border: 1px solid #eee; padding: 15px; margin-bottom: 15px; background: #f9f9f9; }
        .message { margin-bottom: 10px; padding: 10px; border-radius: 10px; }
        .user { background: #e3f2fd; margin-left: auto; text-align: right; max-width: 70%; }
        .assistant { background: #f3e5f5; margin-right: auto; max-width: 70%; }
        .loading { color: #666; font-style: italic; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🤖 Hugging Face AI Assistant</h1>
        
        <div class="input-group">
            <input type="password" id="apiKey" placeholder="Enter HF API Key" style="width: 100%">
        </div>
        
        <div class="input-group">
            <select id="model" style="width: 100%">
                <option value="deepseek-ai/DeepSeek-R1">DeepSeek-R1</option>
                <option value="microsoft/DialoGPT-medium">DialoGPT Medium</option>
                <option value="gpt2">GPT-2</option>
            </select>
        </div>
        
        <div class="input-group">
            <input type="range" id="temperature" min="0.1" max="2.0" step="0.1" value="0.7" style="width: 100%">
            <span id="tempValue">0.7</span>
        </div>
        
        <div class="chat" id="chatContainer">
            <div style="text-align: center; color: #666; padding: 40px;">
                💬 Enter your API key and start chatting!
            </div>
        </div>
        
        <div class="input-group">
            <input type="text" id="messageInput" placeholder="Type your message..." style="width: 80%">
            <button onclick="sendMessage()">Send</button>
        </div>
        
        <div style="text-align: center; margin-top: 10px;">
            <button onclick="clearChat()" style="background: #666;">Clear Chat</button>
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
            
            const message = document.getElementById('messageInput').value.trim();
            const apiKey = document.getElementById('apiKey').value.trim();
            
            if (!message || !apiKey) {
                alert('Please enter both message and API key');
                return;
            }
            
            isLoading = true;
            document.querySelector('button[onclick="sendMessage()"]').disabled = true;
            
            addMessage('user', message);
            document.getElementById('messageInput').value = '';
            
            const loadingMsg = document.createElement('div');
            loadingMsg.className = 'message loading';
            loadingMsg.textContent = '🤔 Thinking...';
            document.getElementById('chatContainer').appendChild(loadingMsg);
            
            try {
                const response = await fetch('/', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({
                        message: message,
                        apiKey: apiKey,
                        model: document.getElementById('model').value,
                        temperature: parseFloat(document.getElementById('temperature').value)
                    })
                });
                
                const data = await response.json();
                loadingMsg.remove();
                
                if (data.success) {
                    addMessage('assistant', data.response);
                } else {
                    addMessage('assistant', '❌ Error: ' + data.error);
                }
            } catch (error) {
                loadingMsg.remove();
                addMessage('assistant', '❌ Network Error: ' + error.message);
            } finally {
                isLoading = false;
                document.querySelector('button[onclick="sendMessage()"]').disabled = false;
            }
        }
        
        function addMessage(role, content) {
            const container = document.getElementById('chatContainer');
            
            // Remove welcome message
            const welcome = container.querySelector('div[style*="text-align: center"]');
            if (welcome) {
                welcome.remove();
            }
            
            const msg = document.createElement('div');
            msg.className = 'message ' + role;
            msg.innerHTML = '<strong>' + (role === 'user' ? '👤 You' : '🤖 Assistant') + '</strong><br>' + content;
            container.appendChild(msg);
            container.scrollTop = container.scrollHeight;
        }
        
        function clearChat() {
            const container = document.getElementById('chatContainer');
            container.innerHTML = '<div style="text-align: center; color: #666; padding: 40px;">💬 Enter your API key and start chatting!</div>';
        }
    </script>
</body>
</html>'''
            
            return {
                'statusCode': 200,
                'headers': {**headers, 'Content-Type': 'text/html'},
                'body': html
            }
        
        elif method == 'POST':
            # Handle chat request
            try:
                body = request.body if hasattr(request, 'body') else b''
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
                        'body': json.dumps({'success': False, 'error': 'Missing message or API key'})
                    }
                
                # Import here to avoid issues
                import requests
                
                try:
                    response = requests.post(
                        f'https://api-inference.huggingface.co/models/{model}',
                        headers={'Authorization': f'Bearer {api_key}'},
                        json={
                            'inputs': message,
                            'parameters': {
                                'max_length': 1000,
                                'temperature': temperature,
                                'do_sample': True,
                                'top_p': 0.9
                            }
                        },
                        timeout=30
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if isinstance(result, list) and len(result) > 0:
                            text = result[0].get('generated_text', '')
                            if text.startswith(message):
                                text = text[len(message):].strip()
                            else:
                                text = text.strip()
                            
                            return {
                                'statusCode': 200,
                                'headers': headers,
                                'body': json.dumps({'success': True, 'response': text})
                            }
                        else:
                            return {
                                'statusCode': 200,
                                'headers': headers,
                                'body': json.dumps({'success': False, 'error': 'No response'})
                            }
                    else:
                        return {
                            'statusCode': 200,
                            'headers': headers,
                            'body': json.dumps({'success': False, 'error': f'API Error: {response.status_code}'})
                        }
                        
                except Exception as e:
                    return {
                        'statusCode': 200,
                        'headers': headers,
                        'body': json.dumps({'success': False, 'error': str(e)})
                    }
                    
            except Exception as e:
                return {
                    'statusCode': 500,
                    'headers': headers,
                    'body': json.dumps({'success': False, 'error': f'Server error: {str(e)}'})
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
            'body': json.dumps({'error': f'Critical error: {str(e)}'})
        }
