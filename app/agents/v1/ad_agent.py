import requests
from dotenv import load_dotenv
import os
import json

load_dotenv()

MODEL = os.getenv("MODEL")
OLLAMA_API = os.getenv("OLLAMA_API")

from app.agents.v1.prompt import SYSTEM_PROMPT

context = []
first_message = True
final_data = None
collected = {
    "campaign_name": None,
    "objective": None,
    "ad_text": None,
    "cta": None,
    "music_id": None
}

payload = {
    "model": MODEL,
    "stream": False
}

print("Please type exit to quit chat.")

def get_next_field(collected):
    order = ["campaign_name", "objective", "ad_text", "cta"]
    if collected["objective"] != None:
        if collected["objective"].lower() == str("CONVERSIONS").lower():
            order.append("music_id")
    for f in order:
        if collected[f] is None:
            return f
    return None

while True:

    state_text = "\n".join([f"{k} = {v}" for k, v in collected.items() if v is not None])
    next_field = get_next_field(collected)
    if first_message:
        payload["prompt"] = f"""
SYSTEM:
{SYSTEM_PROMPT}

Collected so far:
{state_text}

Ask for this field exactly:
{next_field}

Assistant:
"""
        result = requests.post(OLLAMA_API, json=payload)
        response = result.json()
        reply = response.get("response", "")
        print(f"[Assistant]: {reply}")
        first_message = False
    user_message = input("[You]: ").strip()
    if user_message.lower() == "exit":
        print("[Assistant]: Conversation ended.")
        break
    current_field = get_next_field(collected)
    if current_field:
        collected[current_field] = user_message
    next_field = get_next_field(collected)
    if next_field is None:
        final_json = {
            "campaign_name": collected["campaign_name"],
            "objective": collected["objective"],
            "ad_text": collected["ad_text"],
            "cta": collected["cta"],
            "music_id": (
                collected["music_id"]
                if collected["objective"].lower() == "CONVERSIONS".lower()
                else None
            )
        }
        print("\nFINAL DATA COLLECTED:")
        print(json.dumps(final_json, indent=2))
        print("[Assistant]:Thank you for the details your details are processing.")
        final_data = json.dumps(final_json, indent=2)
        break

    state_text = "\n".join(
        [f"{k} = {v}" for k, v in collected.items() if v is not None])
    payload["prompt"] = f"""
SYSTEM:
{SYSTEM_PROMPT}

Collected so far:
{state_text}

Ask for this field exactly:
{next_field}

Assistant:
"""
    if context:
        payload["context"] = context
    result = requests.post(OLLAMA_API, json=payload)
    response = result.json()

    reply = response.get("response", "")
    print(f"[Assistant]: {reply}")

    context = response.get("context", context)

login_details = {
    "client_id":"valid_client_123",
    "region":"US"
}
token_request = requests.post("http://localhost:8080//user/oauth/token", json=login_details)
token_json = token_request.json()
print(token_request.status_code)
print(token_request.text)
access_token = token_json["data"]["access_token"]
headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
result = requests.post("http://localhost:8080/user/api/ad/create", json=final_data, headers=headers)
print("[Assistant]: Thank you for the details, your data is being processed.")
print("Ad API response:", result.text)

