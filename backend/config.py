from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
AUTH_FILE = BASE_DIR / "auth" / "auth_pokecut.json"

DEFAULT_URL = "https://www.pokecut.com/tools/ai-image-extender"
MAX_CONCURRENCY = 5
DEFAULT_VIEWPORT = {"width": 1366, "height": 900}
