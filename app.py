import html
import os
import streamlit as st
import boto3
import json
from datetime import datetime
import time
from dotenv import load_dotenv

# Load optional settings from a local .env file (see .env.example).
# Values already set in the environment win over the file.
load_dotenv()

AWS_REGIONS = ["us-east-1", "us-west-2", "eu-west-1", "ap-southeast-1"]
ENV_REGION = os.getenv("AWS_REGION") or os.getenv("AWS_DEFAULT_REGION") or ""
if ENV_REGION and ENV_REGION not in AWS_REGIONS:
    AWS_REGIONS.insert(0, ENV_REGION)

# Configure page
st.set_page_config(
    page_title="Shipping Agent Assistant",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for minimalistic design
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }

    .main-header h1 {
        color: white;
    }

    .chat-container {
        background: #f8f9fa;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .user-message {
        background: #e3f2fd;
        color: #31333f;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #2196f3;
    }
    
    .agent-message {
        background: #f3e5f5;
        color: #31333f;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #9c27b0;
    }
    
    .status-box {
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    
    .status-connected {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
    }
    
    .status-disconnected {
        background: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
    }
</style>
""", unsafe_allow_html=True)

class AWSAgentConnector:
    def __init__(self):
        self.bedrock_agent = None
        self.session = None
        self.agent_id = None
        self.agent_alias_id = None
        
    def initialize_connection(self, aws_access_key, aws_secret_key, region, agent_id, agent_alias_id):
        """Initialize connection to AWS Bedrock Agent"""
        try:
            if aws_access_key and aws_secret_key:
                self.session = boto3.Session(
                    aws_access_key_id=aws_access_key,
                    aws_secret_access_key=aws_secret_key,
                    region_name=region
                )
            else:
                # No keys typed in: use boto3's default credential chain
                # (AWS_* env vars / .env, AWS profile, SSO, or an IAM role).
                self.session = boto3.Session(region_name=region)
            
            self.bedrock_agent = self.session.client('bedrock-agent-runtime')
            self.agent_id = agent_id
            self.agent_alias_id = agent_alias_id
            
            # Test connection. Read the whole stream: many failures (model
            # access denied, throttling, agent errors) only raise while the
            # completion stream is read, not when invoke_agent returns.
            self._invoke("Hello, are you working?", f"test-session-{int(time.time())}")

            return True, "Successfully connected to AWS Bedrock Agent!"

        except Exception as e:
            self.bedrock_agent = None
            return False, f"Connection failed: {str(e)}"

    def _invoke(self, message, session_id):
        """Call invoke_agent and join the text chunks of the event stream"""
        response = self.bedrock_agent.invoke_agent(
            agentId=self.agent_id,
            agentAliasId=self.agent_alias_id,
            sessionId=session_id,
            inputText=message
        )

        response_text = ""
        for event in response.get('completion', []):
            chunk = event.get('chunk', {})
            if 'bytes' in chunk:
                response_text += chunk['bytes'].decode('utf-8')
        return response_text
    
    def send_message(self, message, session_id):
        """Send message to AWS Bedrock Agent"""
        if not self.bedrock_agent:
            return "Error: Agent not connected. Please configure connection first."
        
        try:
            response_text = self._invoke(message, session_id)

            return response_text if response_text else "The agent returned no text response."

        except Exception as e:
            return f"Error communicating with agent: {str(e)}"

# Initialize session state
if 'agent_connector' not in st.session_state:
    st.session_state.agent_connector = AWSAgentConnector()
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'session_id' not in st.session_state:
    st.session_state.session_id = f"session-{int(time.time())}"
if 'connected' not in st.session_state:
    st.session_state.connected = False

# Main header
st.markdown("""
<div class="main-header">
    <h1>📦 Shipping Agent Assistant</h1>
    <p>Connect your AWS Bedrock Agent for intelligent shipping assistance</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for AWS configuration
with st.sidebar:
    st.header("🔧 AWS Agent Configuration")
    
    with st.form("aws_config"):
        # Key fields are never pre-filled, so secrets from the environment
        # are not sent to the browser. Leave both blank to use the
        # environment / AWS profile instead.
        aws_access_key = st.text_input(
            "AWS Access Key ID", type="password",
            placeholder="Blank = use env / AWS profile"
        )
        aws_secret_key = st.text_input(
            "AWS Secret Access Key", type="password",
            placeholder="Blank = use env / AWS profile"
        )
        region = st.selectbox(
            "AWS Region", AWS_REGIONS,
            index=AWS_REGIONS.index(ENV_REGION) if ENV_REGION else 0
        )
        agent_id = st.text_input("Bedrock Agent ID", value=os.getenv("BEDROCK_AGENT_ID", ""))
        agent_alias_id = st.text_input(
            "Agent Alias ID", value=os.getenv("BEDROCK_AGENT_ALIAS_ID") or "TSTALIASID"
        )

        submit_config = st.form_submit_button("Connect to Agent")

        if submit_config:
            if bool(aws_access_key) != bool(aws_secret_key):
                st.error("Enter both the Access Key ID and the Secret Access Key, or leave both blank")
            elif all([region, agent_id, agent_alias_id]):
                with st.spinner("Connecting to AWS Bedrock Agent..."):
                    success, message = st.session_state.agent_connector.initialize_connection(
                        aws_access_key, aws_secret_key, region, agent_id, agent_alias_id
                    )
                    
                    if success:
                        st.session_state.connected = True
                        st.success(message)
                    else:
                        st.session_state.connected = False
                        st.error(message)
            else:
                st.error("Please fill in all required fields")

# Connection status
if st.session_state.connected:
    st.markdown("""
    <div class="status-box status-connected">
        ✅ <strong>Connected</strong> - Your AWS Bedrock Agent is ready to assist!
    </div>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="status-box status-disconnected">
        ❌ <strong>Not Connected</strong> - Please configure your AWS credentials in the sidebar
    </div>
    """, unsafe_allow_html=True)

# Main chat interface
st.header("💬 Chat with Your Agent")

# Display chat history
chat_container = st.container()
with chat_container:
    for message in st.session_state.messages:
        # Escape user/agent text so it shows as text instead of being
        # injected as HTML, and keep line breaks without blank lines that
        # would end the HTML block.
        content = html.escape(message["content"]).replace("\n", "<br>")
        if message["role"] == "user":
            st.markdown(f"""
            <div class="user-message">
                <strong>You:</strong> {content}
                <small style="float: right; color: #666;">{message["timestamp"]}</small>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="agent-message">
                <strong>Agent:</strong> {content}
                <small style="float: right; color: #666;">{message["timestamp"]}</small>
            </div>
            """, unsafe_allow_html=True)

# Input form
with st.form("chat_form", clear_on_submit=True):
    col1, col2 = st.columns([4, 1])
    
    with col1:
        user_input = st.text_input(
            "Ask your shipping agent anything...",
            placeholder="e.g., What are the shipping rates to New York?",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.form_submit_button("Send 📤", use_container_width=True)

    if send_button and user_input:
        if not st.session_state.connected:
            st.error("Please connect to your AWS agent first using the sidebar configuration.")
        else:
            # Add user message
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.messages.append({
                "role": "user",
                "content": user_input,
                "timestamp": timestamp
            })
            
            # Get agent response
            with st.spinner("Agent is thinking..."):
                response = st.session_state.agent_connector.send_message(
                    user_input, 
                    st.session_state.session_id
                )
                
                # Add agent response
                st.session_state.messages.append({
                    "role": "agent",
                    "content": response,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
            
            # Rerun to update the chat
            st.rerun()

# Quick action buttons
st.header("🚀 Quick Actions")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("📋 Get Shipping Rates", use_container_width=True):
        if st.session_state.connected:
            quick_message = "Can you help me get shipping rates for a package?"
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.messages.append({
                "role": "user",
                "content": quick_message,
                "timestamp": timestamp
            })
            
            with st.spinner("Getting shipping rates..."):
                response = st.session_state.agent_connector.send_message(
                    quick_message, 
                    st.session_state.session_id
                )
                st.session_state.messages.append({
                    "role": "agent",
                    "content": response,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
            st.rerun()
        else:
            st.warning("Connect to your agent in the sidebar first.")

with col2:
    if st.button("📦 Track Package", use_container_width=True):
        if st.session_state.connected:
            quick_message = "I need help tracking a package. What information do you need?"
            timestamp = datetime.now().strftime("%H:%M:%S")
            st.session_state.messages.append({
                "role": "user",
                "content": quick_message,
                "timestamp": timestamp
            })
            
            with st.spinner("Preparing tracking assistance..."):
                response = st.session_state.agent_connector.send_message(
                    quick_message, 
                    st.session_state.session_id
                )
                st.session_state.messages.append({
                    "role": "agent",
                    "content": response,
                    "timestamp": datetime.now().strftime("%H:%M:%S")
                })
            st.rerun()
        else:
            st.warning("Connect to your agent in the sidebar first.")

with col3:
    if st.button("🔄 Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.session_state.session_id = f"session-{int(time.time())}"
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <small>Powered by AWS Bedrock Agent & Streamlit | Session ID: {}</small>
</div>
""".format(st.session_state.session_id), unsafe_allow_html=True)
