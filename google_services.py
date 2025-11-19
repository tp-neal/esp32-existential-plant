# ========================================================================================
#  [FILE NAME]: google_services.py
#  [AUTHOR]: Tyler Neal 
#  [DATE CREATED]: 2025-11-08
#  [LAST MODIFIED]: 2025-11-19
#
#  [DESCRIPTION]: This file contains logic for connecting to and quering a google service.
# ========================================================================================

from confidential import credentials as creds
from ssl import wrap_socket
from config import *
import json
import socket

def get_socket(hostname, port):
    remote_info_list: list = socket.getaddrinfo(hostname, port)

    for remote_info in remote_info_list: 
        try:
            remote_family, remote_sock_type, remote_proto, remote_canonname, remote_sock_addr = remote_info
            sock: socket.socket = socket.socket(remote_family, remote_sock_type)
            sock.connect(remote_sock_addr)
            secure_sock = wrap_socket(sock, server_hostname=hostname)
            
            return secure_sock 

        except Exception as e:
            print(f"Warning: Failed to connect to address: {e}")
            pass
    
    
    return None


def build_llm_request(prompt: str) -> str:

    payload: str = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {
                        "text": prompt
                    }
                ]
            }
        ]
    }
    payload_bytes: int = json.dumps(payload).encode('utf-8')

    header: str = (
                f"POST /v1/models/gemini-2.5-flash:generateContent?key={creds['api_key']} HTTP/1.1\r\n" +
                f"Host: generativelanguage.googleapis.com\r\n" + 
                f"Content-Type: application/json\r\n" + 
                f"Content-Length: {len(payload_bytes)}\r\n" +
                f"Connection: close\r\n" +
                f"\r\n" 
    )
    header_bytes: str = header.encode('utf-8')

    request: str = header_bytes + payload_bytes 
    
    return request


def build_tts_request(prompt: str) -> str:

    payload: str = {
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
    payload_bytes: int = json.dumps(payload).encode('utf-8')

    header: str = (
                f"POST /v1/models/gemini-2.5-flash:generateContent?key={creds.api_key} HTTP/1.1\r\n" +
                f"Host: generativelanguage.googleapis.com\r\n" + 
                f"Content-Type: application/json\r\n" + 
                f"Content-Length: {len(payload_bytes)}\r\n" +
                f"Connection: close\r\n" +
                f"\r\n" 
    )
    header_bytes: str = header.encode('utf-8')

    request: str = header_bytes + payload_bytes 
    
    return request


def read_in_response(socket) -> str:
    raw_response_bytes: bytes = b''
    chunk = None 
    while True: 
        chunk = socket.read(READ_BUFFER_SIZE)
        print(f"Info: Read in {len(chunk)} bytes from server")
        if not chunk:
            break
        raw_response_bytes += chunk
            
    response_text: str = raw_response_bytes.decode('utf-8')

    return response_text


def http_error_check(response_text: str):
    status_line: str = response_text.split('\r\n')[0]
    status_code_str: str = status_line.split(' ')[1]
    status_code = int(status_code_str)
    if status_code != HTTP_OK:
        print()
        print(f"HTTP Error: Status code {status_code}")
        print("Server response:")
        print(response_text)
        raise Exception(f"API request failed with status code {status_code}")


def get_body_json(response_text: str) -> json:
    body_start_index: int = response_text.find('\r\n\r\n') + 4 # Add 4 to skip carriage returns
    json_body_text = response_text[body_start_index:]
    body_json = json.loads(json_body_text)

    return body_json


def query_google_service(service: str, prompt: str) -> str:
    """
    Builds and sends an http request to the tts or llm google service, and returns the response.

    @param service: The name of the service, either 'LLM' or 'TTS'.
    @param hostname: The hostname of the service to connect to.
    @param port: The port to connect to the service on.
    @param prompt: The prompt to send to the google service.
    @return: The response from the server.
    @note: When using the LLM service the return will be the llm's textual response.
           When using the TTS service the return will be the tts's mp3 bytecode response, and must be
           then decoded from base64.
    
    """
    google_service_socket = get_socket(LLM_URL, GS_PORT)
    if not google_service_socket:
        while(True):
            continue

    # Build the request
    request: str 
    if service == "LLM":
        request = build_llm_request(prompt)
    else:
        request = build_tts_request(prompt)
    request_size: int = len(request)

    # Send request to google servers
    bytes_written: int = google_service_socket.write(request)
    if bytes_written < len(request):
        print(f"HTTP Error: Sent {bytes_written} bytes, expected {request_size}")
        raise Exception("Partial write failure")

    # Read in response from llm
    response_text = read_in_response(google_service_socket)

    # Make sure there was no error
    try:
        http_error_check(response_text)
    except Exception as e:
        raise e

    # Extract the response
    body_json = get_body_json(response_text)

    response_content: str
    if service == "LLM": 
        response_content = body_json['candidates'][0]['content'][0]['parts'][0]['text']
    else:
        response_content = body_json['audioContent']

    google_service_socket.close()

    return response_content

