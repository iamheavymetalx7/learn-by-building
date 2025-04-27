from groq import Groq
import os
import json
from dotenv import load_dotenv
import warnings
from urllib3.exceptions import NotOpenSSLWarning
import logging

# Set up 

from tools import tools,get_response,mutual_fund,upi
load_dotenv(dotenv_path=".env")

warnings.simplefilter("ignore", NotOpenSSLWarning)
# Retrieve the secret from the .env file
groq_api_key = os.getenv("GROQ_API")

logging.basicConfig(
    filename='tool_log.log',  # The log file where the logs will be stored
    level=logging.INFO,       # Set the log level to INFO
    format='%(asctime)s - %(levelname)s - %(message)s',  # Log message format
    filemode='w'  # Overwrite the log file each time the script runs
)
# print(f"API Key: {groq_api_key}")
if not groq_api_key:
    raise ValueError("GROQ_API key is missing from the .env file")

client = Groq(api_key=groq_api_key)
MODEL = "llama3-70b-8192"


# Your remaining code here
def run_conversation(user_prompt):
    messages = [
        {
            "role": "system",
            "content": ("You are a function-calling LLM that uses the data extracted from the functions "
                "to answer questions around mutual funds, UPI transactions."
                "Do not apologize under any circumstances, even if information is missing. "
                "Only use the information provided by the tools to give answers, and if information is not "
                "available, state it without elaboration or conjecture.")},
        {
            "role": "user",
            "content": user_prompt,
        },
    ]
    
    response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=tools,
            tool_choice="auto",
            max_tokens=4096
        )
    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls
    
    logging.info(f"Response message: {response_message}")
    logging.info(f"Tool calls: {tool_calls}")
    
    if tool_calls:
        available_functions = {
            "get_response": get_response,
            "mutual_fund": mutual_fund,
            "upi": upi,
        }
        messages.append(response_message)

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_to_call = available_functions[function_name]
            function_args = json.loads(tool_call.function.arguments)
            function_response = function_to_call(**function_args)
            logging.info(f"Calling tool: {function_name} with arguments: {function_args}")
            logging.info(f"Response: {function_response}") 
            messages.append({
                "tool_call_id": tool_call.id,
                "role": "tool",
                "name": function_name,
                "content": function_response,
            })

        second_response = client.chat.completions.create(
            model=MODEL,
            messages=messages
        )
        final_response = second_response.choices[0].message.content
    else:
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            max_tokens=4096
        )
        messages.append(response_message)
        final_response = response.choices[0].message.content

    return final_response

if __name__ == "__main__":
    print(run_conversation("tell me about UTINEXT50.BO mutual fund"))