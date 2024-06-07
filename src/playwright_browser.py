import asyncio
import re
from playwright.sync_api import sync_playwright, Playwright, Page
from playwright.async_api import async_playwright, Playwright
import urllib.request, json
import requests
import time
import pyppeteer


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
        browser = playwright.chromium.launch(headless=True, slow_mo=00)
        page = browser.new_page()
        page.goto("http://localhost:8080")
        page.get_by_text('SharedJSContext').click()
        page.wait_for_url(re.compile("http:\/\/localhost:8080\/devtools\/inspector.html\?ws=localhost:8080\/devtools\/page\/.*"))
        page.wait_for_timeout(300)
        page.keyboard.press('F5',delay=0)
        page.wait_for_timeout(300)
        browser.close()

        
     
def request_url():
    with urllib.request.urlopen("http://localhost:8080/json/version") as url:
        data = json.load(url)
        return data["webSocketDebuggerUrl"]
    
def get_client_url():
    start1 = time.time()
    response = requests.get("http://localhost:8080/json")
    data = json.loads(response.text)
    start2 = time.time()
    print(start2 - start1)
    for i in data:
        if i["title"] == "SharedJSContext":
            end = time.time()
            print(end - start2)
            return i["devtoolsFrontendUrl"]


def connect_via_socket_pw():
    with sync_playwright() as playwright:
        #browser = playwright.chromium.connect("http://localhost:8080" + get_client_url())
        browser = playwright.chromium.connect_over_cdp(request_url())
        context = browser.contexts[0]
        page = context.pages[0]
        page.goto("http://localhost:8080")
        page.get_by_text('SharedJSContext').click()
        page.wait_for_url(re.compile("http:\/\/localhost:8080\/devtools\/inspector.html\?ws=localhost:8080\/devtools\/page\/.*"))
        page.wait_for_timeout(300)
        page.keyboard.press('F5',delay=0)
        page.wait_for_timeout(300)
        browser.close()

