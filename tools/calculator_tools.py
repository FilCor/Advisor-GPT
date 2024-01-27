from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun  # Importazione aggiunta
import wolframalpha
import os
from aws_utilis import get_aws_parameter


class WolframAlphaAPIWrapper(BaseModel):
    """
    Wrapper for Wolfram Alpha API.
    This class simplifies the process of making queries to the Wolfram Alpha API.
    """

    def __init__(self, app_id: str):
        super().__init__()
        self.wolfram_client = wolframalpha.Client(app_id)

    def run(self, query: str) -> str:
        """
        Run a query through WolframAlpha and return the result.
        
        Args:
            query (str): The query string to be sent to Wolfram Alpha.

        Returns:
            str: The result of the query.
        """
        try:
            res = self.wolfram_client.query(query)
            # Assuming the first 'pod' is the most relevant one
            return next(res.results).text if res.results else "No results found."
        except Exception as e:
            return f"An error occurred: {str(e)}"

# Recupero dell'APP ID da AWS
app_id = get_aws_parameter("WOLFRAM_ALPHA_APPID", decrypt=True)

# Assicurati che l'input per lo strumento sia definito
class WolframAlphaInput(BaseModel):
    query: str = Field(description="Query to be asked to Wolfram Alpha")

class WolframAlphaTool(BaseTool):
    name = "Wolfram Alpha"
    description = "Executes queries using Wolfram Alpha API"
    args_schema: Type[BaseModel] = WolframAlphaInput

    def __init__(self, app_id: str):
        super().__init__() 
        self.wolfram = WolframAlphaAPIWrapper(app_id)

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        return self.wolfram.run(query)


