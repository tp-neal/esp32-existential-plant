# ========================================================================================
#  [FILE NAME]: conversation_manager.py
#  [AUTHOR]: Tyler Neal 
#  [DATE CREATED]: 2025-11-08
#  [LAST MODIFIED]: 2025-11-19
#
#  [DESCRIPTION]: This file contains a class used to manage the convorsation history with
#                 the existential plant.
# ========================================================================================

from config import *
import uerrno
import json
import utime

class ConvoHistory:

    def __init__(self):
        convo_history: list = self.loadHistory()
        
        # Count messages from json file
        self.message_counts = {'user': 0, 'model': 0} 
        for entry in convo_history:
            if entry['role'] not in ROLES: 
                print("Warning: Invalid message role of (" + entry['role'] + ") found in conversation history")
            else:
                self.message_counts[entry['role']] += 1
                
    def loadHistory(self) -> list:
        # Load conversation history, or create empty if it doesn't exist
        convo_history: list = []
        try:
            with open(MESSAGES_FILEPATH, "rt") as messages_file:
                convo_history = json.load(messages_file)
                
        except OSError as e:
            if e.errno == uerrno.ENOENT: # file not found, make it
                with open (MESSAGES_FILEPATH, 'wt') as messages_file:
                    json.dump([], messages_file)
            else:
                raise e
        
        return convo_history
 
    def getHistoryByRole(self, role: str) -> list:
        if role not in ROLES: 
            print("Error: Cannot retrieve history by invalid message role (" + role + ")")
            return

        # Get messages from json file
        convo_history: list = self.loadHistory()

        # Filter messages by role
        filtered_history: list = []
        for entry in convo_history:
            if (entry['role'] == role or role == 'any'):
                filtered_history.append(entry)
        
        return filtered_history 

    def addToHistory(self, message) -> None:
        if not message['role'] in ROLES: 
            print("Error: Cannot insert message with invalide role (" + message['role'] + ")")
            return

        convo_history = self.loadHistory()

        # Detemine if we must make room for the new message
        if self.message_counts[message['role']] < 10:
            self.message_counts[message['role']] += 1
        else: 
            self.removeOldestMessage(full_history, message['role'])

        message['timestamp'] = utime.time()
        convo_history.append(message)
        
        with open(MESSAGES_FILEPATH, 'wt') as convo_file:
            json.dump(full_history, convo_file)

    def removeOldestMessage(self, convo_history: list, role: str) -> None:
        oldest_entry = None
        oldest_timestamp = utime.time()
        for entry in convo_history:
            if entry['role'] == role and entry['timestamp'] < oldest_timestamp:
                oldest_entry = entry
                oldest_timestamp = entry['timestamp']

        if oldest_entry:
            convo_history.remove(oldest_entry)

    def getHistoryString(self) -> str:
        convo_history: list = self.getHistoryByRole('any')

        print_string: str = ""
        for entry in convo_history:
            print_string += f"Role: {entry['role']}\n"
            print_string += f"Content: {entry['content']}\n"
            print_string += "Timestamp: " + entry['timestamp'] + "\n\n"
            
        return print_string
