"""
Frontend UI components for the Hugging Face application
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from typing import Dict, Any, List, Optional
import time
import pandas as pd

class UIComponents:
    """Collection of reusable UI components"""
    
    @staticmethod
    def render_metric_card(title: str, value: str, delta: Optional[str] = None, 
                         color: str = "blue", icon: str = "📊"):
        """Render a styled metric card"""
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {color}10, {color}05);
            border: 1px solid {color}30;
            border-radius: 10px;
            padding: 1rem;
            margin: 0.5rem 0;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        ">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <div>
                    <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.25rem;">
                        {icon} {title}
                    </div>
                    <div style="font-size: 1.5rem; font-weight: bold; color: #333;">
                        {value}
                    </div>
                    {f'<div style="font-size: 0.8rem; color: {"green" if delta and "+" in delta else "red"};">{delta}</div>' if delta else ''}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def render_model_selector(available_models: Dict[str, str], selected_model: str) -> str:
        """Render an enhanced model selector with descriptions"""
        st.subheader("🤖 Model Selection")
        
        # Create model cards
        selected = None
        cols = st.columns(2)
        
        for i, (name, model_id) in enumerate(available_models.items()):
            with cols[i % 2]:
                is_selected = name == selected_model
                
                card_style = f"""
                <div style="
                    border: 2px solid {'#2196f3' if is_selected else '#e0e0e0'};
                    border-radius: 10px;
                    padding: 1rem;
                    margin: 0.5rem 0;
                    background: {'#e3f2fd' if is_selected else '#fafafa'};
                    cursor: pointer;
                    transition: all 0.3s ease;
                " onmouseover="this.style.transform='translateY(-2px)'" 
                   onmouseout="this.style.transform='translateY(0)'">
                    <div style="font-weight: bold; color: #333; margin-bottom: 0.5rem;">
                        {name}
                    </div>
                    <div style="font-size: 0.8rem; color: #666; margin-bottom: 0.5rem;">
                        {model_id}
                    </div>
                    <div style="font-size: 0.75rem; color: #888;">
                        Click to select this model
                    </div>
                </div>
                """
                
                st.markdown(card_style, unsafe_allow_html=True)
                
                if st.button(f"Select {name}", key=f"select_{name}", 
                           type="primary" if is_selected else "secondary"):
                    selected = name
        
        return selected or selected_model
    
    @staticmethod
    def render_parameter_controls() -> Dict[str, Any]:
        """Render model parameter controls with visual feedback"""
        st.subheader("⚙️ Model Parameters")
        
        with st.expander("Advanced Parameters", expanded=True):
            # Temperature with visual indicator
            temp = st.slider(
                "Temperature", 
                0.1, 2.0, 0.7, 0.1,
                help="Controls randomness: Lower = more focused, Higher = more creative"
            )
            
            # Temperature color indicator
            temp_color = "green" if temp < 0.5 else "orange" if temp < 1.0 else "red"
            st.markdown(f"""
            <div style="display: flex; align-items: center; margin: 0.5rem 0;">
                <span style="font-weight: bold; margin-right: 0.5rem;">Creativity Level:</span>
                <span style="color: {temp_color}; font-weight: bold;">
                    {"Low" if temp < 0.5 else "Medium" if temp < 1.0 else "High"}
                </span>
            </div>
            """, unsafe_allow_html=True)
            
            # Max Length
            max_length = st.slider(
                "Max Response Length", 
                50, 4096, 2048, 50,
                help="Maximum number of tokens in the response"
            )
            
            # Top P
            top_p = st.slider(
                "Top P", 
                0.1, 1.0, 0.9, 0.05,
                help="Nucleus sampling: Lower = more predictable, Higher = more diverse"
            )
            
            # Additional parameters
            col1, col2 = st.columns(2)
            with col1:
                do_sample = st.checkbox("Enable Sampling", value=True)
                repetition_penalty = st.slider("Repetition Penalty", 1.0, 2.0, 1.1, 0.1)
            
            with col2:
                return_full_text = st.checkbox("Return Full Text", value=False)
                early_stopping = st.checkbox("Early Stopping", value=False)
        
        return {
            "temperature": temp,
            "max_length": max_length,
            "top_p": top_p,
            "do_sample": do_sample,
            "repetition_penalty": repetition_penalty,
            "return_full_text": return_full_text,
            "early_stopping": early_stopping
        }
    
    @staticmethod
    def render_chat_interface(messages: List[Dict[str, Any]]) -> str:
        """Render an enhanced chat interface"""
        st.subheader("💬 Conversation")
        
        # Chat container
        chat_container = st.container()
        
        with chat_container:
            for i, message in enumerate(messages):
                role = message["role"]
                content = message["content"]
                timestamp = message.get("timestamp", time.time())
                
                if role == "user":
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-end; margin: 1rem 0;">
                        <div style="
                            background: #e3f2fd;
                            color: #1565c0;
                            padding: 1rem;
                            border-radius: 18px 18px 4px 18px;
                            max-width: 70%;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        ">
                            <div style="font-weight: bold; margin-bottom: 0.5rem;">👤 You</div>
                            <div>{content}</div>
                            <div style="font-size: 0.7rem; color: #666; margin-top: 0.5rem;">
                                {time.strftime('%H:%M', time.localtime(timestamp))}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div style="display: flex; justify-content: flex-start; margin: 1rem 0;">
                        <div style="
                            background: #f3e5f5;
                            color: #7b1fa2;
                            padding: 1rem;
                            border-radius: 18px 18px 18px 4px;
                            max-width: 70%;
                            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                        ">
                            <div style="font-weight: bold; margin-bottom: 0.5rem;">🤖 Assistant</div>
                            <div>{content}</div>
                            <div style="font-size: 0.7rem; color: #666; margin-top: 0.5rem;">
                                {time.strftime('%H:%M', time.localtime(timestamp))}
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
        
        # Chat input
        user_input = st.chat_input("Type your message here...")
        
        return user_input
    
    @staticmethod
    def render_usage_statistics(messages: List[Dict[str, Any]]) -> None:
        """Render usage statistics and charts"""
        st.subheader("📊 Usage Statistics")
        
        if not messages:
            st.info("No messages yet. Start chatting to see statistics!")
            return
        
        # Calculate statistics
        user_messages = [m for m in messages if m["role"] == "user"]
        assistant_messages = [m for m in messages if m["role"] == "assistant"]
        
        total_messages = len(messages)
        total_tokens = sum(len(m["content"].split()) for m in messages)
        
        # Metrics row
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            UIComponents.render_metric_card(
                "Total Messages", str(total_messages), 
                icon="💬", color="blue"
            )
        
        with col2:
            UIComponents.render_metric_card(
                "User Messages", str(len(user_messages)), 
                icon="👤", color="green"
            )
        
        with col3:
            UIComponents.render_metric_card(
                "AI Responses", str(len(assistant_messages)), 
                icon="🤖", color="purple"
            )
        
        with col4:
            UIComponents.render_metric_card(
                "Total Tokens", f"{total_tokens:,}", 
                icon="📝", color="orange"
            )
        
        # Timeline chart
        if len(messages) > 1:
            st.subheader("📈 Message Timeline")
            
            # Prepare data for timeline
            timeline_data = []
            for i, message in enumerate(messages):
                timeline_data.append({
                    "message_number": i + 1,
                    "role": message["role"],
                    "timestamp": message.get("timestamp", time.time()),
                    "length": len(message["content"])
                })
            
            df = pd.DataFrame(timeline_data)
            
            # Create timeline chart
            fig = px.scatter(
                df, 
                x="message_number", 
                y="length",
                color="role",
                size="length",
                hover_data=["timestamp"],
                title="Message Length Over Time",
                color_discrete_map={"user": "#2196f3", "assistant": "#9c27b0"}
            )
            
            fig.update_layout(
                xaxis_title="Message Number",
                yaxis_title="Message Length (characters)",
                height=400
            )
            
            st.plotly_chart(fig, use_container_width=True)
    
    @staticmethod
    def render_model_comparison(model_data: Dict[str, Any]) -> None:
        """Render model comparison charts"""
        st.subheader("🔄 Model Performance Comparison")
        
        if not model_data:
            st.info("No model performance data available yet.")
            return
        
        # Create comparison metrics
        models = list(model_data.keys())
        response_times = [model_data[m].get("response_time", 0) for m in models]
        success_rates = [model_data[m].get("success_rate", 0) for m in models]
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Response time chart
            fig_time = go.Figure(data=[
                go.Bar(name='Response Time (s)', x=models, y=response_times)
            ])
            fig_time.update_layout(title="Model Response Times", yaxis_title="Seconds")
            st.plotly_chart(fig_time, use_container_width=True)
        
        with col2:
            # Success rate chart
            fig_success = go.Figure(data=[
                go.Bar(name='Success Rate (%)', x=models, y=success_rates)
            ])
            fig_success.update_layout(title="Model Success Rates", yaxis_title="Percentage")
            st.plotly_chart(fig_success, use_container_width=True)
    
    @staticmethod
    def render_quick_actions() -> Dict[str, bool]:
        """Render quick action buttons"""
        st.subheader("⚡ Quick Actions")
        
        col1, col2, col3 = st.columns(3)
        
        actions = {}
        
        with col1:
            if st.button("🗑️ Clear Chat", type="secondary", use_container_width=True):
                actions["clear_chat"] = True
            
            if st.button("💾 Save History", type="secondary", use_container_width=True):
                actions["save_history"] = True
        
        with col2:
            if st.button("📥 Load History", type="secondary", use_container_width=True):
                actions["load_history"] = True
            
            if st.button("📤 Export Chat", type="secondary", use_container_width=True):
                actions["export_chat"] = True
        
        with col3:
            if st.button("🔄 Reset Settings", type="secondary", use_container_width=True):
                actions["reset_settings"] = True
            
            if st.button("❓ Help", type="secondary", use_container_width=True):
                actions["help"] = True
        
        return actions
    
    @staticmethod
    def render_help_section():
        """Render help and documentation section"""
        with st.expander("📚 Help & Documentation"):
            st.markdown("""
            ### Getting Started
            
            1. **API Key Setup**: Enter your Hugging Face API key in the sidebar
            2. **Model Selection**: Choose a model from the available options
            3. **Configure Parameters**: Adjust temperature, max length, etc.
            4. **Start Chatting**: Type your message and press Enter
            
            ### Model Types
            
            - **🧠 Reasoning Models**: Best for problem-solving and logical tasks
            - **💬 Conversational Models**: Optimized for dialogue and chat
            - **📝 General Models**: Good for text generation and completion
            - **💻 Code Models**: Specialized for programming tasks
            
            ### Parameter Guide
            
            - **Temperature**: Controls randomness (0.1 = focused, 2.0 = creative)
            - **Max Length**: Maximum response length in tokens
            - **Top P**: Nucleus sampling parameter
            - **Repetition Penalty**: Reduces repetitive responses
            
            ### Tips
            
            - Start with lower temperature for factual responses
            - Use higher temperature for creative writing
            - Adjust max length based on your needs
            - Clear chat history periodically for better context
            """)
    
    @staticmethod
    def render_status_indicator(status: str, message: str = "") -> None:
        """Render a status indicator"""
        status_colors = {
            "online": "#4caf50",
            "offline": "#f44336", 
            "loading": "#ff9800",
            "error": "#f44336"
        }
        
        color = status_colors.get(status, "#9e9e9e")
        
        st.markdown(f"""
        <div style="
            display: flex;
            align-items: center;
            padding: 0.5rem 1rem;
            background: {color}10;
            border: 1px solid {color}30;
            border-radius: 20px;
            margin: 0.5rem 0;
        ">
            <div style="
                width: 8px;
                height: 8px;
                background: {color};
                border-radius: 50%;
                margin-right: 0.5rem;
                animation: pulse 2s infinite;
            "></div>
            <span style="color: {color}; font-weight: bold;">
                {status.capitalize()}
            </span>
            {f'<span style="margin-left: 0.5rem; color: #666;">{message}</span>' if message else ''}
        </div>
        
        <style>
        @keyframes pulse {{
            0% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
            100% {{ opacity: 1; }}
        }}
        </style>
        """, unsafe_allow_html=True)
