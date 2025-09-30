import asyncio
import os
from pathlib import Path
from playwright.async_api import async_playwright
from backend.tasks.queue_runner import run_all_queues

async def run_backend(
    folder,
    width,
    height,
    fmt,
    concurrency,
    auth="auth/auth_pokecut.json",
    url="https://www.pokecut.com/tools/ai-image-extender",
    chrome=True,
    headless=False,
    output="output"
):
    if folder:
        images = [
            str(Path(folder) / f)
            for f in os.listdir(folder)
            if f.lower().endswith((".jpg", ".jpeg", ".png"))
        ]
    else:
        raise RuntimeError("Cần truyền folder!")

    if not images:
        raise RuntimeError("Không tìm thấy ảnh hợp lệ trong folder")

    pw = await async_playwright().start()

    class Args:
        pass

    args = Args()
    args.auth = auth
    args.url = url
    args.chrome = chrome
    args.headless = headless
    args.width = width
    args.height = height
    args.format = fmt
    args.output = output
    args.concurrency = concurrency

    await run_all_queues(pw, args, images)
    await pw.stop()
