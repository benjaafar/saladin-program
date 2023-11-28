import json

# def save_conversation_history(messages, file_path="/files/conversation_history.json"):
#     print('test')
#     with open(file_path, "w") as file:
#         json.dump([message.to_dict() for message in messages], file, indent=4)

# def save_conversation_history(messages, file_path="/files/conversation_history.json"):
#     try:
#         with open(file_path, "w") as file:
#             json_data = []
#             for message in messages:
#                 # Si l'élément est un objet, utilisez __dict__ pour le convertir en dictionnaire
#                 if hasattr(message, '__dict__'):
#                     json_data.append(message.__dict__)
#                 else:
#                     # Sinon, ajoutez l'élément directement (utile pour les chaînes)
#                     json_data.append(message)
#             json.dump(json_data, file, indent=4)
#     except Exception as e:
#         print(f"Error saving conversation history: {e}")

# import json

# def save_conversation_history(messages, file_path="conversation_history.json"):
#     try:
#         messages_data = {"messages": []}
#         for message in messages:
#             # Création d'un dictionnaire pour chaque message
#             message_dict = {
#                 "assistant_id": message.assistant_id,  # Ajustez selon la structure de votre message
#                 "thread_id": message.thread_id,        # Ajustez selon la structure de votre message
#                 "message_id": message.id,              # Ajustez selon la structure de votre message
#                 "date": message.created_at,            # Ajustez selon la structure de votre message
#                 "input_user": message.user_input,      # Ajustez selon la structure de votre message
#                 "message_value": message.content.text.value  # Ajustez selon la structure de votre message
#             }
#             messages_data["messages"].append(message_dict)

#         # Enregistrement du dictionnaire messages_data en format JSON
#         with open(file_path, "w") as file:
#             json.dump(messages_data, file, indent=4)

#     except Exception as e:
#         print(f"Error saving conversation history: {e}")

def save_conversation_history(thread_messages, file_path="files/conversation_history.json"):
    try:
        messages_data = {"messages": []}
        for msg in thread_messages:
            # Extrait la première partie de la liste content et récupère la valeur
            message_value = msg.content[0].text.value if msg.content else "N/A"

            # Mapping des attributs du message
            message_dict = {
                "assistant_id": msg.assistant_id if msg.assistant_id else "N/A",
                "thread_id": msg.thread_id,
                "message_id": msg.id,
                "date": msg.created_at,  # Vous voudrez peut-être convertir ce timestamp en format lisible
                "input_user": "user" if msg.role == "user" else "assistant",
                "message_value": message_value
            }
            messages_data["messages"].append(message_dict)

        # Enregistrement du dictionnaire messages_data en format JSON
        with open(file_path, "w") as file:
            json.dump(messages_data, file, indent=4)

    except Exception as e:
        print(f"Error saving conversation history: {e}")
