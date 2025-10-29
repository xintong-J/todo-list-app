import json
import os
from importlib import resources

TASKS_FILE = resources.files("app.data").joinpath("tasks.json")


def load_tasks():
    """Load tasks from a JSON file, or return an empty list if not found."""
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)


def save_tasks(tasks):
    """Save the list of tasks to a JSON file."""
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=4)


def show_tasks(tasks):
    """Display all tasks with their status."""
    if not tasks:
        print("\n✅ No tasks found!")
        return
    print("\n📋 Your To-Do List:")
    for i, task in enumerate(tasks, start=1):
        status = "✅" if task["done"] else "❌"
        print(f"{i}. {status} {task['title']}")


def add_task(tasks):
    """Add a new task to the list."""
    title = input("Enter task name: ").strip()
    if title:
        tasks.append({"title": title, "done": False})
        save_tasks(tasks)
        print(f"✅ Task '{title}' added.")
    else:
        print("⚠️ Task name cannot be empty.")


def complete_task(tasks):
    """Mark a task as completed."""
    show_tasks(tasks)
    try:
        task_num = int(input("\nEnter the number of the task to mark complete: "))
        if 1 <= task_num <= len(tasks):
            tasks[task_num - 1]["done"] = True
            save_tasks(tasks)
            print(f"🎉 Task '{tasks[task_num - 1]['title']}' marked complete!")
        else:
            print("⚠️ Invalid task number.")
    except ValueError:
        print("⚠️ Please enter a valid number.")


def delete_task(tasks):
    """Delete a task by number."""
    show_tasks(tasks)
    try:
        task_num = int(input("\nEnter the number of the task to delete: "))
        if 1 <= task_num <= len(tasks):
            removed = tasks.pop(task_num - 1)
            save_tasks(tasks)
            print(f"🗑️ Task '{removed['title']}' deleted.")
        else:
            print("⚠️ Invalid task number.")
    except ValueError:
        print("⚠️ Please enter a valid number.")


def main():
    """Main program loop."""
    tasks = load_tasks()

    while True:
        print("\n==== To-Do List Menu ====")
        print("1. View tasks")
        print("2. Add a task")
        print("3. Mark task as complete")
        print("4. Delete a task")
        print("5. Exit")

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            show_tasks(tasks)
        elif choice == "2":
            add_task(tasks)
        elif choice == "3":
            complete_task(tasks)
        elif choice == "4":
            delete_task(tasks)
        elif choice == "5":
            print("👋 Goodbye!")
            break
        else:
            print("⚠️ Invalid option. Please try again.")


if __name__ == "__main__":
    main()
