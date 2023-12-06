from flask import Flask, render_template, request, jsonify
import AI_Assitant
import logging
import utils
import time

app = Flask(__name__)
logging.basicConfig(filename='assistant_errors.log', level=logging.ERROR, format='%(asctime)s %(levelname)s:%(message)s')

# Initialisez l'assistant et le thread ici
try:
    my_assistant = AI_Assitant.create_assitance()
    assistant_id = my_assistant.id
    my_thread = AI_Assitant.create_thread()
    thread_id = my_thread.id
except Exception as e:
    logging.error(f"Error initializing the assistant or thread: {e}")

@app.route('/')
def index():
    return render_template('/index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    user_input = request.form.get('message')
    if not user_input.strip() or len(user_input) > 1000:
        return jsonify({'error': 'Invalid input or input too long.'})

    try:
        Assistant = AI_Assitant.get_assistant("sst_Rb6OUv3XjA9bnWib6buo9Ex9")
        
        AI_Assitant.create_message(thread_id, "user", user_input)
        run = AI_Assitant.create_run(thread_id, assistant_id)
        
        # Attente de la réponse
        attempts = 0
        max_attempts = 10  # Nombre maximal de tentatives
        delay = 1  # Délai initial en secondes

        while attempts < max_attempts:
            run_status = AI_Assitant.retreive_run(thread_id, run.id)

            if run_status.status == 'completed':
                break
            elif run_status.status == 'failed':
                return jsonify({'error': 'Run failed.'})

            time.sleep(delay)
            attempts += 1

        if attempts == max_attempts:
            return jsonify({'error': 'Run did not complete in a timely manner.'})


        assist = AI_Assitant.get_assistants()
        print( assist)
        messages = AI_Assitant.list_messages(thread_id)
        
        utils.save_conversation_history(messages)
        return jsonify({'response': messages[0].content[0].text.value })

    
    except Exception as e:
        logging.error(f"Error during message processing: {e}")
        return jsonify({'error': 'An error occurred while processing the message.'})

if __name__ == '__main__':
    app.run(debug=True)
