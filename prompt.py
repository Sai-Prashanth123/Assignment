"""
Prompt Management System for AI Interview Assistant
Handles all prompts, technical questions, and conversation flows
"""

import random
from typing import Dict, List, Optional, Tuple
from enum import Enum

class InterviewPhase(Enum):
    """Enum for different interview phases"""
    WELCOME = "welcome"
    TECHNICAL = "technical"
    BEHAVIORAL = "behavioral"
    FOLLOW_UP = "follow_up"
    CLOSING = "closing"
    GENERAL = "general"

class PromptManager:
    """Manages all prompts and conversation flows for the AI interview system"""
    
    def __init__(self):
        self.initialize_prompts()
    
    def initialize_prompts(self):
        """Initialize all prompt templates and technical questions"""
        
        # Welcome messages for different experience levels
        self.welcome_messages = {
            "entry": [
                "Welcome {name}! I'm excited to learn about your journey into {tech_stack}. Let's start with a friendly chat about your skills and aspirations.",
                "Hi {name}! Thanks for joining us today. I'd love to explore your experience with {tech_stack} and understand your career goals.",
                "Hello {name}! I'm here to chat about your {tech_stack} skills and help us get to know each other better. Ready to dive in?"
            ],
            "mid": [
                "Welcome {name}! With your experience in {tech_stack}, I'm looking forward to some engaging technical discussions.",
                "Hi {name}! Your background in {tech_stack} is impressive. Let's explore your expertise and see how we can work together.",
                "Hello {name}! I'm excited to discuss your {tech_stack} experience and understand your technical approach."
            ],
            "senior": [
                "Welcome {name}! Your senior-level experience with {tech_stack} is exactly what we're looking for. Let's dive deep into your expertise.",
                "Hi {name}! I'm thrilled to discuss your leadership and technical skills in {tech_stack}. This should be an interesting conversation.",
                "Hello {name}! Your senior {tech_stack} experience speaks volumes. Let's explore your technical leadership and architectural thinking."
            ]
        }
        
        # Dynamic question generation prompts for different contexts
        self.dynamic_prompts = {
            "technical_exploration": [
                "Based on their response about {topic}, ask a follow-up question that explores their technical depth and practical experience.",
                "Given their explanation of {topic}, probe deeper into their understanding of the underlying concepts and trade-offs.",
                "Following their description of {topic}, ask about real-world challenges they've faced and how they solved them."
            ],
            "experience_probing": [
                "Based on their project experience with {topic}, ask about the scale, complexity, and lessons learned.",
                "Given their work on {topic}, explore their role, responsibilities, and impact on the project.",
                "Following their description of {topic}, ask about collaboration, challenges, and outcomes."
            ],
            "skill_assessment": [
                "Based on their skills in {topic}, ask about advanced concepts and their practical application.",
                "Given their knowledge of {topic}, explore edge cases, performance considerations, and best practices.",
                "Following their explanation of {topic}, ask about troubleshooting, debugging, and optimization strategies."
            ],
            "problem_solving": [
                "Based on their approach to {topic}, ask about alternative solutions and decision-making criteria.",
                "Given their solution for {topic}, explore scalability, maintainability, and future considerations.",
                "Following their problem-solving example, ask about risk assessment and contingency planning."
            ],
            "learning_adaptation": [
                "Based on their learning experience with {topic}, ask about their learning strategies and adaptation methods.",
                "Given their journey with {topic}, explore how they stay updated and handle new challenges.",
                "Following their learning story, ask about knowledge sharing and mentoring others."
            ]
        }
        
        # Follow-up question templates for different response types
        self.follow_up_templates = {
            "technical_detail": [
                "Can you elaborate on the technical implementation details of {topic}?",
                "What were the key technical challenges you faced with {topic}?",
                "How did you handle the technical complexity of {topic}?",
                "What technical decisions did you make when working with {topic}?"
            ],
            "experience_depth": [
                "What was the scale and scope of your work with {topic}?",
                "How long did you work with {topic} and what was your role?",
                "What were the business outcomes of your work with {topic}?",
                "How did your experience with {topic} evolve over time?"
            ],
            "problem_solving": [
                "What was the most challenging aspect of {topic} and how did you solve it?",
                "How did you approach debugging issues with {topic}?",
                "What alternative solutions did you consider for {topic}?",
                "How did you ensure the quality and reliability of {topic}?"
            ],
            "collaboration": [
                "How did you collaborate with others on {topic}?",
                "What was your team structure when working on {topic}?",
                "How did you handle disagreements or conflicts about {topic}?",
                "What did you learn from others while working on {topic}?"
            ],
            "learning_growth": [
                "How did you initially learn {topic} and what resources did you use?",
                "What mistakes did you make with {topic} and what did you learn?",
                "How has your understanding of {topic} improved over time?",
                "What would you do differently now with {topic}?"
            ]
        }
        
        # Behavioral question generation prompts
        self.behavioral_prompts = {
            "teamwork": [
                "Based on their experience with {topic}, ask about a time they had to work with a difficult team member.",
                "Given their collaborative work on {topic}, explore how they handle team conflicts.",
                "Following their team experience, ask about their leadership and mentoring approach."
            ],
            "learning": [
                "Based on their learning journey with {topic}, ask about adapting to new technologies.",
                "Given their skill development, explore how they handle rapid changes in their field.",
                "Following their growth story, ask about their approach to continuous learning."
            ],
            "decision_making": [
                "Based on their technical decisions with {topic}, ask about making choices with incomplete information.",
                "Given their problem-solving approach, explore how they balance technical and business needs.",
                "Following their decision process, ask about handling pressure and deadlines."
            ],
            "challenge_overcoming": [
                "Based on their challenges with {topic}, ask about a time they failed and what they learned.",
                "Given their problem-solving skills, explore how they handle setbacks and obstacles.",
                "Following their success story, ask about going above and beyond expectations."
            ]
        }
        
        # General technical questions for any tech stack (fallback)
        self.general_questions = {
            "entry": [
                "Can you walk me through a recent project you worked on?",
                "What's your approach to debugging when something goes wrong?",
                "How do you stay updated with the latest technology trends?",
                "Describe a challenging problem you solved recently.",
                "What's your experience with version control systems like Git?"
            ],
            "mid": [
                "How do you approach system design for a new feature?",
                "What's your experience with testing strategies and frameworks?",
                "How do you handle technical debt in your projects?",
                "Describe a time when you had to learn a new technology quickly.",
                "How do you collaborate with other developers on a project?"
            ],
            "senior": [
                "How do you approach mentoring junior developers?",
                "What's your strategy for making architectural decisions?",
                "How do you handle technical disagreements in a team?",
                "Describe a time when you had to make a difficult technical decision.",
                "How do you balance technical excellence with business requirements?"
            ]
        }
        
        # Closing questions
        self.closing_questions = [
            "What questions do you have for me about the role or company?",
            "Is there anything about your experience or skills that we haven't covered?",
            "What are your career goals for the next few years?",
            "What are you looking for in your next role?",
            "Do you have any concerns about the position or company?",
            "What would make this role a great fit for you?",
            "Is there anything else you'd like me to know about you?",
            "What are your salary expectations for this role?",
            "When would you be available to start?",
            "What's your timeline for making a decision?"
        ]
        
        # General conversation responses (for non-interview questions)
        self.general_responses = {
            "greeting": [
                "Hello! I'm here to help with your interview. How can I assist you today?",
                "Hi there! I'm ready to help with your interview process. What would you like to know?",
                "Greetings! I'm here to support your interview experience. How can I help?"
            ],
            "help": [
                "I'm an AI interview assistant. I can help you with technical questions, behavioral questions, and general interview guidance. What would you like to know?",
                "I'm here to conduct your interview and answer any questions you might have about the process. What can I help you with?",
                "I'm your AI interviewer! I can ask technical questions, discuss your experience, and help you through the interview process. What would you like to explore?"
            ],
            "thanks": [
                "You're welcome! I'm here to help make your interview experience smooth and engaging.",
                "My pleasure! I'm glad I could help with your interview today.",
                "You're very welcome! I'm here to support you throughout this interview process."
            ],
            "goodbye": [
                "Thank you for the interview! I've enjoyed our conversation. Good luck with your application!",
                "It was great interviewing you today! I appreciate you taking the time to chat with me. Best of luck!",
                "Thanks for a wonderful interview session! I've learned a lot about your skills and experience. Good luck!"
            ],
            "redirect": [
                "I understand, but let's focus on your interview! I'd like to learn more about your technical skills and experience. Can you tell me about a recent Python project you've worked on?",
                "That's interesting, but I'm here to conduct your interview. Let me ask you about your technical background: What's the most challenging Python problem you've solved recently?",
                "I appreciate your response, but let's stay focused on the interview. I'd like to understand your technical expertise better. Can you describe a Python project where you learned something new?",
                "Let's get back to your interview! I'm interested in your technical skills. What Python libraries or frameworks are you most comfortable with, and can you give me an example of how you've used them?",
                "I'd like to focus on your interview now. Let me ask you about your Python experience: What's a technical challenge you've faced in your recent projects, and how did you approach solving it?"
            ]
        }
    
    def get_welcome_message(self, name: str, tech_stack: str, experience_level: str = "mid") -> str:
        """Get a welcome message based on experience level"""
        level = self._normalize_experience_level(experience_level)
        messages = self.welcome_messages.get(level, self.welcome_messages["mid"])
        return random.choice(messages).format(name=name, tech_stack=tech_stack)
    
    def get_dynamic_question_prompt(self, candidate: Dict[str, str], user_response: str, context: str = "", question_type: str = "technical") -> str:
        """Generate a dynamic prompt for asking the next question based on user response"""
        
        # Extract key topics and concepts from user response
        topics = self._extract_topics_from_response(user_response)
        experience_level = self._normalize_experience_level(candidate.get('years_experience', 'mid'))
        
        if question_type == "technical":
            return f"""Based on the candidate's response: "{user_response[:200]}..."

Candidate Profile:
- Tech Stack: {candidate.get('tech_stack', 'general software engineering')}
- Experience Level: {experience_level}
- Key Topics Mentioned: {', '.join(topics) if topics else 'general technical concepts'}

Context: {context}

Generate ONE dynamic, focused technical question that:
1. Builds upon their specific response and mentioned technologies
2. Probes deeper into their technical knowledge and practical experience
3. Is appropriate for their experience level
4. Encourages them to elaborate on their technical approach
5. Helps assess their problem-solving and technical decision-making skills

Ask a single, focused question that naturally flows from their response."""
        
        elif question_type == "behavioral":
            return f"""Based on the candidate's response: "{user_response[:200]}..."

Candidate Profile:
- Experience Level: {experience_level}
- Key Topics Mentioned: {', '.join(topics) if topics else 'work experience'}

Context: {context}

Generate ONE dynamic behavioral question that:
1. Relates to their specific experience and mentioned situations
2. Probes deeper into their soft skills and work approach
3. Is appropriate for their experience level
4. Encourages them to share specific examples and outcomes
5. Helps assess their collaboration, learning, and problem-solving abilities

Ask a single, focused behavioral question that naturally flows from their response."""
        
        elif question_type == "follow_up":
            return f"""Based on the candidate's response: "{user_response[:200]}..."

Key Topics: {', '.join(topics) if topics else 'their experience'}

Context: {context}

Generate ONE dynamic follow-up question that:
1. Probes deeper into their specific response
2. Explores technical depth, practical experience, or decision-making
3. Encourages them to elaborate on specific details
4. Helps understand their approach, challenges, and solutions
5. Maintains natural conversation flow

Ask a single, focused follow-up question that builds upon their response."""
        
        else:
            return f"""Based on the candidate's response: "{user_response[:200]}..."

Context: {context}

Generate ONE dynamic question that:
1. Builds upon their specific response
2. Moves the interview forward naturally
3. Is appropriate for the current conversation flow
4. Encourages detailed elaboration
5. Helps assess their skills and experience

Ask a single, focused question that naturally flows from their response."""
    
    def get_system_prompt(self, candidate: Dict[str, str], phase: InterviewPhase = InterviewPhase.TECHNICAL, user_response: str = "", conversation_context: str = "") -> str:
        """Generate system prompt based on interview phase, candidate info, and user response"""
        
        # Get the target language for questions
        target_language = candidate.get('target_language', 'Auto')
        language_instruction = ""
        
        # Debug logging for language handling
        print(f"DEBUG: target_language received: '{target_language}'")
        print(f"DEBUG: candidate keys: {list(candidate.keys())}")
        print(f"DEBUG: candidate target_language: {candidate.get('target_language', 'NOT_FOUND')}")
        
        if target_language and target_language != 'Auto' and target_language != 'en':
            # Handle both language codes (e.g., 'hi') and full labels (e.g., 'Hindi (hi)')
            if '(' in target_language:
                # Extract language code from format like "Hindi (hi)"
                lang_code = target_language.split('(')[-1].strip(')')
            else:
                # Direct language code like 'hi', 'es', etc.
                lang_code = target_language
            
            print(f"DEBUG: extracted lang_code: '{lang_code}'")
            
            # Map language codes to full names for better AI understanding
            language_map = {
                'hi': 'Hindi', 'es': 'Spanish', 'fr': 'French', 'de': 'German',
                'zh': 'Chinese', 'ar': 'Arabic', 'pt': 'Portuguese', 'ru': 'Russian', 'ja': 'Japanese'
            }
            
            full_language_name = language_map.get(lang_code, lang_code)
            language_instruction = f"\n\nLANGUAGE REQUIREMENT: You MUST ask ALL questions in {full_language_name} ({lang_code}). Never ask questions in English or any other language. This is critical for the candidate's experience."
            
            print(f"DEBUG: language_instruction: '{language_instruction}'")
        else:
            print(f"DEBUG: No language instruction added - target_language: '{target_language}'")

        base_prompt = f"""You are an AI technical interviewer conducting an interview for {candidate.get('full_name', 'a candidate')} applying for {candidate.get('desired_position', 'a technical role')}.

Experience Level: {candidate.get('years_experience', 'N/A')}
Tech Stack: {candidate.get('tech_stack', 'general software engineering')}
Tone: {candidate.get('tone', 'Professional')}
Detail Level: {candidate.get('detail_level', 'Concise')}{language_instruction}

IMPORTANT RULES:
1. NEVER give explanations or reasons for your questions
2. NEVER ask multiple questions at once
3. Ask ONE clear, focused question at a time
4. Make questions DYNAMIC and RESPONSIVE to their specific answers
5. Build upon what they've already shared
6. Stay focused on technical skills and experience
7. Be conversational but professional
8. If they ask non-interview questions, answer them briefly and redirect to the interview
9. Keep responses concise and direct
10. Make each question feel natural and connected to the conversation
11. MAINTAIN CONVERSATION FLOW - don't jump to random topics"""

        if user_response:
            topics = self._extract_topics_from_response(user_response)
            base_prompt += f"\n\nTheir last response mentioned: {', '.join(topics) if topics else 'their experience'}"
            base_prompt += "\n\nMake your next question directly related to what they just shared."
        
        if conversation_context:
            base_prompt += f"\n\nConversation context: {conversation_context}"
            base_prompt += "\n\nEnsure your question builds upon the conversation flow and doesn't jump to unrelated topics."

        if phase == InterviewPhase.WELCOME:
            base_prompt += "\n\nCurrent Phase: Welcome - Start with a friendly greeting and first dynamic technical question"
        elif phase == InterviewPhase.TECHNICAL:
            base_prompt += "\n\nCurrent Phase: Technical Interview - Ask dynamic technical questions that build upon their responses. STAY FOCUSED on technical topics they've mentioned."
        elif phase == InterviewPhase.BEHAVIORAL:
            base_prompt += "\n\nCurrent Phase: Behavioral Interview - Ask dynamic behavioral questions based on their experiences. STAY FOCUSED on soft skills and work situations."
        elif phase == InterviewPhase.FOLLOW_UP:
            base_prompt += "\n\nCurrent Phase: Follow-up - Ask probing questions that naturally extend their responses. DIVE DEEPER into what they just shared."
        elif phase == InterviewPhase.CLOSING:
            base_prompt += "\n\nCurrent Phase: Closing - Ask final questions and wrap up the interview"
        
        return base_prompt
    
    def _extract_topics_from_response(self, response: str) -> List[str]:
        """Extract key technical topics and concepts from user response"""
        if not response:
            return []
        
        # Common technical terms and concepts to look for
        technical_terms = [
            # Programming languages
            "python", "javascript", "java", "c++", "c#", "go", "rust", "php", "ruby", "swift", "kotlin",
            # Frameworks and libraries
            "react", "angular", "vue", "node", "django", "flask", "express", "spring", "laravel", "rails",
            # Databases
            "mysql", "postgresql", "mongodb", "redis", "elasticsearch", "dynamodb", "sqlite",
            # Cloud and infrastructure
            "aws", "azure", "gcp", "docker", "kubernetes", "terraform", "jenkins", "gitlab", "github",
            # Concepts and methodologies
            "api", "rest", "graphql", "microservices", "serverless", "ci/cd", "agile", "scrum", "tdd",
            # Tools and practices
            "git", "jira", "confluence", "slack", "teams", "zoom", "figma", "sketch"
        ]
        
        response_lower = response.lower()
        found_topics = []
        
        for term in technical_terms:
            if term in response_lower:
                found_topics.append(term)
        
        # Also look for common technical patterns
        if any(word in response_lower for word in ["database", "db", "sql", "nosql"]):
            found_topics.append("database")
        if any(word in response_lower for word in ["frontend", "front-end", "ui", "ux"]):
            found_topics.append("frontend")
        if any(word in response_lower for word in ["backend", "back-end", "server", "api"]):
            found_topics.append("backend")
        if any(word in response_lower for word in ["testing", "unit test", "integration test"]):
            found_topics.append("testing")
        if any(word in response_lower for word in ["deployment", "devops", "infrastructure"]):
            found_topics.append("devops")
        
        return list(set(found_topics))  # Remove duplicates
    
    def get_fallback_question(self, tech_stack: str, experience_level: str, question_type: str = "random") -> str:
        """Get a fallback question when dynamic generation isn't available"""
        level = self._normalize_experience_level(experience_level)
        
        # Parse tech stack into individual technologies
        tech_list = [tech.strip().lower() for tech in tech_stack.split(',')]
        
        # Try to get a question from the specified tech stack first
        for tech in tech_list:
            if tech in self.general_questions:
                questions = self.general_questions.get(level, self.general_questions["mid"])
                if questions:
                    return random.choice(questions)
        
        # Fall back to general questions
        general_questions = self.general_questions.get(level, self.general_questions["mid"])
        return random.choice(general_questions)
    
    def get_general_response(self, response_type: str) -> str:
        """Get a general response for non-interview questions"""
        responses = self.general_responses.get(response_type, [])
        if responses:
            return random.choice(responses)
        return "I'm here to help with your interview. What would you like to know?"
    
    def is_interview_question(self, user_input: str) -> bool:
        """Determine if user input is asking about the interview process"""
        interview_keywords = [
            "interview", "question", "ask", "technical", "behavioral", "experience",
            "skills", "project", "work", "job", "position", "role", "company"
        ]
        
        user_lower = user_input.lower()
        return any(keyword in user_lower for keyword in interview_keywords)
    
    def is_general_question(self, user_input: str) -> bool:
        """Determine if user input is a general question or unrelated response"""
        # Very brief responses that don't contribute to interview
        if len(user_input.strip()) <= 3:
            return True
            
        # General greetings and unrelated keywords
        general_keywords = [
            "hello", "hi", "hey", "help", "what", "how", "why", "when", "where",
            "thanks", "thank you", "goodbye", "bye", "see you", "farewell",
            "okay", "ok", "yes", "no", "maybe", "sure", "fine", "good", "bad"
        ]
        
        # Unrelated topics that should redirect to interview
        unrelated_keywords = [
            "apple", "banana", "food", "weather", "sports", "movie", "music", "game",
            "car", "house", "pet", "family", "friend", "school", "college", "university"
        ]
        
        user_lower = user_input.lower()
        
        # Check for general keywords
        if any(keyword in user_lower for keyword in general_keywords):
            return True
            
        # Check for unrelated topics
        if any(keyword in user_lower for keyword in unrelated_keywords):
            return True
            
        # Check if response is too generic (like just "okay", "yes", "no")
        if user_input.strip().lower() in ["okay", "ok", "yes", "no", "maybe", "sure", "fine", "good", "bad"]:
            return True
            
        return False
    
    def get_response_type(self, user_input: str) -> str:
        """Determine the type of response needed based on user input"""
        if self.is_general_question(user_input):
            # Very brief responses
            if len(user_input.strip()) <= 3:
                return "redirect"
            # Greetings
            elif any(word in user_input.lower() for word in ["hello", "hi", "hey"]):
                return "greeting"
            # Help requests
            elif any(word in user_input.lower() for word in ["help", "what", "how"]):
                return "help"
            # Thanks
            elif any(word in user_input.lower() for word in ["thanks", "thank you"]):
                return "thanks"
            # Goodbyes
            elif any(word in user_input.lower() for word in ["goodbye", "bye", "see you"]):
                return "goodbye"
            # Unrelated topics
            elif any(word in user_input.lower() for word in ["apple", "banana", "food", "weather", "sports", "movie", "music", "game", "car", "house", "pet", "family", "friend", "school", "college", "university"]):
                return "redirect"
            # Generic responses
            elif user_input.strip().lower() in ["okay", "ok", "yes", "no", "maybe", "sure", "fine", "good", "bad"]:
                return "redirect"
            else:
                return "redirect"
        elif self.is_interview_question(user_input):
            return "interview"
        else:
            return "interview"  # Default to interview mode
    
    def _normalize_experience_level(self, experience_level: str) -> str:
        """Normalize experience level to standard categories"""
        level_lower = experience_level.lower()
        
        if any(word in level_lower for word in ["entry", "junior", "0-2", "1-2", "0", "1"]):
            return "entry"
        elif any(word in level_lower for word in ["senior", "lead", "principal", "5+", "6+", "7+", "8+", "9+", "10+"]):
            return "senior"
        else:
            return "mid"  # Default to mid-level

