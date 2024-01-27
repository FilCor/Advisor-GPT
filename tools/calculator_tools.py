from typing import Optional, Type
from pydantic import BaseModel, Field
from langchain.tools import BaseTool
from langchain.callbacks.manager import CallbackManagerForToolRun
from langchain_community.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from aws_utilis import get_aws_parameter

# Recupero dell'APP ID da AWS
app_id = get_aws_parameter("WOLFRAM_ALPHA_APPID", decrypt=True)

class WolframAlphaInput(BaseModel):
    """Input model for Wolfram Alpha tool."""
    query: str = Field(description="Query to be asked to Wolfram Alpha")

class WolframAlphaTool(BaseTool):
    """LangChain tool for querying Wolfram Alpha."""
    name = "Wolfram Alpha"
    description = "Usefull when you need to do math calculations!"
    args_schema: Type[BaseModel] = WolframAlphaInput

    def __init__(self):
        super().__init__()
        self.wolfram = WolframAlphaAPIWrapper(wolfram_alpha_appid=app_id)

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """Run the given query using the Wolfram Alpha API."""
        return self.wolfram.run(query)
