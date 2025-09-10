import asyncio
from playwright.async_api import async_playwright

async def main():
    pw = await async_playwright().start()
    browser = await pw.chromium.launch(channel="chrome", headless=False)
    
    context = await browser.new_context(
        storage_state="auth_pokecut.json",
        locale="vi-VN",
        timezone_id="Asia/Ho_Chi_Minh",
        viewport={"width": 1366, "height": 900}
    )

    page = await context.new_page()
    await page.goto("https://www.pokecut.com/vi", wait_until="domcontentloaded")

    if "/log-in" in page.url:
        print("[!] Session hết hạn hoặc chưa đăng nhập.")
    else:
        print(f"[✔] Đã vào Pokecut: {page.url}")

    input("\\n>>> Nhấn ENTER để thoát…")
    await browser.close()
    await pw.stop()

if __name__ == "__main__":
    asyncio.run(main())
