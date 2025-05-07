import asyncio
from typing import Optional
from contextlib import AsyncExitStack

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import groq
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

class MCPClient:
    def __init__(self):
        # Initialize session and client objects
        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self.groq = groq.Client(api_key="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")
    # methods will go here
    
    async def connect_to_server(self, server_script_path: str):
        """Connect to an MCP server

        Args:
            server_script_path: Path to the server script (.py or .js)
        """
        is_python = server_script_path.endswith('.py')
        is_js = server_script_path.endswith('.js')
        if not (is_python or is_js):
            raise ValueError("Server script must be a .py or .js file")

        command = "python" if is_python else "node"
        server_params = StdioServerParameters(
            command=command,
            args=[server_script_path],
            env=None
        )

        stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
        self.stdio, self.write = stdio_transport
        self.session = await self.exit_stack.enter_async_context(ClientSession(self.stdio, self.write))

        await self.session.initialize()

        # List available tools
        response = await self.session.list_tools()
        tools = response.tools
        print("\nConnected to server with tools:", [tool.name for tool in tools])
        
    async def process_query(self, query: str) -> str:
        """Process a query using Claude and available tools"""
        messages = [
            {
                "role": "user",
                "content": query
            }
        ]

        response = await self.session.list_tools()
        available_tools = [{
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema
            }
        } for tool in response.tools]
        # Initial Claude API call
        response = self.groq.chat.completions.create(
            model="llama3-70b-8192",
            max_tokens=1000,
            messages=messages,
            tools=available_tools
        )
        print(response)
        # Process response and handle tool calls
 
        final_text = []
        assistant_message = response.choices[0].message
        if assistant_message.content is not None:
            final_text.append(assistant_message.content)
        # If using tool calls (assuming Groq supports this like OpenAI functions)
        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = tool_call.function.arguments
                if isinstance(tool_args, str):
                    import json
                    tool_args = json.loads(tool_args)  # Convert the string into a dictionary

                # Call tool and handle result
                result = await self.session.call_tool(tool_name, tool_args)
                content_str = "".join([
                    c.text for c in result.content 
                    if c and hasattr(c, "text") and isinstance(c.text, str) and c.text is not None
                ])                # Update conversation
                
                messages.append({
                    "role": "assistant",
                    "tool_calls": [tool_call]
                })
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": content_str
                })

                # Call Groq again with updated messages
                response = self.groq.chat.completions.create(
                    model="llama3-70b-8192",
                    max_tokens=1000,
                    messages=messages,
                    tools=available_tools,
                    tool_choice="auto"
                )
                message_content = response.choices[0].message.content
                if message_content is not None:
                    final_text.append(message_content)
                else:
                    print("Warning: response message content is None")

        return "\n".join(final_text)

    async def chat_loop(self):
        """Run an interactive chat loop"""
        print("\nMCP Client Started!")
        print("Type your queries or 'quit' to exit.")

        while True:
            try:
                query = input("\nQuery: ").strip()

                if query.lower() == 'quit':
                    break

                response = await self.process_query(query)
                print("\n" + response)

            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        """Clean up resources"""
        await self.exit_stack.aclose()

async def main():
    if len(sys.argv) < 2:
        print("Usage: python client.py <path_to_server_script>")
        sys.exit(1)

    client = MCPClient()
    try:
        await client.connect_to_server(sys.argv[1])
        await client.chat_loop()
    finally:
        await client.cleanup()

if __name__ == "__main__":
    import sys
    asyncio.run(main())