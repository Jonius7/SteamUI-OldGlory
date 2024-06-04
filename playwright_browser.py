import asyncio
import re
from playwright.sync_api import sync_playwright, Playwright, Page
import urllib.request, json 


def run(playwright):
    chromium = playwright.chromium # or "firefox" or "webkit".
    browser = chromium.launch()
    page = browser.new_page()
    page.goto("http://localhost:8080/json/version")
    # other actions...
    browser.close()

#with sync_playwright() as playwright:
#    refresh(playwright)
  
  
def refresh():
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=False, slow_mo=00)
        page = browser.new_page()
        page.goto("http://localhost:8080")
        #page.screenshot(path="example.png")
        page.get_by_text('SharedJSContext').click()
        page.wait_for_url(re.compile("http:\/\/localhost:8080\/devtools\/inspector.html\?ws=localhost:8080\/devtools\/page\/.*"))
        #print("WAITED FINISHED")
        #page.locator("body").click()
        #page.reload()
        #page.evaluate("location.reload()")
        page.wait_for_timeout(300)
        page.keyboard.press('F5',delay=0)
        page.wait_for_timeout(300)
        #page.locator("body").wait_for()
        #page.wait_for_load_state()
        browser.close()

        
     
def request():
    with urllib.request.urlopen("http://localhost:8080/json/version") as url:
        data = json.load(url)
        print(data)
        print(data["webSocketDebuggerUrl"])
    
