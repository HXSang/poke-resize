from pathlib import Path

async def upload_image(page, image_path: str, name: str) -> None:
    try:
        # Thử locator theo label trước
        file_input = page.locator("label:has-text('Upload Image') input[type='file']")
        await file_input.set_input_files(image_path)
        print(f"[{name}] Đã upload ảnh: {Path(image_path).name}")
    except Exception:
        try:
            # Fallback: tìm trực tiếp input[type=file]
            file_input = page.locator("//input[@type='file']")
            await file_input.set_input_files(image_path)
            print(f"[{name}] Đã upload ảnh: {Path(image_path).name}")
        except Exception as e:
            raise RuntimeError(f"[{name}] Không upload được ảnh: {e}")
