# python-cli

A command-line task manager written in Python.

## Overview

`taskcli` is a simple CLI application for managing todo tasks from the terminal. Tasks can be added, listed, updated, completed, removed, and exported to CSV.

The application stores task data locally and supports filtering by status and tag.

## Features

- Add tasks
- List tasks
- Mark tasks as completed
- Update task titles
- Remove tasks
- Filter by status or tag
- Export tasks to CSV
- Priority levels and tagging

## Requirements

- Python 3

## Installation

Install the package locally:

```bash
pip install .
```

## Usage

Run the CLI with:

```bash
taskcli [COMMAND]
```

You can also view help information:

```bash
taskcli --help
```

## Commands

### Add a task

```bash
taskcli add "Finish documentation"
```

Optional fields:

```bash
taskcli add "Fix bug" --priority high --tag work
```

Priority options:
- low
- normal
- high

### List tasks

```bash
taskcli list
```

Filter by status:

```bash
taskcli list --status completed
```

Filter by tag:

```bash
taskcli list --tag work
```

### Complete a task

```bash
taskcli complete 1
```

### Update a task

```bash
taskcli update 1 "Updated task title"
```

### Remove a task

```bash
taskcli remove 1
```

Running remove without an index prompts to clear the full list.

### Export tasks to CSV

```bash
taskcli --export tasks.csv
```

## Project Structure

```text
taskcli/
  __init__.py
  main.py
  storage.py

taskcli.egg-info/
README.md
pyproject.toml
```

## Notes

- Tasks are stored locally using the project storage module.
- Completed tasks include timestamps.
- Task listing output is formatted as a table in the terminal.
