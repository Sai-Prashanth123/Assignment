# 🚀 TalentScout Hiring Assistant

<div align="center">

![TalentScout Logo](https://img.shields.io/badge/TalentScout-AI%20Interview%20Assistant-blue?style=for-the-badge&logo=robot)
![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28.1+-red?style=for-the-badge&logo=streamlit)
![Docker](https://img.shields.io/badge/Docker-Ready-blue?style=for-the-badge&logo=docker)
![MongoDB](https://img.shields.io/badge/MongoDB-4.6+-green?style=for-the-badge&logo=mongodb)

**A professional AI-powered technical interview platform built with Streamlit, featuring advanced sentiment analysis, multilingual support, and intelligent question generation.**

[🚀 Quick Start](#quick-start) • [📁 Project Structure](#project-structure) • [🔧 Features](#features) • [🐳 Docker](#docker) • [📊 Demo](#demo)

</div>

---

## ✨ Overview

TalentScout is a sophisticated hiring assistant that conducts automated technical interviews using AI. It provides a seamless three-screen experience for candidates while offering recruiters comprehensive insights into candidate performance, sentiment analysis, and multilingual support.

## 🎯 Key Features

### 🧠 **AI-Powered Intelligence**
- **Dynamic Question Generation** - Tailored questions based on candidate's tech stack
- **Intelligent Follow-ups** - Context-aware follow-up questions
- **Sentiment Analysis** - Real-time emotion detection with inline emoji indicators
- **Multilingual Support** - Auto-detection and translation for global candidates

### 🎨 **Professional User Experience**
- **Three-Screen Flow** - Landing → Form → Interview
- **Modern UI/UX** - Responsive design with progress indicators
- **Real-time Chat** - Interactive interview experience
- **Smart Responses** - Context-aware bot responses with acknowledgments

### 📊 **Analytics & Insights**
- **Candidate Profiles** - Comprehensive information display
- **Interview Analytics** - Performance metrics and insights
- **Results Viewer** - Advanced dashboard for recruiters
- **Database Integration** - MongoDB storage with backup capabilities

---

## 📁 Project Structure

```
talent-scout-hiring-assistant/
├── 🚀 Core Application
│   ├── app.py                 # Main Streamlit application (968 lines)
│   ├── config.py              # Configuration and constants (58 lines)
│   └── requirements.txt       # Python dependencies
│
├── 🤖 AI & Intelligence
│   ├── AI.py                  # AI logic and Groq integration (309 lines)
│   └── prompt.py              # Prompt management system (530 lines)
│
├── 🗄️ Data & Storage
│   ├── db.py                  # MongoDB manager and operations (493 lines)
│   └── results_viewer.py      # Analytics dashboard (324 lines)
│
├── 🐳 Containerization
│   ├── Dockerfile             # Production-ready container
│   ├── docker-compose.yml     # Development environment
│   └── docker-compose.prod.yml # Production environment
│
└── 📚 Documentation
    ├── README.md              # This comprehensive guide
    └── README-Docker.md       # Docker-specific instructions
```

---

## 🔧 File Descriptions

### 🚀 **Core Application Files**

#### `app.py` (968 lines) - Main Application
- **Purpose**: Primary Streamlit application entry point
- **Features**:
  - Three-screen interview flow (Landing → Form → Chat)
  - Custom CSS styling and responsive design
  - Session state management
  - MongoDB integration
  - Sentiment analysis integration
  - Multilingual support with Google Translator
- **Key Components**:
  - Landing page with professional welcome
  - Candidate information form
  - Interactive chat interface
  - Sidebar with preferences and language selection

#### `config.py` (58 lines) - Configuration Management
- **Purpose**: Centralized configuration and constants
- **Features**:
  - Application settings (title, icon, layout)
  - UI color schemes and styling
  - Chat settings and limits
  - Welcome messages and acknowledgments
  - Form validation rules
  - Experience level definitions

#### `requirements.txt` - Dependencies
- **Core**: Streamlit 1.28.1, Pandas 2.1.3, NumPy 1.24.3
- **AI**: Groq ≥0.9.0 for LLM integration
- **Analysis**: VADER Sentiment ≥3.3.2, Deep Translator ≥1.11.4
- **Database**: PyMongo ≥4.6.0
- **Visualization**: Plotly ≥5.17.0

### 🤖 **AI & Intelligence Files**

#### `AI.py` (309 lines) - AI Logic Engine
- **Purpose**: Core AI functionality and Groq integration
- **Features**:
  - Dynamic question generation using LLM
  - Intelligent phase determination (Technical → Behavioral → Follow-up)
  - Context-aware conversation management
  - Response analysis and topic extraction
- **Key Functions**:
  - `generate_next_question()` - Smart question generation
  - `generate_follow_up_question()` - Contextual follow-ups
  - `analyze_user_response()` - Response analysis
  - Phase transition logic

#### `prompt.py` (530 lines) - Prompt Management System
- **Purpose**: Comprehensive prompt and conversation management
- **Features**:
  - Interview phase management (Welcome, Technical, Behavioral, Closing)
  - Dynamic prompt templates
  - Experience-level-specific messaging
  - Technical question bank (Python, JavaScript, Java, React, Django, Node.js, SQL, AWS)
  - Follow-up question generation
- **Key Classes**:
  - `InterviewPhase` - Enum for interview stages
  - `PromptManager` - Central prompt management
  - `QuestionGenerator` - Dynamic question creation

### 🗄️ **Data & Storage Files**

#### `db.py` (493 lines) - MongoDB Manager
- **Purpose**: Database operations and connection management
- **Features**:
  - MongoDB Atlas integration
  - SSL/TLS support with fallback options
  - Interview data storage and retrieval
  - Connection pooling and error handling
  - Health checks and monitoring
- **Key Functions**:
  - `connect()` - Database connection with retry logic
  - `save_interview()` - Interview data persistence
  - `get_interviews()` - Data retrieval with filtering
  - `update_interview()` - Data updates

#### `results_viewer.py` (324 lines) - Analytics Dashboard
- **Purpose**: Comprehensive interview results visualization
- **Features**:
  - Interactive charts and graphs using Plotly
  - Filtering by date, status, experience level
  - Performance metrics and statistics
  - Individual interview details
  - Export capabilities
- **Key Components**:
  - Metrics dashboard
  - Interview timeline
  - Performance analytics
  - Search and filtering

### 🐳 **Containerization Files**

#### `Dockerfile` - Production Container
- **Base**: Python 3.11-slim for performance and security
- **Features**:
  - Multi-stage build optimization
  - Non-root user for security
  - Health checks with curl
  - Port 8501 exposure
  - System dependencies installation

#### `docker-compose.yml` - Development Environment
- **Services**: Streamlit app with MongoDB Atlas
- **Features**:
  - Hot reloading for development
  - Environment variable configuration
  - Volume mounting for data persistence
  - Health checks and restart policies

#### `docker-compose.prod.yml` - Production Environment
- **Services**: Streamlit app + MongoDB container
- **Features**:
  - Resource limits and reservations
  - Logging configuration
  - Backup volume management
  - Production-grade networking
  - Health monitoring

---

## 🚀 Quick Start

### Option 1: Local Development
```bash
# Clone the repository
git clone <repository-url>
cd talent-scout-hiring-assistant

# Install dependencies
pip install -r requirements.txt

# Set environment variables
export GROQ_API_KEY=your_groq_api_key_here

# Run the application
streamlit run app.py
```

### Option 2: Docker Development
```bash
# Start development environment
docker-compose up --build

# Access at http://localhost:8501
```

### Option 3: Production Deployment
```bash
# Set production environment variables
export GROQ_API_KEY=your_production_key
export MONGODB_URI=your_mongodb_uri

# Deploy production stack
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🔑 Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `GROQ_API_KEY` | Groq API key for AI integration | ✅ | - |
| `MONGODB_URI` | MongoDB connection string | ✅ | - |
| `STREAMLIT_SERVER_PORT` | Streamlit server port | ❌ | 8501 |
| `STREAMLIT_SERVER_ADDRESS` | Server binding address | ❌ | 0.0.0.0 |

---

## 🎨 Customization

### Adding New Technologies
Modify the `question_bank` in `prompt.py`:
```python
'new_technology': [
    "What are the key concepts of new_technology?",
    "How do you handle challenges in new_technology?",
    "What's your experience with new_technology?"
]
```

### Styling Customization
Edit CSS in `app.py` under the `st.markdown()` section:
```python
st.markdown("""
<style>
    .custom-class {
        /* Your custom styles */
    }
</style>
""", unsafe_allow_html=True)
```

### Prompt Customization
Modify prompts in `prompt.py` for different interview styles and company cultures.

---

## 📊 Demo Presentation

### 🎯 **Landing Page**
- Professional welcome screen with company branding
- Clear call-to-action for interview start
- Modern, responsive design

### 📝 **Candidate Form**
- Comprehensive information collection
- Experience level and tech stack selection
- Form validation and error handling

### 💬 **Interview Interface**
- Real-time AI-powered chat
- Dynamic question generation
- Sentiment analysis with emoji indicators
- Multilingual support
- Progress tracking

### 📈 **Analytics Dashboard**
- Interview performance metrics
- Candidate response analysis
- Export and reporting capabilities
- Advanced filtering and search

---

## 🔒 Security Features

- **Non-root Docker containers** for production
- **SSL/TLS encryption** for database connections
- **Environment variable management** for sensitive data
- **Input validation** and sanitization
- **Session management** with Streamlit

---

## 🚀 Performance Features

- **Connection pooling** for database operations
- **Caching strategies** for frequently accessed data
- **Resource limits** in production containers
- **Health checks** for service monitoring
- **Optimized Docker images** with multi-stage builds

---

## 🌐 Browser Compatibility

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 90+ | ✅ Recommended |
| Firefox | 88+ | ✅ Supported |
| Safari | 14+ | ✅ Supported |
| Edge | 90+ | ✅ Supported |

---

## 🔮 Future Enhancements

- [ ] **Video/Audio Interviews** - Multi-modal interview capabilities
- [ ] **ATS Integration** - Applicant Tracking System connectivity
- [ ] **Advanced Analytics** - Machine learning insights
- [ ] **Multi-language UI** - Localized user interfaces
- [ ] **API Endpoints** - RESTful API for external integrations
- [ ] **Real-time Collaboration** - Multi-interviewer support
- [ ] **Assessment Scoring** - Automated candidate evaluation
- [ ] **Email Notifications** - Automated recruiter alerts

---

## 🛠️ Troubleshooting

### Common Issues

#### Database Connection
```bash
# Check MongoDB connection
docker-compose logs mongodb

# Verify environment variables
echo $MONGODB_URI
```

#### AI Integration
```bash
# Verify Groq API key
echo $GROQ_API_KEY

# Check API limits and quotas
```

#### Container Issues
```bash
# Rebuild containers
docker-compose down
docker-compose up --build

# Check container health
docker-compose ps
```

---

## 📚 API Documentation

### Groq Integration
- **Model**: Llama 3.3 70B Versatile
- **Endpoints**: Question generation, response analysis
- **Rate Limits**: Based on Groq plan

### MongoDB Schema
```javascript
// Interview Collection
{
  candidate_id: String,
  full_name: String,
  email: String,
  tech_stack: Array,
  experience_level: String,
  responses: Array,
  sentiment_scores: Array,
  interview_phase: String,
  created_at: Date,
  completed_at: Date
}
```

---

## 🤝 Contributing

1. **Fork the repository**
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'Add amazing feature'`)
4. **Push to the branch** (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🆘 Support

- **Documentation**: [Streamlit Docs](https://docs.streamlit.io/)
- **Issues**: Create an issue in the project repository
- **Community**: [Streamlit Community](https://discuss.streamlit.io/)

---

<div align="center">

**Built with ❤️ using Streamlit, Docker, and AI**

*Empowering recruiters with intelligent hiring solutions*

[⬆️ Back to Top](#-talentscout-hiring-assistant)

</div>
