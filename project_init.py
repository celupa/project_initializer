import os
import shutil
import platform
import subprocess
from pathlib import Path
from datetime import datetime
from typing import List, Tuple



# CONFIG------------------------------------------------------------------------
# will create the following files and folders based on running OS
# modify folder/files names and content here
SUPPORTED_OS = ("Windows", "Linux")
WORKING_DIR = Path.cwd()
PROJECT_ARTIFACTS = []
INITIALIZATION_TIME = None
OPERATING_SYSTEM = None

# folders
DOCUMENTS_FOLDER_NAME = "docs"
MODULES_FOLDER_NAME = "src"
SCRIPTS_FOLDER_NAME = "scripts"
TESTS_FOLDER_NAME = "tests"
DATA_FOLDER_NAME = "data"
IMAGES_FOLDER_NAME = "images"

DEFAULT_FOLDERS_LIST = [
    DOCUMENTS_FOLDER_NAME,
    MODULES_FOLDER_NAME,
    SCRIPTS_FOLDER_NAME,
    TESTS_FOLDER_NAME,
    DATA_FOLDER_NAME,
    IMAGES_FOLDER_NAME
]

# files


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
            """
    },
    "Windows": {
        "extension": ".bat",
        "content": """
            @echo off
            REM add all changes
            git add .

            REM set commit message
            set commit_message=%1
            if "%commit_message%"=="" set commit_message=auto commit

            REM commit
            git commit -m "%commit_message%"

            REM push
            git push
        """
    }
}

# LOGIC-------------------------------------------------------------------------
def create_folders(folders_list: list=DEFAULT_FOLDERS_LIST) -> None:
    for folder_name in folders_list:
        folder_path = WORKING_DIR / folder_name
        folder_path.mkdir(exist_ok=True)
        print(f"---Created: {folder_path}")

def snapshot_initial_state() -> Tuple[datetime, List[str]]:
    """Take a snapshot of the initial project (will be used to reverse changes)."""
    return datetime.now(), [path.resolve() for path in WORKING_DIR.iterdir()]

def reverse_init() -> None:
    """
    Reverses initialization changes (addition of folders and files)
    WARNING: this function should ONLY be used on project initialization as
    it doesn't keep track of additional user changes done throughout the project lifespan.
    """

    user_input = input(
f"""
--- This action will delete all content except the following items:

{os.linesep.join([str(path) for path in PROJECT_ARTIFACTS])}

Do you wish to continue? (y/n)
"""
)

    # TODO: handle files in-use
    if user_input == "y":
        for item in WORKING_DIR.iterdir():
            if item not in PROJECT_ARTIFACTS:
                # remove directory
                try:
                    if item.is_dir():
                        shutil.rmtree(item)
                    else:
                        item.unlink()
                except Exception as e:
                    print("Failed to delete {item}: {e}")
    else:
        print("---Deletion cancelled.")

def detect_os() -> str | None:
    os_name = platform.system()

    if os_name in SUPPORTED_OS:
        return os_name

    return None
    
def make_gitauto_exec(script_path: str) -> None:
    """Make the git_auto.sh script executable on Linux"""

    subprocess.run(["chmod", "+x", f"{script_path}"], check=True)
    
def create_git_auto(git_extension: str, git_content: str) -> None:
    """Creates a git_auto.ext script in the "scripts" folder."""
    # adding the newline arg for the special kid: Windows –
    # it automatically adds a "\r" to "\n", leading to duplicate newlines
    # reason? historical (carriage return). couldn't be bothered to investigate
    # Yes Bobby, you're daddy's 'special' little boy.
    filename = WORKING_DIR / SCRIPTS_FOLDER_NAME / f"git_auto{git_extension}"
    with open(filename, "w", newline="") as git_auto_script:
        git_auto_script.write(git_content)
    
    # make linux script executable
    if "sh" in git_extension:
        make_gitauto_exec(str(filename))

def format_content(text: str) -> str:
    """Remove leading spaces from a text."""
    formatted_text = os.linesep.join(line.lstrip() for line in text.strip().splitlines())
    return formatted_text

# RUN---------------------------------------------------------------------------
if __name__ == "__main__":
    INITIALIZATION_TIME, PROJECT_ARTIFACTS = snapshot_initial_state()
    OPERATING_SYSTEM = detect_os()
    # get get git auto script extension and content based on OS
    git_extension, git_content = (
        GIT_AUTO_ROUTING[OPERATING_SYSTEM]["extension"],
        format_content(GIT_AUTO_ROUTING[OPERATING_SYSTEM]["content"])
    )
    print(repr(git_content))
    print(git_content)
    create_folders()
    create_git_auto(git_extension, git_content)
    # reverse_init()
