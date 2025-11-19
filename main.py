from wifi import init_wifi
from machine import Pin, UART, ADC, DAC
from config import *
from confidential import credentials as creds
from conversation_manager import ConvoHistory
from prompt_builder import build_llm_prompt
from google_services import *
from file_io import overwrite_file
import utime

def generate_interaction(reason: str, history: ConvoHistory) -> None:
    prompt: str = build_llm_prompt(history, reason='N/A')

    # Query llm and add to convorsation history
    llm_text_response = query_google_service('LLM', prompt)
    message: dict = {'role': 'model', 'content': llm_text_response, 'timestamp': utime.time()}
    history.addToHistory(message)
        
    # # Query tts and write response mp3 to file
    # tts_response = query_google_service('TTS', llm_text_response)
    # overwrite_file(TTS_MP3_FILEPATH, ubinascii.a2b_base64(tts_response.json()['audioContent']), 'wb')
    

def main() -> None:
    print("--- main.py starting ---")

    # Begin an interaction with the plant
    init_wifi()
    convo_history: ConvoHistory = ConvoHistory()
    generate_interaction(reason='N/A', history=convo_history)


if __name__ == '__main__':
    main()
