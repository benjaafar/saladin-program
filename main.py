import openai_api

def main():
    user_message = input("Enter your message for analysis: ")
    chat_client = openai_api.OpenAIChatClient()
    analyzed_response = chat_client.get_analyzed_response(user_message)
    
    print("AI's Analysis:\n", analyzed_response)

    # next_action_prompt = agent(analyzed_response)
    
    # print("Next Action Prompt:\n", next_action_prompt)

if __name__ == "__main__":
    main()
