import streamlit as st
from PIL import Image
import base64
import time
import random
from g4f.client import Client

# Page configuration
st.set_page_config(
    page_title="InfluenceIQ Bot",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for the space/tech theme
def add_bg_from_local(image_file):
    with open(image_file, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode()
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url(data:image/png;base64,{encoded_string});
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

# Since we can't access local files in this environment, let's use a CSS background instead
st.markdown(
    """
    <style>
    .stApp {
        background-color: #000000;
        background-image: radial-gradient(#ffffff15 1px, transparent 1px);
        background-size: 20px 20px;
    }
    
    .title {
        font-family: 'Courier New', monospace;
        font-size: 3.5rem;
        color: white;
        text-align: center;
        padding: 1rem 0;
        text-shadow: 0 0 10px #00f3ff, 0 0 20px #00f3ff, 0 0 30px #00f3ff;
        letter-spacing: 3px;
    }
    
    .subtitle {
        font-family: 'Arial', sans-serif;
        font-size: 1.2rem;
        color: #a0a0a0;
        text-align: center;
        margin-bottom: 2rem;
    }
    
    .chat-container {
        background-color: rgba(0, 0, 0, 0.7);
        border-radius: 10px;
        padding: 20px;
        border: 1px solid #00f3ff;
        box-shadow: 0 0 10px #00f3ff;
    }
    
    .user-message {
        background-color: rgba(100, 100, 255, 0.2);
        border-left: 4px solid #5050ff;
        padding: 10px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }
    
    .bot-message {
        background-color: rgba(100, 255, 255, 0.1);
        border-left: 4px solid #00f3ff;
        padding: 10px;
        margin: 10px 0;
        border-radius: 0 10px 10px 0;
    }
    
    .stTextInput > div > div > input {
        background-color: rgba(0, 0, 0, 0.6);
        color: white;
        border: 1px solid #00f3ff;
        border-radius: 5px;
    }
    
    .stButton > button {
        background-color: #00f3ff;
        color: black;
        font-weight: bold;
        border: none;
        transition: all 0.3s;
    }
    
    .stButton > button:hover {
        background-color: #ffffff;
        box-shadow: 0 0 15px #00f3ff;
        transform: translateY(-2px);
    }
    
    .metrics-container {
        background-color: rgba(0, 0, 0, 0.7);
        border-radius: 10px;
        padding: 15px;
        border: 1px solid #00f3ff;
        margin-top: 20px;
    }
    
    .metric-item {
        padding: 10px;
        margin: 5px 0;
        border-left: 3px solid #00f3ff;
        background-color: rgba(0, 243, 255, 0.1);
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

# Initialize the client
@st.cache_resource
def get_client():
    return Client()

client = get_client()

# Initialize session state for chat history
if 'messages' not in st.session_state:
    st.session_state.messages = []

# Initialize session state for tracking the last processed input
if 'last_processed_input' not in st.session_state:
    st.session_state.last_processed_input = ""

# Function to handle form submission
def handle_submit():
    input_text = st.session_state.user_text
    
    # Check if this input has already been processed
    if input_text and input_text != st.session_state.last_processed_input:
        # Mark this input as processed
        st.session_state.last_processed_input = input_text
        
        # Add user message to chat
        st.session_state.messages.append({"role": "user", "content": input_text})
        
        # Clear the input field after submission
        st.session_state.user_text = ""
        
        # Show typing indicator
        with st.spinner("InfluenceIQ Bot is thinking..."):
            # Prepare context for the model
            context = """
            InfluenceIQ is an AI-powered system that ranks who really matters in the digital world.
            
            Key Features:
            - Measures credibility & trustworthiness in a person's field
            - Tracks fame longevity (how long someone has remained relevant)
            - Analyzes meaningful engagement (positive influence vs. just trending)
            - Creates fair ratings that distinguish consistent achievers from short-term viral hits
            
            Key Challenges InfluenceIQ Addresses:
            - Fighting fake fame by preventing spam reviews and manipulative ratings
            - Balancing recent buzz with established legacy when measuring influence
            - Providing real-time ratings that adapt with trends while staying credible
            - Using AI responsibly to ensure unbiased results with ethical considerations
            
            Benefits:
            - Bridges the fame gap by going beyond just followers and likes
            - Uses AI for fair evaluation of genuine influence
            - Provides value to recruiters, brands, and researchers seeking credible collaborators
            - Offers a dynamic rating system that evolves with changing times
            
            The web application has a sleek, futuristic design with a space/tech theme featuring a robot
            mascot. The interface is minimalist with navigation options for Home, Contacts, Projects, and About.
            """
            
            # Prepare the prompt with user query and context
            prompt = f"User asked about InfluenceIQ: '{input_text}'\n\nInformation about InfluenceIQ:\n{context}\n\nProvide a helpful, conversational response to the user's query as the InfluenceIQ chatbot. Keep responses concise, informative, and engaging."
            
            try:
                # Get response from model
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{"role": "user", "content": prompt}],
                    web_search=False
                )
                bot_response = response.choices[0].message.content
            except Exception as e:
                bot_response = f"I'm sorry, I encountered an error: {str(e)}. Please try again later."
        
        # Add bot response to chat
        st.session_state.messages.append({"role": "assistant", "content": bot_response})

# Header
st.markdown("<h1 class='title'>InfluenceIQ</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>The AI-Powered System That Ranks Who Really Matters!</p>", unsafe_allow_html=True)

# Layout with columns
col1, col2 = st.columns([2, 1])

with col1:
    # Chat interface
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"<div class='user-message'><strong>You:</strong> {message['content']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='bot-message'><strong>InfluenceIQ Bot:</strong> {message['content']}</div>", unsafe_allow_html=True)
    
    # Chat input with form
    with st.form(key="chat_form", clear_on_submit=True):
        # Initialize the text input state if it doesn't exist
        if "user_text" not in st.session_state:
            st.session_state.user_text = ""
        
        st.text_input(
            "Ask about InfluenceIQ:", 
            key="user_text", 
            placeholder="e.g., How does InfluenceIQ measure credibility?"
        )
        
        submit_button = st.form_submit_button(label="Send", on_click=handle_submit)
    
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    # Side panel with key metrics
    st.markdown("<div class='metrics-container'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #00f3ff; text-align: center;'>Key Metrics</h3>", unsafe_allow_html=True)
    
    metrics = [
        "⭐ Credibility & Trustworthiness",
        "⏳ Fame Longevity",
        "📈 Meaningful Engagement",
        "🔒 Anti-Manipulation Systems",
        "⚖️ Buzz vs. Legacy Balance",
        "🌐 Real-Time Adaptation"
    ]
    
    for metric in metrics:
        st.markdown(f"<div class='metric-item'>{metric}</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Demo visualization
    st.markdown("<div class='metrics-container'>", unsafe_allow_html=True)
    st.markdown("<h3 style='color: #00f3ff; text-align: center;'>Sample Influence Rating</h3>", unsafe_allow_html=True)
    
    # Random data for visualization
    if 'random_data' not in st.session_state:
        st.session_state.random_data = [random.randint(60, 95) for _ in range(3)]
    
    col_a, col_b, col_c = st.columns(3)
    col_a.metric("Credibility", f"{st.session_state.random_data[0]}%", "+5%")
    col_b.metric("Longevity", f"{st.session_state.random_data[1]}%", "+2%")
    col_c.metric("Engagement", f"{st.session_state.random_data[2]}%", "-3%")
    
    # Reset button for demo
    if st.button("Generate New Rating"):
        st.session_state.random_data = [random.randint(60, 95) for _ in range(3)]
        st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <div style="text-align: center; margin-top: 30px; color: #a0a0a0; font-size: 0.8rem;">
        InfluenceIQ © 2025 | Redefining fame—fairly, intelligently, and transparently
    </div>
    """, 
    unsafe_allow_html=True
)