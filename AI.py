import os
from typing import Dict, List, Optional
from groq import Groq
from prompt import (
    get_system_prompt, 
    get_dynamic_question_prompt,
    InterviewPhase,
    is_general_question,
    get_general_response,
    get_response_type,
    extract_topics_from_response
)

GROQ_MODEL = "llama-3.3-70b-versatile"


def _build_system_prompt(candidate: Dict[str, str], phase: InterviewPhase = InterviewPhase.TECHNICAL, user_response: str = "", conversation_context: str = "") -> str:
    """Build system prompt using the prompt management system with user response context"""
    return get_system_prompt(candidate, phase, user_response, conversation_context)


def _build_messages(candidate: Dict[str, str], history: List[Dict[str, str]], user_latest: Optional[str], phase: InterviewPhase = InterviewPhase.TECHNICAL) -> List[Dict[str, str]]:
    """Build messages for the AI model with proper context"""
    
    # Determine if this is a general question or interview question
    if user_latest and is_general_question(user_latest):
        # For general questions, provide a simple system prompt
        system_prompt = """You are a helpful AI assistant. Answer questions briefly and professionally. If asked about the interview, redirect them back to the interview process."""
    else:
        # For interview questions, use the structured interview prompt with user response context
        system_prompt = _build_system_prompt(candidate, phase, user_latest)
    
    messages: List[Dict[str, str]] = [
        {"role": "system", "content": system_prompt}
    ]
    
    # Include minimal chat history for context (last 10 messages)
    for m in history[-10:]:
        role = m.get("role", "assistant")
        content = m.get("content", "")
        messages.append({"role": role, "content": content})
    
    if user_latest:
        messages.append({"role": "user", "content": user_latest})
    
    return messages


def _determine_next_phase(candidate: Dict[str, str], history: List[Dict[str, str]], user_response: str, current_phase: InterviewPhase) -> InterviewPhase:
    """Intelligently determine the next interview phase based on conversation flow"""
    
    if not user_response:
        return current_phase
    
    # Analyze the user response to understand what they're talking about
    topics = extract_topics_from_response(user_response)
    analysis = analyze_user_response(user_response)
    
    # If they're asking to start the interview, begin with technical questions
    if any(word in user_response.lower() for word in ["start", "begin", "interview", "questions"]):
        return InterviewPhase.TECHNICAL
    
    # If they're discussing technical topics, stay in technical phase
    if topics and len(topics) > 0:
        return InterviewPhase.TECHNICAL
    
    # If they mention behavioral topics, switch to behavioral
    behavioral_keywords = ["team", "collaboration", "conflict", "learning", "challenge", "difficult", "mentor", "lead", "worked with", "helped", "solved"]
    if any(keyword in user_response.lower() for keyword in behavioral_keywords):
        return InterviewPhase.BEHAVIORAL
    
    # If they're giving a technical answer, follow up with technical questions
    if current_phase == InterviewPhase.TECHNICAL:
        return InterviewPhase.FOLLOW_UP
    
    # Default to current phase
    return current_phase


def _should_ask_follow_up(history: List[Dict[str, str]], user_response: str) -> bool:
    """Determine if we should ask a follow-up question based on conversation context"""
    
    if len(history) < 2:
        return False
    
    # Check if the last AI message was a question
    last_ai_message = None
    for msg in reversed(history):
        if msg['role'] == 'assistant':
            last_ai_message = msg['content']
            break
    
    if not last_ai_message:
        return False
    
    # If the last AI message was a question and this is a response, ask follow-up
    if last_ai_message.endswith('?') and len(user_response.strip()) > 10:
        return True
    
    return False


