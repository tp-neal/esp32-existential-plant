from requests import Response, post
from confidential import credentials as creds
from config import *
import time
import json

def get_llm_response(prompt: str, retry_on_fail: bool | None) -> Response:
    headers = {
        'x-goog-api-key': creds['api_key'],
        'Content-Type': 'aplication/json',
    }
    payload = {
        'contents': [
            {
                'parts': [
                    {
                        "text": prompt 
                    }
                ]
            }
        ]
    }

    # Query the LLM on an interval until it sends a response
    response: Response = post(LLM_URL, headers=headers, data=json.dumps(payload)) 

    if (retry_on_fail and ('error' in response.json())):
        error_code: int = -1
        while (error_code != HTTP_OK):
            for i in range(LLM_RETRY_COUNT):
                response = post(LLM_URL, headers=headers, data=json.dumps(payload)) 

                if 'error' not in response.json():
                    error_code = HTTP_OK
                    break

                error_code = response.json()['error']['code']
                print("Warning: failed to get response from llm")
                
            if (error_code != HTTP_OK):
                print("Warning: stalling...")
                time.sleep(LLM_RETRY_STALL)

    return response

def get_synthesized_speech(prompt: str) -> Response:
    headers = {
        'Content-Type': 'aplication/json',
    }
    payload = {
        'input': {
            'text': prompt
        },

        'voice': {
            'languageCode': 'en-US',
            'ssmlGender': 'Female',
        },

        'audioConfig': {
            'audioEncoding': 'MP3'
        }
    }

    response: Response = post(TTS_URL, headers=headers, data=json.dumps(payload)) 
    if 'error' in response.json():
        print("Warning: failed to get response from tts")

    return response
