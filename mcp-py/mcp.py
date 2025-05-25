

## pseudo code - wrong code
## do not look into this - wrong implementation
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



client = MCPClient(manifest="tools.json")

# Call any model - MCP handles the translation behind the scenes
response = client.chat_completions(
    model="llama3-70b-8192",  # or "claude-3-5-sonnet" or any supported model
    messages=[{"role": "user", "content": "What's the weather in Boston?"}]
)

if response.functions:
    results = []
    for func in response.functions:
        result = run_tool(func.name, **func.args)
        results.append({"name": func.name, "result": result})
    
    # Send results back - MCP formats it correctly for each provider
    final_response = client.chat_completions(
        model="llama3-70b-8192", # or "claude-3-5-sonnet" or any supported model
        messages=[{"role": "user", "content": "What's the weather in Boston?"}],
        tools_result=results
    )
    print(final_response.content)
else:
    print(response.content)
