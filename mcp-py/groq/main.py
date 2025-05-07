import json
import groq
# Groq-specific function definition
groq_tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"]
                    }
                },
                "required": ["location"]
            }
        }
    }
]


def get_weather(location: str, unit: str = "celsius") -> dict:
    dummy_data = {
        "Chennai": {"celsius": 33, "fahrenheit": 91.4},
        "Delhi": {"celsius": 35, "fahrenheit": 95},
        "Mumbai": {"celsius": 32, "fahrenheit": 89.6}
    }

    city = location.split(",")[0].strip()
    temp = dummy_data.get(city, {"celsius": 25, "fahrenheit": 77})[unit]

    return {
        "location": location,
        "temperature": temp,
        "unit": unit,
        "condition": "Sunny"
    }
# Groq API call

def run_tool(name: str, **args) -> dict:
    try:
        if name == "get_weather":
            location = args.get("location")
            if not location:
                raise ValueError("Missing required parameter: location")
            
            unit = args.get("unit", "celsius")
            if unit not in ["celsius", "fahrenheit"]:
                raise ValueError(f"Invalid unit: {unit}. Must be 'celsius' or 'fahrenheit'.")
            
            return get_weather(location=location, unit=unit)

        else:
            raise NotImplementedError(f"Tool '{name}' is not implemented.")
    
    except Exception as e:
        return {
            "error": str(e),
            "tool": name,
            "input": args
        }

groq_client = groq.Client(api_key="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")
initial_response = groq_client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[{"role": "user", "content": "What's the weather in Boston?"}],
    tools=groq_tools
)
print(initial_response.choices[0].message.tool_calls[0].function.name)

tool_call = initial_response.choices[0].message.tool_calls[0]
tool_name = tool_call.function.name
tool_args = json.loads(tool_call.function.arguments)

# Step 6: Run tool
tool_output = run_tool(tool_name, **tool_args)

final_response = groq_client.chat.completions.create(
    model="llama3-70b-8192",
    messages=[
        {"role": "user", "content": "What's the weather in Boston?"},
        {
            "role": "assistant",
            "tool_calls": [tool_call.model_dump()]
        },
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(tool_output)
        }
    ]
)

# Step 8: Print LLM's final answer
print(final_response.choices[0].message.content)