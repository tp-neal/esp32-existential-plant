from config import *
from conversation_manager import ConvoHistory
from prompt_builder import buildPrompt
from google_services import *
from file_io import overwrite_file
import datetime
import base64

def main():
    conversation_history: ConvoHistory = ConvoHistory()

    prompt: str = buildPrompt(conversation_history, reason='N/A')

    llm_response = get_llm_response(prompt, retry_on_fail=True) 
    llm_response_text: str = llm_response.json()['candidates'][0]['content']['parts'][0]['text']

    message: dict = {'role': 'model', 'content': llm_response_text, 'timestamp': datetime.datetime.now()}
    conversation_history.addToHistory(message)
        
    tts_response = get_synthesized_speech(llm_response_text)

    overwrite_file(TTS_MP3_FILEPATH, base64.b64decode(tts_response.json()['audioContent']), 'wb')

if __name__ == '__main__':
    main()