import pytest

from ipfs_handler import IPFSHandler
from tests.conftest import path_file, path_folder, unarchive_get_content_single_file, unarchive_get_content_folder

import ipfshttpclient2


@pytest.mark.parametrize(
    "is_folder, path, expected_hash, expected_content",
    [
        (False, path_file, "Qma3LUfthidHTfGjv8kJF8eYLMW3wdWqus3EHBrCtw4fmX", "abc\nabc2\nabc3"),
        (True, path_folder, "QmbYVSjYEF5x466Uuoc3Gfs7ge2rqWAV8T98ByjZsaUkwg", "acb\nacb1\nacb2"),
    ],
)
def test_upload_file_folder(is_folder, path, expected_hash, expected_content):

    """That case hash remains the same each time for unprotected file"""

    file_folder = IPFSHandler(path, False)
    file_folder_hash, gateway = file_folder.upload_file()
    assert gateway == f"http://127.0.0.1:8080/ipfs/{expected_hash}"
    client = ipfshttpclient2.connect()
    client.get(file_folder_hash, "./tests/testing_files")
    client.close()
    if is_folder:
        with open(f"./tests/testing_files/{file_folder_hash}/subfolder/test_file3.txt") as f:
            content = f.read()
        assert content == expected_content
    else:
        with open(f"./tests/testing_files/{file_folder_hash}") as f:
            content = f.read()
        assert content == expected_content


@pytest.mark.parametrize(
    "is_folder, path, expected_hash, expected_content",
    [
        (False, path_file, "QmUphraLMyE7eJomLMiHdiWAAny1jhxW816UpGM2uTmpRA", "abc\nabc2\nabc3"),
        (True, path_folder, "QmfTJu84gjsFCYeUADaQyimsqA3yypTgtTq8TC7NLF8bxT", "acb\nacb1\nacb2"),
    ],
)
def test_upload_file_folder_archive_no_pwd(is_folder, path, expected_hash, expected_content):

    """That case hash remains the same each time for unprotected archive"""

    archive = IPFSHandler(path, True, False)
    archive_hash, gateway = archive.upload_file()
    assert gateway == f"http://127.0.0.1:8080/ipfs/{expected_hash}"
    client = ipfshttpclient2.connect()
    client.get(archive_hash, "./tests/testing_files")
    client.close()
    if is_folder:
        assert unarchive_get_content_folder(f"./tests/testing_files/{archive_hash}", None) == expected_content
    else:
        assert unarchive_get_content_single_file(f"./tests/testing_files/{archive_hash}", None) == expected_content


@pytest.mark.parametrize(
    "is_folder, path, expected_content", [(False, path_file, "abc\nabc2\nabc3"), (True, path_folder, "acb\nacb1\nacb2")]
)
def test_upload_file_folder_archive_pwd(is_folder, path, expected_content):

    """That case hash changes each time because of password"""

    archive = IPFSHandler(path, True, True)
    password = archive.password
    archive_hash, gateway = archive.upload_file()
    assert archive_hash.startswith("Qm")
    client = ipfshttpclient2.connect()
    client.get(archive_hash, "./tests/testing_files")
    client.close()
    if is_folder:
        assert unarchive_get_content_folder(f"./tests/testing_files/{archive_hash}", password) == expected_content
    else:
        assert unarchive_get_content_single_file(f"./tests/testing_files/{archive_hash}", password) == expected_content


@pytest.mark.parametrize(
    "some_hash",
    [
        "QmUphraLMyE7eJomLMiHdiWAAny1jhxW816UpGM2uTmpRA",
        "QmfTJu84gjsFCYeUADaQyimsqA3yypTgtTq8TC7NLF8bxT",
        "QmbYVSjYEF5x466Uuoc3Gfs7ge2rqWAV8T98ByjZsaUkwg",
        "Qma3LUfthidHTfGjv8kJF8eYLMW3wdWqus3EHBrCtw4fmX",
    ],
)
def test_unpin(some_hash):

    """Unpin and remove file from local IPFS node. Folder file no password"""

    assert IPFSHandler.delete_file(some_hash) is True
    client = ipfshttpclient2.connect()
    assert hash not in client.pin.ls(type="all")["Keys"].keys()
    client.close()
