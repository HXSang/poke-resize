# backend/tasks/queue_runner.py
import os
import asyncio
from pathlib import Path
from backend.tasks.uploader import upload_image
from backend.tasks.extender import customize_and_extend
from backend.tasks.downloader import download_result


# ----- Hàm chia ảnh thành N queue -----
def split_into_queues(images, n):
    queues = [[] for _ in range(n)]
    for i, img in enumerate(sorted(images)):  # sort để ổn định
        queues[i % n].append(img)
    return queues


# ----- Xử lý 1 queue (1 browser) -----
async def run_queue(playwright, args, queue_images, browser_name: str):
    browser = await playwright.chromium.launch(
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

    ok, fail = 0, 0
    out_dir = Path(args.output)   

    for idx, img in enumerate(queue_images, start=1):
        page = await context.new_page()
        name = f"{browser_name}-Img{idx}"
        try:
            # 1. Upload
            await page.goto(args.url, wait_until="domcontentloaded", timeout=60000)
            await upload_image(page, img, name)

            # 2. Extend
            await customize_and_extend(page, args.width, args.height, name)

            # 3. Download
            await download_result(page, img, out_dir, args.format, name)

            ok += 1
        except Exception as e:
            print(f"[{name}]Lỗi: {e}")
            fail += 1
        finally:
            await page.close()

    await context.close()
    await browser.close()
    return ok, fail


# ----- Hàm tổng chạy nhiều queue -----
async def run_all_queues(playwright, args, images):
    n = max(1, min(10, args.concurrency))
    queues = split_into_queues(images, n)

    tasks = []
    for i, q in enumerate(queues, start=1):
        if q:
            tasks.append(run_queue(playwright, args, q, f"Browser-{i}"))

    results = await asyncio.gather(*tasks)
    total_ok = sum(ok for ok, _ in results)
    total_fail = sum(fail for _, fail in results)
    print(f"\nTổng kết: OK={total_ok}, FAIL={total_fail}, Tổng ảnh={len(images)}")
