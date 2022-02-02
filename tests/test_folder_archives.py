import pytest

from tests.conftest import path_folder, unarchive_get_content_folder
from ipfs_handler import IPFSHandler


def test_unarchived_folder():
    folder = IPFSHandler(path_folder, False)
    with open(f"{folder.file_path}/subfolder/test_file3.txt") as f:
        content = f.read()
    assert content == "acb\nacb1\nacb2"


def test_archive_folder_no_pwd():
    archive = IPFSHandler(path_folder, True, False)
    password = archive.password
    assert password is None
    assert unarchive_get_content_folder(archive.file_path, password) == "acb\nacb1\nacb2"


@pytest.mark.parametrize("as_archive, password_protect, password_length", [(True, True, 8), (True, True, 24)])
def test_archived_folder_pwd(as_archive, password_protect, password_length):
    archive = IPFSHandler(path_folder, as_archive, password_protect, password_length)
    password = archive.password
    assert len(password) == password_length
    assert password.isalnum() is True
    assert unarchive_get_content_folder(archive.file_path, password) == "acb\nacb1\nacb2"
