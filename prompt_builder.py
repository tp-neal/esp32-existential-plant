# ========================================================================================
#  [FILE NAME]: prompt_builder.py
#  [AUTHOR]: Tyler Neal 
#  [DATE CREATED]: 2025-11-08
#  [LAST MODIFIED]: 2025-11-19
#
#  [DESCRIPTION]: This file contains functionality for building an llm prompt.
# ========================================================================================

from config import PROMPT_HEADER_FILEPATH
from conversation_manager import ConvoHistory

def build_llm_prompt(convo_history: ConvoHistory, reason: str) -> str:
    prompt: str = ""
    with open(PROMPT_HEADER_FILEPATH, 'rt') as prompt_file:
        prompt += prompt_file.read()

    prompt += "\n"
    prompt += f"Reason for response: {reason}\n"
    prompt += "Message history:"    
    message_history = convo_history.getHistoryString()
    prompt += ("\n" + message_history) if message_history else " N/A\n" 

    return prompt