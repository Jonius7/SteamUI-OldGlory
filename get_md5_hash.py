import hashlib

with open(r"C:\Program Files (x86)\0E Games\Steam\package\steamui_websrc_all.zip.vz.996bf6091ef8a0822f336e6fc912471ab0fee08d_23943287", "rb") as f:
    file_hash = hashlib.md5()
    while chunk := f.read(8192):
        file_hash.update(chunk)

print(file_hash.digest())
print(file_hash.hexdigest())  # to get a printable str instead of bytes