from abc import ABC, ABCMeta, abstractmethod
from pathlib import Path


class IPFSProto(ABC):
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, path: Path, as_archive: bool, encrypt_archive: bool = True, archive_key_length: int = 8):
        """
        Класс для работы с IPFS
        :param path: Путь к папке, или файлу
        :param as_archive: Запаковывать ли нам все это дело в архив
        :param encrypt_archive:  Шифровать ли архив
        :param archive_key_length: Длина ключа для архива по умолчанию
        """
        ...

    @abstractmethod
    def upload_file(self) -> (str, str):
        """
        :return кортеж из ссылки на файл в ipfs (по протоколу ipfs) и ссылки на файл через шлюз
        """
        ...

    @staticmethod
    @abstractmethod
    def delete_file(_hash: str) -> bool:
        """
        Удаляем файл с локальной ноды
        :param _hash: хэш файла в ipfs
        :return флаг статуса операции
        """
        ...

    @staticmethod
    @abstractmethod
    def create_archive(path: Path, encrypt_archive: bool = True, archive_key_length: int = 8) -> (Path, str):
        """
        :return кортеж из пути к архиву и пароля от архива
        """
        ...
