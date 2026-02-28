import argparse
import csv
import datetime
import sys
from taskcli.storage import load_tasks, save_tasks

def main():
    parser = argparse.ArgumentParser(
        prog="taskcli",
        description="task manager CLI"
    )
    parser.add_argument("--export", type=str, metavar="FILE", help="export tasks to a csv file")
    subparser = parser.add_subparsers(
        dest="command"
    )
    add_parser = subparser.add_parser(
        "add",
        help="add a new task to your list"
    )
    add_parser.add_argument(
        "title",
        type=str,
        help="the title or description of the task"
    )
    add_parser.add_argument("--priority", type=str, choices=["low", "normal", "high"], default="normal", help="priority level (low, normal, high)")
    add_parser.add_argument("--tag", type=str, default="-", help="category or tag for the task (e.g. work, personal)")
    remove_parser = subparser.add_parser(
        "remove",
        help="remove a task from your list by its index"
    )
    remove_parser.add_argument("index", type=int, nargs="?", help="index of task to remove (leave empty to clear the entire list)")
    list_parser = subparser.add_parser("list", help="list tasks, optionally filtered by tag or status")
    list_parser.add_argument("--status", type=str, choices=["pending", "completed"], help="filter tasks by status")
    list_parser.add_argument("--tag", type=str, help="filter tasks by tag")
    complete_parser = subparser.add_parser("complete", help="mark a pending task as completed")
    complete_parser.add_argument("index", type=int, help="index of the task to complete")
    update_parser = subparser.add_parser("update", help="update the title of an existing task")
    update_parser.add_argument("index", type=int, help="index of the task to update")
    update_parser.add_argument("title", type=str, help="new title for the task")
    args = parser.parse_args()
    
    if args.export:
        handle_export(args.export)
        sys.exit(0)
        
    if args.command is None:
        print(f"""taskcli - A basic python-cli for todo lists.
        \nFunctionalities: 1. add, 2. list, 3. remove, 4. update, 5. complete
        \nUse -h, --help for more information.""")

        sys.exit(1)
    if args.command == "add":
        handle_add(args.title, args.priority, args.tag)
    elif args.command == "remove":
        handle_remove(args.index)
    elif args.command == "list":
        handle_list(args.status, args.tag)
    elif args.command == "update":
        handle_update(args.index, args.title)
    elif args.command == "complete":
        handle_complete(args.index)

def handle_add(title, priority, tag):
    tasks = load_tasks()
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tasks.append({
        "title": title,
        "status": "pending",
        "priority": priority,
        "tag": tag,
        "added_at": now,
        "completed_at": "-"
    })
    save_tasks(tasks)
    print(f"Task added: {title} (Priority: {priority}, Tag: {tag})")

def handle_remove(index):
    tasks = load_tasks()
    if index is None:
        try:
            choice = input("NOTE: taskcli remove {index} may remove the task you desire, remove command if run without any index CLEAR the list.\nDo you wish to proceed [y/N]: ")
        except KeyboardInterrupt:
            print("\nOperation cancelled.")
            sys.exit(0)
            
        if choice.strip().lower() == 'y':
            save_tasks([])
            print("List cleared.")
            return
        elif choice.strip().lower() == 'n':
            print("enter index with remove command, use taskcli list to check index number.")
            return
        else:
            print("Invalid choice, enter y or n.")
            handle_remove(None)
            return

    if index < 1 or index > len(tasks):
        print(f"Invalid task index: {index}, check using 'taskcli list'")
        sys.exit(1)
    removed_task = tasks.pop(index - 1)
    save_tasks(tasks)
    print(f"Task removed: {removed_task['title']}")

def handle_list(status_filter=None, tag_filter=None):
    tasks = load_tasks()
    if not tasks:
        print("nothing to list, create a task using 'taskcli add <task_name>'")
        return
        
    filtered_tasks = []
    for i, t in enumerate(tasks, 1):
        if status_filter and t.get("status", "pending") != status_filter:
            continue
        if tag_filter and t.get("tag", "-") != tag_filter:
            continue
        filtered_tasks.append((i, t))
        
    if not filtered_tasks:
        print("No tasks match the given filters.")
        return
    
    max_id = max(2, len(str(len(tasks))))
    max_title = max(5, max(len(t['title']) for _, t in filtered_tasks))
    max_tag = max(3, max(len(t.get('tag', '-')) for _, t in filtered_tasks))
    
    print(f"┌─{'─'*max_id}─┬─{'─'*max_title}─┬───────────┬──────────┬─{'─'*max_tag}─┬─────────────────────┬─────────────────────┐")
    print(f"│ {'ID'.ljust(max_id)} │ {'Title'.ljust(max_title)} │ Status    │ Priority │ {'Tag'.ljust(max_tag)} │ Added At            │ Completed At        │")
    print(f"├─{'─'*max_id}─┼─{'─'*max_title}─┼───────────┼──────────┼─{'─'*max_tag}─┼─────────────────────┼─────────────────────┤")
    for i, t in filtered_tasks:
        status = t.get("status", "pending")
        priority = t.get("priority", "normal")
        tag = t.get("tag", "-")
        added = t.get("added_at", "-")
        completed = t.get("completed_at", "-")
        print(f"│ {str(i).ljust(max_id)} │ {t['title'].ljust(max_title)} │ {status.ljust(9)} │ {priority.ljust(8)} │ {tag.ljust(max_tag)} │ {added.ljust(19)} │ {completed.ljust(19)} │")
    print(f"└─{'─'*max_id}─┴─{'─'*max_title}─┴───────────┴──────────┴─{'─'*max_tag}─┴─────────────────────┴─────────────────────┘")

def handle_update(index, title):
    tasks = load_tasks()
    if index < 1 or index > len(tasks):
        print(f"Invalid task index: {index}, check using 'taskcli list'")
        sys.exit(1)
    tasks[index - 1]["title"] = title
    save_tasks(tasks)
    print(f"Task updated: {title}")

def handle_complete(index):
    tasks = load_tasks()
    if index < 1 or index > len(tasks):
        print(f"Invalid task index: {index}, check using 'taskcli list'")
        sys.exit(1)
    if tasks[index - 1].get("status") == "completed":
        print(f"Task is already completed: {tasks[index - 1]['title']}")
        return
    tasks[index - 1]["status"] = "completed"
    tasks[index - 1]["completed_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    save_tasks(tasks)
    print(f"Task completed: {tasks[index - 1]['title']}")

def handle_export(filename):
    tasks = load_tasks()
    if not tasks:
        print("No tasks to export.")
        return
    
    try:
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            fieldnames = ["id", "title", "status", "priority", "tag", "added_at", "completed_at"]
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for i, t in enumerate(tasks, 1):
                row = {"id": i}
                row.update(t)
                writer.writerow(row)
        print(f"Tasks successfully exported to {filename}")
    except Exception as e:
        print(f"Failed to export tasks: {e}")

if __name__ == "__main__":
    main()