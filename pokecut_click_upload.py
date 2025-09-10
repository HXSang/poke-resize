# pokecut_click_upload.py
from typing import Optional
from playwright.async_api import Page

# Selector đa ngôn ngữ/biến thể
UPLOAD_BTN = (
    "button:has-text('Tải lên hình ảnh'), "
    "button:has-text('Tải lên ảnh'), "
    "button:has-text('Upload Image'), "
    "button:has-text('Upload image')"
)
FILE_INPUT = "input[type='file']"

async def click_pokecut_upload(page: Page, image_path: Optional[str] = None) -> bool:
    try:
        btn = await page.wait_for_selector(UPLOAD_BTN, timeout=30_000)
    except Exception:
        # Fallback: tìm theo text rồi leo lên ancestor là button/container có thể click
        dz = page.locator(
            "xpath=//*[contains(., 'Tải lên hình ảnh') or contains(., 'Upload Image')]"
            "/ancestor::*[self::button or contains(@class,'upload') or contains(@class,'drop')][1]"
        )
        if await dz.count() == 0:
            return False
        await dz.first.scroll_into_view_if_needed()
        await dz.first.click()
    else:
        await btn.scroll_into_view_if_needed()
        await btn.click()

    # Nếu có truyền file -> thử gán vào input
    if image_path:
        try:
            fi = await page.wait_for_selector(FILE_INPUT, timeout=5_000)
            await fi.set_input_files(image_path)
            print(f"[✔] Đã gán file vào input: {image_path}")
        except Exception:
            # Không có input file (do mở file picker native) -> bỏ qua
            print("[i] Không tìm thấy input[type=file]; trang có thể dùng file picker hệ điều hành.")
    return True


# --- CLI optional (test riêng file này) ---
if __name__ == "__main__":
    import asyncio, argparse, pathlib
    from use_pokecut_auth import open_pokecut

    ap = argparse.ArgumentParser("Click nút 'Tải lên hình ảnh' trên Pokecut")
    ap.add_argument("--auth", default="auth_pokecut.json")
    ap.add_argument("--url", default="https://pokecut.com/vi")
    ap.add_argument("--chrome", action="store_true")
    ap.add_argument("--headless", action="store_true")
    ap.add_argument("--image", help="Đường dẫn ảnh để gán vào input nếu có")
    ap.add_argument("--keep-open", action="store_true")
    args = ap.parse_args()

    async def _run():
        pw, browser, page = await open_pokecut(
            auth=args.auth, url=args.url,
            chrome=args.chrome, headless=args.headless
        )
        try:
            ok = await click_pokecut_upload(page, image_path=args.image)
            print("[result] click_upload =", ok)
            if args.keep_open:
                input("\n>>> Nhấn ENTER để đóng… ")
        finally:
            await browser.close()
            await pw.stop()

    asyncio.run(_run())
