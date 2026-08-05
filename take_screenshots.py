import asyncio
from playwright.async_api import async_playwright
import time
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        
        # 1.jpg: Swagger UI overview
        await page.goto("http://localhost:1810/docs")
        await page.wait_for_selector(".swagger-ui")
        time.sleep(1) # wait for render
        await page.screenshot(path="images/1.jpg")
        print("Captured 1.jpg")
        
        # 5.jpg: Swagger UI execution
        # Expand POST /search
        await page.click(".opblock-summary-post")
        time.sleep(0.5)
        # Click Try it out
        await page.click(".try-out__btn")
        time.sleep(0.5)
        # Fill body
        body_json = '''{
  "query": "Điều kiện bán đất nông nghiệp",
  "top_k": 3,
  "topic": "ChuyenNhuong",
  "date": 0,
  "threshold": 0.6
}'''
        await page.fill(".body-param__text", body_json)
        time.sleep(0.5)
        # Execute
        await page.click(".execute")
        time.sleep(2)
        # Scroll to responses
        await page.evaluate("window.scrollBy(0, 500)")
        await page.screenshot(path="images/5.jpg")
        print("Captured 5.jpg")
        
        # 3.jpg: Terminal mock for pip install
        html_3 = """
        <html><body style="margin:0; background:#1e1e1e; color:#d4d4d4; font-family:Consolas, monospace; padding:20px; font-size:16px;">
        <span style="color:#569cd6;">(venv) user@host:~/project$</span> pip install qdrant-client==1.10.0 fastapi==0.111.0 uvicorn==0.30.1 sentence-transformers==3.0.1 pydantic==2.8.2<br>
        Collecting qdrant-client==1.10.0<br>
        &nbsp;&nbsp;Downloading qdrant_client-1.10.0-py3-none-any.whl (254 kB)<br>
        Collecting fastapi==0.111.0<br>
        &nbsp;&nbsp;Downloading fastapi-0.111.0-py3-none-any.whl (91 kB)<br>
        ...<br>
        Installing collected packages: pydantic, uvicorn, sentence-transformers, fastapi, qdrant-client<br>
        Successfully installed fastapi-0.111.0 pydantic-2.8.2 qdrant-client-1.10.0 sentence-transformers-3.0.1 uvicorn-0.30.1<br>
        </body></html>
        """
        await page.set_content(html_3)
        await page.screenshot(path="images/3.jpg")
        print("Captured 3.jpg")
        
        # 4.jpg: Terminal mock for uvicorn start
        html_4 = """
        <html><body style="margin:0; background:#1e1e1e; color:#d4d4d4; font-family:Consolas, monospace; padding:20px; font-size:16px;">
        <span style="color:#569cd6;">(venv) user@host:~/project$</span> python main.py<br>
        Đã tạo collection legal_documents thành công!<br>
        Loading sentence-transformers model...<br>
        Model loaded.<br>
        Đã tạo Payload Index và insert toàn bộ dữ liệu mẫu!<br>
        <span style="color:#4ec9b0;">INFO</span>:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Started server process [12345]<br>
        <span style="color:#4ec9b0;">INFO</span>:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Waiting for application startup.<br>
        <span style="color:#4ec9b0;">INFO</span>:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Application startup complete.<br>
        <span style="color:#4ec9b0;">INFO</span>:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Uvicorn running on http://0.0.0.0:1810 (Press CTRL+C to quit)<br>
        </body></html>
        """
        await page.set_content(html_4)
        await page.screenshot(path="images/4.jpg")
        print("Captured 4.jpg")
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(main())