# Global instance
prompt_manager = PromptManager()

# Export main functions for easy access
def get_welcome_message(name: str, tech_stack: str, experience_level: str = "mid") -> str:
    """Get a welcome message for the candidate"""
    return prompt_manager.get_welcome_message(name, tech_stack, experience_level)

def get_dynamic_question_prompt(candidate: Dict[str, str], user_response: str, context: str = "", question_type: str = "technical") -> str:
    """Get a dynamic prompt for generating questions based on user response"""
    return prompt_manager.get_dynamic_question_prompt(candidate, user_response, context, question_type)

def get_fallback_question(tech_stack: str, experience_level: str, question_type: str = "random") -> str:
    """Get a fallback question when dynamic generation isn't available"""
    return prompt_manager.get_fallback_question(tech_stack, experience_level, question_type)

def get_general_response(response_type: str) -> str:
    """Get a general response for non-interview questions"""
    return prompt_manager.get_general_response(response_type)

def is_interview_question(user_input: str) -> bool:
    """Check if user input is about the interview"""
    return prompt_manager.is_interview_question(user_input)

def is_general_question(user_input: str) -> bool:
    """Check if user input is a general question"""
    return prompt_manager.is_general_question(user_input)

def get_response_type(user_input: str) -> bool:
    """Determine the type of response needed"""
    return prompt_manager.get_response_type(user_input)

def get_system_prompt(candidate: Dict[str, str], phase: InterviewPhase = InterviewPhase.TECHNICAL, user_response: str = "", conversation_context: str = "") -> str:
    """Get system prompt for AI model with user response context"""
    return prompt_manager.get_system_prompt(candidate, phase, user_response, conversation_context)

def extract_topics_from_response(response: str) -> List[str]:
    """Extract key technical topics from user response"""
    return prompt_manager._extract_topics_from_response(response)

# Export the main class and enum for advanced usage
__all__ = [
    "PromptManager", "InterviewPhase", "prompt_manager",
    "get_welcome_message", "get_dynamic_question_prompt", "get_fallback_question",
    "get_general_response", "is_interview_question", "is_general_question", 
    "get_response_type", "get_system_prompt", "extract_topics_from_response"
]
