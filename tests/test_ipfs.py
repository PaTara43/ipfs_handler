import sys

sys.path.append("..")
from ipfs_handler import IPFSHandler
from test_archives import get_content_folder, get_content_single_file

import ipfshttpclient
from pathlib import Path

path = Path("./testing_files/test_file.txt")
path_folder = Path("./testing_files/folder")

# Single file with password (each time hash is different)
file = IPFSHandler(path, True)
file_hash, gateway = file.upload_file()
assert file_hash.startswith("Qm")
assert gateway.startswith("http://127.0.0.1:8080/ipfs/Qm")


# Single file no password (each time hash remains the same)
file = IPFSHandler(path, True, False)
file_hash, gateway = file.upload_file()
assert file_hash == "QmUphraLMyE7eJomLMiHdiWAAny1jhxW816UpGM2uTmpRA"
assert gateway == "http://127.0.0.1:8080/ipfs/QmUphraLMyE7eJomLMiHdiWAAny1jhxW816UpGM2uTmpRA"
client = ipfshttpclient.connect()
client.get(file_hash, "./testing_files")
assert get_content_single_file(f"./testing_files/{file_hash}", None) == "abc\nabc2\nabc3"

# Folder with password (each time hash is different)
file = IPFSHandler(path_folder, True)
folder_hash, gateway = file.upload_file()
assert folder_hash.startswith("Qm")
assert gateway.startswith("http://127.0.0.1:8080/ipfs/Qm")


# Folder file no password (each time hash remains the same)
file = IPFSHandler(path_folder, True, False)
folder_hash, gateway = file.upload_file()
assert folder_hash == "QmfTJu84gjsFCYeUADaQyimsqA3yypTgtTq8TC7NLF8bxT"
assert gateway == "http://127.0.0.1:8080/ipfs/QmfTJu84gjsFCYeUADaQyimsqA3yypTgtTq8TC7NLF8bxT"
client.get(folder_hash, "./testing_files")
assert get_content_folder(f"./testing_files/{folder_hash}", None) == "acb\nacb1\nacb2"


# Unpin and remove file from local IPFS node. Folder file no password
assert IPFSHandler.delete_file("QmfTJu84gjsFCYeUADaQyimsqA3yypTgtTq8TC7NLF8bxT") is True
assert "QmfTJu84gjsFCYeUADaQyimsqA3yypTgtTq8TC7NLF8bxT" not in client.pin.ls(type="all")["Keys"].keys()
