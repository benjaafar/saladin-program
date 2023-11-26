from openai import OpenAI
import os

class OpenAIChatClient:
  
    api_key = os.getenv('OPENAI_API_KEY')

    if api_key is not None:
     print("API Key found!")
    # You can now use the api_key in your application
    else:
     print("API Key not set in environment variables.")  
  
    def __init__(self):
        self.client = OpenAI(api_key= self.api_key )
        self.messages = []

    def add_system_message(self, content):
        self.messages.append({"role": "system", "content": content})

    def add_user_message(self, content):
        self.messages.append({"role": "user", "content": content})

    def get_response(self):
        response = self.client.chat.completions.create(
            model="gpt-4-vision-preview",
            messages=self.messages,
            max_tokens=1000
        )
        return response

    def get_analyzed_response(self, user_message):
        self.add_system_message("You are a helpful assistant.")
        analyzed_prompt = agent_analyzer(user_message)
        self.add_user_message(analyzed_prompt)

        response = self.get_response()

        if response and response.choices:
            latest_response = response.choices[0].message.content
            return latest_response
        else:
            return "No response from the AI."

# def agent_analyzer(user_message):
#     analyzed_prompt = (
#         "Analyze the following message. Please provide a detailed breakdown covering these aspects Please provide a concise and precise response:\n\n"
#         "Content Summary: Briefly summarize the core content of the message.\n"
#         "Intent and Needs: Identify and explain the intent behind the message. What needs or objectives is the sender trying to address or convey?\n"
#         "Tone and Context: Assess the tone of the message. What context might be relevant to fully understand it?\n"
#         "Desired Outcome: Based on the content and tone, what seems to be the desired outcome or response from the recipient?\n"
#         "Suggestions for Response: If applicable, suggest a suitable response that aligns with the message’s intent and desired outcome.\n"
#         "Please apply this analysis to the following message : "
#         f"{user_message}"
#     )
#     return analyzed_prompt

def agent_analyzer(user_message):
    analyzed_prompt = (
        "Please analyze the following message and initially determine if all necessary information is available for comprehensive processing:\n\n"
        "- Initial Check: Assess if the message contains all the necessary details required for a complete analysis. "
        "State '#Yes#' if all information is present, and '#No#' if there are missing details.\n\n"
        "- If 'Yes', briefly summarize the core content of the message, identify the intent and needs, assess the tone and context, "
        "and suggest the desired outcome or response.\n\n"
        "- If 'No', identify what crucial information is missing.\n\n"
        f"Apply this to: {user_message}"
    )
    return analyzed_prompt

def agent(analyzed_response):
    # This is a placeholder for logic that interprets the analyzed response.
    # In a real scenario, this would involve some natural language processing to understand the response.
    # For simplicity, let's assume we have a way to determine if information is missing or if needs are clear.
    needs_are_clear = "needs identified" in analyzed_response.lower()
    information_is_missing = "information missing" in analyzed_response.lower()

    if information_is_missing:
        prompt = (
            "It appears that some crucial details might be missing from the message to fully understand and respond appropriately. "
            "Please specify what additional information is needed for a comprehensive analysis. "
            "Here are some questions to consider: [List specific questions based on the gaps identified in the analysis]."
        )
    elif needs_are_clear:
        prompt = (
            "Based on the identified needs in the message, outline the skills and resources required to effectively address these needs. "
            "Additionally, provide a brief context setup that explains how these skills and resources align with the objectives mentioned in the message."
        )
    else:
        prompt = "Unable to determine the next course of action based on the provided analysis."

    return prompt

def apply_analyzer_result(analyzed_response):
    if "Yes" in analyzed_response:
        # All necessary information is present
        action = "Proceed with processing the request based on the analysis."
        # Additional logic can be added here to handle the response when all info is present
    elif "No" in analyzed_response:
        # There are missing details
        action = "Request further information based on the missing details identified."
        # Additional logic can be added here to handle the response when info is missing
    else:
        # In case the response is unclear
        action = "Unable to determine the completeness of information. Further clarification may be needed."

    return action

def execute_prompt(prompt, model="gpt-4-vision-preview", max_tokens=150):
    try:
        response = OpenAI().chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens
        )
        if response and response.choices:
            return response.choices[0].message.content
        else:
            return "No response from the AI."
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def user_agent(initial_message, analyzed_response):
    print("Initial Analysis indicates missing information.")
    print(analyzed_response)
    
    while "No" in analyzed_response:
        additional_info = input("Please provide the additional information that is missing: ")
        updated_message = initial_message + " " + additional_info
        analyzed_response = agent_analyzer(updated_message)
        
        if "Yes" in analyzed_response:
            print("All necessary information is now present.")
            break
        else:
            print("There are still missing details.")

    return updated_message

def task_creator(analyzed_response):
    # Placeholder logic for task handling
    # Example task execution
    task_prompt = "Generate a response based on this analysis: " + analyzed_response
    return execute_prompt(task_prompt)

assistant = client.beta.assistants.create(
    name="Math Tutor",
    instructions="You are a  super AI assistant designed to provide comprehensive and accurate information across a wide range of topics, including science, technology, and general knowledge. It should interact in a professional but approachable manner, using clear and concise language suitable for a diverse audience. The assistant must prioritize user privacy and adhere to ethical guidelines, avoiding biased or discriminatory responses. It should be contextually aware, adapting its responses based on user preferences and feedback. Safety protocols should be in place to prevent misuse, and the assistant should clearly communicate its limitations when it cannot provide certain types of information or advice.",
    tools=[{"type": "code_interpreter"}],
    model="gpt-4-1106-preview"
)