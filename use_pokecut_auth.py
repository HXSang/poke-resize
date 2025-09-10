import asyncio, argparse
from playwright.async_api import async_playwright

DEFAULT_URL = "https://www.pokecut.com/vi"

async def set_custom_size(page, width: int, height: int, lock_aspect: bool = False):
    # Dùng JS để set trực tiếp giá trị
    await page.evaluate(
        """([w,h,lock]) => {
            const inputs = document.querySelectorAll("div:has(p:textContent('Kích thước tùy chỉnh')) input[type=number]");
            if (inputs.length >= 2) {
                inputs[0].value = w;
                inputs[1].value = h;
                // Kích hoạt sự kiện input/change để trang nhận giá trị mới
                inputs[0].dispatchEvent(new Event('input', { bubbles: true }));
                inputs[1].dispatchEvent(new Event('input', { bubbles: true }));
                inputs[0].dispatchEvent(new Event('change', { bubbles: true }));
                inputs[1].dispatchEvent(new Event('change', { bubbles: true }));
            }
            if (lock) {
                const box = document.querySelector("#aspect-lock");
                if (box && !box.checked) {
                    box.click();
                }
            }
        }""",
        [width, height, lock_aspect]
    )

    # Sau khi set xong thì bấm nút OK
    await page.locator("button:has-text('OK')").click()

async def main():
    ap = argparse.ArgumentParser(description="Đăng nhập Pokecut, upload 1 ảnh và bấm 'đổi cỡ'.")
    ap.add_argument("--auth", default="auth/auth_pokecut.json")
    ap.add_argument("--url", default=DEFAULT_URL)
    ap.add_argument("--image", required=True, help="Ảnh cần upload")
    ap.add_argument("--chrome", action="store_true")
    ap.add_argument("--headless", action="store_true")
    args = ap.parse_args()

    pw = await async_playwright().start()
    browser = await pw.chromium.launch(
        channel="chrome" if args.chrome else None,
        headless=args.headless
    )

    context = await browser.new_context(
        storage_state=args.auth,
        accept_downloads=True,
        viewport={"width": 1366, "height": 900},
        locale="vi-VN",
        timezone_id="Asia/Ho_Chi_Minh",
    )
    page = await context.new_page()
    await page.goto(args.url, wait_until="domcontentloaded")

    # Kiểm tra đã đăng nhập chưa
    if "/log-in" in page.url:
        print("[!] Chưa đăng nhập hoặc session hết hạn.")
        await browser.close()
        await pw.stop()
        return
    print(f"[✔] Đã vào: {page.url}")

    # Chấp nhận cookie nếu có
    try:
        await page.get_by_text("Chấp nhận tất cả Cookie", exact=True).click()
        print("[✔] Đã bấm 'Chấp nhận tất cả Cookie'")
    except:
        print("[i] Không thấy nút cookie, bỏ qua")

    # Upload ảnh trực tiếp
    try:
        await page.set_input_files("input[type='file']", args.image)
        print(f"[✔] Đã chọn ảnh: {args.image}")
    except Exception as e:
        print(f"[!] Không upload được ảnh: {e}")
        await browser.close()
        await pw.stop()
        return

    # Bỏ qua hướng dẫn
    try:
        await page.locator("button.tour-btn--skip").click()
        print("[✔] Đã nhấn nút 'bỏ qua'")
    except:
        print("[i] Không thấy popup hướng dẫn, bỏ qua")

    # Bấm nút "Công cụ AI"
    try:
        await page.get_by_text("Công cụ AI", exact=True).click()
        print("[✔] Đã nhấn nút 'Công cụ AI'")
    except:
        print("[!] Không tìm thấy nút 'Công cụ AI'")
        
    try:
        await page.get_by_text("Mở Rộng Hình Ảnh AI", exact=True).click()
        print("[✔] Đã nhấn nút 'Mở Rộng Hình Ảnh AI'")
    except:
        print("[!] Không tìm thấy nút 'Mở Rộng Hình Ảnh AI'")

    try:
        await page.get_by_text("Customize", exact=True).click()
        print("[✔] Đã bấm nút 'Customize'")
    except:
        print("[!] Không tìm thấy nút 'Customize'")
        
    try:    
        w = int(input("Nhập chiều rộng: "))
        h = int(input("Nhập chiều cao: "))
        await set_custom_size(page, width=w, height=h, lock_aspect=False)
        print("[✔] Đã bấm nút 'OK'")
    except:
        print("[!] Lỗi khi thiết lập kích thước tuỳ chỉnh")

    input("\\n>>> Nhấn ENTER để thoát…")
    await browser.close()
    await pw.stop()

if __name__ == "__main__":
    asyncio.run(main())
