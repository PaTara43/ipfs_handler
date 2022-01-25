import sys

sys.path.append("..")
from ipfs_handler import IPFSHandler

from pathlib import Path


path = Path("./testing_files/test_file.txt")
path_folder = Path("./testing_files/folder")

res = IPFSHandler.create_archive(path)
print(res)

res = IPFSHandler.create_archive(path_folder)
print(res)

