import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def main():
    url = "https://www.siddharthacapital.com/"
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # Go to Siddhartha Capital homepage
        page.goto(url, wait_until="domcontentloaded", timeout=30000)
        
        # Wait until the current-nav container loads on the page
        page.wait_for_selector(".current-nav", timeout=15000)
        
        html = page.content()
        browser.close()

    soup = BeautifulSoup(html, 'html.parser')
    
    # Locate the element with class 'current-nav-value'
    nav_elem = soup.select_one(".current-nav-value")
    
    if nav_elem and nav_elem.text.strip():
        try:
            nav = float(nav_elem.text.strip())
            
            # Save the NAV value to nav.txt
            with open("nav.txt", "w") as f:
                f.write(str(nav))
                
            print(f"Successfully extracted SSIS Daily NAV: {nav}")
        except ValueError:
            print(f"Could not parse NAV text to float: '{nav_elem.text.strip()}'")
    else:
        print("Could not find '.current-nav-value' on the page.")

if __name__ == "__main__":
    main()
