import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import GenerateContentConfig

# Load environment variables from .env file
load_dotenv()
GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]

# Create Gemini client
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# for model in client.models.list():
#     print(model.name)

chat_history = []  # keep track of all messages

print("Chat-Bot (type 'quit' to exit)")
print("----------------------------------------")

while True:
    user_input = input("You: ")
    if user_input.lower() in ['quit', 'exit']:
        print("Goodbye!")
        break
    
    # Add user message to history
    chat_history.append(f"User: {user_input}")
    
    # Prepare prompt for Gemini (include previous messages)
    prompt = "\n".join(chat_history) + "\nBot:"
    
    response = client.models.generate_content(
        model="models/gemini-flash-lite-latest",
        contents=prompt,
        config=GenerateContentConfig(
            temperature=0.7,
            top_p=1,
            max_output_tokens=100
        )
    )
    
    # Extract model response text
    bot_reply = "".join([part.text for part in response.candidates[0].content.parts])
    
    # Add bot response to history
    chat_history.append(f"Bot: {bot_reply}")
    
    print(f"Bot: {bot_reply}\n")