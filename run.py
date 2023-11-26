import os
import AI_Assitant
import time
import logging
import utils

logging.basicConfig(filename='assistant_errors.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')


# Initialize OpenAI API
def main():

    try:
    # Create an assistant
        my_assistant = AI_Assitant.create_assitance()
        assistant_id = my_assistant.id

    # Create a thread
        my_thread = AI_Assitant.create_thread()
        thread_id = my_thread.id

    except Exception as e:
        logging.error(f"Error initializing the assistant or thread: {e}")
        return

    print("Welcome to the Super AI Assistant. Type 'quit' to exit.")

    while True:
        user_input = input("You: ")
        if not user_input.strip():
            print("Please enter a valid message.")
            continue
        
        max_length = 1000  # Par exemple, limiter à 500 caractères
        if len(user_input) > max_length:
            print(f"Input is too long. Please limit your message to {max_length} characters.")
            continue

        if user_input.lower() == 'quit':
            break

        try:
        # Create a message in the thread
            AI_Assitant.create_message(thread_id, "user", user_input)

        # Run the assistant on the thread
            run = AI_Assitant.create_run(thread_id, assistant_id)
        
        # Retreive run status
            attempts = 0
            max_attempts = 10  # Nombre maximal de tentatives
            delay = 1  # Délai initial en secondes
            
            while attempts < max_attempts:
                run_status = AI_Assitant.retreive_run(thread_id, run.id)
            
                if run_status.status == 'completed':
                    break
                elif run_status.status == 'failed':
                    print("Run failed.")
                    break

                time.sleep(delay)
                attempts += 1
                delay = min(5, delay + 1) 
                
            if attempts == max_attempts:
                print("Run did not complete in a timely manner.")
        
    
        # List all messages in the thread to get the response
            messages = AI_Assitant.list_messages(thread_id)
            for message in messages:
                if message.role == 'assistant':
                    for item in message.content:
                        message_value = item.text.value
                        print(f"Assistant: {message_value} ")
                        utils.save_conversation_history(message_value)

        except Exception as e:
            logging.error(f"Error during message processing: {e}")

if __name__ == "__main__":
    main()
