# ========================================================================================
#  [FILE NAME]: config.py
#  [AUTHOR]: Tyler Neal 
#  [DATE CREATED]: 2025-11-08
#  [LAST MODIFIED]: 2025-11-19
#
#  [DESCRIPTION]: This file contains configuration information related to the project.
# ========================================================================================

LLM_URL: str = "generativelanguage.googleapis.com"
TTS_URL: str = "texttospeech.googleapis.com"
GS_PORT: int = 443

MESSAGES_FILEPATH: str = "./messages.txt"
PROMPT_HEADER_FILEPATH: str = "./prompt_header.txt"
TTS_MP3_FILEPATH: str = "./output.mp3"

ROLES = ['model', 'user', 'any']

HTTP_OK: int = 200

LLM_RETRY_COUNT: int = 5
LLM_RETRY_DELAY: int = 20 # ms

READ_BUFFER_SIZE = 1024