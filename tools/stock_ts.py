from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
import requests

from aws_utilis import get_aws_parameter

app_id = get_aws_parameter("POLIGON_API_KEY", decrypt=True)

class StockPriceInput(BaseModel):
    ticker_symbol: str = Field(description="Symbol of the stock")
    start_date: str = Field(description="Start date for the price data")
    end_date: str = Field(description="End date for the price data")

# Definizione dell'input
class StockPriceTool(BaseTool):
    name = "Stock Price"
    description = """Retrieves first and last closing stock prices for a given date range
    
    The Stock Price tool is designed to fetch the first and last closing stock prices for a specific stock within a given date range. 
    This tool expects the input in a specific format: a single string where the stock ticker symbol and the date range (start and end dates) are separated by pipes (|).

    For example, the correct input format would be 'TickerSymbol|StartDate|EndDate'. An example of a valid input for this tool is 'AAPL|2023-01-01|2023-12-31'. In this example, 'AAPL' represents the ticker symbol for Apple Inc., and '2023-01-01' to '2023-12-31' represents the date range from January 1, 2023, to December 31, 2023.

    It's important that inputs are formatted in this way to ensure accurate parsing and data retrieval. 
    The tool will extract the ticker symbol, 'AAPL', and then use the provided start and end dates to query the stock prices for Apple Inc. 
    within the specified date range.
    We are right now in 2024"""
    args_schema: Type[BaseModel] = StockPriceInput

    def __init__(self):
        super().__init__()
        # Non assegnare qui l'api_key

    def get_api_client(self):
        """Crea e restituisce un client configurato per l'API di Polygon."""
        api_key = get_aws_parameter("POLIGON_API_KEY", decrypt=True)
        return {"base_url": "https://api.polygon.io/v2/aggs/ticker/", "api_key": api_key}

    def _run(
        self, 
        ticker_symbol: str, 
        start_date: str, 
        end_date: str, 
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        client = self.get_api_client()
        url = f"{client['base_url']}{ticker_symbol}/range/1/day/{start_date}/{end_date}?adjusted=true&sort=asc&limit=120&apiKey={client['api_key']}"
        response = requests.get(url)
        results = response.json().get('results', [])

        if not results:
            return "No data available for the given dates."

        first_day = results[0]
        last_day = results[-1]

        return f"First Day Closing Price: {first_day.get('c')}, Last Day Closing Price: {last_day.get('c')}"

    async def _arun(
        self, 
        ticker_symbol: str, 
        start_date: str, 
        end_date: str, 
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Stock Price Tool does not support async")
