import json

def handler(request):
    """Simple Vercel API function"""
    
    if request.method == 'GET':
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'text/html'},
            'body': '''<!DOCTYPE html>
<html>
<head>
    <title>HF Chat</title>
    <style>
        body { font-family: Arial; background: #f0f0f0; padding: 20px; }
        .container { max-width: 500px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; }
        input, button { padding: 8px; margin: 5px; border: 1px solid #ccc; border-radius: 4px; }
        button { background: #007bff; color: white; border: none; cursor: pointer; }
        #chat { height: 300px; border: 1px solid #ddd; padding: 10px; overflow-y: auto; margin: 10px 0; }
        .msg { margin: 5px 0; padding: 8px; border-radius: 4px; }
        .user { background: #e3f2fd; text-align: right; }
        .bot { background: #f8f9fa; }
    </style>
</head>
<body>
    <div class="container">
        <h2>🤖 HF Chat</h2>
        <input type="password" id="key" placeholder="API Key" style="width: 100%">
        <input type="text" id="msg" placeholder="Message..." style="width: 75%">
        <button onclick="send()">Send</button>
        <div id="chat">
            <div style="text-align: center; color: #666; padding: 20px;">Enter API key and start chatting</div>
        </div>
    </div>
    <script>
        async function send() {
            const key = document.getElementById('key').value;
            const msg = document.getElementById('msg').value;
            if (!key || !msg) { alert('Enter key and message'); return; }
            
            const chat = document.getElementById('chat');
            const userMsg = document.createElement('div');
            userMsg.className = 'msg user';
            userMsg.innerHTML = '<strong>You:</strong> ' + msg;
            chat.appendChild(userMsg);
            
            const loading = document.createElement('div');
            loading.className = 'msg bot';
            loading.innerHTML = '<em>Thinking...</em>';
            chat.appendChild(loading);
            
            document.getElementById('msg').value = '';
            
            try {
                const res = await fetch('/api/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({key, msg})
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
            } catch (err) {
                loading.remove();
                const errormsg = document.createElement('div');
                errormsg.className = 'msg bot';
                errormsg.innerHTML = '<strong>Network Error:</strong> ' + err.message;
                chat.appendChild(errormsg);
            }
        }
    </script>
</body>
</html>'''
        }
    
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)
            key = data.get('key', '').strip()
            msg = data.get('msg', '').strip()
            
            if not key or not msg:
                return {
                    'statusCode': 400,
                    'headers': {'Content-Type': 'application/json'},
                    'body': json.dumps({'success': False, 'error': 'Missing key or message'})
                }
            
            import requests
            
            response = requests.post(
                'https://api-inference.huggingface.co/models/gpt2',
                headers={'Authorization': f'Bearer {key}'},
                json={'inputs': msg, 'parameters': {'max_length': 100}},
                timeout=20
            )
            
            if response.status_code == 200:
                result = response.json()
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
                    'body': json.dumps({'success': False, 'error': f'API Error {response.status_code}'})
                }
                
        except Exception as e:
            return {
                'statusCode': 500,
                'headers': {'Content-Type': 'application/json'},
                'body': json.dumps({'success': False, 'error': str(e)})
            }
    
    else:
        return {
            'statusCode': 405,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': 'Method not allowed'})
        }
