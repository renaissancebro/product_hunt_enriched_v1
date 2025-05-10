from playwright.sync_api import sync_playwright

def enrich_products(products):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        for product in products:
            try:
                page.goto(product['url'])
                page.wait_for_selector('main')
                twitter_el = page.locator('a[href*="twitter.com"]')
                twitter = twitter_el.first.get_attribute('href') if twitter_el.count() > 0 else "N/A"
                website_el = page.locator('a[data-test="website-link"]')
                website = website_el.first.get_attribute('href') if website_el.count() > 0 else "N/A"
                description_el = page.locator('meta[name="description"]')
                description = description_el.first.get_attribute('content') if description_el.count() > 0 else product['description']
                product['twitter'] = twitter
                product['website'] = website
                product['description'] = description
                print(f"Enriched: {product['name']} → Twitter: {twitter}, Website: {website}")
            except Exception as e:
                print(f"Failed to enrich {product['name']}: {e}")
        browser.close()