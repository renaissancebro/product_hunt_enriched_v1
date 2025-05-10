import csv
from playwright.sync_api import sync_playwright
from scrape_categories import scrape_category_page
from enrich_data import enrich_products



def clean_products(products):
    cleaned_products = []
    seen_urls = set()
    for product in products:
        url = product['url']
        name = product['name']
        if "/products/" not in url:
            continue
        if "/shoutouts" in url or "#" in url:
            continue
        if name == "No name":
            continue
        if url in seen_urls:
            continue
        seen_urls.add(url)
        cleaned_products.append(product)
    print(f"✅ Cleaned product count: {len(cleaned_products)} (from raw {len(products)})")
    return cleaned_products



def save_to_csv(products, filename='products.csv'):
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['name', 'url', 'description', 'twitter', 'website']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(products)
    print(f"Saved {len(products)} products to {filename}")

# === MAIN RUNNER ===
print("Main is RUNNING")
if __name__ == "__main__":
    category_url = "https://www.producthunt.com/categories/ai-chatbots"
    products = scrape_category_page(category_url)
    cleaned_products = clean_products(products)
    enrich_products(cleaned_products)
    save_to_csv(cleaned_products)
