# flow_pokecut.py
import argparse, asyncio
from use_pokecut_auth import open_pokecut
from pokecut_click_upload import click_pokecut_upload

async def main():
    ap = argparse.ArgumentParser("Luồng Pokecut: mở site (auth) rồi click nút upload")
    ap.add_argument("--auth", default="auth_pokecut.json")
    ap.add_argument("--url", default="https://pokecut.com/vi")
    ap.add_argument("--chrome", action="store_true")
    ap.add_argument("--headless", action="store_true")
    ap.add_argument("--keep-open", action="store_true")
    ap.add_argument("--image", help="(tuỳ chọn) file ảnh để gán vào input[type=file] nếu có")
    args = ap.parse_args()

    pw, browser, page = await open_pokecut(
        auth=args.auth, url=args.url,
        chrome=args.chrome, headless=args.headless
    )
    try:
        ok = await click_pokecut_upload(page, image_path=args.image)
        if not ok:
            raise SystemExit("Không tìm thấy nút 'Tải lên hình ảnh'.")

        if args.keep_open:
            input("\n>>> Xong. Nhấn ENTER để đóng… ")
    finally:
        await browser.close()
        await pw.stop()

if __name__ == "__main__":
    asyncio.run(main())
