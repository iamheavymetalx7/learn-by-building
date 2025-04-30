from mirascope.groq import GroqTool

def ask_user(input_prompt: str) -> str:
    """
    Prompts the user with a given message and returns their input.

    Args:
        input_prompt (str): The message or question to display to the user.

    Returns:
        str: The user's input as a string.
    """
    user_input = input(f"💬 {input_prompt}\n👉 Enter Message: ")
    return user_input


tool_type = GroqTool.from_fn(ask_user)
print(tool_type.tool_schema())  # prints the Groq-specific tool schema