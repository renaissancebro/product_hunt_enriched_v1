from playwright.sync_api import sync_playwright

def scrape_category_page(link):
    print("Scraping categories")
    products = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(link)
        page.wait_for_selector('#product-feed')

        print("Page title:", page.title())

        # === Click "See more products" button repeatedly ===
        prev_count = 0
        max_clicks = 10

        for i in range(max_clicks):
            product_links = page.locator('#product-feed a h3')
            curr_count = product_links.count()

            if curr_count == prev_count:
                print("No new products loaded — stopping scroll.")
                break

            see_more_button = page.locator('button:has-text("See more products"), button:has-text("See more listings")')
            if see_more_button.count() > 0:
                print(f"Clicking 'See more products' button... ({i + 1})")
                see_more_button.first.click()
                page.wait_for_timeout(2000)  # wait for loading
            else:
                print("No 'See more products' button found — stopping.")
                break

            prev_count = curr_count

        # === After all clicks, get final count ===
        product_links = page.locator('#product-feed a h3')
        count = product_links.count()
        print(f"Final product count: {count}")

        # === Loop over all products ===
        for i in range(count):
            try:
                name = product_links.nth(i).inner_text().strip()
                parent_a = product_links.nth(i).locator('..')
                href = parent_a.get_attribute('href')
                if href and not href.startswith('http'):
                    href = "https://www.producthunt.com" + href

                full_text = parent_a.inner_text().strip()
                description = full_text.replace(name, '').strip('—').strip()

                products.append({
                    'name': name,
                    'url': href,
                    'description': description,
                    'twitter': 'Twitter TBD'
                })

                print(f"Collected: {name} → {href} → {description}")

            except Exception as e:
                print(f"Error processing item {i}: {e}")

        browser.close()
    return products