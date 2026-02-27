import json
from pathlib import Path

APP_DIR = Path.home() / ".taskcli"
TASKS_FILE = APP_DIR / "tasks.json"

def ensure_file_exists():
    if not APP_DIR.exists():
        APP_DIR.mkdir()
    if not TASKS_FILE.exists():
        TASKS_FILE.write_text("[]")

def load_tasks():
    ensure_file_exists()
    try:
        with TASKS_FILE.open("r") as f:
            tasks = json.load(f)
            return tasks
    except json.JSONDecodeError:
        save_tasks([])
        return []
    
def save_tasks(tasks):
    ensure_file_exists()
    with TASKS_FILE.open("w") as f:
        json.dump(tasks, f)

