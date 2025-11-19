# ========================================================================================
#  [FILE NAME]: file_io.py
#  [AUTHOR]: Tyler Neal 
#  [DATE CREATED]: 2025-11-08
#  [LAST MODIFIED]: 2025-11-19
#
#  [DESCRIPTION]: This file contains functionality for overwriting a file path if it exists.
# ========================================================================================

import os

def overwrite_file(filepath: str, content: str, mode: str) -> int:
    try:
        os.remove(filepath)
    except FileNotFoundError:
        pass

    with open(filepath, mode) as file:
        return file.write(content)
