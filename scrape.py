import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def main():
    url = "https://www.siddharthacapital.com/"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        
        # Wait for the nav banners to load on screen
        page.wait_for_selector(".current-nav", timeout=15000)
        
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, 'html.parser')
    
    # 1. Find all current-nav containers on the page
    nav_containers = soup.find_all('div', class_='current-nav')
    
    ssis_nav = None
    
    # 2. Iterate through them to find the one dedicated to "SSIS Daily NAV"
    for container in nav_containers:
        title_elem = container.find(class_='current-nav-title')
        if title_elem and 'SSIS' in title_elem.text:
            value_elem = container.find(class_='current-nav-value')
            if value_elem and value_elem.text.strip():
                try:
                    ssis_nav = float(value_elem.text.strip())
                    break
                except ValueError:
                    pass

    # 3. Fallback: If containers weren't structured in divs, search text directly
    if ssis_nav is None:
        title_node = soup.find(text=lambda t: t and 'SSIS Daily NAV' in t)
        if title_node:
            parent = title_node.find_parent()
            value_elem = parent.find_next_sibling(class_='current-nav-value') or parent.find(class_='current-nav-value')
            if value_elem:
                try:
                    ssis_nav = float(value_elem.text.strip())
                except ValueError:
                    pass

    # Save output
    if ssis_nav is not None:
        with open("nav.txt", "w") as f:
            f.write(str(ssis_nav))
        print(f"Successfully extracted SSIS Daily NAV: {ssis_nav}")
    else:
        print("Could not locate SSIS Daily NAV on the page.")

if __name__ == "__main__":
    main()
