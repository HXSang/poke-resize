import asyncio, argparse, pathlib
from playwright.async_api import async_playwright

POKECUT_LOGIN = "https://www.pokecut.com/vi/log-in"
TARGET_USERNAME = "User2JW"   # <- đổi đúng tên bạn muốn “khóa”

async def see_correct_user(page) -> bool:
    # Tìm tên hiển thị ở header/nav (tùy UI Pokecut – bạn chỉnh selector nếu cần)
    try:
        if await page.get_by_text(TARGET_USERNAME, exact=True).is_visible():
            return True
    except:
        pass
    try:
        header = page.locator("header, nav, [class*='header'], [class*='navbar']")
        if await header.get_by_text(TARGET_USERNAME, exact=True).is_visible():
            return True
    except:
        pass
    return False

async def main():
    ap = argparse.ArgumentParser(description="Đăng nhập tay Pokecut và CHỈ lưu khi đúng username mong muốn.")
    ap.add_argument("--out", default="auth_pokecut.json", help="Đường dẫn lưu file auth")
    ap.add_argument("--chrome", action="store_true", help="Ưu tiên Chrome channel")
    ap.add_argument("--headless", action="store_true", help="Ẩn trình duyệt")
    ap.add_argument("--timeout", type=int, default=300, help="Thời gian tối đa chờ đăng nhập (giây)")
    args = ap.parse_args()

    out_path = pathlib.Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    pw = await async_playwright().start()
    try:
        browser = await pw.chromium.launch(channel="chrome" if args.chrome else None, headless=args.headless)
    except Exception as e:
        print(f"[!] Không mở được Chrome channel, fallback Chromium: {e}")
        browser = await pw.chromium.launch(headless=args.headless)

    ctx = await browser.new_context(
        accept_downloads=True,
        viewport={"width":1366, "height":900},
        locale="vi-VN",
        timezone_id="Asia/Ho_Chi_Minh",
    )
    page = await ctx.new_page()

    print(f"[i] Mở: {POKECUT_LOGIN}")
    await page.goto(POKECUT_LOGIN, wait_until="domcontentloaded")

    # Đóng cookie/hướng dẫn nếu có (best-effort)
    for t in ("Chấp nhận tất cả Cookie", "Bỏ qua", "Đóng", "Skip", "Got it"):
        try: await page.get_by_text(t, exact=True).click(timeout=800)
        except: pass

    print("[i] Hãy đăng nhập tay. Mình sẽ đợi rời /log-in và nhận diện đúng username…")

    # 1) Chờ rời trang /log-in (fail → báo và KHÔNG lưu)
    try:
        await page.wait_for_function("() => !location.pathname.includes('log-in')", timeout=args.timeout*1000)
    except:
        print("[!] Hết thời gian chờ, vẫn còn ở /log-in → KHÔNG lưu session (tránh lưu guest).")
        input("\n>>> Nhấn ENTER để đóng… ")
        await browser.close(); await pw.stop()
        return

    # 2) Chờ hiển thị đúng username mục tiêu (fail → KHÔNG lưu)
    try:
        ok = await page.wait_for_function(
            """(name) => !!document.body && document.body.innerText.includes(name)""",
            arg=TARGET_USERNAME, timeout=20_000
        )
    except:
        ok = False

    # Nếu check tổng quát chưa chắc ăn, thử selector cụ thể
    if not ok:
        ok = await see_correct_user(page)

    if not ok:
        print(f"[!] Không thấy username '{TARGET_USERNAME}' sau khi login → KHÔNG lưu (tránh sai user).")
        print("    • Hãy đảm bảo bạn đang ở đúng tài khoản, nếu sai hãy đăng xuất/switch account rồi chạy lại.")
        input("\n>>> Nhấn ENTER để đóng… ")
        await browser.close(); await pw.stop()
        return

    # 3) Đúng user rồi → LƯU
    await ctx.storage_state(path=str(out_path))
    print(f"[✔] Đã lưu session cho '{TARGET_USERNAME}' → {out_path}")

    input("\n>>> Kiểm tra lại UI, xong nhấn ENTER để đóng… ")
    await browser.close(); await pw.stop()

if __name__ == "__main__":
    asyncio.run(main())
