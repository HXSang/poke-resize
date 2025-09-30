import asyncio
from backend.pokecut import run_backend

async def main():
    await run_backend(
        folder="input",
        width=1420,
        height=1080,
        fmt="png",
        concurrency=10,
        chrome=True,
        headless=True,
    )

if __name__ == "__main__":
    asyncio.run(main())
