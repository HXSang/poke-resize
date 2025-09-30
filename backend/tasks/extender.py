async def customize_and_extend(page, width: int, height: int, name: str) -> None:
    # 1. Nhấn Customize
    try:
        customize_btn = page.get_by_text("Customize", exact=True)
        await customize_btn.wait_for(state="visible", timeout=8000)
        await customize_btn.click()
        print(f"[{name}] Đã bấm 'Customize'")
    except Exception as e:
        raise RuntimeError(f"[{name}] Không bấm được 'Customize': {e}")

    # 2. Nhập width/height
    try:
        width_input = page.locator("input#width")
        height_input = page.locator("input#height")
        await width_input.fill(str(width))
        await height_input.fill(str(height))
        print(f"[{name}] Đã nhập kích thước: {width} x {height}")
    except Exception as e:
        raise RuntimeError(f"[{name}] Không nhập được kích thước: {e}")

    # 3. Nhấn OK
    try:
        ok_btn = page.get_by_text("OK", exact=True)
        await ok_btn.wait_for(state="visible", timeout=5000)
        await ok_btn.click()
        print(f"[{name}] Đã bấm 'OK'")
    except Exception as e:
        raise RuntimeError(f"[{name}] Không bấm được 'OK': {e}")

    # 4. Nhấn AI Extend
    try:
        ai_extend_btn = page.get_by_text("AI Extend", exact=True)
        await ai_extend_btn.wait_for(state="visible", timeout=15000)
        await ai_extend_btn.click()
        print(f"[{name}] Đã bấm 'AI Extend'")
    except Exception as e:
        raise RuntimeError(f"[{name}] Không bấm được 'AI Extend': {e}")
