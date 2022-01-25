import sys

sys.path.append("..")
from ipfs_handler import IPFSHandler

import pyminizip
from pathlib import Path


def get_content_single_file(archive, archive_password):
    unzipped: Path = Path("./testing_files/test_file_unzipped.txt")

    pyminizip.uncompress(str(archive), archive_password, str(unzipped), 0)
    with open(unzipped) as f_func:
        content_func = f_func.read()
    return content_func


def get_content_folder(archive, archive_password):
    unzipped: Path = Path("./testing_files/folder_unzipped")

    pyminizip.uncompress(str(archive), archive_password, str(unzipped), 0)
    with open(f"{unzipped}/subfolder/test_file3.txt") as f_func:
        content_func = f_func.read()
    return content_func


path = Path("./testing_files/test_file.txt")
path_folder = Path("./testing_files/folder")

# Single file archive with password
file_pwd_8 = IPFSHandler(path, True)
file_path = file_pwd_8.file_path
assert str(file_path) == "testing_files/test_file.zip"
password = file_pwd_8.password
assert len(password) == 8
assert password.isalnum() is True
# print(get_content_single_file(file_path, password))


# Single file archive with custom length password
file_pwd_28 = IPFSHandler(path, True, True, 28)
file_path = file_pwd_28.file_path
assert str(file_path) == "testing_files/test_file.zip"
password = file_pwd_28.password
assert len(password) == 28
assert password.isalnum() is True
# print(get_content_single_file(file_path, password))


# Single file archive no password
file_no_pwd_8 = IPFSHandler(path, True, False)
file_path = file_no_pwd_8.file_path
assert str(file_path) == "testing_files/test_file.zip"
password = file_no_pwd_8.password
assert password is None
# print(get_content_single_file(file_path, None))


# Single file no archive
file = IPFSHandler(path, False)
file_path = file.file_path
assert str(file_path) == "testing_files/test_file.txt"
with open(file_path) as f:
    content = f.read()
assert content == "abc\nabc2\nabc3"

# Folder with password
folder_pwd = IPFSHandler(path_folder, True)
file_path = folder_pwd.file_path
assert str(file_path) == "testing_files/folder.zip"
password = folder_pwd.password
assert len(password) == 8
assert password.isalnum() is True
# print(get_content_folder(file_path, password))


# Folder no password
folder_no_pwd = IPFSHandler(path_folder, True, False)
file_path = folder_no_pwd.file_path
assert str(file_path) == "testing_files/folder.zip"
password = folder_no_pwd.password
assert password is None

# Folder file no archive
folder = IPFSHandler(path_folder, False)
file_path = folder.file_path
assert str(file_path) == "testing_files/folder"
with open(f"{file_path}/subfolder/test_file3.txt") as f:
    content = f.read()
assert content == "acb\nacb1\nacb2"
