import pytest

from tests.conftest import path_file, unarchive_get_content_single_file
from ipfs_handler import IPFSHandler


def test_unarchived_file():
    file = IPFSHandler(path_file, False)
    with open(file.file_path) as f:
        content = f.read()
    assert content == "abc\nabc2\nabc3"


def test_archive_file_no_pwd():
    archive = IPFSHandler(path_file, True, False)
    password = archive.password
    assert password is None
    assert unarchive_get_content_single_file(archive.file_path, password) == "abc\nabc2\nabc3"


@pytest.mark.parametrize("as_archive, password_protect, password_length",
                         [(True, True, 8), (True, True, 24)])
def test_archived_file_pwd(as_archive, password_protect, password_length):
    archive = IPFSHandler(path_file, as_archive, password_protect, password_length)
    password = archive.password
    assert len(password) == password_length
    assert password.isalnum() is True
    assert unarchive_get_content_single_file(archive.file_path, password) == "abc\nabc2\nabc3"
