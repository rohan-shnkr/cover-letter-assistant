from dotenv import load_dotenv
import os
from openai import OpenAI

# Load the environment variables from the .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def main():
    print("Starting the Interview Agent...")

    # Basic test to see if the API key is working
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini-2024-07-18",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say Hello!"},
            ]
        )
        print(response.choices[0].message.content)
        print("API Key is working!")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()