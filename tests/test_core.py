import os
import shutil
import tempfile
from pathlib import Path

import project_init as projin


def test_create_folders():
    with tempfile.TemporaryDirectory() as temp_dir:
        # create a test dir
        cwd = Path.cwd()
        test_dir = Path(temp_dir)
        os.chdir(test_dir)

        # setup function
        asset_folders = projin.DEFAULT_FOLDERS_LIST
        projin.WORKING_DIR = test_dir
        projin.create_folders(asset_folders)
        dir_content = [item.name for item in test_dir.rglob("*")]

        assert sorted(asset_folders) == sorted(dir_content)

        # revert to original dir for cleanup
        os.chdir(cwd)

def test_format_content():
    raw_text = "    line1\n        line2\n  line3"
    formatted = projin.format_content(raw_text)
    assert formatted == "line1\nline2\nline3"

# def test_create_git_auto_creates_script_file():
#     with tempfile.TemporaryDirectory() as temp_dir:
#         scripts_dir = Path(temp_dir) / projin.SCRIPTS_FOLDER_NAME
#         scripts_dir.mkdir()

#         extension = ".sh"
#         content = "echo Hello"
#         os.chdir(temp_dir)

#         projin.create_git_auto(extension, content)
#         script_file = scripts_dir / f"git_auto{extension}"

#         assert script_file.exists()
#         with open(script_file) as f:
#             assert "echo Hello" in f.read()