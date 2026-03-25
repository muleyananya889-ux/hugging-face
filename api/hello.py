def handler(request):
    """Simple test handler"""
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'text/html'},
        'body': '''
<!DOCTYPE html>
<html>
<head>
    <title>HF Assistant Working!</title>
    <style>
        body { font-family: Arial; background: #f0f0f0; margin: 20px; }
        .container { max-width: 600px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; text-align: center; }
        .success { color: #4CAF50; font-size: 24px; }
    </style>
</head>
<body>
    <div class="container">
        <h1 class="success">🎉 Deployment Successful!</h1>
        <p>Your Hugging Face AI Assistant is now running on Vercel!</p>
        <p>Function is working correctly.</p>
        <hr>
        <h3>Next Steps:</h3>
        <p>1. Get your Hugging Face API key from <a href="https://huggingface.co/settings/tokens" target="_blank">Hugging Face</a></p>
        <p>2. The full chat interface will be available soon!</p>
    </div>
</body>
</html>
        '''
    }
