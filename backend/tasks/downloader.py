from pathlib import Path

async def download_result(page, image_path: str, output_dir: Path, fmt: str, name: str) -> str:
    try:
        # 1. Nhấn Download HD
        download_hd_btn = page.get_by_text("Download HD", exact=True)
        await download_hd_btn.wait_for(state="visible", timeout=60000)
        await download_hd_btn.click()
        print(f"[{name}] Đã bấm 'Download HD'")
    except Exception as e:
        raise RuntimeError(f"[{name}] Không bấm được 'Download HD': {e}")

    try:
        # 2. Chọn định dạng (JPG / PNG)
        fmt = fmt.strip().lower()
        btn = page.get_by_role("button", name=fmt.upper())
        await btn.wait_for(state="visible", timeout=5000)
        await btn.click()
        print(f"[{name}] Đã chọn định dạng {fmt.upper()}")
    except Exception as e:
        raise RuntimeError(f"[{name}] Không chọn được định dạng {fmt.upper()}: {e}")

    try:
        # 3. Nhấn Download cuối cùng và bắt sự kiện tải về
        final_download_btn = page.get_by_text("Download", exact=True)
        await final_download_btn.wait_for(state="visible", timeout=60000)
        async with page.expect_download() as dlinfo:
            await final_download_btn.click()
        download = await dlinfo.value

        # 4. Giữ nguyên tên file gốc (chỉ đổi đuôi theo fmt)
        base_name = Path(image_path).stem
        save_name = f"{base_name}.{fmt}"

        output_dir.mkdir(parents=True, exist_ok=True)
        save_path = output_dir / save_name
        await download.save_as(str(save_path))

        print(f"[{name}] Đã tải file về: {save_path}")
        return str(save_path)

    except Exception as e:
        raise RuntimeError(f"[{name}] Không tải được file: {e}")
