import os
import pyminizip
import shutil
import warnings

from pathlib import Path

warnings.filterwarnings("ignore")

path_file = Path("./tests/testing_files/test_file.txt")
path_folder = Path("./tests/testing_files/folder")


def unarchive_get_content_single_file(archive, archive_password):
    pyminizip.uncompress(str(archive), archive_password, None, 0)
    # pyminizip somehow unpacks content in a executing script folder only
    unzipped = Path("./tests/testing_files/test_file_unzipped.txt")
    shutil.move("./test_file.txt", unzipped)

    with open(unzipped) as f_func:
        content_func = f_func.read()
    return content_func


def unarchive_get_content_folder(archive, archive_password):
    pyminizip.uncompress(str(archive), archive_password, None, 0)
    # pyminizip somehow unpacks content in a executing script folder only

    unzipped = Path("./tests/testing_files/folder_unzipped")
    if os.path.exists(unzipped):
        shutil.rmtree(unzipped)
    shutil.move("./folder", unzipped)

    with open(f"{unzipped}/subfolder/test_file3.txt") as f_func:
        content_func = f_func.read()
    return content_func
