import uuid
import random

# ================== OAuth Manager ================== #
class OAuthManager:
    """
    Simulates TikTok OAuth Authorization Code flow.
    Handles common OAuth failures with human-readable messages.
    """

    def __init__(self):
        self.token = None

    def authenticate(self):
        print("\n🔐 Authenticating with TikTok OAuth...")
        outcome = random.choice([
            "success",
            "expired_token",
            "missing_scope",
            "geo_restricted"
        ])

        if outcome == "success":
            self.token = "valid_access_token"
            print("✅ OAuth successful")
            return self.token

        if outcome == "expired_token":
            raise Exception(
                "OAuth token expired. Please re-authenticate to obtain a new token."
            )

        if outcome == "missing_scope":
            raise Exception(
                "Missing required Ads permission scope. Enable ads permissions."
            )

        if outcome == "geo_restricted":
            raise Exception(
                "403 Geo-restriction detected. Ads API not available in this region."
            )


# ================== Mock TikTok Ads API ================== #
class TikTokAdsAPI:
    """
    Mocked TikTok Ads API client.
    Responsible for music validation and ad submission.
    """

    def validate_music(self, music_id):
        # Simulated validation logic
        return music_id.startswith("music_")

    def submit_ad(self, payload, token):
        # OAuth validation
        if token != "valid_access_token":
            return {"error": "Invalid or expired OAuth token"}

        # Music validation failure
        if payload["creative"]["music_id"] == "invalid":
            return {"error": "Invalid music ID"}

        return {
            "status": "success",
            "ad_id": str(uuid.uuid4())
        }


# ================== User Input Collection ================== #
def collect_campaign_inputs():
    print("\n📝 Collecting campaign details")

    campaign_name = input("Campaign name: ")
    if len(campaign_name) < 3:
        raise ValueError("Campaign name must be at least 3 characters")

    objective = input("Objective (Traffic / Conversions): ")
    if objective not in ["Traffic", "Conversions"]:
        raise ValueError("Objective must be Traffic or Conversions")

    ad_text = input("Ad text (max 100 chars): ")
    if len(ad_text) > 100:
        raise ValueError("Ad text exceeds 100 characters")

    cta = input("CTA (e.g., Shop Now): ")
    if not cta:
        raise ValueError("CTA is required")

    return campaign_name, objective, ad_text, cta


# ================== Music Logic (Core Evaluation Area) ================== #
def handle_music_logic(objective, api):
    print("\n🎵 Music Selection")
    print("1. Use existing music ID")
    print("2. Upload custom music")
    print("3. No music")

    choice = input("Choose option (1/2/3): ")

    # Case A: Existing Music ID
    if choice == "1":
        music_id = input("Enter Music ID: ")
        if not api.validate_music(music_id):
            raise ValueError(
                "Music ID validation failed. Please try another ID or upload music."
            )
        return music_id

    # Case B: Custom Music Upload
    if choice == "2":
        print("Uploading custom music...")
        music_id = f"music_{uuid.uuid4().hex[:6]}"
        print(f"Generated Music ID: {music_id}")
        return music_id

    # Case C: No Music
    if choice == "3":
        if objective == "Conversions":
            raise ValueError(
                "No-music ads are not allowed for Conversion campaigns."
            )
        return None

    raise ValueError("Invalid music selection")


# ================== Main Agent ================== #
def run_agent():
    print("🤖 TikTok Ad Creation AI Agent")

    oauth = OAuthManager()
    api = TikTokAdsAPI()

    try:
        # OAuth Authentication
        token = oauth.authenticate()

        # Conversational input collection
        campaign_name, objective, ad_text, cta = collect_campaign_inputs()

        # Business rule enforcement for music
        music_id = handle_music_logic(objective, api)

        # Final structured ad payload
        payload = {
            "campaign_name": campaign_name,
            "objective": objective,
            "creative": {
                "text": ad_text,
                "cta": cta,
                "music_id": music_id
            }
        }

        print("\n📦 Final Ad Payload (Structured Output)")
        print(payload)

        # Submission attempt
        print("\n🚀 Submitting ad...")
        response = api.submit_ad(payload, token)

        if "error" in response:
            print(f"❌ Submission failed: {response['error']}")
            print("👉 Suggested action: Fix the issue and retry submission.")
        else:
            print(f"✅ Ad submitted successfully! Ad ID: {response['ad_id']}")

    except Exception as error:
        print(f"\n⚠️ Error handled gracefully: {error}")
        print("👉 Suggested action: Resolve the issue and restart the flow.")


if __name__ == "__main__":
    run_agent()
