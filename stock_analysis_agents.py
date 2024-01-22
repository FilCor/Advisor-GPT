from crewai import Agent
import os

from tools.browser_tools import BrowserTools
from tools.calculator_tools import CalculatorTools
from tools.search_tools import SearchTools
from tools.sec_tools import SECTools

from langchain.tools.yahoo_finance_news import YahooFinanceNewsTool
from langchain.llms import Ollama
from langchain.chat_models import ChatOpenAI
from langchain_community.tools.google_finance import GoogleFinanceQueryRun
from langchain_community.utilities.google_finance import GoogleFinanceAPIWrapper

# llm = ChatOpenAI(model='gpt-3.5-turbo', base_url="http://127.0.0.1:8000",openai_api_key="sk-00a5k_7O2hXR_DUYjNPNQg")
# litellm_chat = ChatLiteLLM(model="gpt-3.5-turbo",openai_api_key="sk-00a5k_7O2hXR_DUYjNPNQg",api_base="http://0.0.0.0:8000") # Loading GPT-3.5
#ollama_openchat = Ollama(model="dolphin-mixtral")

# llm = GoogleGenerativeAI(model="gemini-pro", google_api_key="AIzaSyA2i2P9hlJ7lSkOhMdYfgqtCkC7Vwj-pPE")
llm = ChatOpenAI(model="gpt-3.5-turbo-16k")
Googlefinance_tool = GoogleFinanceQueryRun(api_wrapper=GoogleFinanceAPIWrapper())
from aws_utils import get_aws_parameter

# Recupera le chiavi API da AWS Systems Manager Parameter Store
openai_api_key = get_aws_parameter("OPENAI_API_KEY", decrypt=True)
serpapi_api_key = get_aws_parameter("SERPAPI_API_KEY", decrypt=True)

# Ora puoi utilizzare queste variabili dove necessario nel tuo codice


class StockAnalysisAgents():
  def financial_analyst(self):
    return Agent(
      role='The Best Financial Analyst',
      goal="""Impress all customers with your financial data 
      and market trends analysis""",
      backstory="""The most seasoned financial analyst with 
      lots of expertise in stock market analysis and investment
      strategies that is working for a super important customer.""",
      verbose=True,
      llm = llm,
      allow_delegation = False,
      #llm=ollama_openchat,
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        CalculatorTools.calculate,
        SECTools.search_10q,
        SECTools.search_10k
      ]
    )

  def research_analyst(self):
    return Agent(
      role='Staff Research Analyst',
      goal="""Being the best at gather, interpret data and amaze
      your customer with it""",
      backstory="""Known as the BEST research analyst, you're
      skilled in sifting through news, company announcements, 
      and market sentiments. Now you're working on a super 
      important customer""",
      verbose=True,
      #llm=ollama_openchat,
      llm = llm,
      allow_delegation = False,
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        SearchTools.search_news,
        Googlefinance_tool,
        SECTools.search_10q,
        SECTools.search_10k
      ]
  )

  def investment_advisor(self):
    return Agent(
      role='Private Investment Advisor',
      goal="""Impress your customers with full analyses over stocks
      and completer investment recommendations""",
      backstory="""You're the most experienced investment advisor
      and you combine various analytical insights to formulate
      strategic investment advice. You are now working for
      a super important customer you need to impress.""",
      verbose=True,
      #llm=ollama_openchat,
      llm = llm,
      allow_delegation = False,
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        SearchTools.search_news,
        CalculatorTools.calculate,
      ]
    )