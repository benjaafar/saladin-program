import os
from openai import OpenAI

# Initialize OpenAI API
OpenAI.api_key = os.getenv("OPENAI_API_KEY")

client = OpenAI()

def create_assitance():
    my_assistant = client.beta.assistants.create(
      instructions="You are a  super AI assistant designed to provide comprehensive and accurate information across a wide range of topics, including science, technology, and general knowledge. It should interact in a professional but approachable manner, using clear and concise language suitable for a diverse audience. The assistant must prioritize user privacy and adhere to ethical guidelines, avoiding biased or discriminatory responses. It should be contextually aware, adapting its responses based on user preferences and feedback. Safety protocols should be in place to prevent misuse, and the assistant should clearly communicate its limitations when it cannot provide certain types of information or advice.",
      name="Math Tutor",
      tools=[{"type": "code_interpreter"}],
      model="gpt-4",
    )
    return my_assistant


def create_thread():
    empty_thread = client.beta.threads.create()
    return empty_thread

def get_threat(thread):
    my_thread = client.beta.threads.retrieve(thread)
    return my_thread

def delete_threat(thread):
    my_thread = client.beta.threads.delete(thread)
    return my_thread

def create_message(thread,role,message):
    thread_message = client.beta.threads.messages.create(
  thread,
  role=role,
  content=message,
    )
    return thread_message


def get_message(message_id,thread_id):
  message = client.beta.threads.messages.retrieve(
  message_id=message_id,
  thread_id=thread_id,
)
  return message



def update_message(message_id,thread_id,user):
    message = client.beta.threads.messages.update(
    message_id=message_id,
    thread_id=thread_id,
    metadata={
        "modified": "true",
        "user": user,
    },
    )
    return message

def list_messages(thread):
    thread_messages = client.beta.threads.messages.list(thread)
    return thread_messages.data

def create_run(thread,assistant):

    run = client.beta.threads.runs.create(
    thread_id=thread,
    assistant_id=assistant
)
    return run

    

def retreive_run(thread_id , run_id):
    run = client.beta.threads.runs.retrieve(
    thread_id=thread_id,
    run_id=run_id
    )
    return run



