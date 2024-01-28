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
    
    The input to this tool should be a pipe (|) separated text containing
    the stock ticker and the date range for which the stock prices are needed.
    For example, `AAPL|2022-01-01|2022-12-31` represents the stock symbol 'AAPL'
    and the date range from January 1, 2022, to December 31, 2022."""
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
