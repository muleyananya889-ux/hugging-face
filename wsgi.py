"""
WSGI entry point for Vercel deployment
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def application(environ, start_response):
    """WSGI application for Vercel"""
    
    # Set environment variables
    os.environ.setdefault('HF_API_KEY', environ.get('HF_API_KEY', ''))
    os.environ.setdefault('HF_MODEL', environ.get('HF_MODEL', 'deepseek-ai/DeepSeek-R1'))
    
    # Import and run the Streamlit app
    try:
        import streamlit as st
        from app import main
        
        # Configure Streamlit for WSGI
        st.runtime.legacy_script_runner_util.script_run_context = st.runtime.scriptrunner.script_run_context.ScriptRunContext(
            script_path=str(project_root / "app.py"),
            script_hash="wsgi"
        )
        
        # Run the main app
        main()
        
        # Return a simple HTML response
        response_body = b'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Hugging Face AI Assistant</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <script src="https://cdn.streamlit.io/streamlit.v1.28.0.min.js"></script>
        </head>
        <body>
            <div id="root">
                <h1>Loading Hugging Face AI Assistant...</h1>
                <p>If this page doesn't load, please check the deployment logs.</p>
            </div>
            <script>
                // Streamlit will automatically render the app here
            </script>
        </body>
        </html>
        '''
        
        status = '200 OK'
        headers = [
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(response_body)))
        ]
        
        start_response(status, headers)
        return [response_body]
        
    except Exception as e:
        # Return error page
        error_body = f'''
        <!DOCTYPE html>
        <html>
        <head>
            <title>Error - Hugging Face AI Assistant</title>
            <meta charset="utf-8">
        </head>
        <body>
            <h1>Application Error</h1>
            <p>There was an error starting the Streamlit application:</p>
            <pre>{str(e)}</pre>
            <p>Please check the deployment logs for more information.</p>
        </body>
        </html>
        '''.encode('utf-8')
        
        status = '500 Internal Server Error'
        headers = [
            ('Content-Type', 'text/html'),
            ('Content-Length', str(len(error_body)))
        ]
        
        start_response(status, headers)
        return [error_body]

if __name__ == '__main__':
    # For local testing
    from wsgiref.simple_server import make_server
    httpd = make_server('', 8000, application)
    print("Serving on http://localhost:8000")
    httpd.serve_forever()
