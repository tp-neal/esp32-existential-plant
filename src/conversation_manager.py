from config import *
import json
import datetime

class ConvoHistory:

    def __init__(self):
        self.message_counts = {'user': 0, 'model': 0} 

        # Count messages from json file
        convo_history: list = []
        try:
            with open(MESSAGES_FILEPATH, "rt") as messages_json:
                convo_history = json.load(messages_json)

        except FileNotFoundError:
            with open(MESSAGES_FILEPATH, 'wt') as messages_json:
                json.dump([], messages_json) 
        
        except json.JSONDecodeError:
            pass
        
        for entry in convo_history:
            if entry['role'] not in ROLES: 
                print("Warning: Invalid message role")
            else:
                self.message_counts[entry['role']] += 1
 
    def getHistoryByRole(self, role: str) -> list:
        if role not in ROLES: 
            print("Warning: Invalid message role")
            return

        # Get messages from json file
        convo_history: list = []
        try:
            with open(MESSAGES_FILEPATH, "rt") as messages_json:
                convo_history = json.load(messages_json)

        except FileNotFoundError:
            with open(MESSAGES_FILEPATH, 'wt') as messages_json:
                json.dump([], messages_json) 
        
        except json.JSONDecodeError:
            pass

        # Filter messages by role
        filtered_history: list = []
        for entry in convo_history:
            if (entry['role'] == role or role == 'any'):
                entry['timestamp'] = datetime.datetime.fromisoformat(entry['timestamp'])
                filtered_history.append(entry)
        
        return filtered_history 

    def addToHistory(self, message) -> None:
        if not message['role'] in ROLES: 
            print("Warning: Invalid message role")
            return

        full_history = self.getHistoryByRole('any')

        if self.message_counts[message['role']] < 10:
            self.message_counts[message['role']] += 1
        else: 
            self.removeOldestMessage(full_history, message['role'])

        full_history.append(message)
        
        for entry in full_history:
            entry['timestamp'] = entry['timestamp'].isoformat()

        with open(MESSAGES_FILEPATH, 'wt') as convo_file:
            convo_file.truncate(0)
            json.dump(full_history, convo_file)

    def removeOldestMessage(self, convo_history: list, role: str) -> None:
        oldest_entry = None
        oldest_timestamp = datetime.datetime.now()
        for entry in convo_history:
            if entry['timestamp'] < oldest_timestamp:
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
            print_string += "Timestamp: " + entry['timestamp'].strftime("%Y-%m-%d %H:%M:%S") + "\n\n"
            
        return print_string
