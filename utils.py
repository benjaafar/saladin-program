import json

def save_conversation_history(messages, file_path="/files/conversation_history.json"):
    with open(file_path, "w") as file:
        json.dump([message.to_dict() for message in messages], file, indent=4)
