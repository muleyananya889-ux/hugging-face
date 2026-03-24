"""
Main entry point for Vercel deployment
"""

import json
import os
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

class handler(BaseHTTPRequestHandler):
    """Main handler for Vercel serverless functions"""
    
    def do_GET(self):
        """Serve the main HTML page"""
        try:
            html_content = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hugging Face AI Assistant</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .gradient-bg {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        .chat-container {
            max-height: 500px;
            overflow-y: auto;
        }
        .user-message {
            background: #e3f2fd;
            border-radius: 18px 18px 4px 18px;
            margin-left: auto;
            max-width: 70%;
        }
        .assistant-message {
            background: #f3e5f5;
            border-radius: 18px 18px 18px 4px;
            margin-right: auto;
            max-width: 70%;
        }
        .loading {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #3498db;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
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
            </div>
        </div>
        
        <div>
            <input type="text" id="msg" placeholder="Type message..." style="width: 80%;">
            <button onclick="send()">Send</button>
        </div>
    </div>

    <script>
        async function send() {
            const key = document.getElementById('key').value;
            const msg = document.getElementById('msg').value;
            const model = document.getElementById('model').value;
            
            if (!key || !msg) {
                alert('Enter API key and message');
                return;
            }
            
            const chat = document.getElementById('chat');
            
            // Add user message
            const userMsg = document.createElement('div');
            userMsg.className = 'msg user';
            userMsg.innerHTML = '<strong>You:</strong> ' + msg;
            chat.appendChild(userMsg);
            
            // Clear welcome if exists
            const welcome = chat.querySelector('div[style*="text-align"]');
            if (welcome) welcome.remove();
            
            // Show loading
            const loading = document.createElement('div');
            loading.className = 'msg bot';
            loading.innerHTML = '<em>Thinking...</em>';
            chat.appendChild(loading);
            
            try {
                const res = await fetch('/', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({key, msg, model})
                });
                
                const data = await res.json();
                loading.remove();
                
                if (data.success) {
                    const botMsg = document.createElement('div');
                    botMsg.className = 'msg bot';
                    botMsg.innerHTML = '<strong>Bot:</strong> ' + data.response;
                    chat.appendChild(botMsg);
                } else {
                    const errorMsg = document.createElement('div');
                    errorMsg.className = 'msg bot';
                    errorMsg.innerHTML = '<strong>Error:</strong> ' + data.error;
                    chat.appendChild(errorMsg);
                }
                
                document.getElementById('msg').value = '';
                chat.scrollTop = chat.scrollHeight;
                
            } catch (err) {
                loading.remove();
                const errormsg = document.createElement('div');
                errormsg.className = 'msg bot';
                errormsg.innerHTML = '<strong>Network Error:</strong> ' + err.message;
                chat.appendChild(errormsg);
            }
        }
        
        // Enter key to send
        document.getElementById('msg').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') send();
        });
    </script>
</body>
</html>'''
            }
        
        elif method == 'POST':
            # Handle API request
            try:
                body = getattr(request, 'body', b'')
                if isinstance(body, bytes):
                    body = body.decode('utf-8')
                
                data = json.loads(body) if body else {}
                key = data.get('key', '').strip()
                msg = data.get('msg', '').strip()
                model = data.get('model', 'gpt2')
                
                if not key or not msg:
                    return {
                        'statusCode': 400,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({'success': False, 'error': 'Missing key or message'})
                    }
                
                # Simple API call
                import requests
                
                try:
                    resp = requests.post(
                        f'https://api-inference.huggingface.co/models/{model}',
                        headers={'Authorization': f'Bearer {key}'},
                        json={'inputs': msg, 'parameters': {'max_length': 200}},
                        timeout=20
                    )
                    
                    if resp.status_code == 200:
                        result = resp.json()
                        text = result[0].get('generated_text', '') if result else ''
                        if text.startswith(msg):
                            text = text[len(msg):].strip()
                        else:
                            text = text.strip()
                        
                        return {
                            'statusCode': 200,
                            'headers': {'Content-Type': 'application/json'},
                            'body': json.dumps({'success': True, 'response': text})
                        }
                    else:
                        return {
                            'statusCode': 200,
                            'headers': {'Content-Type': 'application/json'},
                            'body': json.dumps({'success': False, 'error': f'API Error: {resp.status_code}'})
                        }
                        
                except Exception as e:
                    return {
                        'statusCode': 200,
                        'headers': {'Content-Type': 'application/json'},
                        'body': json.dumps({'success': False, 'error': str(e)})
                    }
                    
            except requests.exceptions.RequestException as e:
                response_data = {'success': False, 'error': f'Network error: {str(e)}'}
            except Exception as e:
                response_data = {'success': False, 'error': f'Server error: {str(e)}'}
            
            self.send_json_response(200, response_data)
            
        except Exception as e:
            response_data = {'success': False, 'error': f'Server error: {str(e)}'}
            self.send_json_response(500, response_data)
    
    def send_response(self, status_code, content):
        """Send HTML response"""
        self.send_response(status_code)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Length', str(len(content)))
        self.end_headers()
        self.wfile.write(content.encode('utf-8'))
    
    def send_json_response(self, status_code, data):
        """Send JSON response"""
        json_data = json.dumps(data)
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Content-Length', str(len(json_data)))
        self.end_headers()
        self.wfile.write(json_data.encode('utf-8'))
