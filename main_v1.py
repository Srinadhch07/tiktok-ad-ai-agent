from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

from google import genai
import os

client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# List all available models
print("Available Models:")
for model in client.models.list():
    print(f"Name: {model.name}")
    print(f"Display Name: {model.display_name}")
    print(f"Supported Actions: {model.supported_actions}")
    print("-" * 20)

from google.genai import types

response = client.models.generate_content(
    model="gemini-2.5-flash-lite",
    contents="ask 100 coding questions in a plain text. keep level and mention level of each question in ()",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(include_thoughts=True)
    )
)

# This shows the "hidden" reasoning process
print(f"Thinking: {response.candidates[0].grounding_metadata}") 
print(f"Final Answer: {response.text}")

