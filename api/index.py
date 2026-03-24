"""
Vercel serverless function for Streamlit app
"""

import os
import sys
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def handler(request):
    """Vercel serverless handler"""
    
    # Set environment variables
    os.environ.setdefault('HF_API_KEY', os.getenv('HF_API_KEY', ''))
    os.environ.setdefault('HF_MODEL', os.getenv('HF_MODEL', 'deepseek-ai/DeepSeek-R1'))
    
    # Import and run the Streamlit app
    try:
        import streamlit as st
        from app import main
        
        # Configure Streamlit for serverless
        st.runtime.legacy_script_runner_util.script_run_context = st.runtime.scriptrunner.script_run_context.ScriptRunContext(
            script_path=str(project_root / "app.py"),
            script_hash="serverless"
        )
        
        # Run the main app
        main()
        
        return {
            'statusCode': 200,
            'body': 'Streamlit app running successfully',
            'headers': {
                'Content-Type': 'text/html'
            }
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error running Streamlit app: {str(e)}',
            'headers': {
                'Content-Type': 'text/plain'
            }
        }
