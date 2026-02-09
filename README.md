# Chatbot-Driven TikTok Ad Campaign Creation

This project implements a conversational AI agent that assists users in
creating TikTok Ad campaign configurations through step-by-step dialogue.

## Key Features
- Conversational ad creation
- Structured ad payload generation
- Business rule enforcement
- TikTok OAuth error handling (mocked)
- Music logic validation
- Graceful API failure reasoning

## OAuth Handling
The OAuth flow is simulated to represent the TikTok Authorization Code flow.
The agent detects and explains:
- Expired OAuth tokens
- Missing Ads permission scope
- Geo-restrictions

## Music Logic
The agent supports three cases:
1. Existing music ID validation
2. Custom music upload (simulated)
3. No-music ads (allowed only for Traffic campaigns)

## Structured Output
The final ad configuration is generated as a structured JSON payload
ready for submission to the TikTok Ads API.

## How to Run
```bash
python tiktok_ad_agent.py
