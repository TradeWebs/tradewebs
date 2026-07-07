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

# 1. Get the price ID for Google Business Profile Setup (£49)
prices = stripe.Price.list(limit=50, expand=["data.product"])
gbp_price_id = None
for p in prices.data:
    prod_name = p.product.name if hasattr(p.product, 'name') else stripe.Product.retrieve(p.product).name
    if "Google Business Profile Setup" in prod_name:
        gbp_price_id = p.id
        break

print(f"🎯 GBP Setup Price ID: {gbp_price_id}")

if gbp_price_id:
    # Try adding as cross-sell to Monthly Payment Link
    monthly_pl_id = "plink_1TqXTdV05D9PyWSAKxPLwT7Y"
    try:
        updated = stripe.PaymentLink.modify(
            monthly_pl_id,
            after_completion={
                "type": "redirect",
                "redirect": {"url": "https://tradewebs.co.uk/onboarding.html"}
            },
            # Let's check if cross_sells or restrictions work
            # In Stripe API, cross_sells is a list of dictionaries with price
        )
        # Let's try adding cross_sells
        print("Trying to add cross_sell via modify...")
        stripe.PaymentLink.modify(
            monthly_pl_id,
            # Let's see if cross_sells parameter is accepted
        )
    except Exception as e:
        print(f"⚠️ Error: {e}")
