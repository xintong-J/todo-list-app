import os
import json
import pytest
from app import todo

# Use a temporary file for testing to avoid overwriting real tasks
TEST_FILE = "test_tasks.json"

@pytest.fixture(autouse=True)
def setup_teardown(monkeypatch):
    """Setup and teardown fixture to use a test file instead of tasks.json."""
    monkeypatch.setattr(todo, "TASKS_FILE", TEST_FILE)
    # Start each test with a clean file
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    yield
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


def test_load_tasks_empty_file():
    """Should return an empty list if file does not exist."""
    tasks = todo.load_tasks()
    assert tasks == []


def test_add_and_save_task():
    """Should save and load a task correctly."""
    tasks = []
    tasks.append({"title": "Write tests", "done": False})
    todo.save_tasks(tasks)

    loaded = todo.load_tasks()
    assert len(loaded) == 1
    assert loaded[0]["title"] == "Write tests"
    assert not loaded[0]["done"]


def test_complete_task(monkeypatch):
    """Should mark a task as complete."""
    tasks = [{"title": "Finish homework", "done": False}]
    todo.save_tasks(tasks)

    # Simulate user input: choose task 1
    monkeypatch.setattr("builtins.input", lambda _: "1")
    todo.complete_task(tasks)

    assert tasks[0]["done"] is True


def test_delete_task(monkeypatch):
    """Should delete a task by number."""
    tasks = [{"title": "Task A", "done": False}, {"title": "Task B", "done": False}]
    todo.save_tasks(tasks)

    # Simulate user input: delete first task
    monkeypatch.setattr("builtins.input", lambda _: "1")
    todo.delete_task(tasks)

    assert len(tasks) == 1
    assert tasks[0]["title"] == "Task B"


def test_add_task(monkeypatch):
    """Should add a new task."""
    tasks = []

    # Simulate user input
    monkeypatch.setattr("builtins.input", lambda _: "Learn pytest")
    todo.add_task(tasks)

    assert len(tasks) == 1
    assert tasks[0]["title"] == "Learn pytest"
    assert not tasks[0]["done"]
