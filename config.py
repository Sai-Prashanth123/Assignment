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
MAX_QUESTIONS = 5
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

# Technical Question Bank
TECHNICAL_QUESTIONS = {
    'python': [
        "Can you explain the difference between lists and tuples in Python?",
        "How would you handle exceptions in Python?",
        "What are decorators and how do you use them?",
        "Explain the concept of generators in Python.",
        "What's the difference between shallow and deep copying?",
        "How do you work with virtual environments in Python?"
    ],
    'javascript': [
        "What's the difference between var, let, and const?",
        "How does hoisting work in JavaScript?",
        "Explain closures in JavaScript.",
        "What are promises and how do you use them?",
        "What's the difference between == and ===?",
        "How do you handle asynchronous operations with async/await?"
    ],
    'java': [
        "What's the difference between HashMap and HashTable?",
        "Explain the concept of polymorphism in Java.",
        "How does garbage collection work in Java?",
        "What are the differences between abstract classes and interfaces?",
        "What is the difference between String, StringBuilder, and StringBuffer?",
        "How do you handle exceptions in Java?"
    ],
    'react': [
        "What are hooks in React and how do you use them?",
        "Explain the difference between state and props.",
        "How does the virtual DOM work?",
        "What are controlled and uncontrolled components?",
        "What is the difference between functional and class components?",
        "How do you handle side effects in React?"
    ],
    'django': [
        "What is the Django ORM and how does it work?",
        "Explain Django's MVT architecture.",
        "How do you handle database migrations in Django?",
        "What are Django signals and when would you use them?",
        "How do you implement authentication in Django?",
        "What are Django middleware and how do you use them?"
    ],
    'node.js': [
        "What is the event loop in Node.js?",
        "How do you handle asynchronous operations in Node.js?",
        "Explain the difference between require and import.",
        "What are streams in Node.js?",
        "How do you handle errors in Node.js?",
        "What is the difference between process.nextTick and setImmediate?"
    ],
    'sql': [
        "What's the difference between INNER JOIN and LEFT JOIN?",
        "How do you optimize a slow SQL query?",
        "Explain the concept of database normalization.",
        "What are indexes and when would you use them?",
        "What's the difference between WHERE and HAVING?",
        "How do you handle NULL values in SQL?"
    ],
    'aws': [
        "What are the main AWS services you've worked with?",
        "How do you handle security in AWS?",
        "Explain the difference between EC2 and Lambda.",
        "How do you implement CI/CD with AWS?",
        "What is the difference between S3 and EBS?",
        "How do you monitor applications in AWS?"
    ],
    'docker': [
        "What is Docker and how does it work?",
        "What's the difference between Docker and virtual machines?",
        "How do you create a Dockerfile?",
        "What are Docker volumes and when would you use them?",
        "How do you handle environment variables in Docker?",
        "What is Docker Compose and how do you use it?"
    ],
    'kubernetes': [
        "What is Kubernetes and what are its main components?",
        "What's the difference between a Pod and a Deployment?",
        "How do you handle configuration in Kubernetes?",
        "What are Services in Kubernetes?",
        "How do you scale applications in Kubernetes?",
        "What is a ConfigMap and when would you use it?"
    ]
}

# General Questions (fallback)
GENERAL_QUESTIONS = [
    "Can you describe a challenging project you've worked on?",
    "How do you approach debugging complex issues?",
    "What's your experience with version control systems?",
    "How do you stay updated with technology trends?",
    "Describe a time when you had to learn a new technology quickly.",
    "How do you handle working in a team environment?",
    "What's your process for code review?",
    "How do you ensure code quality in your projects?"
]
