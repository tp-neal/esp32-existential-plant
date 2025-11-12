import base64
import os

def overwrite_file(filepath: str, content: str, mode: str) -> int:
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass

    with open(filepath, mode) as file:
        return file.write(content)
