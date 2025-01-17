import streamlit as st
from interview_agent import InterviewAgent
import traceback

def main():
    st.title("Professional Background Interview")
    
    # Initialize the interview agent
    if 'agent' not in st.session_state:
        try:
            st.session_state.agent = InterviewAgent()
            st.session_state.messages = []
            st.session_state.current_question = st.session_state.agent.get_next_question()
            # Add the initial question to messages right away
            st.session_state.messages.append({"role": "assistant", "content": st.session_state.current_question})
        except Exception as e:
            st.error(f"Error initializing agent: {str(e)}")
            st.error(traceback.format_exc())
            return

    # Display chat history
    try:
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])

        # Get user input
        user_response = st.chat_input("Your response")
        
        if user_response:
            # Add user response to chat history
            st.session_state.messages.append({"role": "user", "content": user_response})
            
            try:
                # Get next question
                next_question = st.session_state.agent.get_next_question(user_response)
                st.session_state.messages.append({"role": "assistant", "content": next_question})
                
                # Rerun to update the display
                st.experimental_rerun()
            except Exception as e:
                st.error(f"Error processing response: {str(e)}")
                st.error(traceback.format_exc())
                
    except Exception as e:
        st.error(f"Error in main loop: {str(e)}")
        st.error(traceback.format_exc())

if __name__ == "__main__":
    main()