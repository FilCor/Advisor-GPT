from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
import requests

from aws_utilis import get_aws_parameter

app_id = get_aws_parameter("POLIGON_API_KEY", decrypt=True)

# Definizione dell'input
class StockPriceInput(BaseModel):
    ticker_symbol: str = Field(description="Symbol of the stock")
    start_date: str = Field(description="Start date for the price data")
    end_date: str = Field(description="End date for the price data")

# Implementazione dello strumento personalizzato
class StockPriceTool(BaseTool):
    name = "Stock Price"
    description = "Retrieves first and last closing stock prices for a given date range"
    args_schema: Type[BaseModel] = StockPriceInput

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://api.polygon.io/v2/aggs/ticker/"

    def _run(
        self, 
        ticker_symbol: str, 
        start_date: str, 
        end_date: str, 
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        url = f"{self.base_url}{ticker_symbol}/range/1/day/{start_date}/{end_date}?adjusted=true&sort=asc&limit=120&apiKey={self.api_key}"
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