def generate_next_question(candidate: Dict[str, str], history: List[Dict[str, str]], user_latest: Optional[str] = None, phase: InterviewPhase = InterviewPhase.TECHNICAL) -> str:
    """Generate the next interview question or follow-up based on user response.

    Args:
        candidate: dict with keys like full_name, desired_position, years_experience, tech_stack, location, email, phone, tone, detail_level, target_language
        history: prior messages in the list of dicts with roles 'user' or 'assistant' and 'content'
        user_latest: the latest user reply to consider for follow-up
        phase: current interview phase to guide question generation

    Returns:
        A single question string.
    """
    
    # Check if this is a general question or unrelated response first
    if user_latest and is_general_question(user_latest):
        response_type = get_response_type(user_latest)
        response = get_general_response(response_type)
        
        # If it's a redirect response, it should count as a proper interview question
        if response_type == "redirect":
            # Update the question count since this is now a proper interview question
            return response
        
        return response
    
    # Determine the appropriate phase for the next question
    next_phase = _determine_next_phase(candidate, history, user_latest, phase)
    
    # Check if we should ask a follow-up question
    should_follow_up = _should_ask_follow_up(history, user_latest) if user_latest else False
    
    # Lazy import to prevent app crash if 'groq' is not installed
    try:
        from groq import Groq  # type: ignore
    except Exception as import_exc:
        return (
            "Python package 'groq' is not installed. Install it with: pip install groq "
            f"(details: {import_exc})"
        )

    api_key = "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"
    if not api_key:
        return (
            "Environment variable GROQ_API_KEY is not set. "
            "Please add your Groq API key to the environment to enable AI-generated questions."
        )

    client = Groq(api_key=api_key)
    
    # Build conversation context for better continuity
    conversation_context = _build_conversation_context(history, user_latest)
    
    # Build dynamic prompt based on user response and phase
    if user_latest and next_phase != InterviewPhase.WELCOME:
        # Generate dynamic question prompt based on user's response
        question_type = "follow_up" if should_follow_up else ("technical" if next_phase == InterviewPhase.TECHNICAL else "behavioral")
        
        dynamic_prompt = get_dynamic_question_prompt(
            candidate=candidate,
            user_response=user_latest,
            context=conversation_context,
            question_type=question_type
        )
        
        # Use dynamic prompt to guide the AI
        messages = [
            {"role": "system", "content": _build_system_prompt(candidate, next_phase, user_latest, conversation_context)},
            {"role": "user", "content": dynamic_prompt}
        ]
    else:
        # Use standard message building for welcome or when no user response
        messages = _build_messages(candidate, history, user_latest, next_phase)

    try:
        completion = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=messages,
            temperature=0.7,  # Slightly higher for more dynamic responses
            max_completion_tokens=200,
            top_p=1,
            stream=False,
        )
        content = completion.choices[0].message.content or ""
        
        # Clean up the response to ensure it's just a question
        content = content.strip()
        
        # Remove any explanations or multiple questions
        if "\n\n" in content:
            content = content.split("\n\n")[0]
        
        # Ensure it ends with a question mark or is clearly a question
        if not content.endswith("?") and not any(word in content.lower() for word in ["can you", "what", "how", "why", "when", "where", "tell me", "describe", "explain"]):
            # If it doesn't look like a question, add a follow-up prompt
            content = f"{content} Can you elaborate on that?"
        
        return content
        
    except Exception as exc: # noqa: BLE001 - user-facing message
        return f"Unable to generate question right now: {exc}"


def _build_conversation_context(history: List[Dict[str, str]], user_response: str) -> str:
    """Build conversation context for better question continuity"""
    
    if not history:
        return "Starting new interview"
    
    # Get the last few exchanges for context
    recent_messages = history[-6:]  # Last 6 messages (3 exchanges)
    
    context_parts = []
    
    for msg in recent_messages:
        role = msg.get('role', '')
        content = msg.get('content', '')
        
        if role == 'assistant' and content.endswith('?'):
            context_parts.append(f"AI asked: {content}")
        elif role == 'user':
            context_parts.append(f"Candidate responded: {content[:100]}...")
    
    if user_response:
        context_parts.append(f"Latest response: {user_response[:100]}...")
    
    return " | ".join(context_parts) if context_parts else "No recent context"


def generate_follow_up_question(candidate: Dict[str, str], user_response: str, history: List[Dict[str, str]]) -> str:
    """Generate a dynamic follow-up question based on the user's specific response"""
    return generate_next_question(
        candidate=candidate,
        history=history,
        user_latest=user_response,
        phase=InterviewPhase.FOLLOW_UP
    )


def generate_behavioral_question(candidate: Dict[str, str], history: List[Dict[str, str]], user_response: str = "") -> str:
    """Generate a behavioral question, optionally based on user response"""
    return generate_next_question(
        candidate=candidate,
        history=history,
        user_latest=user_response,
        phase=InterviewPhase.BEHAVIORAL
    )


def generate_closing_question(candidate: Dict[str, str], history: List[Dict[str, str]]) -> str:
    """Generate a closing question"""
    return generate_next_question(
        candidate=candidate,
        history=history,
        user_latest=None,
        phase=InterviewPhase.CLOSING
    )


def analyze_user_response(user_response: str) -> Dict[str, any]:
    """Analyze user response to extract insights for better question generation"""
    analysis = {
        "topics": extract_topics_from_response(user_response),
        "response_length": len(user_response),
        "technical_depth": 0,
        "experience_level": "mid",
        "sentiment": "neutral"
    }
    
    # Analyze technical depth based on technical terms and concepts
    technical_indicators = [
        "architecture", "design pattern", "algorithm", "data structure", "optimization",
        "performance", "scalability", "security", "testing", "deployment", "monitoring",
        "debugging", "troubleshooting", "best practices", "trade-offs", "alternatives"
    ]
    
    response_lower = user_response.lower()
    technical_count = sum(1 for indicator in technical_indicators if indicator in response_lower)
    
    if technical_count >= 3:
        analysis["technical_depth"] = "high"
    elif technical_count >= 1:
        analysis["technical_depth"] = "medium"
    else:
        analysis["technical_depth"] = "low"
    
    # Simple sentiment analysis
    positive_words = ["successful", "achieved", "improved", "solved", "learned", "grew", "excited", "proud"]
    negative_words = ["challenging", "difficult", "struggled", "failed", "frustrated", "overwhelmed"]
    
    positive_count = sum(1 for word in positive_words if word in response_lower)
    negative_count = sum(1 for word in negative_words if word in response_lower)
    
    if positive_count > negative_count:
        analysis["sentiment"] = "positive"
    elif negative_count > positive_count:
        analysis["sentiment"] = "negative"
    
    return analysis


__all__ = [
    "generate_next_question", 
    "generate_follow_up_question", 
    "generate_behavioral_question", 
    "generate_closing_question",
    "analyze_user_response"
]