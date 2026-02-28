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
            migrated = []
            needs_migration = False
            for task in tasks:
                if isinstance(task, str):
                    needs_migration = True
                    migrated.append({
                        "title": task,
                        "status": "pending",
                        "priority": "normal",
                        "tag": "-",
                        "added_at": "Legacy",
                        "completed_at": "-"
                    })
                else:
                    if "priority" not in task or "tag" not in task:
                        needs_migration = True
                        task.setdefault("priority", "normal")
                        task.setdefault("tag", "-")
                    migrated.append(task)
            if needs_migration:
                save_tasks(migrated)
            return migrated
    except json.JSONDecodeError:
        save_tasks([])
        return []
    
def save_tasks(tasks):
    ensure_file_exists()
    with TASKS_FILE.open("w") as f:
        json.dump(tasks, f)

