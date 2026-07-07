import os
import stripe

env_path = "/Users/admin/.gemini/antigravity/scratch/tradewebs/.env"
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                key, val = line.strip().split("=", 1)
                os.environ[key] = val.strip('"').strip("'")

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

plinks = stripe.PaymentLink.list(limit=50)

print("--- Updating Main Retainer Payment Links via stripe.PaymentLink.modify ---")
for pl in plinks.data:
    if "dRm7sO1rA9x30TF4Xm6oo00" in pl.url or "5kQ00m3zIdNjgSD0H66oo01" in pl.url:
        try:
            stripe.PaymentLink.modify(
                pl.id,
                after_completion={
                    "type": "redirect",
                    "redirect": {"url": "https://tradewebs.co.uk/onboarding.html"}
                }
            )
            print(f"✅ Modified redirect for Payment Link: {pl.url} -> https://tradewebs.co.uk/onboarding.html")
        except Exception as e:
            print(f"⚠️ Could not modify link {pl.url}: {e}")

print("\n--- 📊 SUMMARY OF ALL ACTIVE STRIPE PAYMENT LINKS ---")
for pl in stripe.PaymentLink.list(limit=50).data:
    print(f"• ID: {pl.id} | URL: {pl.url}")
