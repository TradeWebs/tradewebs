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

pl = stripe.PaymentLink.retrieve("plink_1TqXTdV05D9PyWSAKxPLwT7Y")
print("--- Payment Link Attributes ---")
for k, v in pl.to_dict().items():
    print(f"{k}: {v}")
