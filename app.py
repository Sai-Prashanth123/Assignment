import streamlit as st
import json
import time
import random
from datetime import datetime
import os
from typing import Tuple
from config import *
from AI import generate_next_question, generate_follow_up_question, generate_behavioral_question, generate_closing_question, analyze_user_response
from prompt import get_welcome_message, InterviewPhase
from db import MongoDBManager  

try:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer  # type: ignore
except Exception:
    SentimentIntensityAnalyzer = None  
try:
    from deep_translator import GoogleTranslator  # type: ignore
except Exception:
    GoogleTranslator = None  # type: ignore

# Initialize MongoDB connection
if 'db_manager' not in st.session_state:
    st.session_state.db_manager = MongoDBManager()
    if st.session_state.db_manager.connect():
        st.session_state.db_connected = True
    else:
        st.session_state.db_connected = False
        st.warning("⚠️ Could not connect to database. Interview data will not be saved.")

# Page configuration
st.set_page_config(
    page_title=APP_TITLE,
    page_icon=APP_ICON,
    layout=PAGE_LAYOUT,
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/icon?family=Material+Icons');
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    
    .sub-header {
        font-size: 1.5rem;
        text-align: center;
        color: #666;
        margin-bottom: 3rem;
    }
    
    .start-button {
        display: block;
        margin: 0 auto;
        padding: 1rem 3rem;
        font-size: 1.2rem;
        background-color: #1f77b4;
        color: white;
        border: none;
        border-radius: 10px;
        cursor: pointer;
    }
    
    .bot-message {
        background-color: #2d3748;
        color: #e2e8f0;
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 0.5rem;
        width: fit-content;
        max-width: 80%;
        margin-right: auto;
        position: relative;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .bot-message .message-row { display: flex; gap: 0.5rem; align-items: flex-start; }
    
    .user-message {
        background-color: #4a5568;
        color: #e2e8f0;
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 0.5rem;
        width: fit-content;
        max-width: 80%;
        margin-left: auto;
        text-align: right;
        position: relative;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .user-message .message-row { display: flex; gap: 0.5rem; align-items: flex-start; justify-content: flex-end; }
    
    /* Icon styling */
    .message-icon {
        font-size: 1.2rem;
        display: flex;
        align-items: center;
        justify-content: center;
        height: 100%;
    }
    
    /* Material icon styling */
    .material-icons {
        font-size: 32px !important;
        color: #e2e8f0 !important;
        opacity: 0.9;
        margin: 0;
        padding: 0;
    }
    
    /* Bot icon specific styling */
    .bot-icon {
        color: #3182ce !important;
    }
    
    /* User icon specific styling */
    .user-icon {
        color: #e2e8f0 !important;
    }
    
    .message-time {
        font-size: 0.75rem;
        opacity: 0.7;
        margin-top: 0.5rem;
    }
    
    .bot-message .message-time {
        text-align: left;
    }
    
    .user-message .message-time {
        text-align: right;
    }
    
    .profile-card {
        background-color: #2d3748;
        color: #e2e8f0;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3182ce;
        margin-bottom: 2rem;
    }
    
    /* Sticky bottom navbar styles */
    .sticky-bottom-navbar {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #1a202c;
        border-top: 1px solid #2d3748;
        padding: 1rem;
        z-index: 1000;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.3);
    }
    
    .input-container {
        display: flex;
        gap: 0.5rem;
        max-width: 800px;
        margin: 0 auto;
    }
    
    .chat-input {
        flex: 1;
        background-color: #2d3748;
        border: 1px solid #4a5568;
        border-radius: 25px;
        padding: 0.75rem 1rem;
        color: #e2e8f0;
        font-size: 1rem;
    }
    
    .chat-input:focus {
        outline: none;
        border-color: #3182ce;
        box-shadow: 0 0 0 2px rgba(49, 130, 206, 0.2);
    }
    
    .send-button {
        background-color: #3182ce;
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.75rem 1.5rem;
        font-size: 1rem;
        cursor: pointer;
        transition: background-color 0.2s;
    }
    
    .send-button:hover {
        background-color: #2c5aa0;
    }
    
    /* Fixed input bar container */
    .fixed-input-container {
        position: fixed;
        bottom: 0;
        left: 0;
        right: 0;
        background-color: #1a202c;
        border-top: 1px solid #2d3748;
        padding: 1rem;
        z-index: 1000;
        box-shadow: 0 -2px 10px rgba(0,0,0,0.3);
    }
    
    /* Add bottom padding to main content to prevent overlap with fixed input bar */
    .main-content {
        padding-bottom: 120px;
        max-height: calc(100vh - 220px);
        overflow-y: auto;
    }
    
    /* Style the input area */
    div[data-testid="stTextInput"] {
        background-color: transparent !important;
        border: 1px solid #4a5568 !important;
        border-radius: 25px !important;
        color: #e2e8f0 !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
    }
    
    div[data-testid="stTextInput"] input {
        background-color: transparent !important;
        border: 1px solid #4a5568 !important;
        border-radius: 25px !important;
        color: #e2e8f0 !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
    }
    
    div[data-testid="stTextInput"] input:focus {
        border-color: #3182ce !important;
        box-shadow: 0 0 0 2px rgba(49, 130, 206, 0.2) !important;
    }
    
    /* Remove background from text areas */
    div[data-testid="stTextArea"] {
        background-color: transparent !important;
    }
    
    div[data-testid="stTextArea"] textarea {
        background-color: transparent !important;
        border: 1px solid #4a5568 !important;
        border-radius: 25px !important;
        color: #e2e8f0 !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
    }
    
    /* Remove background from select boxes */
    div[data-testid="stSelectbox"] {
        background-color: transparent !important;
    }
    
    div[data-testid="stSelectbox"] select {
        background-color: transparent !important;
        border: 1px solid #4a5568 !important;
        border-radius: 25px !important;
        color: #e2e8f0 !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
    }
    
    /* Remove background from select sliders */
    div[data-testid="stSelectSlider"] {
        background-color: transparent !important;
    }
    
    div[data-testid="stSelectSlider"] select {
        background-color: transparent !important;
        border: 1px solid #4a5568 !important;
        border-radius: 25px !important;
        color: #e2e8f0 !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
    }
    
    button[data-testid="stButton"] {
        background-color: #3182ce !important;
        color: white !important;
        border: none !important;
        border-radius: 25px !important;
        padding: 0.75rem 1.5rem !important;
        font-size: 1rem !important;
        transition: background-color 0.2s !important;
    }
    
    button[data-testid="stButton"]:hover {
        background-color: #2c5aa0 !important;
    }

    /* Streamlit chat bubbles: left (assistant) and right (user) */
    [data-testid="stChatMessage"],
    [data-testid="stChatMessageUser"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0.25rem 0 !important;
        display: flex;
    }

    [data-testid="stChatMessage"] { justify-content: flex-start; }
    [data-testid="stChatMessageUser"] { justify-content: flex-end; }

    [data-testid="stChatMessage"] .stMarkdown { max-width: 80%; }
    [data-testid="stChatMessage"] .stMarkdown p {
        background: #2d3748;
        color: #ffffff;
        padding: 0.75rem 1rem;
        border-radius: 16px 16px 16px 4px;
        display: inline-block;
        margin: 0;
    }
    [data-testid="stChatMessageUser"] .stMarkdown { margin-left: auto; text-align: right; max-width: 80%; }
    [data-testid="stChatMessageUser"] .stMarkdown p {
        background: #4a5568;
        color: #ffffff;
        padding: 0.75rem 1rem;
        border-radius: 16px 16px 4px 16px;
        display: inline-block;
        margin: 0;
    }

    /* Custom container-based chat (left-right rows) */
    .chat-container { display: flex; flex-direction: column; gap: 0.85rem; padding: 0.25rem 0; }
    .chat-row { display: flex; width: 100%; }
    .assistant-row { justify-content: flex-start; }
    .user-row { justify-content: flex-end; }
    .chat-bubble {
        max-width: 80%;
        padding: 0.85rem 1.1rem;
        border-radius: 16px;
        color: #ffffff;
        margin: 2px 0;
        line-height: 1.5;
        overflow-wrap: anywhere;
        word-break: break-word;
        white-space: pre-wrap;
    }
    .assistant-bubble { background: #2d3748; border-radius: 16px 16px 16px 4px; }
    .user-bubble { background: #4a5568; border-radius: 16px 16px 4px 16px; }

    /* Typing dots animation */
    .typing { display: inline-flex; gap: 6px; align-items: center; }
    .typing span { width: 6px; height: 6px; background: #e2e8f0; opacity: 0.6; border-radius: 50%; display: inline-block; animation: typingBlink 1.2s infinite; }
    .typing span:nth-child(2) { animation-delay: 0.2s; }
    .typing span:nth-child(3) { animation-delay: 0.4s; }
    @keyframes typingBlink { 0%, 80%, 100% { transform: scale(0.6); opacity: 0.4; } 40% { transform: scale(1.0); opacity: 1; } }
    .send-status { font-size: 0.8rem; color: #a0aec0; opacity: 0.85; padding: 0 6px; }

</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'landing'
if 'candidate_info' not in st.session_state:
    st.session_state.candidate_info = {}
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'awaiting_response' not in st.session_state:
    st.session_state.awaiting_response = False
if '_last_prompt' not in st.session_state:
    st.session_state._last_prompt = ""
if 'sentiment' not in st.session_state:
    st.session_state.sentiment = []  
if 'language' not in st.session_state:
    st.session_state.language = {
        'detected': 'en',  
        'selected': 'Auto',  
        'code': 'en',  
    }
if 'preferences' not in st.session_state:
    st.session_state.preferences = {
            'tone': 'Professional',  
        'detail_level': 'Concise',  
    }
if 'question_count' not in st.session_state:
    st.session_state.question_count = 0  
if 'interview_completed' not in st.session_state:
    st.session_state.interview_completed = False  

# Technical questions based on tech stack
def generate_technical_questions(tech_stack):
    """Generate technical questions using the prompt management system"""
    
    return []

def landing_page():
    
    
    st.markdown(f'<h1 class="main-header">{APP_TITLE} {APP_ICON}</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">I\'ll guide you through a quick interview to learn about your skills and experience.</p>', unsafe_allow_html=True)
    
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Interview", key="start_interview", use_container_width=True):
            st.session_state.current_screen = 'form'
            st.rerun()
    
    st.markdown("---")
    
    
    st.markdown("### ✨ Key Features")
    
    
    col1, col2 = st.columns(2)
    with col1:
        with st.container():
            st.markdown("• **🎯 Personalized Experience**")
            st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;Customize AI response tone (Friendly / Professional / Formal) and detail level (Concise / Balanced / In-depth) for a tailored interview experience.")
            st.markdown("• **🌐 Multi-Language Support**")
            st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;Chat seamlessly in 11+ languages with automatic language detection, making the platform globally accessible.")
    
    with col2:
        with st.container():
            st.markdown("• **🤖 Dynamic Question Generation**")
            st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;AI generates interview questions intelligently based on your tech stack, role, and experience level.")
            st.markdown("• **🔄 Adaptive Follow-Ups**")
            st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;AI asks context-aware follow-up questions based on your responses, allowing deeper evaluation and a realistic interview flow.")
    
    
    with st.container():
        st.markdown("• **📝 Complete Interview Transcript**")
        st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;Provides a full conversation history along with sentiment analysis of each response for detailed review.")
        st.markdown("• **📊 Performance Metrics & Insights**")
        st.markdown("&nbsp;&nbsp;&nbsp;&nbsp;Track question count, response quality, message analysis, and sentiment trends to evaluate performance and identify improvement areas.")

def interview_form():
    st.markdown('<h1 class="main-header">Candidate Information</h1>', unsafe_allow_html=True)
    
    with st.form("candidate_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            full_name = st.text_input("Full Name", placeholder="Enter your full name")
            email = st.text_input("Email Address", placeholder="your.email@example.com")
            phone = st.text_input("Phone Number", placeholder="+1 (555) 123-4567")
            years_experience = st.selectbox(
                "Years of Experience",
                EXPERIENCE_LEVELS
            )
        
        with col2:
            desired_position = st.text_input("Desired Position(s)", placeholder="e.g., Software Engineer, Full Stack Developer")
            current_location = st.text_input("Current Location", placeholder="City, State/Country")
            tech_stack = st.text_area(
                "Tech Stack (comma-separated)",
                placeholder="e.g., Python, JavaScript, React, Django, AWS",
                help="List your technical skills separated by commas"
            )

        st.markdown("---")
        st.markdown("### Preferences & Language")
        pref_col1, pref_col2 = st.columns(2)
        with pref_col1:
            tone = st.select_slider(
                "Response tone",
                options=["Friendly", "Professional", "Formal"],
                value=st.session_state.preferences.get('tone', 'Professional')
            )
            detail_level = st.select_slider(
                "Detail level",
                options=["Concise", "Balanced", "In-depth"],
                value=st.session_state.preferences.get('detail_level', 'Concise')
            )
        with pref_col2:
            lang_options = [
                "Auto", "English (en)", "Spanish (es)", "French (fr)", "German (de)",
                "Hindi (hi)", "Chinese (zh)", "Arabic (ar)", "Portuguese (pt)", "Russian (ru)", "Japanese (ja)"
            ]
            current_label = st.session_state.language.get('selected', 'Auto')
            try:
                current_index = lang_options.index(current_label)
            except ValueError:
                current_index = 0
            selected_label = st.selectbox("Chat language", options=lang_options, index=current_index)
        
        submitted = st.form_submit_button("Submit & Start Chat", use_container_width=True)
        
        if submitted:
            
            if full_name and email and tech_stack:
                st.session_state.candidate_info = {
                    'full_name': full_name,
                    'email': email,
                    'phone': phone,
                    'years_experience': years_experience,
                    'desired_position': desired_position,
                    'current_location': current_location,
                    'tech_stack': tech_stack
                }
                
                st.session_state.preferences['tone'] = tone
                st.session_state.preferences['detail_level'] = detail_level
                st.session_state.language['selected'] = selected_label
                st.session_state.language['code'] = 'en' if selected_label == 'Auto' else selected_label.split('(')[-1].strip(')')
                
                
                st.session_state.current_screen = 'chat'
                st.rerun()
            else:
                st.error("Please fill in at least Full Name, Email, and Tech Stack fields.")

def display_interview_results():
    """Display the complete interview results in a formatted way"""
    
    
    st.markdown('<h1 class="main-header">📊 Interview Results</h1>', unsafe_allow_html=True)
    
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("🔄 Back to Chat", key="back_to_chat", use_container_width=True):
            st.session_state.current_screen = 'chat'
            st.rerun()
    with col3:
        if st.button("🏠 Back to Landing", key="back_to_landing", use_container_width=True):
            st.session_state.current_screen = 'landing'
            st.session_state.chat_messages = []
            st.session_state.candidate_info = {}
            st.session_state.messages = []
            st.session_state.sentiment = []
            st.session_state.question_count = 0
            st.session_state.interview_completed = False
            st.rerun()
    
    st.markdown("---")
    
    
    with st.expander("💬 Complete Interview Conversation", expanded=True):
        st.markdown("### Full Interview Transcript")
        for i, msg in enumerate(st.session_state.messages):
            if msg["role"] == "user":
                st.markdown(f"**👤 You (Message {i+1}):**")
                st.markdown(f"*{msg['content']}*")
                if i < len(st.session_state.sentiment):
                    score, label = st.session_state.sentiment[i]
                    st.markdown(f"*Sentiment: {label} ({score:.2f})*")
            else:
                st.markdown(f"**🤖 Interviewer (Message {i+1}):**")
                st.markdown(f"{msg['content']}")
            st.markdown("---")
    
    st.markdown("---")
    st.markdown("## 📊 Interview Results Summary")
    

    with st.expander("👤 Candidate Information", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Full Name:** {st.session_state.candidate_info.get('full_name', 'N/A')}")
            st.markdown(f"**Email:** {st.session_state.candidate_info.get('email', 'N/A')}")
            st.markdown(f"**Phone:** {st.session_state.candidate_info.get('phone', 'N/A')}")
        with col2:
            st.markdown(f"**Position:** {st.session_state.candidate_info.get('desired_position', 'N/A')}")
            st.markdown(f"**Experience:** {st.session_state.candidate_info.get('years_experience', 'N/A')}")
            st.markdown(f"**Location:** {st.session_state.candidate_info.get('current_location', 'N/A')}")
            st.markdown(f"**Tech Stack:** {st.session_state.candidate_info.get('tech_stack', 'N/A')}")
    
    
    with st.expander("📈 Interview Statistics", expanded=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Questions", st.session_state.question_count)
        with col2:
            st.metric("Total Messages", len(st.session_state.messages))
        with col3:
            if st.session_state.sentiment:
                avg_sentiment = sum([s[0] for s in st.session_state.sentiment]) / len(st.session_state.sentiment)
                st.metric("Avg Sentiment", f"{avg_sentiment:.2f}")
            else:
                st.metric("Avg Sentiment", "N/A")
    
    
    if st.session_state.sentiment:
        with st.expander("😊 Sentiment Analysis", expanded=True):
            positive_count = len([s for s in st.session_state.sentiment if s[1] == 'positive'])
            negative_count = len([s for s in st.session_state.sentiment if s[1] == 'negative'])
            neutral_count = len([s for s in st.session_state.sentiment if s[1] == 'neutral'])
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Positive", positive_count, delta=f"+{positive_count}")
            with col2:
                st.metric("Neutral", neutral_count, delta="0")
            with col3:
                st.metric("Negative", negative_count, delta=f"-{negative_count}")

def chat_interface():
    if st.session_state.candidate_info:
        with st.sidebar:
            st.markdown("### 👤 Candidate Profile")
            st.markdown(f"**Name:** {st.session_state.candidate_info.get('full_name', 'N/A')}")
            st.markdown(f"**Position:** {st.session_state.candidate_info.get('desired_position', 'N/A')}")
            st.markdown(f"**Experience:** {st.session_state.candidate_info.get('years_experience', 'N/A')}")
            st.markdown(f"**Tech Stack:** {st.session_state.candidate_info.get('tech_stack', 'N/A')}")
            st.markdown(f"**Location:** {st.session_state.candidate_info.get('current_location', 'N/A')}")
            
            st.markdown("---")

            
            with st.expander("Preferences & Language", expanded=True):
                st.markdown(f"**Tone:** {st.session_state.preferences.get('tone', 'Professional')}")
                st.markdown(f"**Detail:** {st.session_state.preferences.get('detail_level', 'Concise')}")
                st.markdown(f"**Language:** {st.session_state.language.get('selected', 'Auto')}")
            
            
            with st.expander("Interview Progress", expanded=True):
                st.markdown(f"**Questions Asked:** {st.session_state.question_count}/7")
                if st.session_state.interview_completed:
                    st.success("✅ Interview Completed!")
                else:
                    st.info("🔄 Interview in Progress...")
            

            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Back", key="back_button", use_container_width=True):
                    st.session_state.current_screen = 'form'
                    st.rerun()
            with col2:
                if st.button("Exit", key="exit_button", use_container_width=True):
                    
                    if st.session_state.get('db_connected', False) and not st.session_state.interview_completed:
                        save_interview_to_database()
                    elif st.session_state.interview_completed:
                        st.success("✅ Interview data already saved!")
                    
                    st.session_state.current_screen = 'landing'
                    st.session_state.chat_messages = []
                    st.session_state.candidate_info = {}
                    st.session_state.messages = []
                    st.session_state.sentiment = []
                    st.session_state.question_count = 0
                    st.session_state.interview_completed = False
                    st.rerun()
            
            
            st.markdown("---")
            if st.button("📊 View All Results", key="view_all_results", use_container_width=True):
                st.info("💡 To view all interview results, run the results viewer separately:")
                st.code("streamlit run results_viewer.py")
    else:
        
        with st.sidebar:
            st.markdown("### 👤 Candidate Profile")
            st.markdown("**No candidate information available**")
            st.markdown("Please complete the form to start the interview.")
    
    
    if not st.session_state.messages:
        
        st.session_state.question_count = 0
        st.session_state.interview_completed = False
        
        
        welcome_message = get_welcome_message(
            name=st.session_state.candidate_info.get('full_name', 'there'),
            tech_stack=st.session_state.candidate_info.get('tech_stack', 'your skills'),
            experience_level=st.session_state.candidate_info.get('years_experience', 'mid')
        )
        st.session_state.messages.append({"role": "assistant", "content": maybe_translate(welcome_message, target_language_code=current_target_language())})
        
        
        first_question = generate_next_question(
            candidate={**st.session_state.candidate_info, **st.session_state.preferences, 'target_language': st.session_state.language.get('code', 'en')},
            history=st.session_state.messages,
            user_latest=None,
            phase=InterviewPhase.WELCOME
        )
        
        # Debug logging for language handling
        print(f"DEBUG: Language selected: {st.session_state.language.get('selected', 'Auto')}")
        print(f"DEBUG: Language code: {st.session_state.language.get('code', 'en')}")
        print(f"DEBUG: Target language passed to AI: {st.session_state.language.get('code', 'en')}")
        
        if first_question.startswith("Environment variable GROQ_API_KEY"):
            st.info(first_question)
        else:
            st.session_state.messages.append({"role": "assistant", "content": first_question})
            st.session_state.question_count += 1  

    
    st.markdown("<div class='chat-container'>", unsafe_allow_html=True)
    for i, msg in enumerate(st.session_state.messages):
        if msg["role"] == "user":
            sent_html = sentiment_badge_html(i)
            st.markdown(
                f"<div class='chat-row user-row'><div class='chat-bubble user-bubble'>{msg['content']}{sent_html}</div></div>",
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"<div class='chat-row assistant-row'><div class='chat-bubble assistant-bubble'>{msg['content']}</div></div>",
                unsafe_allow_html=True,
            )
    st.markdown("</div>", unsafe_allow_html=True)
    
    
    if st.session_state.interview_completed:
        st.success("🎉 **Interview Completed Successfully!**")
        
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("📊 See Results", key="see_results", use_container_width=True):
                st.session_state.current_screen = 'results'
                st.rerun()

    
    if prompt := st.chat_input("Type your message..."):
        if not st.session_state.awaiting_response and prompt.strip() and prompt != st.session_state._last_prompt:
            
            detected_code = detect_language_code(prompt)
            st.session_state.language['detected'] = detected_code or st.session_state.language.get('detected', 'en')
            translated_in = maybe_translate(prompt, source_language_code=detected_code or 'auto', target_language_code='en')
            st.session_state.messages.append({"role": "user", "content": prompt})
            score, label = analyze_sentiment(translated_in)
            st.session_state.sentiment.append((score, label))
            st.session_state._last_prompt = prompt
            st.session_state.awaiting_response = True
            st.rerun()

    
    if st.session_state.awaiting_response:
        
        st.markdown("<div class='chat-row user-row'><div class='send-status'>Sending…</div></div>", unsafe_allow_html=True)
        
        st.markdown("<div class='chat-row assistant-row'><div class='chat-bubble assistant-bubble'><span class='typing'><span></span><span></span><span></span></div></div>", unsafe_allow_html=True)
        time.sleep(0.6)
        last = st.session_state._last_prompt or ""
        if last.lower() in EXIT_COMMANDS:
            response = random.choice(EXIT_MESSAGES).format(
                name=st.session_state.candidate_info.get('full_name', 'there')
            )
            response = maybe_translate(response, target_language_code=current_target_language())
            
            
            if st.session_state.get('db_connected', False):
                save_interview_to_database()
        else:
            
            response = generate_bot_response(last)
        st.session_state.messages.append({"role": "assistant", "content": response})
        st.session_state.awaiting_response = False
        st.rerun()

def generate_bot_response(user_input):
    """Use AI to generate the next question or follow-up based on conversation."""
    
    
    if st.session_state.question_count >= 7 and not st.session_state.interview_completed:
        
        closing_question = generate_closing_question(
            candidate={**st.session_state.candidate_info, **st.session_state.preferences, 'target_language': st.session_state.language.get('code', 'en')},
            history=st.session_state.messages
        )
        st.session_state.interview_completed = True
        
        
        if st.session_state.get('db_connected', False):
            save_interview_to_database()
        
        return closing_question
    
    
    if st.session_state.interview_completed:
        return "Thank you for completing the interview! Your responses have been recorded and saved. You can now exit the interview."
    
    
    response_analysis = analyze_user_response(user_input)
    
    
    if len(st.session_state.messages) > 2:  
        
        last_ai_message = None
        for msg in reversed(st.session_state.messages):
            if msg['role'] == 'assistant':
                last_ai_message = msg['content']
                break
        
        if last_ai_message and last_ai_message.endswith('?') and len(user_input.strip()) > 10:
            
            follow_up = generate_follow_up_question(
                candidate={**st.session_state.candidate_info, **st.session_state.preferences, 'target_language': st.session_state.language.get('code', 'en')},
                user_response=user_input,
                history=st.session_state.messages
            )
            st.session_state.question_count += 1  
            return follow_up
    
    
    
    next_question = generate_next_question(
        candidate={**st.session_state.candidate_info, **st.session_state.preferences, 'target_language': st.session_state.language.get('code', 'en')},
        history=st.session_state.messages,
        user_latest=user_input,
        phase=InterviewPhase.TECHNICAL  
    )
    st.session_state.question_count += 1  
    return next_question

def save_interview_to_database():
    """Save interview details and conversation to MongoDB"""
    try:
        if not st.session_state.get('db_connected', False):
            st.error("Database not connected. Interview data could not be saved.")
            return
        
        
        interview_data = {
            'candidate_name': st.session_state.candidate_info.get('full_name', 'Unknown'),
            'email': st.session_state.candidate_info.get('email', ''),
            'phone': st.session_state.candidate_info.get('phone', ''),
            'position': st.session_state.candidate_info.get('desired_position', ''),
            'experience_level': st.session_state.candidate_info.get('years_experience', ''),
            'tech_stack': st.session_state.candidate_info.get('tech_stack', ''),
            'location': st.session_state.candidate_info.get('current_location', ''),
            'interview_date': datetime.now().strftime('%Y-%m-%d'),
            'interview_time': datetime.now().strftime('%H:%M:%S'),
            'duration': 'Variable',  
            'status': 'completed',
            'preferences': st.session_state.preferences,
            'language': st.session_state.language,
            'total_messages': len(st.session_state.messages),
            'question_count': st.session_state.question_count,
            'interview_completed': st.session_state.interview_completed,
            'sentiment_summary': {
                'positive_count': len([s for s in st.session_state.sentiment if s[1] == 'positive']),
                'negative_count': len([s for s in st.session_state.sentiment if s[1] == 'negative']),
                'neutral_count': len([s for s in st.session_state.sentiment if s[1] == 'neutral']),
                'average_sentiment': sum([s[0] for s in st.session_state.sentiment]) / len(st.session_state.sentiment) if st.session_state.sentiment else 0
            }
        }
        
        
        if st.session_state.db_manager.save_interview_details(interview_data):
            interview_id = interview_data['interview_id']
            
            
            questions_data = []
            for i, msg in enumerate(st.session_state.messages):
                if msg['role'] == 'assistant':
                    
                    question_data = {
                        'interview_id': interview_id,
                        'question_text': msg['content'],
                        'question_type': 'ai_generated',
                        'message_index': i,
                        'role': 'assistant'
                    }
                    questions_data.append(question_data)
                elif msg['role'] == 'user':
                    
                    question_data = {
                        'interview_id': interview_id,
                        'question_text': msg['content'],
                        'question_type': 'user_response',
                        'message_index': i,
                        'role': 'user',
                        'sentiment_score': st.session_state.sentiment[i] if i < len(st.session_state.sentiment) else (0, 'neutral')
                    }
                    questions_data.append(question_data)
            

            if questions_data:
                st.session_state.db_manager.save_interview_questions(questions_data)
            
            st.success(f"✅ Interview data saved successfully! Interview ID: {interview_id}")
            
        else:
            st.error("❌ Failed to save interview data to database.")
            
    except Exception as e:
        st.error(f"❌ Error saving interview data: {str(e)}")
        st.exception(e)



def get_sentiment_analyzer():
    if SentimentIntensityAnalyzer is None:
        return None
    if '_sentiment_analyzer' not in st.session_state:
        try:
            st.session_state._sentiment_analyzer = SentimentIntensityAnalyzer()
        except Exception:
            st.session_state._sentiment_analyzer = None
    return st.session_state._sentiment_analyzer


def analyze_sentiment(text: str) -> Tuple[float, str]:
    analyzer = get_sentiment_analyzer()
    if not analyzer:
        return 0.0, 'neutral'
    scores = analyzer.polarity_scores(text)
    compound = scores.get('compound', 0.0)
    label = 'positive' if compound >= 0.2 else ('negative' if compound <= -0.2 else 'neutral')
    return compound, label


def sentiment_badge_html(message_index: int) -> str:
    
    if message_index >= len(st.session_state.sentiment):
        return ""
    score, label = st.session_state.sentiment[message_index]
    color = '#48bb78' if label == 'positive' else ('#f56565' if label == 'negative' else '#a0aec0')
    emoji = '😊' if label == 'positive' else ('😟' if label == 'negative' else '😐')
    return f"<span style='margin-left:8px;font-size:0.85rem;color:{color};opacity:0.9'>{emoji}</span>"


def current_target_language() -> str:
    selected = st.session_state.language.get('selected', 'Auto')
    
    if isinstance(selected, str) and (selected == 'Auto' or selected.lower() == 'auto'):
        return st.session_state.language.get('detected', 'en')
    
    return st.session_state.language.get('code', 'en')


def detect_language_code(text: str) -> str | None:
    try:
        if GoogleTranslator is None:
            return None
        
        return None
    except Exception:
        return None


def maybe_translate(text: str, source_language_code: str | None = None, target_language_code: str | None = None) -> str:
    if not text:
        return text
    if GoogleTranslator is None:
        return text
    try:
        src = source_language_code or 'auto'
        tgt = (target_language_code or 'en')
        if src == tgt or (src in ('auto', None) and tgt in ('auto', None)):
            
            pass
        translated = GoogleTranslator(source=src, target=tgt).translate(text)
        return translated or text
    except Exception:
        return text


if st.session_state.current_screen == 'landing':
    landing_page()
elif st.session_state.current_screen == 'form':
    interview_form()
elif st.session_state.current_screen == 'chat':
    chat_interface()
elif st.session_state.current_screen == 'results':
    display_interview_results()


st.markdown("<br><br>", unsafe_allow_html=True)
