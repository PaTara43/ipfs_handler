import ipfshttpclient
import pyminizip
import random
import string
import typing as tp

from ipfs_proto import IPFSProto
from os import path, walk
from pathlib import Path


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
        :param as_archive: whether archive file/folder or nor
        :param password_protect: whether protect the archive with password or not
        :param password_length: if protected, set a password length. Password generally consists of small and capital
        latin letters and digits
        """

        if as_archive:
            self.file_path, self.password = self.create_archive(file_path, password_protect, password_length)
        else:
            self.file_path = file_path

    def upload_file(self) -> tp.Tuple[str, str]:
        """
        add file to local IPFS node

        :return tuple consisting of IPFS hash and gateway link to it
        """

        client: ipfshttpclient.Client = ipfshttpclient.connect()  # Connects to: /dns/localhost/tcp/5001/http
        file_hash: str = client.add(str(self.file_path), recursive=True)["Hash"]
        client.close()

        result: tp.Tuple[str, str] = (file_hash, f"http://127.0.0.1:8080/ipfs/{file_hash}")
        return result

    @staticmethod
    def delete_file(_hash: str, filepath: Path = None) -> bool:
        """
        Удаляем файл с локальной ноды
        :param _hash: хэш файла в ipfs
        :param filepath: путь к файлу на локальной машине (нужен ли он?
        Или можно по хэшу достать расположение на локальной ноде?)
        :return флаг статуса операции
        """

        client: ipfshttpclient.Client = ipfshttpclient.connect()  # Connects to: /dns/localhost/tcp/5001/http
        client

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
            archive, password = zip_folder(file_path, password_length if password_protect else None)
        else:
            archive, password = zip_single_file(file_path, password_length if password_protect else None)

        result = (Path(archive), password)

        return result


def zip_single_file(file_path: Path, password_length: tp.Optional[int]) -> (str, tp.Optional[str]):
    """
    `.zip`-compress a single file with optional password protection.

    :param file_path: path to a file to be compressed.
    :param password_length: password length

    :return: new archive path (absolute/relative depends on the way `filepath` was passed) and password (None if was not
    set to password protect)
    """

    new_archive = f"{path.splitext(file_path)[0]}.zip"
    password = random_string(password_length)

    pyminizip.compress(str(file_path), None, new_archive, password, 9)

    return new_archive, password


def zip_folder(folder_path: Path, password_length: tp.Optional[int]) -> (str, tp.Optional[str]):
    """
    `.zip`-compress a folder with optional password protection.

    :param folder_path: path to a folder to be compressed.
    :param password_length: password length

    :return: new archive path (absolute/relative depends on the way `filepath` was passed) and password (None if was not
    set to password protect)
    """

    new_archive = f"{path.splitext(folder_path)[0]}.zip"
    password = random_string(password_length)

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


def random_string(length: tp.Optional[int]) -> tp.Optional[str]:
    """
    create a random string of a specified length consisting of small and capital letters, digits

    :param length: string length

    :return: generated string or None if None was passed
    """

    if not length:
        return None

    letter_count = random.randint(0, length)
    digit_count = length - letter_count

    str1 = "".join((random.choice(string.ascii_letters) for x in range(letter_count)))
    str1 += "".join((random.choice(string.digits) for x in range(digit_count)))

    sam_list = list(str1)  # it converts the string to list.
    random.shuffle(sam_list)  # It uses a random.shuffle() function to shuffle the string.
    final_string = "".join(sam_list)
    return final_string
