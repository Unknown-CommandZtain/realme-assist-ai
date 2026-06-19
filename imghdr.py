# A patch to replace the deprecated imghdr module
def what(file, h=None):
    if h is None:
        if isinstance(file, str):
            with open(file, 'rb') as f: h = f.read(32)
        else:
            pos = file.tell()
            h = file.read(32)
            file.seek(pos)
    if h.startswith(b'\xff\xd8'): return 'jpeg'
    if h.startswith(b'\x89PNG\r\n\x1a\n'): return 'png'
    if h.startswith(b'GIF8'): return 'gif'
    if h.startswith(b'WEBP', 8): return 'webp'
    return None