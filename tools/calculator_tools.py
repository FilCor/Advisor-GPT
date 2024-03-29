from typing import Any, Dict, Optional, Type
from pydantic import BaseModel, Field
from langchain.callbacks.manager import CallbackManagerForToolRun
#from langchain_community.utilities.wolfram_alpha import WolframAlphaAPIWrapper
from langchain.tools import BaseTool
from aws_utilis import get_aws_parameter
from langchain_core.pydantic_v1 import BaseModel, Extra, root_validator
from langchain_core.utils import get_from_dict_or_env
import wolframalpha


class WolframAlphaAPIWrapper(BaseModel):
    """Wrapper for Wolfram Alpha."""
    wolfram_client: Any
    wolfram_alpha_appid: Optional[str] = None

    def __init__(self, wolfram_alpha_appid: Optional[str] = None, **data):
        super().__init__(**data)
        app_id = wolfram_alpha_appid or data.get("wolfram_alpha_appid")
        self.wolfram_client = wolframalpha.Client(app_id)

    def run(self, query: str) -> str:
        """Run query through WolframAlpha and parse result."""
        res = self.wolfram_client.query(query)

        try:
            assumption = next(res.pods).text
            answer = next(res.results).text
        except StopIteration:
            return "Wolfram Alpha wasn't able to answer it"

        if answer is None or answer == "":
            # We don't want to return the assumption alone if answer is empty
            return "No good Wolfram Alpha Result was found"
        else:
            return f"Assumption: {assumption} \nAnswer: {answer}"
        
app_id = get_aws_parameter("WOLFRAM_ALPHA_APPID", decrypt=True)

class WolframAlphaInput(BaseModel):
    """Input model for Wolfram Alpha tool."""
    query: str = Field(description="Query to be asked to Wolfram Alpha")

class WolframAlphaTool(BaseTool):
    """LangChain tool for querying Wolfram Alpha."""
    name = "Wolfram Alpha"
    description = "Useful when you need to do math calculations!"
    args_schema: Type[BaseModel] = WolframAlphaInput

    def __init__(self):
        super().__init__()
        # Non creare qui l'istanza di WolframAlphaAPIWrapper

    def get_wolfram_client(self):
        """Crea e restituisce un'istanza di WolframAlphaAPIWrapper."""
        return WolframAlphaAPIWrapper(wolfram_alpha_appid=app_id)

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """Run the given query using the Wolfram Alpha API."""
        wolfram_client = self.get_wolfram_client()
        return wolfram_client.run(query)