"""
Styling utilities for the Hugging Face application
"""

import streamlit as st

class ThemeManager:
    """Manages application themes and styling"""
    
    @staticmethod
    def get_css() -> str:
        """Return the main CSS for the application"""
        return """
        /* Global Styles */
        .stApp {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        /* Main Container */
        .main-container {
            background: rgba(255, 255, 255, 0.95);
            border-radius: 20px;
            padding: 2rem;
            margin: 1rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
            backdrop-filter: blur(10px);
        }
        
        /* Header Styles */
        .main-header {
            font-size: 3rem;
            font-weight: 700;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-bottom: 2rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }
        
        /* Chat Message Styles */
        .chat-container {
            max-height: 600px;
            overflow-y: auto;
            padding: 1rem;
            border-radius: 15px;
            background: #f8f9fa;
        }
        
        .message-wrapper {
            margin: 1rem 0;
            animation: slideIn 0.3s ease-out;
        }
        
        .user-message {
            background: linear-gradient(135deg, #e3f2fd, #bbdefb);
            color: #1565c0;
            padding: 1rem 1.5rem;
            border-radius: 18px 18px 4px 18px;
            margin-left: auto;
            max-width: 70%;
            box-shadow: 0 4px 12px rgba(33, 150, 243, 0.2);
            border: 2px solid #2196f3;
        }
        
        .assistant-message {
            background: linear-gradient(135deg, #f3e5f5, #e1bee7);
            color: #7b1fa2;
            padding: 1rem 1.5rem;
            border-radius: 18px 18px 18px 4px;
            margin-right: auto;
            max-width: 70%;
            box-shadow: 0 4px 12px rgba(156, 39, 176, 0.2);
            border: 2px solid #9c27b0;
        }
        
        .message-header {
            font-weight: 600;
            margin-bottom: 0.5rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        .message-content {
            line-height: 1.6;
            white-space: pre-wrap;
        }
        
        .message-timestamp {
            font-size: 0.75rem;
            opacity: 0.7;
            margin-top: 0.5rem;
        }
        
        /* Sidebar Styles */
        .sidebar-section {
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            border-radius: 15px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 1px solid #dee2e6;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        }
        
        .sidebar-header {
            font-weight: 600;
            color: #495057;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }
        
        /* Model Card Styles */
        .model-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            border: 2px solid #e9ecef;
            transition: all 0.3s ease;
            cursor: pointer;
        }
        
        .model-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
            border-color: #667eea;
        }
        
        .model-card.selected {
            background: linear-gradient(135deg, #667eea10, #764ba210);
            border-color: #667eea;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        
        .model-name {
            font-weight: 600;
            color: #212529;
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }
        
        .model-id {
            font-family: 'Courier New', monospace;
            background: #f8f9fa;
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.85rem;
            color: #6c757d;
            margin-bottom: 0.5rem;
        }
        
        .model-description {
            color: #6c757d;
            font-size: 0.9rem;
            line-height: 1.4;
        }
        
        /* Metric Card Styles */
        .metric-card {
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            text-align: center;
            border: 1px solid #e9ecef;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
            transition: all 0.3s ease;
        }
        
        .metric-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
        }
        
        .metric-icon {
            font-size: 2rem;
            margin-bottom: 0.5rem;
        }
        
        .metric-title {
            font-weight: 600;
            color: #6c757d;
            margin-bottom: 0.5rem;
            font-size: 0.9rem;
        }
        
        .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: #212529;
        }
        
        .metric-change {
            font-size: 0.8rem;
            margin-top: 0.5rem;
        }
        
        .metric-change.positive {
            color: #28a745;
        }
        
        .metric-change.negative {
            color: #dc3545;
        }
        
        /* Button Styles */
        .stButton > button {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            border-radius: 8px;
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            transition: all 0.3s ease;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        }
        
        .stButton > button:active {
            transform: translateY(0);
        }
        
        /* Input Styles */
        .stTextInput > div > div > input {
            border-radius: 8px;
            border: 2px solid #e9ecef;
            padding: 0.75rem;
            transition: all 0.3s ease;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }
        
        /* Slider Styles */
        .stSlider {
            margin: 1rem 0;
        }
        
        /* Selectbox Styles */
        .stSelectbox > div > div > select {
            border-radius: 8px;
            border: 2px solid #e9ecef;
            padding: 0.75rem;
        }
        
        /* Chat Input Styles */
        .stChatInput {
            background: white;
            border-radius: 25px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }
        
        /* Status Indicator */
        .status-indicator {
            display: flex;
            align-items: center;
            gap: 0.5rem;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            margin: 0.5rem 0;
        }
        
        .status-indicator.online {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
        }
        
        .status-indicator.offline {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
        }
        
        .status-indicator.loading {
            background: #fff3cd;
            color: #856404;
            border: 1px solid #ffeaa7;
        }
        
        .status-dot {
            width: 8px;
            height: 8px;
            border-radius: 50%;
            animation: pulse 2s infinite;
        }
        
        .status-dot.online {
            background: #28a745;
        }
        
        .status-dot.offline {
            background: #dc3545;
        }
        
        .status-dot.loading {
            background: #ffc107;
        }
        
        /* Animations */
        @keyframes slideIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes pulse {
            0% {
                opacity: 1;
            }
            50% {
                opacity: 0.5;
            }
            100% {
                opacity: 1;
            }
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        
        /* Responsive Design */
        @media (max-width: 768px) {
            .main-header {
                font-size: 2rem;
            }
            
            .user-message, .assistant-message {
                max-width: 85%;
            }
            
            .metric-card {
                padding: 1rem;
            }
            
            .model-card {
                padding: 1rem;
            }
        }
        
        /* Loading Animation */
        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid #f3f3f3;
            border-top: 3px solid #667eea;
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        /* Code Block Styles */
        .code-block {
            background: #f8f9fa;
            border: 1px solid #e9ecef;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
            font-family: 'Courier New', monospace;
            overflow-x: auto;
        }
        
        /* Error Message Styles */
        .error-message {
            background: #f8d7da;
            color: #721c24;
            border: 1px solid #f5c6cb;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        /* Success Message Styles */
        .success-message {
            background: #d4edda;
            color: #155724;
            border: 1px solid #c3e6cb;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
        
        /* Info Message Styles */
        .info-message {
            background: #d1ecf1;
            color: #0c5460;
            border: 1px solid #bee5eb;
            border-radius: 8px;
            padding: 1rem;
            margin: 1rem 0;
        }
        """
    
    @staticmethod
    def inject_css():
        """Inject CSS into Streamlit app"""
        st.markdown(f"<style>{ThemeManager.get_css()}</style>", unsafe_allow_html=True)
    
    @staticmethod
    def get_theme_colors() -> dict:
        """Get current theme color palette"""
        return {
            "primary": "#667eea",
            "secondary": "#764ba2",
            "success": "#28a745",
            "warning": "#ffc107",
            "error": "#dc3545",
            "info": "#17a2b8",
            "light": "#f8f9fa",
            "dark": "#343a40"
        }
    
    @staticmethod
    def render_gradient_text(text: str, color1: str = "#667eea", color2: str = "#764ba2") -> str:
        """Create gradient text effect"""
        return f"""
        <span style="
            background: linear-gradient(45deg, {color1}, {color2});
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            font-weight: 600;
        ">{text}</span>
        """
    
    @staticmethod
    def render_card(title: str, content: str, icon: str = "", color: str = "#667eea") -> str:
        """Render a styled card component"""
        return f"""
        <div style="
            background: white;
            border-radius: 12px;
            padding: 1.5rem;
            margin: 1rem 0;
            border: 2px solid {color}20;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        ">
            <div style="
                display: flex;
                align-items: center;
                gap: 0.5rem;
                margin-bottom: 1rem;
                color: {color};
                font-weight: 600;
                font-size: 1.1rem;
            ">
                {icon} {title}
            </div>
            <div style="color: #495057; line-height: 1.6;">
                {content}
            </div>
        </div>
        """
    
    @staticmethod
    def render_loading_animation(message: str = "Loading...") -> str:
        """Render a loading animation"""
        return f"""
        <div style="
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            padding: 2rem;
        ">
            <div class="loading-spinner"></div>
            <span style="color: #6c757d; font-weight: 600;">{message}</span>
        </div>
        """
    
    @staticmethod
    def render_empty_state(icon: str, title: str, description: str) -> str:
        """Render an empty state component"""
        return f"""
        <div style="
            text-align: center;
            padding: 3rem 1rem;
            color: #6c757d;
        ">
            <div style="font-size: 4rem; margin-bottom: 1rem;">{icon}</div>
            <h3 style="margin-bottom: 0.5rem; color: #495057;">{title}</h3>
            <p>{description}</p>
        </div>
        """

class AnimationManager:
    """Manages UI animations and transitions"""
    
    @staticmethod
    def fade_in(element_id: str, duration: float = 0.3) -> str:
        """Create fade-in animation"""
        return f"""
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const element = document.querySelector('{element_id}');
            if (element) {{
                element.style.animation = 'fadeIn {duration}s ease-in';
            }}
        }});
        </script>
        """
    
    @staticmethod
    def slide_in(element_id: str, direction: str = "up", duration: float = 0.3) -> str:
        """Create slide-in animation"""
        transforms = {
            "up": "translateY(20px)",
            "down": "translateY(-20px)",
            "left": "translateX(20px)",
            "right": "translateX(-20px)"
        }
        
        transform = transforms.get(direction, "translateY(20px)")
        
        return f"""
        <script>
        document.addEventListener('DOMContentLoaded', function() {{
            const element = document.querySelector('{element_id}');
            if (element) {{
                element.style.animation = `slideIn {duration}s ease-out`;
                element.style.transform = '{transform}';
            }}
        }});
        </script>
        """
