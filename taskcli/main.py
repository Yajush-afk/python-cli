import argparse
import sys
from taskcli.storage import load_tasks, save_tasks

def main():
    parser = argparse.ArgumentParser(
        prog="taskcli",
        description="task manager CLI"
    )
    subparser = parser.add_subparsers(
        dest="command"
    )
    add_parser = subparser.add_parser(
        "add",
        help="add a task"
    )
    add_parser.add_argument(
        "title",
        type=str,
        help="task title"
    )
    remove_parser = subparser.add_parser(
        "remove",
        help="remove a task"
    )
    remove_parser.add_argument("index", type=int, nargs="?", help="index of task to remove")
    subparser.add_parser("list", help="list all tasks")
    update_parser = subparser.add_parser("update", help="update a task")
    update_parser.add_argument("index", type=int, help="index of task to update")
    update_parser.add_argument("title", type=str, help="new title for the task")
    args = parser.parse_args()
    if args.command is None:
        print(f"""taskcli - A basic python-cli for todo lists.
        \nFunctionalities: 1. add, 2. list, 3. remove, 4. update
        \nUse -h, --help for more information.""")

        sys.exit(1)
    if args.command == "add":
        handle_add(args.title)
    elif args.command == "remove":
        handle_remove(args.index)
    elif args.command == "list":
        handle_list()
    elif args.command == "update":
        handle_update(args.index, args.title)

def handle_add(title):
    tasks = load_tasks()
    tasks.append(title)
    save_tasks(tasks)
    print(f"Task added: {title}")

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
    print(f"Task removed: {removed_task}")

def handle_list():
    tasks = load_tasks()
    if not tasks:
        print("nothing to list, create a task using 'taskcli add <task_name>'")
        return
    
    lines = [f"{i}. {task}" for i, task in enumerate(tasks, 1)]
    max_len = max(len(line) for line in lines)
    width = max_len + 2
    
    print("┌" + "─" * width + "┐")
    for line in lines:
        print(f"│ {line.ljust(max_len)} │")
    print("└" + "─" * width + "┘")

def handle_update(index, title):
    tasks = load_tasks()
    if index < 1 or index > len(tasks):
        print(f"Invalid task index: {index}, check using 'taskcli list'")
        sys.exit(1)
    tasks[index - 1] = title
    save_tasks(tasks)
    print(f"Task updated: {title}")

if __name__ == "__main__":
    main()