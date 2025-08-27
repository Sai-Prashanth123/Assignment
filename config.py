# Configuration file for TalentScout Hiring Assistant

# Application Settings
APP_TITLE = "TalentScout Hiring Assistant"
APP_ICON = "🤖"
PAGE_LAYOUT = "wide"

# UI Colors
PRIMARY_COLOR = "#1f77b4"
SECONDARY_COLOR = "#007bff"
BACKGROUND_COLOR = "#f9f9f9"
BOT_MESSAGE_COLOR = "#e9ecef"
USER_MESSAGE_COLOR = "#007bff"

# Chat Settings
MAX_QUESTIONS = 7
CHAT_CONTAINER_HEIGHT = "70vh"

# Welcome Messages
WELCOME_MESSAGES = [
    "Welcome {name} 👋, thanks for sharing your details. Based on your experience with {tech_stack}, I'll ask you a few technical questions.",
    "Hi {name}! Great to meet you. I see you're experienced with {tech_stack}. Let's dive into some technical questions.",
    "Hello {name} 👋! Thanks for your information. I'll ask you some questions about {tech_stack} and your experience."
]

# Acknowledgment Messages
ACKNOWLEDGMENTS = [
    "Got it ✅",
    "Interesting approach 👌",
    "That's helpful, thanks! 👍",
    "Good to know! 📝",
    "Excellent point! 💡",
    "Thanks for sharing! 📚",
    "Great insight! 🎯"
]

# Exit Messages
EXIT_MESSAGES = [
    "Thank you for your time, {name}. Our recruiters will review your responses and contact you soon. Have a great day! 👋",
    "Thanks {name}! We've captured all your responses. Our team will be in touch shortly. Good luck! 🚀",
    "Appreciate your time, {name}. We'll review your interview and get back to you soon. Take care! ✨"
]

# Form Validation
REQUIRED_FIELDS = ['full_name', 'email', 'tech_stack']

# Experience Levels
EXPERIENCE_LEVELS = [
    "0-1 years",
    "1-3 years", 
    "3-5 years",
    "5-10 years",
    "10+ years"
]

# Exit Commands
EXIT_COMMANDS = ['exit', 'quit', 'bye', 'goodbye', 'end', 'finish']
