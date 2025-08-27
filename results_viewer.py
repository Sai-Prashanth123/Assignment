import streamlit as st
import pandas as pd
from datetime import datetime
from db import MongoDBManager
import plotly.express as px
import plotly.graph_objects as go

# Page configuration
st.set_page_config(
    page_title="Interview Results Viewer",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    
    .metric-card {
        background-color: #2d3748;
        color: #e2e8f0;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #3182ce;
        margin-bottom: 1rem;
    }
    
    .interview-card {
        background-color: #2d3748;
        color: #e2e8f0;
        padding: 1.5rem;
        border-radius: 10px;
        border: 1px solid #4a5568;
        margin-bottom: 1rem;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .interview-card:hover {
        border-color: #3182ce;
        box-shadow: 0 4px 8px rgba(49, 130, 206, 0.3);
    }
    
    .stats-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize MongoDB connection
@st.cache_resource
def init_db():
    db_manager = MongoDBManager()
    if db_manager.connect():
        return db_manager
    return None

def main():
    st.markdown('<h1 class="main-header">📊 Interview Results Viewer</h1>', unsafe_allow_html=True)
    
    # Initialize database connection
    db_manager = init_db()
    if not db_manager:
        st.error("❌ Could not connect to database. Please check your connection settings.")
        return
    
    # Sidebar filters
    with st.sidebar:
        st.markdown("### 🔍 Filters")
        
        # Date range filter
        st.markdown("**Date Range:**")
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("From", value=datetime.now().replace(day=1))
        with col2:
            end_date = st.date_input("To", value=datetime.now())
        
        # Status filter
        status_filter = st.selectbox("Status", ["All", "completed", "in_progress"])
        
        # Experience level filter
        experience_filter = st.selectbox("Experience Level", ["All"] + ["Entry Level", "Mid Level", "Senior Level", "Expert Level"])
        
        # Search by name
        name_search = st.text_input("Search by Name", placeholder="Enter candidate name...")
        
        # Apply filters button
        if st.button("🔍 Apply Filters", use_container_width=True):
            st.rerun()
    
    # Main content
    tab1, tab2, tab3 = st.tabs(["📈 Dashboard", "📋 Interview List", "🔍 Detailed View"])
    
    with tab1:
        show_dashboard(db_manager, start_date, end_date, status_filter, experience_filter, name_search)
    
    with tab2:
        show_interview_list(db_manager, start_date, end_date, status_filter, experience_filter, name_search)
    
    with tab3:
        show_detailed_view(db_manager)

def show_dashboard(db_manager, start_date, end_date, status_filter, experience_filter, name_search):
    """Display dashboard with charts and metrics"""
    st.markdown("## 📊 Interview Analytics Dashboard")
    
    # Get filtered data
    interviews = get_filtered_interviews(db_manager, start_date, end_date, status_filter, experience_filter, name_search)
    
    if not interviews:
        st.info("No interviews found with the current filters.")
        return
    
    # Convert to DataFrame for analysis
    df = pd.DataFrame(interviews)
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Interviews", len(interviews))
    with col2:
        completed = len([i for i in interviews if i.get('status') == 'completed'])
        st.metric("Completed", completed)
    with col3:
        avg_questions = df['question_count'].mean() if 'question_count' in df.columns else 0
        st.metric("Avg Questions", f"{avg_questions:.1f}")
    with col4:
        avg_sentiment = df['sentiment_summary.average_sentiment'].mean() if 'sentiment_summary.average_sentiment' in df.columns else 0
        st.metric("Avg Sentiment", f"{avg_sentiment:.2f}")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Experience level distribution
        if 'experience_level' in df.columns:
            exp_counts = df['experience_level'].value_counts()
            fig = px.pie(values=exp_counts.values, names=exp_counts.index, title="Experience Level Distribution")
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Question count distribution
        if 'question_count' in df.columns:
            fig = px.histogram(df, x='question_count', title="Question Count Distribution", nbins=10)
            st.plotly_chart(fig, use_container_width=True)
    
    # Sentiment trend over time
    if 'interview_date' in df.columns and 'sentiment_summary.average_sentiment' in df.columns:
        df['interview_date'] = pd.to_datetime(df['interview_date'])
        df_sorted = df.sort_values('interview_date')
        
        fig = px.line(df_sorted, x='interview_date', y='sentiment_summary.average_sentiment', 
                     title="Sentiment Trend Over Time")
        st.plotly_chart(fig, use_container_width=True)

def show_interview_list(db_manager, start_date, end_date, status_filter, experience_filter, name_search):
    """Display list of interviews with basic information"""
    st.markdown("## 📋 Interview List")
    
    interviews = get_filtered_interviews(db_manager, start_date, end_date, status_filter, experience_filter, name_search)
    
    if not interviews:
        st.info("No interviews found with the current filters.")
        return
    
    # Display interviews in cards
    for interview in interviews:
        with st.container():
            col1, col2, col3 = st.columns([3, 2, 1])
            
            with col1:
                st.markdown(f"**{interview.get('candidate_name', 'Unknown')}**")
                st.markdown(f"*{interview.get('position', 'N/A')}*")
                st.markdown(f"📧 {interview.get('email', 'N/A')}")
            
            with col2:
                st.markdown(f"📅 {interview.get('interview_date', 'N/A')}")
                st.markdown(f"⏰ {interview.get('interview_time', 'N/A')}")
                st.markdown(f"❓ {interview.get('question_count', 0)} questions")
            
            with col3:
                status = interview.get('status', 'unknown')
                if status == 'completed':
                    st.success("✅ Completed")
                else:
                    st.info("🔄 In Progress")
                
                if st.button(f"View Details", key=f"view_{interview.get('_id', 'unknown')}"):
                    st.session_state.selected_interview = interview
                    st.rerun()
            
            st.markdown("---")

def show_detailed_view(db_manager):
    """Show detailed view of a selected interview"""
    st.markdown("## 🔍 Detailed Interview View")
    
    if 'selected_interview' not in st.session_state:
        st.info("Please select an interview from the Interview List tab to view details.")
        return
    
    interview = st.session_state.selected_interview
    
    # Interview header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### 👤 {interview.get('candidate_name', 'Unknown')}")
        st.markdown(f"**Position:** {interview.get('position', 'N/A')}")
        st.markdown(f"**Experience:** {interview.get('experience_level', 'N/A')}")
    with col2:
        if interview.get('status') == 'completed':
            st.success("✅ Completed")
        else:
            st.info("🔄 In Progress")
    
    # Candidate details
    with st.expander("👤 Candidate Information", expanded=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"**Email:** {interview.get('email', 'N/A')}")
            st.markdown(f"**Phone:** {interview.get('phone', 'N/A')}")
            st.markdown(f"**Location:** {interview.get('location', 'N/A')}")
        with col2:
            st.markdown(f"**Tech Stack:** {interview.get('tech_stack', 'N/A')}")
            st.markdown(f"**Interview Date:** {interview.get('interview_date', 'N/A')}")
            st.markdown(f"**Interview Time:** {interview.get('interview_time', 'N/A')}")
    
    # Interview statistics
    with st.expander("📈 Interview Statistics", expanded=True):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Questions Asked", interview.get('question_count', 0))
        with col2:
            st.metric("Total Messages", interview.get('total_messages', 0))
        with col3:
            if 'sentiment_summary' in interview:
                st.metric("Positive Responses", interview['sentiment_summary'].get('positive_count', 0))
        with col4:
            if 'sentiment_summary' in interview:
                st.metric("Average Sentiment", f"{interview['sentiment_summary'].get('average_sentiment', 0):.2f}")
    
    # Sentiment analysis
    if 'sentiment_summary' in interview:
        with st.expander("😊 Sentiment Analysis", expanded=True):
            sentiment = interview['sentiment_summary']
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Positive", sentiment.get('positive_count', 0), delta=f"+{sentiment.get('positive_count', 0)}")
            with col2:
                st.metric("Neutral", sentiment.get('neutral_count', 0), delta="0")
            with col3:
                st.metric("Negative", sentiment.get('negative_count', 0), delta=f"-{sentiment.get('negative_count', 0)}")
    
    # Get interview questions and responses
    if 'interview_id' in interview:
        questions = db_manager.get_interview_questions(interview['interview_id'])
        if questions:
            with st.expander("💬 Interview Conversation", expanded=True):
                st.markdown("### Complete Interview Transcript")
                for q in questions:
                    if q.get('role') == 'assistant':
                        st.markdown(f"**🤖 Interviewer:**")
                        st.markdown(f"{q.get('question_text', 'N/A')}")
                    else:
                        st.markdown(f"**👤 Candidate:**")
                        st.markdown(f"*{q.get('question_text', 'N/A')}*")
                        if 'sentiment_score' in q:
                            score, label = q['sentiment_score']
                            st.markdown(f"*Sentiment: {label} ({score:.2f})*")
                    st.markdown("---")
    
    # Back button
    if st.button("← Back to Interview List"):
        del st.session_state.selected_interview
        st.rerun()

def get_filtered_interviews(db_manager, start_date, end_date, status_filter, experience_filter, name_search):
    """Get filtered interviews from database"""
    try:
        # Build filter query
        filter_query = {}
        
        # Date range filter
        if start_date and end_date:
            filter_query['interview_date'] = {
                '$gte': start_date.strftime('%Y-%m-%d'),
                '$lte': end_date.strftime('%Y-%m-%d')
            }
        
        # Status filter
        if status_filter != "All":
            filter_query['status'] = status_filter
        
        # Experience level filter
        if experience_filter != "All":
            filter_query['experience_level'] = experience_filter
        
        # Name search
        if name_search:
            filter_query['candidate_name'] = {'$regex': name_search, '$options': 'i'}
        
        # Get interviews from database
        interviews = db_manager.get_interviews(filter_query)
        return interviews or []
        
    except Exception as e:
        st.error(f"Error fetching interviews: {str(e)}")
        return []

if __name__ == "__main__":
    main()
