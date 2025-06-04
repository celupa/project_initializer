# Overview
Quick, dirty and customizable script to bootstrap a new project.

## Requirements
- An environment with Python ≥ 3.11
- Git initialized in the local project

## Usage
Download and place "project_init.py" in the root directory of your project and execute it. After the execution you can delete the file.
At the project root level, run the following commands to push to your Git repo with the pre-commit config:
- Linux (bash): "scripts/git_auto.sh" 
- Windows (cmd): "absolute path of git_auto.bat"

## Features
- Detects OS (Windows or Linux currently)
- Creates standard folders (docs, scripts...)
- Generates pre-filled config files:
  - git_auto.sh|bat depending on OS (automatically makes git_auto.sh executable on linux)
  - pre-commit-hook.yaml
  - Makefile (setup is left to the user's discretion)
- Installs dependencies and related installations:
  - [uv](https://github.com/astral-sh/uv)
  - [ruff](https://github.com/astral-sh/ruff)
  - [mypy](http://mypy-lang.org/)
  - [pytest](https://docs.pytest.org/)
  - [pre-commit](https://pre-commit.com/) (+ install)

 You can easily modify the config in "project_init.py" to your tastes (dependencies, git flow...).

## Example
![before and after](assets/before_after_projinit.png)