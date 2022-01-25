import sys

sys.path.append("..")
from ipfs_handler import IPFSHandler

import pyminizip
from pathlib import Path


# TODO
# unarchive and read
def get_content_single_file(archive, archive_password):
    unzipped: Path = Path("./testing_files/test_file_unzipped.txt")

    pyminizip.uncompress(str(archive), archive_password, str(unzipped), 0)
    with open(unzipped) as f_func:
        content_func = f_func.read()
    return content_func


# TODO
# unarchive and read
def get_content_folder(archive, archive_password):
    unzipped: Path = Path("./testing_files/folder_unzipped")

    pyminizip.uncompress(str(archive), archive_password, str(unzipped), 0)
    with open(f"{unzipped}/subfolder/test_file3.txt") as f_func:
        content_func = f_func.read()
    return content_func


if __name__ == "__main__":
    path = Path("./testing_files/test_file.txt")
    path_folder = Path("./testing_files/folder")

    # Single file archive with password
    file_pwd_8 = IPFSHandler(path, True)
    file_path = file_pwd_8.file_path
    assert str(file_path) == "testing_files/test_file.zip"
    password = file_pwd_8.password
    assert len(password) == 8
    assert password.isalnum() is True
    print(get_content_single_file(file_path, password))
    assert get_content_single_file(file_path, password) == "abc\nabc2\nabc3"

    # Single file archive with custom length password
    file_pwd_28 = IPFSHandler(path, True, True, 28)
    file_path = file_pwd_28.file_path
    assert str(file_path) == "testing_files/test_file.zip"
    password = file_pwd_28.password
    assert len(password) == 28
    assert password.isalnum() is True
    assert get_content_single_file(file_path, password) == "abc\nabc2\nabc3"

    # Single file archive no password
    file_no_pwd_8 = IPFSHandler(path, True, False)
    file_path = file_no_pwd_8.file_path
    assert str(file_path) == "testing_files/test_file.zip"
    password = file_no_pwd_8.password
    assert password is None
    assert get_content_single_file(file_path, None) == "abc\nabc2\nabc3"

    # Single file no archive
    file = IPFSHandler(path, False)
    file_path = file.file_path
    assert str(file_path) == "testing_files/test_file.txt"
    with open(file_path) as f:
        content = f.read()
    assert content == "abc\nabc2\nabc3"

    # Folder with password
    folder_pwd = IPFSHandler(path_folder, True)
    folder_path = folder_pwd.file_path
    assert str(folder_path) == "testing_files/folder.zip"
    password = folder_pwd.password
    assert len(password) == 8
    assert password.isalnum() is True
    assert get_content_folder(folder_path, password) == "acb\nacb1\nacb2"

    # Folder no password
    folder_no_pwd = IPFSHandler(path_folder, True, False)
    folder_path = folder_no_pwd.file_path
    assert str(folder_path) == "testing_files/folder.zip"
    password = folder_no_pwd.password
    assert password is None
    assert get_content_folder(folder_path, None) == "acb\nacb1\nacb2"

    # Folder file no archive
    folder = IPFSHandler(path_folder, False)
    folder_path = folder.file_path
    assert str(folder_path) == "testing_files/folder"
    with open(f"{folder_path}/subfolder/test_file3.txt") as f:
        content = f.read()
    assert content == "acb\nacb1\nacb2"
