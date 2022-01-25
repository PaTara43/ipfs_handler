import sys

sys.path.append("..")
from ipfs_handler import IPFSHandler

from pathlib import Path


path = Path("./testing_files/test_file.txt")
path_folder = Path("./testing_files/folder")
#
# res = IPFSHandler.create_archive(path, password_protect=False)
# print(res)
#
# res = IPFSHandler.create_archive(path_folder)
# print(res)

file = IPFSHandler(path, True)

file_path = file.file_path
password = file.password
print(file_path)
print(password)

file_hash, gateway = file.upload_file()
print(file_hash)
print(gateway)

file.delete_file(file_hash.replace('5', '4'))
