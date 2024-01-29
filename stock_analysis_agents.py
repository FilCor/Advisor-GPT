from crewai import Agent
import os

from tools.browser_tools import BrowserTools
from tools.calculator_tools import WolframAlphaTool
from tools.search_tools import SearchTools
from tools.sec_tools import SECTools
from tools.stock_ts import StockPriceTool


from langchain.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain.llms import Ollama
from langchain.chat_models import ChatOpenAI
from langchain_community.tools.google_finance import GoogleFinanceQueryRun
from langchain_community.utilities.google_finance import GoogleFinanceAPIWrapper

# llm = ChatOpenAI(model='gpt-3.5-turbo', base_url="http://127.0.0.1:8000",openai_api_key="sk-00a5k_7O2hXR_DUYjNPNQg")
# litellm_chat = ChatLiteLLM(model="gpt-3.5-turbo",openai_api_key="sk-00a5k_7O2hXR_DUYjNPNQg",api_base="http://0.0.0.0:8000") # Loading GPT-3.5
#ollama_openchat = Ollama(model="dolphin-mixtral")

# llm = GoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyA2i2P9hlJ7lSkOhMdYfgqtCkC7Vwj-pPE")


from aws_utilis import get_aws_parameter

app_id = get_aws_parameter("WOLFRAM_ALPHA_APPID", decrypt=True)
polygon_api_key = get_aws_parameter("POLIGON_API_KEY", decrypt=True)

# Recupera le chiavi API da AWS Systems Manager Parameter Store
openai_api_key = get_aws_parameter("OPENAI_API_KEY", decrypt=True)
serpapi_api_key = get_aws_parameter("SERPAPI_API_KEY", decrypt=True)
llm = ChatOpenAI(model="gpt-3.5-turbo-16k", openai_api_key=openai_api_key, max_tokens=8000, temperature=0.3)
Googlefinance_tool = GoogleFinanceQueryRun(api_wrapper=GoogleFinanceAPIWrapper(serp_api_key=serpapi_api_key))
# Ora puoi utilizzare queste variabili dove necessario nel tuo codice

class StockAnalysisAgents():
  def financial_analyst(self):

    wolfram_alpha_tool = WolframAlphaTool()
    stock_price_tool = StockPriceTool()

    return Agent(
      role='the best Financial Analyst ever',
      goal="""Impress all coworkers with your financial data 
      and market trends analysis""",
      backstory="""The most seasoned financial analyst with 
      lots of expertise in stock market analysis and investment
      strategies that is working for a super mega important asset manager.""",
      verbose=True,
      llm = llm,
      allow_delegation = False,
      #llm=ollama_openchat,
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        wolfram_alpha_tool,
        stock_price_tool,
        SECTools.search_10q,
        SECTools.search_10k

      ]
    )
  
  def equity_analyst(self):

    wolfram_alpha_tool = WolframAlphaTool()
    stock_price_tool = StockPriceTool()

    return Agent(
      role='the best equity Analyst ever',
      goal="""Impress all coworkers with your equity analysis""",
      backstory="""The most seasoned equity analyst with 
      lots of expertise in stock market analysis and investment
      strategies that is working for a super mega important asset manager.""",
      verbose=True,
      llm = llm,
      allow_delegation = False,
      #llm=ollama_openchat,
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        wolfram_alpha_tool,
        stock_price_tool
      ]
    )

  def research_analyst(self):
    return Agent(
      role='Staff Research Analyst',
      goal="""Being the best at gather, interpret data and amaze
      your coworker with it""",
      backstory="""Known as the BEST research analyst, you're
      skilled in sifting through news, company announcements, 
      and market sentiments. Now you're working on a super 
      important analysis""",
      verbose=True,
      #llm=ollama_openchat,
      llm = llm,
      allow_delegation = False,
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        SearchTools.search_news,
        #SECTools.search_10q,
        #SECTools.search_10k
      ]
  )

  def investment_advisor(self):
    wolfram_alpha_tool = WolframAlphaTool()
    return Agent(
      role='Private Investment Advisor',
      goal="""Impress your coworker with full analyses over stocks
      and completer investment recommendations""",
      backstory="""You're the most experienced investment advisor
      and you combine various analytical insights to formulate
      strategic report. You are now working for
      a super important manging director you need to impress.""",
      verbose=True,
      #llm=ollama_openchat,
      llm = llm,
      allow_delegation = False,
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        SearchTools.search_news,
        wolfram_alpha_tool
      ]
    )