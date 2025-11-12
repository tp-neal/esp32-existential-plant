from confidential import credentials as creds

LLM_URL: str = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent"
TTS_URL: str = "https://texttospeech.googleapis.com/v1/text:synthesize?key=" + creds['api_key']

MESSAGES_FILEPATH: str = "./messages.txt"
PROMPT_HEADER_FILEPATH: str = "./prompt_header.txt"
TTS_MP3_FILEPATH: str = "./output.mp3"

ROLES = ['model', 'user', 'any']

HTTP_OK: int = 200

LLM_RETRY_COUNT: int = 5
LLM_RETRY_DELAY: int = 0.1 # ms
LLM_RETRY_STALL: int = 20 # ms

