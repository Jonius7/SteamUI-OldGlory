import asyncio
import pyppeteer
import urllib.request, json

def request_url():
    with urllib.request.urlopen("http://localhost:8080/json/version") as url:
        data = json.load(url)
        return data["webSocketDebuggerUrl"]

async def connect_via_socket():
    browser = await pyppeteer.connect(browserWSEndpoint=request_url())
    pages = await browser.pages()
    page = pages[-1]
    await page.evaluate("location.reload()")
   
async def main():
    await connect_via_socket()

asyncio.get_event_loop().run_until_complete(main())