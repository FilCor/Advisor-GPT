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

c# Definizione dell'input per lo strumento
class WolframAlphaInput(BaseModel):
    query: str = Field(description="Query to be asked to Wolfram Alpha")

# Implementazione dello strumento personalizzato
class WolframAlphaTool(BaseTool):
    name = "Wolfram Alpha"
    description = "Executes queries using Wolfram Alpha API"
    args_schema: Type[BaseModel] = WolframAlphaInput

    def __init__(self):
        super().__init__()  # Chiamata al costruttore della superclasse
        self.wolfram = WolframAlphaAPIWrapper(app_id=app_id)

    def _run(
        self, 
        query: str, 
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return self.wolfram.run(query)

    async def _arun(
        self, 
        query: str, 
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool asynchronously."""
        raise NotImplementedError("Wolfram Alpha Tool does not support async")


