import os
import stripe

# Load environment variables from .env
env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            if "=" in line and not line.strip().startswith("#"):
                key, val = line.strip().split("=", 1)
                os.environ[key] = val.strip('"').strip("'")

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

if not stripe.api_key:
    print("❌ Error: STRIPE_SECRET_KEY not found.")
    exit(1)

print("🔍 Inspecting Stripe Account & Configuring Payment Links...\n")

# 1. Get all prices & products
prices = stripe.Price.list(limit=50, expand=["data.product"])
product_map = {}
for p in prices.data:
    if isinstance(p.product, dict) or hasattr(p.product, 'name'):
        prod_name = p.product.name
    else:
        prod = stripe.Product.retrieve(p.product)
        prod_name = prod.name
    product_map[prod_name] = {"price_id": p.id, "amount": p.unit_amount / 100, "currency": p.currency, "recurring": p.recurring}

# 2. Get existing payment links
plinks = stripe.PaymentLink.list(limit=50)
plink_url_map = {}
for pl in plinks.data:
    plink_url_map[pl.url] = pl.id

print("--- 1. Updating Main Retainer Payment Links with Onboarding Redirect ---")
main_links_updated = 0
for pl in plinks.data:
    # If this is our Monthly or Annual link
    try:
        updated = stripe.PaymentLink.update(
            pl.id,
            after_completion={
                "type": "redirect",
                "redirect": {"url": "https://tradewebs.co.uk/onboarding.html"}
            }
        )
        print(f"✅ Updated redirect for Payment Link: {pl.url} -> https://tradewebs.co.uk/onboarding.html")
        main_links_updated += 1
    except Exception as e:
        print(f"⚠️ Could not update link {pl.url}: {e}")

print("\n--- 2. Creating 1-Click WhatsApp Payment Links for Add-Ons ---")
addon_names = [
    "Google Business Profile Setup",
    "GBP Monthly Management",
    "Extra Custom Page",
    "Google Workspace Professional Email"
]

addon_links = {}

for name in addon_names:
    if name in product_map:
        price_info = product_map[name]
        price_id = price_info["price_id"]
        
        # Check if payment link already exists for this price
        existing_url = None
        for pl in plinks.data:
            line_items = stripe.PaymentLink.list_line_items(pl.id)
            for item in line_items.data:
                if item.price.id == price_id:
                    existing_url = pl.url
                    break
            if existing_url:
                break
        
        if existing_url:
            addon_links[name] = existing_url
            print(f"🔗 Existing link found for '{name}': {existing_url}")
        else:
            try:
                new_pl = stripe.PaymentLink.create(
                    line_items=[{"price": price_id, "quantity": 1}],
                    after_completion={
                        "type": "redirect",
                        "redirect": {"url": "https://tradewebs.co.uk/onboarding.html"}
                    }
                )
                addon_links[name] = new_pl.url
                print(f"✨ Created NEW 1-Click Payment Link for '{name}': {new_pl.url}")
            except Exception as e:
                print(f"❌ Failed to create link for '{name}': {e}")
    else:
        print(f"⚠️ Product '{name}' not found in Stripe catalogue.")

print("\n--- 📊 SUMMARY OF YOUR 1-CLICK ADD-ON CHECKOUT LINKS ---")
for name, url in addon_links.items:
    print(f"• {name}: {url}")
