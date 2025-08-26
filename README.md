# TalentScout Hiring Assistant 🤖

A professional Streamlit-based chatbot interface for conducting automated technical interviews. This application provides a seamless three-screen experience for candidates to showcase their skills and experience.

## Features

### 🎯 Three-Screen Flow
1. **Landing Page** - Professional welcome screen with clear call-to-action
2. **Interview Form** - Comprehensive candidate information collection
3. **Chat Interface** - AI-powered technical interview with dynamic questions

### 🚀 Key Features
- **Dynamic Question Generation** - Questions tailored to candidate's tech stack
- **Professional UI/UX** - Modern, responsive design with progress indicators
- **Real-time Chat** - Interactive interview experience
- **Candidate Profile** - Sidebar display of candidate information
- **Smart Responses** - Context-aware bot responses with acknowledgments
- **Exit Handling** - Graceful interview completion

## Installation

1. **Clone or download the project files**

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** and navigate to the URL shown in the terminal (typically `http://localhost:8501`)

## Usage

### For Candidates
1. **Start Interview** - Click the "Start Interview" button on the landing page
2. **Fill Information** - Complete the candidate information form with your details
3. **Technical Chat** - Answer dynamic technical questions based on your skills
4. **Complete Interview** - Finish the interview or type "exit" to end early

### For Recruiters
- The application automatically generates relevant technical questions based on the candidate's tech stack
- All candidate information and responses are captured in the session
- Professional interface builds trust and provides a positive candidate experience

## Technical Questions

The application includes a comprehensive question bank covering:

- **Python** - Lists vs tuples, exceptions, decorators, generators
- **JavaScript** - var/let/const, hoisting, closures, promises
- **Java** - HashMap vs HashTable, polymorphism, garbage collection
- **React** - Hooks, state vs props, virtual DOM, components
- **Django** - ORM, MVT architecture, migrations, signals
- **Node.js** - Event loop, async operations, streams
- **SQL** - JOINs, optimization, normalization, indexes
- **AWS** - Services, security, EC2 vs Lambda, CI/CD

## Customization

### Adding New Technologies
To add support for new technologies, modify the `question_bank` dictionary in the `generate_technical_questions()` function:

```python
'new_tech': [
    "Question 1 about new_tech?",
    "Question 2 about new_tech?",
    "Question 3 about new_tech?"
]
```

### Styling
The application uses custom CSS for styling. Modify the CSS in the `st.markdown()` section to customize the appearance.

### Question Logic
The bot response logic can be customized in the `generate_bot_response()` function to implement more sophisticated interview flows.

## File Structure

```
talent-scout-hiring-assistant/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## Dependencies

- **Streamlit** (1.28.1) - Web application framework
- **Pandas** (2.1.3) - Data manipulation (if needed for future features)
- **NumPy** (1.24.3) - Numerical computing (if needed for future features)

## Browser Compatibility

The application works best with modern browsers:
- Chrome (recommended)
- Firefox
- Safari
- Edge

## Future Enhancements

Potential improvements for future versions:
- Database integration for storing candidate responses
- Email notifications to recruiters
- Advanced AI integration for more sophisticated responses
- Video/audio interview capabilities
- Integration with ATS (Applicant Tracking Systems)
- Analytics dashboard for interview performance

## Support

For issues or questions, please check the Streamlit documentation or create an issue in the project repository.

---

**Built with ❤️ using Streamlit**
