from openai import OpenAI
import os
from datetime import datetime
import json
from pinecone import Pinecone 
from dotenv import load_dotenv

# Load the environment variables from the .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Initialize Pinecone correctly with new API
pc = Pinecone(
    api_key=os.getenv("PINECONE_API_KEY"),
    environment=os.getenv("PINECONE_ENVIRONMENT")
)

class InterviewAgent:
    def __init__(self):
        self.index_name = "self-kb"
        self.index = pc.Index(self.index_name)

        # Building a structure to track chronological experience
        self.collected_data = {
            'education': {
                'undergrad': {},
                'graduate': {},
                'certifications': []
                },
            'experiences': [], # Will store chronologically
            'skills': {
                'technical': {},
                'soft': {},
                'domain': {}
            },

            'projects': {},
            'achievements': {},
            'personal_brand': {}
        }

        self.interview_stages = [
            'education_undergrad',
            'education_graduate',
            'early_experience',
            'recent_experience',
            'skills_summary'
        ]

        self.current_stage = 0
        self.interview_context = {
            'current_stage': self.interview_stages[0],
            'current_experience': None,
            'current_project': None,
            'follow-up_needed': True
        }

    def get_next_question(self, user_response=None):
        """Generate the next appropriate question based on current stage"""
        try:
            if user_response:
                # Update context with user response
                self._update_context(user_response)

                system_prompt = f"""
                You are conducting a chronological professional interview.
                Current Stage: {self.interview_context['current_stage']}
                Previous Data: {json.dumps(self.collected_data)}

                Guidelines:
                1. Ask 1 focused question at a time.
                2. For each experience/project, gather:
                    - Skills Used/Developed
                    - Achievements
                    - Challenges Overcome
                3. Keep Questions Conversational but specific
                4. Don't jump topics until current topic is fully explored.
                """

                messages = [
                    {"role": "system", "content": system_prompt}
                ]

                if user_response:
                    messages.append({"role": "user", "content": user_response})

                response = client.chat.completions.create(
                    model="gpt-4o-mini-2024-07-18",
                    messages=messages
                )

                return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error: {e}")
            return "An error occurred. Please try again."
        
    def _update_context(self, user_response):
        """Update context and collected data based on response"""
        # Logic to update stage and stored information
        pass

    def debug_show_collected_data(self):
        """Debug function to print currently collected data"""
        print("Currently collected data:")
        print(json.dumps(self.collected_data, indent=2))
    
    def test_pinecone_storage(self, test_data):
        """Test function to verify Pinecone storage"""
        try:
            # Create a test vector with some non-zero values
            test_vector = [0.0] * 1536
            test_vector[0] = 1.0
            test_vector[100] = 0.5
            test_vector[500] = -0.3
            
            # Test upsert
            upsert_response = self.index.upsert(
                vectors=[{
                    'id': 'test_entry',
                    'values': test_vector,
                    'metadata': test_data
                }]
            )
            print(f"Upsert status: {upsert_response['upserted_count']} vectors stored")
            
            # Test query
            query_result = self.index.query(
                vector=test_vector,
                top_k=1,
                include_metadata=True
            )
            
            print("\nPinecone test results:")
            print("Matches found:")
            for match in query_result.matches:
                print(f"\nMatch details:")
                print(f"- ID: {match.id}")
                print(f"- Score: {match.score}")
                print(f"- Metadata: {match.metadata}")
            
            return True
            
        except Exception as e:
            print(f"Pinecone test failed: {str(e)}")
            print(f"Error type: {type(e)}")
            return False