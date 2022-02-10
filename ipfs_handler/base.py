import ipfshttpclient2
import pyminizip
import secrets
import string
import typing as tp
import warnings

from .proto import IPFSProto
from os import path, walk
from pathlib import Path

warnings.filterwarnings("ignore")


def connect_close_ipfs_client(func):
    """
    Decorator for working with ipfshttpclient. Opens and closes connection to local node

    :param func: decorated IPFSHandler method to be executed with the opened connection

    :return: wrapper function with ipfshttpclient interaction commands
    """

    def wrapper(ref):
        """
        Open and close connection to local IPFS node over ipfshttpclient

        :param ref: Wrapped method first parameter (`self` for upload_file, `file_hash` for delete_file)

        :return: result of `func`
        """

        client_decorator: ipfshttpclient2.Client = ipfshttpclient2.connect()  # Connects to /dns/localhost/tcp/5001/http
        ipfs_interaction_result: tp.Any = func(ref, client_decorator)
        client_decorator.close()
        return ipfs_interaction_result

    return wrapper


class IPFSHandler(IPFSProto):
    def __init__(
            self,
            file_path: Path,
            as_archive: bool,
            password_protect: bool = True,
            password_length: int = 8,
    ):
        """
        Class for interacting with IPFS and `.zip` archives

        :param file_path: path to a target file/folder
        :param as_archive: whether archive file/folder or not
        :param password_protect: whether protect the archive with password or not
        :param password_length: if protected, set a password length. Password generally consists of small and capital
        latin letters and digits
        """

        if as_archive:
            self.file_path, self.password = self.create_archive(file_path, password_protect, password_length)
        else:
            self.file_path = file_path

    @connect_close_ipfs_client
    def upload_file(self, client: ipfshttpclient2.Client) -> tp.Tuple[str, str]:
        """
        Add file to local IPFS node

        :param client: ipfshttpclient ot interact with IPFS node

        :return tuple consisting of IPFS hash and gateway link to it
        """

        if self.file_path.is_dir():
            file_hash: str = client.add(str(self.file_path), recursive=True)[-1]["Hash"]
        else:
            file_hash: str = client.add(str(self.file_path), recursive=True)["Hash"]
        result: tp.Tuple[str, str] = (file_hash, f"http://127.0.0.1:8080/ipfs/{file_hash}")
        return result

    @staticmethod
    @connect_close_ipfs_client
    def delete_file(file_hash: str, client: ipfshttpclient2.Client) -> bool:
        """
        Unpin and remove file from local node. Warning! This method collects garbage: all unpinned items will be removed

        :param client: ipfshttpclient ot interact with IPFS node
        :param file_hash: IPFS file hash

        :return success flag
        """

        try:
            client.pin.rm(file_hash, recursive=True)  # unpins file
            client.repo.gc()  # collects garbage (i.e. deletes unpinned)
        except ipfshttpclient2.exceptions.ErrorResponse:
            return False

        return True

    @staticmethod
    def create_archive(
            file_path: Path, password_protect: bool = True, password_length: int = 8
    ) -> tp.Tuple[Path, tp.Optional[str]]:
        """
        Create an optionally password protected `.zip` file of a single file/folder.

        :param file_path: absolute or relative path to a file/folder to be archived
        :param password_protect: whether protect the archive with password or not
        :param password_length: if protected, set a password length. Password generally consists of small and capital
        latin letters and digits

        :return: tuple with a new archive path (absolute/relative depends on the way `filepath` was passed) and password
        (None if was not set to password protect)
        """

        if not file_path.exists():
            raise FileNotFoundError

        if file_path.is_dir():
            with Zipper() as zipper:
                archive, password = zipper.zip_folder(file_path, password_length if password_protect else None)
        else:
            with Zipper() as zipper:
                archive, password = zipper.zip_single_file(file_path, password_length if password_protect else None)

        result = (Path(archive), password)

        return result


class Zipper:

    def __enter__(self):
        return self

    def zip_single_file(self, file_path: Path, password_length: tp.Optional[int]) -> (str, tp.Optional[str]):
        """
        `.zip`-compress a single file with optional password protection.

        :param file_path: path to a file to be compressed.
        :param password_length: password length

        :return: new archive path (absolute/relative depends on the way `filepath` was passed) and password (None if was
        not set to password protect)
        """

        new_archive = f"{path.splitext(file_path)[0]}.zip"
        password = self.random_string(password_length)

        pyminizip.compress(str(file_path), None, new_archive, password, 9)

        return new_archive, password

    def zip_folder(self, folder_path: Path, password_length: tp.Optional[int]) -> (str, tp.Optional[str]):
        """
        `.zip`-compress a folder with optional password protection.

        :param folder_path: path to a folder to be compressed.
        :param password_length: password length

        :return: new archive path (absolute/relative depends on the way `filepath` was passed) and password (None if was
        not set to password protect)
        """

        new_archive = f"{path.splitext(folder_path)[0]}.zip"
        password = self.random_string(password_length)

        parent_folder = path.dirname(folder_path)
        absolute_path_list = []
        prefix_list = []

        contents = walk(folder_path)
        for root, subfolders, files in contents:
            for file_name in files:
                absolute_path = path.join(root, file_name)
                absolute_path_list.append(absolute_path)
                prefix = absolute_path.replace(f"{parent_folder}/", "").replace(file_name, "")
                prefix_list.append(prefix)

        pyminizip.compress_multiple(absolute_path_list, prefix_list, new_archive, password, 9)

        return new_archive, password

    @staticmethod
    def random_string(length: tp.Optional[int]) -> tp.Optional[str]:
        """
        create a random string of a specified length consisting of small and capital letters, digits

        :param length: string length

        :return: generated string or None if None was passed
        """

        if not length:
            return None

        alphabet = string.ascii_letters + string.digits
        password = "".join(secrets.choice(alphabet) for i in range(length))

        return password

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False
