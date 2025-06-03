"""Main app file. May be deployed as a package."""

import platform
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Tuple, NoReturn

# CONFIG------------------------------------------------------------------------
# will create the following files and folders based on running OS
# modify folder/files names and content here
SUPPORTED_OS = ("Windows", "Linux")
WORKING_DIR = Path.cwd()
PROJECT_ARTIFACTS: List[Path] = []
INITIALIZATION_TIME: datetime = datetime.now()
OPERATING_SYSTEM: str | None = None

# folders
DOCUMENTS_FOLDER_NAME = "docs"
MODULES_FOLDER_NAME = "src"
SCRIPTS_FOLDER_NAME = "scripts"
TESTS_FOLDER_NAME = "tests"
DATA_FOLDER_NAME = "data"
IMAGES_FOLDER_NAME = "images"

DEFAULT_FOLDERS_LIST = (
    DOCUMENTS_FOLDER_NAME,
    MODULES_FOLDER_NAME,
    SCRIPTS_FOLDER_NAME,
    TESTS_FOLDER_NAME,
    DATA_FOLDER_NAME,
    IMAGES_FOLDER_NAME,
)

# files
PRE_COMMIT_CONTENT = """
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.12
    hooks:
      - id: ruff
        args: [--fix]
        types: [python]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.16.0
    hooks:
      - id: mypy
        types: [python]
"""
MAKEFILE_CONTENT = """
.PHONY: all format hooks push

all: push

format: hooks
	pre-commit run --all-files

hooks:
	pre-commit install
	pre-commit autoupdate

push: format
ifndef m
	$(error Commit message not provided. Use 'make m="your message"')
endif
	git add .
	git commit -m "$(m)"
	git push
"""
APP = ""
AUTO_FILES ={
    ".pre-commit-config.yaml": PRE_COMMIT_CONTENT,
    "Makefile": MAKEFILE_CONTENT,
    "app.py": APP
}

# routing
GIT_AUTO_ROUTING = {
    "Linux": {
        "extension": ".sh",
        "content": """
            #!/bin/bash

            # add all changes
            git add .

            # commit (with default message if none provided)
            commit_message=${1:-"auto commit"}
            git commit -m "$commit_message"

            # push to remote
            git push
            """,
    },
    "Windows": {
        "extension": ".bat",
        "content": """
            @echo off
            REM add all changes
            git add .

            REM set commit message
            set commit_message=%*
            if "%commit_message%"=="" set commit_message=auto commit

            REM commit
            git commit -m "%commit_message%"

            REM push
            git push
        """,
    }
}

# dependencies
PACKAGES = {
    "package_manager": {
        "items": ["uv"],
        "command": ["pip", "install"],
    },
    "dependencies": {
        "items": ["ruff", "mypy", "pytest", "pre-commit"],
        "command": ["uv", "pip", "install"]
    },
    "precommit_hook": {
        "items": ["pre-commit"],
        "command": ["pre-commit", "install"]
    }
}

# LOGIC-------------------------------------------------------------------------
def create_folders(folders_list: tuple = DEFAULT_FOLDERS_LIST) -> None:
    """Create starting folders in the app directory."""
    for folder_name in folders_list:
        folder_path = WORKING_DIR / folder_name
        if not folder_path.exists():
            folder_path.mkdir(exist_ok=True)
            print(f"---Created: {folder_path}")
        else:
            print(f"---Already exists: {folder_path}")

def snapshot_initial_state() -> Tuple[datetime, List[Path]]:
    """Take a snapshot of the initial project (will be used to reverse changes)."""
    return datetime.now(), [path.resolve() for path in WORKING_DIR.iterdir()]

# # TODO: future feature
# def reverse_init() -> None:
#     """
#     Reverses initialization changes (addition of folders and files)
#     WARNING: this function should ONLY be used on project initialization as
#     it doesn't keep track of additional user changes done throughout the project lifespan.
#     """

#     user_input = input(
#         f"""
# --- This action will delete all content except the following items:

# {os.linesep.join([str(path) for path in PROJECT_ARTIFACTS])}

# Do you wish to continue? (y/n)
# """
#     )

#     # TODO: handle files in-use
#     if user_input == "y":
#         for item in WORKING_DIR.iterdir():
#             if item not in PROJECT_ARTIFACTS:
#                 # remove directory
#                 try:
#                     if item.is_dir():
#                         shutil.rmtree(item)
#                     else:
#                         item.unlink()
#                 except (FileNotFoundError, PermissionError, OSError) as e:
#                     print(f"Failed to delete {item}: {e}")
#     else:
#         print("---Deletion cancelled.")

def detect_os() -> str | NoReturn:
    """Return the string representation of the Operation System the app is running on."""
    os_name = platform.system()

    if os_name in SUPPORTED_OS:
        return os_name
    else:
        print("---OS not supported. Exiting.")
        sys.exit()

    return None

def make_gitauto_exec(script_path: str) -> None:
    """Make the git_auto.sh script executable on Linux"""

    subprocess.run(["chmod", "+x", f"{script_path}"], check=True)

def format_git_auto(text: str) -> str:
    """Remove leading spaces from a text."""
    formatted_text = "\n".join(line.lstrip() for line in text.strip().splitlines())
    return formatted_text

def create_git_auto(extension: str, content: str) -> None:
    """Creates a git_auto.ext script in the "scripts" folder."""

    filename = WORKING_DIR / SCRIPTS_FOLDER_NAME / f"git_auto{extension}"

    with open(filename, "w", encoding="utf-8") as git_auto_script:
        git_auto_script.write(format_git_auto(content))

    # make linux script executable
    if "sh" in extension:
        make_gitauto_exec(str(filename))

def write_auto_files(files: dict) -> None:
    """Create pre-commit and Makefile."""

    for fname, fcontent in files.items():
        with open(WORKING_DIR / fname, "w", encoding="utf-8") as f:
            f.write(fcontent.strip())

def install_dependencies() -> None:
    """Install components from ENV_CONTENT global."""

    for key in PACKAGES.keys():
        packages = PACKAGES[key]["items"]
        command = PACKAGES[key]["command"]
        
        for package in packages:
            # TODO: package installation and commands should be decoupled (precommit)
            if "precommit_hook" in key:
                package_command = command
            else:
                package_command = command + [package]

            try:
                subprocess.run(package_command, check=True)
            except subprocess.CalledProcessError as e:
                print(f"---Failed to install {package}. Check environment: {e}")


def main() -> None:
    """Wrap the workflow into CLI > Makefile > pre-commit"""

# RUN---------------------------------------------------------------------------
if __name__ == "__main__":
    INITIALIZATION_TIME, PROJECT_ARTIFACTS = snapshot_initial_state()
    OPERATING_SYSTEM = detect_os()
    # get get git auto script extension and content based on OS
    git_extension, git_content = (
        GIT_AUTO_ROUTING[OPERATING_SYSTEM]["extension"],
        GIT_AUTO_ROUTING[OPERATING_SYSTEM]["content"],
    )
    create_folders()
    create_git_auto(git_extension, git_content)
    write_auto_files(AUTO_FILES)
    install_dependencies()
