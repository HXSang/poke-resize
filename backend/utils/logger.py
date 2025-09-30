import sys
from datetime import datetime

def log_info(msg: str, prefix: str = ""):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] [INFO] {prefix} {msg}", file=sys.stdout)

def log_error(msg: str, prefix: str = ""):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] [ERROR] {prefix} {msg}", file=sys.stderr)

def log_success(msg: str, prefix: str = ""):
    now = datetime.now().strftime("%H:%M:%S")
    print(f"[{now}] [OK] {prefix} {msg}", file=sys.stdout)
