import asyncio
import pyppeteer
import urllib.request, json

def request_url():
    with urllib.request.urlopen("http://localhost:8080/json/version") as url:
        data = json.load(url)
        return data["webSocketDebuggerUrl"]
    
async def get_sharedjscontext(pages):
    for page in pages:
        title = await page.title()
        if title == "SharedJSContext":
            return page

async def connect_via_socket():
    browser = await pyppeteer.connect(browserWSEndpoint=request_url(), defaultViewport=None)
    pages = await browser.pages()
    sharedjscontext = await get_sharedjscontext(pages)
    await sharedjscontext.reload()
   
async def main():
    await connect_via_socket()

asyncio.run(connect_via_socket())