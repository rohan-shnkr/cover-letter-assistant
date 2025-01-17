from interview_agent import InterviewAgent

def test_basic_functionality():
    agent = InterviewAgent()
    
    # Test 1: Basic data collection
    print("\nTest 1: Adding sample data")
    agent.collected_data['education']['undergrad'] = {
        'university': 'IIT Kharagpur',
        'major': 'Industrial Engineering',
        'year': '2018'
    }
    agent.debug_show_collected_data()
    
    # Test 2: Pinecone connectivity
    print("\nTest 2: Testing Pinecone storage")
    test_data = {
        'type': 'education',
        'details': 'Test entry'
    }
    agent.test_pinecone_storage(test_data)

if __name__ == "__main__":
    test_basic_functionality()