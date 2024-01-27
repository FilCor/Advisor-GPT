from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun  # Importazione aggiunta
from langchain_community.utilities.wolfram_alpha import WolframAlphaAPIWrapper
import wolframalpha
import os
from aws_utilis import get_aws_parameter

# Recupero dell'APP ID da AWS
app_id = get_aws_parameter("WOLFRAM_ALPHA_APPID", decrypt=True)

class WolframAlphaInput(BaseModel):
    query: str = Field(description="Query to be asked to Wolfram Alpha")

# Implementazione dello strumento personalizzato
class WolframAlphaTool(BaseTool):
    name = "Wolfram Alpha"
    description = "Executes queries using Wolfram Alpha API"
    args_schema: Type[BaseModel] = WolframAlphaInput

    def __init__(self, app_id: str):
        super().__init__()  # Chiamata al costruttore della superclasse
        self.app_id = app_id  # Memorizza l'APP ID come attributo dell'istanza

    def _run(
        self, 
        query: str, 
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        wolfram_client = wolframalpha.Client(self.app_id)  # Utilizza l'APP ID qui
        res = wolfram_client.query(query)
        return next(res.results).text if res.results else "No results found."

    async def _arun(
        self, 
        query: str, 
        run_manager: Optional[CallbackManagerForToolRun] = None
        ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Wolfram Alpha Tool does not support async")


