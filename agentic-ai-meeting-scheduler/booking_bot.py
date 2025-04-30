
from groq import Groq
from typing import List
from tools.ask_user import ask_user
from tools.tools import (
    ask_user_schema,
    get_booking_slots_schema,
    book_table_schema,
    use_tool,
)
from groq.types.chat import ChatCompletionMessageParam
from tools.tool_use_block import ToolUseBlock
from dotenv import load_dotenv
import os
load_dotenv(dotenv_path="/Users/nitishkumar/Documents/learn-by-building/agentic-ai-meeting-scheduler/.env")

groq_api_key = os.getenv("GROQ_API")
# print(groq_api_key,"groq_api_key")
client = Groq(api_key=groq_api_key)
MODEL = "llama3-70b-8192"


messages_history: List[ChatCompletionMessageParam] = [
    {
        "role": "system",
        "content": """
        You are a chatbot specializing in restaurant table reservations. Guide users smoothly through the booking process.

1. Collect Details:

Start by asking for the reservation name, time, and number of people using the ask_user tool.

2. Retrieve Available Slots:

Use the get_booking_slots function to retrieve available slots based on the provided details.

List the available options to the user using the ask_user tool.

3. Book the Table:

Once the user selects a slot, confirm all details (time, table, and reservation name).

Use the book_table function to finalize the reservation.

Continue assisting until the booking is complete or the user decides to stop.
        """  }]
def send_message_block(new_message_block: dict, messages_history: list[dict] = []):
    """Main function to send a message block to Groq and receive a response."""
    # print(f"💬 New message Message: {new_message_block}\n")
    messages = messages_history.copy()
    messages.append(new_message_block)
    # print(messages,"**messages**")
    response = client.chat.completions.create(
        model=MODEL,
        max_tokens=4096,
        temperature=0,
        tools=[
            ask_user_schema,
            get_booking_slots_schema,
            book_table_schema,
        ],
        tool_choice="auto",
        messages=messages
    )

    response_text = response.choices[0].message
    print(f"✨ System Response: {response_text}\n")

    # Process the response to construct a valid system message
    if hasattr(response.choices[0], "message") and response.choices[0].message.tool_calls:
        # Extract information from tool calls
        tool_call = response.choices[0].message.tool_calls[0]
        function_name = tool_call.function.name
        function_args = tool_call.function.arguments
        response_content = (
            f"System invoked tool '{function_name}' with arguments: {function_args}."
        )
    else:
        # Default to plain text content or reasoning if available
        response_content = response.choices[0].message.content or "No response content."

    # Construct the system message
    response_block = {
        "role": "system",
        "content": response_content,
    }
    # print(f"✨ Final System Message Block: {response_block}\n")

    messages.append(response_block)

    # Check if a tool is used and process the tool result.
    messages = check_and_use_tool(messages, response)
    return messages


def send_message(new_message: str, messages_history: list[dict] = messages_history):
    """Wrapper function to send a new (text) message to Groq."""
    new_message_block = {
        "role": "user",
        "content": [{"type": "text", "text": new_message}],
    }
    return send_message_block(
        new_message_block=new_message_block, messages_history=messages_history
    )


def send_tool_result(
    tool_result: str, tool_use_id: str, messages_history: list[dict] = []
):
    """Wrapper function to send a tool result (output) back to Groq."""
    tool_response_block = {
        "role": "user",
        "content": [
            {
                "type": "text",  # Adjusting the type to 'text' to meet API requirements
                "text": f"Tool Result: {tool_result} (Tool Use ID: {tool_use_id})",
            }
        ],
    }
    return send_message_block(
        new_message_block=tool_response_block, messages_history=messages_history
    )

def extract_tool_calls(tool_calls):
    """Extracts tool call details and maps them to ToolUseBlock instances."""
    tool_use_blocks = []

    for tool_call in tool_calls:
        tool_use_block = ToolUseBlock(
            id=tool_call.id,
            name=tool_call.function.name,
            input=tool_call.function.arguments,
            type="tool_use"  
        )
        tool_use_blocks.append(tool_use_block)

    return tool_use_blocks

def check_and_use_tool(messages: list[dict], response):

    tool_calls = response.choices[0].message.tool_calls
    if tool_calls:
        tool_use_blocks = extract_tool_calls(tool_calls)
        # print(tool_use_blocks,"tool_use_blocks")
        tool_use_content = tool_use_blocks[0]
        # print(tool_use_content,"tool_use_content")
        tool_result = use_tool(tool_use_content)
        # print(f"type of Tool Result: {type(tool_result)}")
        print(f"🛠️ Using Tool [{tool_use_content.name}]: \033[32m{tool_result}\033[0m\n")
        
        
        # If the tool used is `get_booking_slots`, pass options to `ask_user`
        # if tool_use_content.name == "get_booking_slots":
        #     # Assuming tool_result is a list of strings representing booking slots
        #     formatted_slots = "\n".join(tool_result)  # Format for user readability
        #     prompt_with_options = f"Here are the available tables:\n{formatted_slots}\nWhich table would you like to book?"
        #     # Send this prompt to `ask_user`
        #     return send_tool_result(prompt_with_options, tool_use_content.id, messages)

        # Send the tool result back to the API.
        # print(tool_result,tool_use_content.id)
        send_tool_result(tool_result, tool_use_content.id, messages)

    return messages


if __name__ == "__main__":
    first_message = ask_user("Tell me about the time/seats you'd like to book.")
    messages_history = send_message(first_message)