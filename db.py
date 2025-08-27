import pymongo
from datetime import datetime
from typing import Dict, List, Optional
import json
import ssl
import certifi
import sys

class MongoDBManager:
    def __init__(self):
        # MongoDB connection string - clean version without problematic SSL params
        self.connection_string = "mongodb+srv://saip00519:hqicJwS5iFsswYFF@cluster0.ul56bs8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
        self.client = None
        self.db = None
        self.interviews_collection = None
        self.questions_collection = None
        
        # Check SSL/TLS support
        self._check_ssl_support()
        
    def _check_ssl_support(self):
        """Check SSL/TLS support and provide helpful information"""
        try:
            # Check Python version
            python_version = sys.version_info
            print(f"Python version: {python_version.major}.{python_version.minor}.{python_version.micro}")
            
            # Check OpenSSL version
            openssl_version = ssl.OPENSSL_VERSION
            print(f"OpenSSL version: {openssl_version}")
            
            # Check if certifi is available
            try:
                certifi_path = certifi.where()
                print(f"Certifi certificates available at: {certifi_path}")
            except Exception as e:
                print(f"Warning: Certifi not available: {e}")
                print("Installing certifi...")
                try:
                    import subprocess
                    subprocess.check_call([sys.executable, "-m", "pip", "install", "certifi"])
                    print("Certifi installed successfully!")
                except Exception as install_e:
                    print(f"Failed to install certifi: {install_e}")
            
            # Check TLS version support
            try:
                context = ssl.create_default_context()
                print(f"Default SSL context created successfully")
            except Exception as e:
                print(f"Warning: Could not create default SSL context: {e}")
                
        except Exception as e:
            print(f"Error checking SSL support: {e}")
    
    def connect(self):
        """Establish connection to MongoDB"""
        # Try multiple connection approaches with proper SSL handling
        connection_attempts = [
            # Attempt 1: Standard connection with proper SSL (recommended)
            {
                'uri': "mongodb+srv://saip00519:hqicJwS5iFsswYFF@cluster0.ul56bs8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
                'options': {
                    'serverSelectionTimeoutMS': 30000,
                    'connectTimeoutMS': 30000,
                    'socketTimeoutMS': 30000,
                    'maxPoolSize': 10,
                    'retryWrites': True,
                    'w': 'majority',
                    'tls': True,
                    'tlsAllowInvalidCertificates': False
                }
            },
            # Attempt 2: With TLS but allow invalid certificates (fallback)
            {
                'uri': "mongodb+srv://saip00519:hqicJwS5iFsswYFF@cluster0.ul56bs8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
                'options': {
                    'serverSelectionTimeoutMS': 30000,
                    'connectTimeoutMS': 30000,
                    'socketTimeoutMS': 30000,
                    'maxPoolSize': 10,
                    'retryWrites': True,
                    'w': 'majority',
                    'tls': True,
                    'tlsAllowInvalidCertificates': True
                }
            },
            # Attempt 3: Minimal connection options
            {
                'uri': "mongodb+srv://saip00519:hqicJwS5iFsswYFF@cluster0.ul56bs8.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
                'options': {
                    'serverSelectionTimeoutMS': 30000,
                    'connectTimeoutMS': 30000,
                    'socketTimeoutMS': 30000
                }
            }
        ]
        
        for i, attempt in enumerate(connection_attempts, 1):
            try:
                print(f"Connection attempt {i}...")
                self.client = pymongo.MongoClient(attempt['uri'], **attempt['options'])
                
                # Test the connection with a timeout
                self.client.admin.command('ping', serverSelectionTimeoutMS=10000)
                print(f"Successfully connected to MongoDB on attempt {i}!")
                
                # Get database and collections
                self.db = self.client['interview_db']
                self.interviews_collection = self.db['interviews']
                self.questions_collection = self.db['questions']
                
                # Create indexes for better performance
                self.interviews_collection.create_index([("interview_id", pymongo.ASCENDING)], unique=True)
                self.questions_collection.create_index([("question_id", pymongo.ASCENDING)], unique=True)
                
                return True
                
            except pymongo.errors.ServerSelectionTimeoutError as e:
                print(f"Attempt {i} - Server selection timeout: {e}")
                if self.client:
                    self.client.close()
                continue
                
            except pymongo.errors.ConnectionFailure as e:
                print(f"Attempt {i} - Connection failure: {e}")
                if self.client:
                    self.client.close()
                continue
                
            except Exception as e:
                print(f"Attempt {i} - Error: {e}")
                if self.client:
                    self.client.close()
                continue
        
        print("All connection attempts failed. Please check:")
        print("1. Your internet connection")
        print("2. MongoDB Atlas cluster status")
        print("3. Network firewall settings")
        print("4. MongoDB Atlas IP whitelist")
        print("\nTrying to fix common SSL/TLS issues...")
        
        # Try to fix certificate issues
        if self._fix_certificate_issues():
            print("Certificate issues fixed. Trying connection again...")
            return self.connect()
        
        return False
    
    def _fix_certificate_issues(self):
        """Try to fix common SSL/TLS certificate issues"""
        try:
            print("Attempting to fix certificate issues...")
            
            # Try to install/upgrade certifi
            try:
                import subprocess
                print("Installing/upgrading certifi...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "certifi"])
                print("Certifi upgraded successfully!")
                
                # Also try to install/upgrade pymongo
                print("Installing/upgrading pymongo...")
                subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "pymongo"])
                print("PyMongo upgraded successfully!")
                
                return True
                
            except Exception as e:
                print(f"Failed to upgrade packages: {e}")
                return False
                
        except Exception as e:
            print(f"Error fixing certificate issues: {e}")
            return False
    
    def disconnect(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("MongoDB connection closed.")
    
    def save_interview_details(self, interview_data: Dict) -> bool:
        """Save interview details to MongoDB"""
        try:
            if self.interviews_collection is None:
                print("Database not connected. Please connect first.")
                return False
            
            # Add timestamp
            interview_data['created_at'] = datetime.utcnow()
            interview_data['updated_at'] = datetime.utcnow()
            
            # Generate unique interview ID if not provided
            if 'interview_id' not in interview_data:
                current_time = datetime.utcnow()
                interview_data['interview_id'] = f"interview_{current_time.strftime('%Y%m%d_%H%M%S_%f')}"
            
            # Insert the interview data
            result = self.interviews_collection.insert_one(interview_data)
            
            if result.inserted_id:
                print(f"Interview details saved successfully with ID: {result.inserted_id}")
                return True
            else:
                print("Failed to save interview details")
                return False
                
        except Exception as e:
            print(f"Error saving interview details: {e}")
            
            # Handle duplicate key errors specifically
            if "duplicate key error" in str(e) and "interview_id" in str(e):
                print("Duplicate interview_id detected. Attempting to regenerate ID and retry...")
                try:
                    # Regenerate interview ID with fresh timestamp
                    current_time = datetime.utcnow()
                    interview_data['created_at'] = current_time
                    interview_data['updated_at'] = current_time
                    interview_data['interview_id'] = f"interview_{current_time.strftime('%Y%m%d_%H%M%S_%f')}"
                    
                    # Try inserting again
                    result = self.interviews_collection.insert_one(interview_data)
                    if result.inserted_id:
                        print(f"Interview details saved successfully after retry with ID: {result.inserted_id}")
                        return True
                except Exception as retry_e:
                    print(f"Retry failed: {retry_e}")
            
            return False
    
    def save_interview_questions(self, questions_data: List[Dict]) -> bool:
        """Save interview questions to MongoDB"""
        try:
            if self.questions_collection is None:
                print("Database not connected. Please connect first.")
                return False
            
            # Add timestamps and IDs to each question with unique IDs
            for i, question in enumerate(questions_data):
                current_time = datetime.utcnow()
                question['created_at'] = current_time
                question['updated_at'] = current_time
                
                # Generate unique question ID if not provided
                if 'question_id' not in question:
                    # Use index to ensure uniqueness even if timestamps are identical
                    question['question_id'] = f"q_{current_time.strftime('%Y%m%d_%H%M%S_%f')}_{i:03d}"
            
            # Insert all questions
            result = self.questions_collection.insert_many(questions_data)
            
            if result.inserted_ids:
                print(f"Successfully saved {len(result.inserted_ids)} questions")
                return True
            else:
                print("Failed to save questions")
                return False
                
        except Exception as e:
            print(f"Error saving questions: {e}")
            
            # Handle duplicate key errors specifically
            if "duplicate key error" in str(e) and "question_id" in str(e):
                print("Duplicate question_id detected. Attempting to regenerate IDs and retry...")
                try:
                    # Regenerate all IDs with fresh timestamps
                    for i, question in enumerate(questions_data):
                        current_time = datetime.utcnow()
                        question['created_at'] = current_time
                        question['updated_at'] = current_time
                        question['question_id'] = f"q_{current_time.strftime('%Y%m%d_%H%M%S_%f')}_{i:03d}"
                    
                    # Try inserting again
                    result = self.questions_collection.insert_many(questions_data)
                    if result.inserted_ids:
                        print(f"Successfully saved {len(result.inserted_ids)} questions after retry")
                        return True
                except Exception as retry_e:
                    print(f"Retry failed: {retry_e}")
            
            return False
    
    def get_interview_by_id(self, interview_id: str) -> Optional[Dict]:
        """Retrieve interview details by ID"""
        try:
            if self.interviews_collection is None:
                print("Database not connected. Please connect first.")
                return None
            
            interview = self.interviews_collection.find_one({"interview_id": interview_id})
            return interview
            
        except Exception as e:
            print(f"Error retrieving interview: {e}")
            return None
    
    def get_questions_by_interview_id(self, interview_id: str) -> List[Dict]:
        """Retrieve interview questions by ID"""
        try:
            if self.questions_collection is None:
                print("Database not connected. Please connect first.")
                return []
            
            questions = list(self.questions_collection.find({"interview_id": interview_id}))
            return questions
            
        except Exception as e:
            print(f"Error retrieving questions: {e}")
            return []
    
    def update_interview(self, interview_id: str, update_data: Dict) -> bool:
        """Update interview details"""
        try:
            if self.interviews_collection is None:
                print("Database not connected. Please connect first.")
                return False
            
            update_data['updated_at'] = datetime.utcnow()
            
            result = self.interviews_collection.update_one(
                {"interview_id": interview_id},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                print(f"Interview {interview_id} updated successfully")
                return True
            else:
                print(f"No interview found with ID: {interview_id}")
                return False
                
        except Exception as e:
            print(f"Error updating interview: {e}")
            return False
    
    def delete_interview(self, interview_id: str) -> bool:
        """Delete interview and all associated questions"""
        try:
            if self.interviews_collection is None or self.questions_collection is None:
                print("Database not connected. Please connect first.")
                return False
            
            # Delete interview
            interview_result = self.interviews_collection.delete_one({"interview_id": interview_id})
            
            # Delete associated questions
            questions_result = self.questions_collection.delete_many({"interview_id": interview_id})
            
            if interview_result.deleted_count > 0:
                print(f"Interview {interview_id} and {questions_result.deleted_count} questions deleted successfully")
                return True
            else:
                print(f"No interview found with ID: {interview_id}")
                return False
                
        except Exception as e:
            print(f"Error deleting interview: {e}")
            return False
    
    def get_all_interviews(self) -> List[Dict]:
        """Retrieve all interviews"""
        try:
            if self.interviews_collection is None:
                print("Database not connected. Please connect first.")
                return []
            
            interviews = list(self.interviews_collection.find().sort("created_at", -1))
            return interviews
            
        except Exception as e:
            print(f"Error retrieving interviews: {e}")
            return []
    
    def search_interviews(self, search_criteria: Dict) -> List[Dict]:
        """Search interviews based on criteria"""
        try:
            if self.interviews_collection is None:
                print("Database not connected. Please connect first.")
                return []
            
            interviews = list(self.interviews_collection.find(search_criteria).sort("created_at", -1))
            return interviews
            
        except Exception as e:
            print(f"Error searching interviews: {e}")
            return []
    
    def get_interviews(self, filter_query: Dict = None) -> List[Dict]:
        """Get interviews with optional filtering"""
        try:
            if self.interviews_collection is None:
                print("Database not connected. Please connect first.")
                return []
            
            if filter_query is None:
                filter_query = {}
            
            interviews = list(self.interviews_collection.find(filter_query).sort("created_at", -1))
            return interviews
            
        except Exception as e:
            print(f"Error retrieving interviews: {e}")
            return []
    
    def get_interview_questions(self, interview_id: str) -> List[Dict]:
        """Get all questions and responses for a specific interview"""
        try:
            if self.questions_collection is None:
                print("Database not connected. Please connect first.")
                return []
            
            # Get questions sorted by message index
            questions = list(self.questions_collection.find(
                {"interview_id": interview_id}
            ).sort("message_index", 1))
            
            return questions
            
        except Exception as e:
            print(f"Error retrieving interview questions: {e}")
            return []

# Example usage and test functions
def test_mongodb_connection():
    """Test MongoDB connection and basic operations"""
    db_manager = MongoDBManager()
    
    # Test connection
    if not db_manager.connect():
        print("Failed to connect to MongoDB")
        return
    
    try:
        # Test saving interview details
        interview_data = {
            "candidate_name": "John Doe",
            "position": "Software Engineer",
            "interview_date": "2024-01-15",
            "duration": "60 minutes",
            "status": "completed",
            "notes": "Strong technical skills, good communication"
        }
        
        if db_manager.save_interview_details(interview_data):
            print("Interview details saved successfully")
            
            # Get the interview ID from the saved data
            interview_id = interview_data['interview_id']
            
            # Test saving questions
            questions_data = [
                {
                    "interview_id": interview_id,
                    "question_text": "Tell me about your experience with Python",
                    "question_type": "technical",
                    "difficulty": "medium",
                    "category": "programming"
                },
                {
                    "interview_id": interview_id,
                    "question_text": "How do you handle conflicts in a team?",
                    "question_type": "behavioral",
                    "difficulty": "easy",
                    "category": "soft_skills"
                }
            ]
            
            if db_manager.save_interview_questions(questions_data):
                print("Questions saved successfully")
                
                # Test retrieving data
                retrieved_interview = db_manager.get_interview_by_id(interview_id)
                retrieved_questions = db_manager.get_questions_by_interview_id(interview_id)
                
                print(f"Retrieved interview: {retrieved_interview}")
                print(f"Retrieved questions: {len(retrieved_questions)}")
                
        else:
            print("Failed to save interview details")
            
    except Exception as e:
        print(f"Test failed: {e}")
    
    finally:
        # Clean up
        db_manager.disconnect()

if __name__ == "__main__":
    # Run test if file is executed directly
    test_mongodb_connection()
