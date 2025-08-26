#!/usr/bin/env python3
"""
Demo script for TalentScout Hiring Assistant
This script demonstrates the key features and provides a quick test of the application.
"""

import streamlit as st
import sys
import os

def main():
    st.title("🎯 TalentScout Hiring Assistant - Demo")
    st.markdown("---")
    
    st.header("🚀 Features Overview")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 📱 Three-Screen Flow")
        st.markdown("""
        - **Landing Page**: Professional welcome
        - **Interview Form**: Candidate info collection
        - **Chat Interface**: AI-powered interview
        """)
    
    with col2:
        st.markdown("### 🤖 Smart Features")
        st.markdown("""
        - Dynamic question generation
        - Tech stack-based questions
        - Real-time chat interface
        - Professional UI/UX
        """)
    
    with col3:
        st.markdown("### 🎨 User Experience")
        st.markdown("""
        - Progress indicators
        - Candidate profile sidebar
        - Responsive design
        - Graceful exit handling
        """)
    
    st.markdown("---")
    
    st.header("🛠️ Supported Technologies")
    
    tech_cols = st.columns(4)
    technologies = [
        ("Python", "🐍"),
        ("JavaScript", "📜"),
        ("Java", "☕"),
        ("React", "⚛️"),
        ("Django", "🎸"),
        ("Node.js", "🟢"),
        ("SQL", "🗄️"),
        ("AWS", "☁️"),
        ("Docker", "🐳"),
        ("Kubernetes", "⚓"),
        ("Git", "📚"),
        ("Linux", "🐧")
    ]
    
    for i, (tech, emoji) in enumerate(technologies):
        with tech_cols[i % 4]:
            st.markdown(f"**{emoji} {tech}**")
    
    st.markdown("---")
    
    st.header("🚀 Quick Start")
    
    st.markdown("""
    ### To run the application:
    
    1. **Install dependencies:**
       ```bash
       pip install -r requirements.txt
       ```
    
    2. **Run the app:**
       ```bash
       streamlit run app.py
       ```
    
    3. **Open browser:**
       Navigate to `http://localhost:8501`
    """)
    
    st.markdown("---")
    
    st.header("📋 Sample Interview Flow")
    
    with st.expander("Click to see sample interview flow"):
        st.markdown("""
        ### Sample Candidate Journey:
        
        1. **Landing Page**
           - Candidate sees professional welcome screen
           - Clicks "Start Interview" button
        
        2. **Information Form**
           - Fills in: Name, Email, Tech Stack, etc.
           - Example tech stack: "Python, Django, JavaScript, React"
        
        3. **Technical Interview**
           - Bot welcomes candidate personally
           - Asks Python questions: "Can you explain the difference between lists and tuples?"
           - Asks Django questions: "What is the Django ORM and how does it work?"
           - Asks React questions: "What are hooks in React and how do you use them?"
           - Provides acknowledgments and moves to next questions
        
        4. **Completion**
           - Thanks candidate
           - Informs about next steps
        """)
    
    st.markdown("---")
    
    st.header("⚙️ Configuration")
    
    st.markdown("""
    The application is highly configurable through `config.py`:
    
    - **Colors and styling**
    - **Question banks**
    - **Welcome/exit messages**
    - **Experience levels**
    - **Chat settings**
    """)
    
    if st.button("🎯 Launch Full Application"):
        st.success("Redirecting to main application...")
        st.markdown("""
        <script>
            window.location.href = "app.py";
        </script>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
