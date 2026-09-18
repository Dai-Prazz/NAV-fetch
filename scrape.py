import time
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto("https://www.sharesansar.com/mutual-fund-navs", timeout=30000)
        page.wait_for_selector("table", timeout=10000)
        
        open_end_btn = page.query_selector("text='Open End'") or page.query_selector("a:has-text('Open End')")
        if open_end_btn:
            open_end_btn.click()
            time.sleep(2)
            
        html = page.content()
        browser.close()

        soup = BeautifulSoup(html, 'html.parser')
        ssis_link = soup.find('a', href=lambda h: h and '/company/ssis' in h) or soup.find(text=lambda t: t and 'SSIS' in t)
        if ssis_link:
            row = ssis_link.find_parent('tr')
            if row:
                nav_elem = row.find('a', {'criteria': 'DAILY'}) or row.find('a', {'class': 'priceVsNav'})
                if nav_elem and nav_elem.text.strip():
                    nav = float(nav_elem.text.strip())
                    # Write the extracted NAV number to nav.txt
                    with open("nav.txt", "w") as f:
                        f.write(str(nav))
                    print(f"Updated nav.txt with value: {nav}")

if __name__ == "__main__":
    main()
