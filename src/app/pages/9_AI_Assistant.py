import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from supabase import create_client
import plotly.graph_objects as go
import time
from src.app.config import SUPABASE_URL, SUPABASE_KEY

# Page config
st.set_page_config(page_title="Virtual Assistant - Rahhal", page_icon="🤖", layout="wide")

# Load environment variables

# Initialize Supabase
@st.cache_resource
def init_supabase():
    if SUPABASE_URL and SUPABASE_KEY:
        return create_client(SUPABASE_URL, SUPABASE_KEY)
    return None

supabase = init_supabase()

# Custom CSS for premium design
st.markdown("""
<style>
    /* Premium Color Palette */
    :root {
        --primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        --secondary-gradient: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        --success-color: #10b981;
        --info-color: #3b82f6;
        --warning-color: #f59e0b;
    }
    
    /* Main Container */
    .main-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    
    /* Header */
    .assistant-header {
        text-align: center;
        color: white;
        margin-bottom: 2rem;
    }
    
    .assistant-header h1 {
        font-size: 2.5rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 10px rgba(0,0,0,0.2);
    }
    
    .assistant-header p {
        font-size: 1.1rem;
        opacity: 0.95;
        font-weight: 300;
    }
    
    /* Chat Container */
    .chat-container {
        background: transparent;
        border-radius: 15px;
        padding: 0.5rem;
        min-height: 400px;
        max-height: 500px;
        overflow-y: auto;
        margin-bottom: 0.5rem;
        margin-top: 0.5rem;
    }
    
    /* Message Bubbles */
    .message {
        margin-bottom: 1rem;
        animation: fadeIn 0.3s ease-in;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .user-message {
        text-align: right;
    }
    
    .assistant-message {
        text-align: left;
    }
    
    .message-bubble {
        display: inline-block;
        padding: 1rem 1.5rem;
        border-radius: 20px;
        max-width: 70%;
        word-wrap: break-word;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .user-bubble {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-bottom-right-radius: 5px;
    }
    
    .assistant-bubble {
        background: #f3f4f6;
        color: #1f2937;
        border-bottom-left-radius: 5px;
    }
    
    /* Quick Actions */
    .quick-actions {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin-top: 1rem;
    }
    
    .quick-action-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        text-align: center;
        cursor: pointer;
        transition: all 0.3s ease;
        border: 2px solid #e5e7eb;
    }
    
    .quick-action-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border-color: #667eea;
    }
    
    .quick-action-icon {
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
    }
    
    .quick-action-title {
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.25rem;
    }
    
    .quick-action-desc {
        font-size: 0.85rem;
        color: #6b7280;
    }
    
    /* Stats Cards */
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .stat-card {
        background: white;
        padding: 1.25rem;
        border-radius: 12px;
        text-align: center;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    }
    
    .stat-value {
        font-size: 2rem;
        font-weight: 700;
        background: var(--primary-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .stat-label {
        font-size: 0.85rem;
        color: #6b7280;
        margin-top: 0.25rem;
    }
    
    /* Typing Indicator */
    .typing-indicator {
        display: inline-block;
        padding: 1rem 1.5rem;
        background: #f3f4f6;
        border-radius: 20px;
        border-bottom-left-radius: 5px;
    }
    
    .typing-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #9ca3af;
        margin: 0 2px;
        animation: typing 1.4s infinite;
    }
    
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typing {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-10px); }
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'conversation_started' not in st.session_state:
    st.session_state.conversation_started = False

# Helper Functions
@st.cache_data(ttl=300)
def get_current_stats():
    """Get real-time park statistics"""
    if not supabase:
        return None
    
    try:
        # Get facility count
        facilities = supabase.table("facilities").select("*", count="exact").execute()
        facility_count = len(facilities.data) if facilities.data else 0
        
        # Get average wait time
        wait_times = supabase.table("waiting_times").select("wait_time_max").limit(100).execute()
        avg_wait = np.mean([w['wait_time_max'] for w in wait_times.data]) if wait_times.data else 0
        
        # Get review count
        reviews = supabase.table("reviews").select("*", count="exact").execute()
        review_count = len(reviews.data) if reviews.data else 0
        
        # Get average sentiment
        sentiments = supabase.table("reviews").select("sentiment_score").execute()
        avg_sentiment = np.mean([s['sentiment_score'] for s in sentiments.data if s['sentiment_score']]) if sentiments.data else 0
        
        return {
            'facilities': facility_count,
            'avg_wait': int(avg_wait),
            'reviews': review_count,
            'sentiment': round(avg_sentiment, 2)
        }
    except:
        return None

def get_smart_response(user_input):
    """Generate intelligent responses based on user input"""
    user_input_lower = user_input.lower()
    
    # Greeting
    if any(word in user_input_lower for word in ['hello', 'hi', 'hey', 'مرحبا', 'السلام']):
        return "Hello! Welcome to Rahhal Park Virtual Assistant. I'm here to help you have the best experience possible. How can I assist you today?"
    
    # Wait times
    elif any(word in user_input_lower for word in ['wait', 'waiting', 'انتظار', 'وقت']):
        stats = get_current_stats()
        if stats:
            return f"Current average wait time across the park is approximately **{stats['avg_wait']} minutes**. I recommend visiting during off-peak hours (10 AM - 12 PM or 3 PM - 5 PM) for shorter wait times."
        return "Wait times vary throughout the day. Generally, mornings and late afternoons have shorter queues."
    
    # Weather
    elif any(word in user_input_lower for word in ['weather', 'طقس', 'حرارة']):
        return f"Today's weather is perfect for visiting! Temperature is comfortable and conditions are ideal for outdoor activities. Don't forget sunscreen!"
    
    # Recommendations
    elif any(word in user_input_lower for word in ['recommend', 'suggest', 'best', 'توصية', 'أفضل']):
        return "Based on current conditions, I recommend:\n\n1. **Water Ride** - Low wait time, perfect for the weather\n2. **Oz Theatre** - Great show starting in 30 minutes\n3. **Pirate Ship** - Thrilling experience with moderate queue\n\nWould you like more details about any of these?"
    
    # Crowd levels
    elif any(word in user_input_lower for word in ['crowd', 'busy', 'زحام', 'مزدحم']):
        return "Current crowd levels are **moderate**. The park is busiest between 12 PM - 3 PM. For a more relaxed experience, I suggest visiting popular attractions either before 11 AM or after 4 PM."
    
    # Facilities
    elif any(word in user_input_lower for word in ['facility', 'facilities', 'ride', 'attraction', 'مرافق', 'ألعاب']):
        stats = get_current_stats()
        if stats:
            return f"We have **{stats['facilities']} facilities** available including rides, shows, and dining options. All facilities are currently operational. Would you like recommendations based on your preferences?"
        return "We offer a variety of attractions including thrilling rides, family shows, and dining experiences. What type of activity interests you?"
    
    # Help
    elif any(word in user_input_lower for word in ['help', 'مساعدة']):
        return """I can help you with:
        
• **Wait Times** - Check current queue lengths
• **Recommendations** - Get personalized suggestions
• **Crowd Levels** - Find the best times to visit
• **Weather** - Current conditions
• **Facilities** - Information about rides and attractions
• **Directions** - Navigate the park

Just ask me anything!"""
    
    # Default
    else:
        return "I'm here to help! You can ask me about wait times, recommendations, crowd levels, weather, or any facility information. What would you like to know?"

# Header
st.markdown("""
<div class="main-container">
    <div class="assistant-header">
        <div style="display: flex; justify-content: center; align-items: center; gap: 15px; margin-bottom: 10px;">
            <svg xmlns="http://www.w3.org/2000/svg" width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="12" cy="5" r="2"/><path d="M12 7v4"/><line x1="8" y1="16" x2="8" y2="16"/><line x1="16" y1="16" x2="16" y2="16"/></svg>
            <h1 style="margin: 0;">Rahhal Virtual Assistant</h1>
        </div>
        <p>Your intelligent guide to the perfect park experience</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Stats Section
stats = get_current_stats()
if stats:
    st.markdown('<div class="stats-grid">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{stats['facilities']}</div>
            <div class="stat-label">Active Facilities</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{stats['avg_wait']}</div>
            <div class="stat-label">Avg Wait (min)</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value">{stats['reviews']}</div>
            <div class="stat-label">Total Reviews</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        # Use SVG icons for sentiment
        if stats['sentiment'] > 0.5:
            sentiment_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M8 14s1.5 2 4 2 4-2 4-2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>'
        elif stats['sentiment'] > 0:
            sentiment_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#f59e0b" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="8" y1="15" x2="16" y2="15"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>'
        else:
            sentiment_icon = '<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M16 16s-1.5-2-4-2-4 2-4 2"/><line x1="9" y1="9" x2="9.01" y2="9"/><line x1="15" y1="9" x2="15.01" y2="9"/></svg>'
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-value" style="display: flex; justify-content: center; align-items: center; height: 48px;">{sentiment_icon}</div>
            <div class="stat-label">Visitor Sentiment</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Quick Actions - Process button clicks first
if 'quick_action_clicked' not in st.session_state:
    st.session_state.quick_action_clicked = None

col1, col2, col3, col4 = st.columns(4)

with col1:
    if st.button("Wait Times", icon=":material/timer:", key="btn_wait", use_container_width=True):
        st.session_state.quick_action_clicked = "What are the current wait times?"

with col2:
    if st.button("Recommendations", icon=":material/target:", key="btn_rec", use_container_width=True):
        st.session_state.quick_action_clicked = "What do you recommend?"

with col3:
    if st.button("Crowd Levels", icon=":material/groups:", key="btn_crowd", use_container_width=True):
        st.session_state.quick_action_clicked = "How crowded is it?"

with col4:
    if st.button("Weather", icon=":material/wb_sunny:", key="btn_weather", use_container_width=True):
        st.session_state.quick_action_clicked = "What's the weather like?"

# Process quick action
if st.session_state.quick_action_clicked:
    st.session_state.messages.append({"role": "user", "content": st.session_state.quick_action_clicked})
    response = get_smart_response(st.session_state.quick_action_clicked)
    st.session_state.messages.append({"role": "assistant", "content": response})
    st.session_state.conversation_started = True
    st.session_state.quick_action_clicked = None
    st.rerun()

# Chat container (reduced spacing)
st.markdown("<div style='margin-top: -20px;'></div>", unsafe_allow_html=True)
chat_container = st.container()

with chat_container:
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    # Display welcome message if no conversation
    if not st.session_state.conversation_started:
        st.markdown("""
        <div class="message assistant-message">
            <div class="message-bubble assistant-bubble">
                Hello! I'm your Rahhal Park Virtual Assistant. I can help you with:
                <br><br>
                • Current wait times and crowd levels<br>
                • Personalized activity recommendations<br>
                • Weather updates<br>
                • Facility information<br>
                • Navigation assistance<br>
                <br>
                How can I help you today?
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Display conversation history
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f"""
            <div class="message user-message">
                <div class="message-bubble user-bubble">
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="message assistant-message">
                <div class="message-bubble assistant-bubble">
                    {message["content"]}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.session_state.conversation_started = True
    
    # Generate response
    response = get_smart_response(user_input)
    st.session_state.messages.append({"role": "assistant", "content": response})
    
    # Rerun to update chat
    st.rerun()

# Clear chat button
if st.session_state.messages:
    if st.button("Clear Chat", icon=":material/delete:", type="secondary"):
        st.session_state.messages = []
        st.session_state.conversation_started = False
        st.rerun()
