import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1000, "height": 200})
        
        # fig/docker_running.png: Terminal mock for docker compose up -d (v2 style)
        html = """
        <html><body style="margin:0; background:#1e1e1e; color:#d4d4d4; font-family:Consolas, monospace; padding:20px; font-size:16px;">
        <span style="color:#569cd6;">user@host:~/project$</span> docker compose up -d<br>
        [+] Running 2/2<br>
        <span style="color:#4ec9b0;"> &#10004; Network bai1_default </span> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Created &nbsp;&nbsp;&nbsp;&nbsp;0.1s<br>
        <span style="color:#4ec9b0;"> &#10004; Container qdrant_local_bai1 </span> Started &nbsp;&nbsp;&nbsp;&nbsp;0.1s<br>
        <span style="color:#569cd6;">user@host:~/project$</span>
        </body></html>
        """
        await page.set_content(html)
        os.makedirs("fig", exist_ok=True)
        await page.screenshot(path="fig/docker_running.png")
        print("Captured fig/docker_running.png")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
