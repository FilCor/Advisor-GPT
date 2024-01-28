import os
from crewai import Crew
from textwrap import dedent
from dotenv import load_dotenv
from pydantic import BaseModel
from aws_utilis import get_aws_parameter


from stock_analysis_agents import StockAnalysisAgents
from stock_analysis_tasks import StockAnalysisTasks
openai_api_key = get_aws_parameter("OPENAI_API_KEY", decrypt=True)


class FinancialCrew:
  def __init__(self, company):
    self.company = company

  def run(self):
    agents = StockAnalysisAgents()
    tasks = StockAnalysisTasks()

    research_analyst_agent = agents.research_analyst()
    financial_analyst_agent = agents.financial_analyst()
    investment_advisor_agent = agents.investment_advisor()

    research_task = tasks.research(research_analyst_agent, self.company)
    financial_task = tasks.financial_analysis(financial_analyst_agent)
    timeseries_task = tasks.timeseries_analysis(financial_analyst_agent)
    filings_task = tasks.filings_analysis(financial_analyst_agent)
    recommend_task = tasks.recommend(investment_advisor_agent)

    crew = Crew(
      agents=[
        research_analyst_agent,
        financial_analyst_agent,
        financial_analyst_agent,
        financial_analyst_agent,
        investment_advisor_agent
      ],
      tasks=[
        research_task,
        financial_task,
        timeseries_task,
        filings_task,
        recommend_task
      ],
      verbose=2,
    )

    result = crew.kickoff()
    return result
# Run with Uvicorn
# uvicorn yourfilename:app --reload
