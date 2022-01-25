import pyminizip
import random
import string

from ipfs_proto import IPFSProto
from os import path, walk
from pathlib import Path


class IPFSHandler(IPFSProto):
    def __init__(
        self,
        filepath: Path,
        as_archive: bool,
        encrypt_archive: bool = True,
        archive_key_length: int = 8,
    ):
        """
        Класс для работы с IPFS
        :param filepath: Путь к папке, или файлу
        :param as_archive: Запаковывать ли нам все это дело в архив
        :param encrypt_archive:  Шифровать ли архив
        :param archive_key_length: Длина ключа для архива по умолчанию
        """

    def upload_file(self) -> (str, str):
        """
        :return кортеж из ссылки на файл в ipfs (по протоколу ipfs) и ссылки на файл через шлюз
        """
        ...

    @staticmethod
    def delete_file(_hash: str, filepath: Path = None) -> bool:
        """
        Удаляем файл с локальной ноды
        :param _hash: хэш файла в ipfs
        :param filepath: путь к файлу на локальной машине (нужен ли он?
        Или можно по хэшу достать расположение на локальной ноде?)
        :return флаг статуса операции
        """
        ...

    @staticmethod
    def create_archive(
        filepath: Path, encrypt_archive: bool = True, archive_key_length: int = 8
    ) -> (Path, str):
        """
        :return кортеж из пути к архиву и пароля от архива
        """
        if not filepath.exists():
            raise FileNotFoundError

        if filepath.is_dir():
            archived_file, password = zip_folder(filepath, archive_key_length)
        else:
            archived_file, password = zip_single_file(filepath, archive_key_length)

        result = (archived_file, password)

        return result


def zip_single_file(file_path, archive_key_length):
    new_archive = f"{path.splitext(file_path)[0]}.zip"
    password = random_string(archive_key_length)

    pyminizip.compress(str(file_path), None, new_archive, password, 9)

    return new_archive, password


def zip_folder(folder_path, archive_key_length):
    new_archive = f"{path.splitext(folder_path)[0]}.zip"
    password = random_string(archive_key_length)

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


def random_string(length):
    letter_count = random.randint(0, length)
    digit_count = length - letter_count

    str1 = "".join((random.choice(string.ascii_letters) for x in range(letter_count)))
    str1 += "".join((random.choice(string.digits) for x in range(digit_count)))

    sam_list = list(str1)  # it converts the string to list.
    random.shuffle(
        sam_list
    )  # It uses a random.shuffle() function to shuffle the string.
    final_string = "".join(sam_list)
    return final_string
