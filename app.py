import streamlit as st
import json
import random
from datetime import datetime
from config import *

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
        background-color: #4a5568;
        color: #e2e8f0;
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        max-width: 80%;
        margin-right: auto;
        position: relative;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .bot-message::after {
        content: '';
        position: absolute;
        left: -8px;
        top: 15px;
        width: 0;
        height: 0;
        border: 8px solid transparent;
        border-right-color: #4a5568;
    }
    
    .user-message {
        background-color: #3182ce;
        color: white;
        padding: 1rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        max-width: 80%;
        margin-left: auto;
        text-align: right;
        position: relative;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .user-message::after {
        content: '';
        position: absolute;
        right: -8px;
        top: 15px;
        width: 0;
        height: 0;
        border: 8px solid transparent;
        border-left-color: #3182ce;
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
    }
    
    /* Style the input area */
    div[data-testid="stTextInput"] {
        background-color: #2d3748 !important;
        border: 1px solid #4a5568 !important;
        border-radius: 25px !important;
        color: #e2e8f0 !important;
        padding: 0.75rem 1rem !important;
        font-size: 1rem !important;
    }
    
    div[data-testid="stTextInput"] input {
        background-color: #2d3748 !important;
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

</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_screen' not in st.session_state:
    st.session_state.current_screen = 'landing'
if 'candidate_info' not in st.session_state:
    st.session_state.candidate_info = {}
if 'chat_messages' not in st.session_state:
    st.session_state.chat_messages = []
if 'current_question_index' not in st.session_state:
    st.session_state.current_question_index = 0
if 'technical_questions' not in st.session_state:
    st.session_state.technical_questions = []

# Technical questions based on tech stack
def generate_technical_questions(tech_stack):
    questions = []
    tech_list = [tech.strip().lower() for tech in tech_stack.split(',')]
    
    # Generate questions based on tech stack
    for tech in tech_list:
        if tech in TECHNICAL_QUESTIONS:
            questions.extend(random.sample(TECHNICAL_QUESTIONS[tech], min(2, len(TECHNICAL_QUESTIONS[tech]))))
    
    # If no specific tech questions, add general questions
    if not questions:
        questions = GENERAL_QUESTIONS
    
    return questions[:MAX_QUESTIONS]  # Return max questions from config

def landing_page():
    
    
    st.markdown(f'<h1 class="main-header">{APP_TITLE} {APP_ICON}</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">I\'ll guide you through a quick interview to learn about your skills and experience.</p>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🚀 Start Interview", key="start_interview", use_container_width=True):
            st.session_state.current_screen = 'form'
            st.rerun()

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
        
        submitted = st.form_submit_button("Submit & Start Chat", use_container_width=True)
        
        if submitted:
            # Check if required fields are filled
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
                
                # Generate technical questions
                st.session_state.technical_questions = generate_technical_questions(tech_stack)
                st.session_state.current_screen = 'chat'
                st.rerun()
            else:
                st.error("Please fill in at least Full Name, Email, and Tech Stack fields.")

def chat_interface():

    
    # Candidate profile summary - always visible in sidebar
    if st.session_state.candidate_info:
        with st.sidebar:
            st.markdown("### 👤 Candidate Profile")
            st.markdown(f"**Name:** {st.session_state.candidate_info.get('full_name', 'N/A')}")
            st.markdown(f"**Position:** {st.session_state.candidate_info.get('desired_position', 'N/A')}")
            st.markdown(f"**Experience:** {st.session_state.candidate_info.get('years_experience', 'N/A')}")
            st.markdown(f"**Tech Stack:** {st.session_state.candidate_info.get('tech_stack', 'N/A')}")
            st.markdown(f"**Location:** {st.session_state.candidate_info.get('current_location', 'N/A')}")
            
            st.markdown("---")
            
            # Navigation buttons in sidebar
            col1, col2 = st.columns(2)
            with col1:
                if st.button("← Back", key="back_button", use_container_width=True):
                    st.session_state.current_screen = 'form'
                    st.rerun()
            with col2:
                if st.button("Exit", key="exit_button", use_container_width=True):
                    st.session_state.current_screen = 'landing'
                    st.session_state.chat_messages = []
                    st.session_state.candidate_info = {}
                    st.rerun()
    else:
        # Show placeholder in sidebar if no candidate info
        with st.sidebar:
            st.markdown("### 👤 Candidate Profile")
            st.markdown("**No candidate information available**")
            st.markdown("Please complete the form to start the interview.")
    
    # Initialize chat with welcome message
    if not st.session_state.chat_messages:
        welcome_message = random.choice(WELCOME_MESSAGES).format(
            name=st.session_state.candidate_info.get('full_name', 'there'),
            tech_stack=st.session_state.candidate_info.get('tech_stack', 'your skills')
        )
        st.session_state.chat_messages.append({"role": "bot", "content": welcome_message})
        
        if st.session_state.technical_questions:
            first_question = st.session_state.technical_questions[0]
            st.session_state.chat_messages.append({"role": "bot", "content": first_question})
    
    # Chat messages container with bottom padding
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Display chat messages
    if st.session_state.chat_messages:
        for message in st.session_state.chat_messages:
            current_time = datetime.now().strftime("%H:%M")
            if message["role"] == "bot":
                st.markdown(f'''
                    <div class="bot-message">
                        <div>🤖 {message["content"]}</div>
                        <div class="message-time">{current_time}</div>
                    </div>
                ''', unsafe_allow_html=True)
            else:
                st.markdown(f'''
                    <div class="user-message">
                        <div>👤 {message["content"]}</div>
                        <div class="message-time">{current_time}</div>
                    </div>
                ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Fixed input area at the bottom
    st.markdown('<div class="fixed-input-container">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([4, 1, 1])
    with col1:
        user_input = st.text_input("Your response:", key="user_input", placeholder="Type your answer here...", label_visibility="collapsed")
    with col2:
        send_button = st.button("Send", key="send_message", use_container_width=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Handle user input
    if (send_button or (user_input and st.session_state.get('_last_input') != user_input)) and user_input.strip():
        st.session_state._last_input = user_input
        
        # Add user message
        st.session_state.chat_messages.append({"role": "user", "content": user_input})
        
        # Check for exit command
        if user_input.lower() in EXIT_COMMANDS:
            exit_message = random.choice(EXIT_MESSAGES).format(
                name=st.session_state.candidate_info.get('full_name', 'there')
            )
            st.session_state.chat_messages.append({"role": "bot", "content": exit_message})
        else:
            # Generate bot response
            bot_response = generate_bot_response(user_input)
            st.session_state.chat_messages.append({"role": "bot", "content": bot_response})
        
        st.rerun()

def generate_bot_response(user_input):
    """Generate appropriate bot response based on user input and current question"""
    
    # Acknowledgment responses
    acknowledgments = ACKNOWLEDGMENTS
    
    # Check if we should move to next question
    if st.session_state.current_question_index < len(st.session_state.technical_questions) - 1:
        # Move to next question
        st.session_state.current_question_index += 1
        next_question = st.session_state.technical_questions[st.session_state.current_question_index]
        return f"{random.choice(acknowledgments)} {next_question}"
    else:
        # Final question answered
        return f"{random.choice(acknowledgments)} Thank you for completing the technical interview! Our team will review your responses and get back to you soon. Have a great day! 🎉"

# Navigation
if st.session_state.current_screen == 'landing':
    landing_page()
elif st.session_state.current_screen == 'form':
    interview_form()
elif st.session_state.current_screen == 'chat':
    chat_interface()

# Add some spacing at the bottom
st.markdown("<br><br>", unsafe_allow_html=True)
