import yfinance as yf
import json
from logging_config import logging

def get_response(question):
    return json.dumps({"question": question})



def mutual_fund(fund_symbol):
    """
    argument is function_symbol
    this function is for getting the details of a mutual fund given the symbol from yahoo finance
    """
    try:
        # Fetch data for the mutual fund symbol
        fund_data = yf.Ticker(fund_symbol)

        # Retrieve the required information
        fund_info = fund_data.info
        historical_data = fund_data.history(period="1y")  # Get 1-year historical data
       
        logging.info("Historical data head:\n%s", historical_data.head())
        logging.info("Historical data tail:\n%s", historical_data.tail())

        if not fund_info or historical_data.empty:
            return json.dumps({"error": f"No data found for symbol '{fund_symbol}'"})

        # Calculate the 1-year return if possible
        start_price = historical_data["Open"].iloc[0]
        end_price = historical_data["Close"].iloc[-1]
        
        one_year_return = ((end_price - start_price) / start_price) * 100
        # Build the response
        response = {
            "fund_name": fund_info.get("longName", "Unknown Fund"),
            "symbol": fund_symbol,
            "nav": fund_info.get("navPrice", "N/A"),
            "1_year_return": f"{one_year_return:.2f}%" if start_price and end_price else "N/A",
            "category": fund_info.get("category", "N/A"),
        }

        return json.dumps(response)

    except Exception as e:
        return json.dumps({"error": str(e)})


def upi(transaction_id):
    if transaction_id == "TX123":
        return json.dumps(
            {"transaction_id": "TX123", "status": "Success", "amount": 1500}
        )
    else:
        return json.dumps({"transaction_id": transaction_id, "status": "Pending"})



tools = [
    {
        "type": "function",
        "function": {
            "name": "get_response",
            "description": "Responding a casual chat",
            "parameters": {
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Responding a casual chat",
                    }
                },
                "required": ["question"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "mutual_fund",
            "description": "Get the details of a mutual fund",
            "parameters": {
                "type": "object",
                "properties": {
                    "fund_symbol": {
                        "type": "string",
                        "description": "The name of the mutual fund (e.g. 'Growth Fund')",
                        }
                    },
                    "required": ["fund_symbol"],
                },
            },
        },
    {
        "type": "function",
        "function": {
            "name": "upi",
            "description": "Get the status of a UPI transaction",
            "parameters": {
                "type": "object",
                "properties": {
                    "transaction_id": {
                        "type": "string",
                        "description": "The ID of the UPI transaction (e.g. 'TX123')",
                    }
                },
                "required": ["transaction_id"],
            },
        }
    }
]
