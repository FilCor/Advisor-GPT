from crewai import Task
from textwrap import dedent

class StockAnalysisTasks():
  def research(self, agent, company):
    return Task(description=dedent(f"""
        Collect recent news articles, press
        releases, and market analyses related to the stock and
        its industry.
        Pay special attention to any significant events, market
        sentiments, and analysts' opinions. Also include upcoming 
        events like earnings and others.
  
        Your final answer MUST be a report that includes among the ther informations a
        comprehensive summary of the latest news, any notable
        shifts in market sentiment, and potential impacts on 
        the stock.
        Also make sure to return the stock ticker.
        
        {self.__tip_section()}
  
        Make sure to use the most recent data as possible.
  
        Selected company by the customer: {company}
      """),
      agent=agent
    )
    
  def financial_analysis(self, agent): 
    return Task(description=dedent(f"""
        Conduct a thorough analysis of the stock's financial
        health and market performance. 
        This includes examining key financial metrics such as
        P/E ratio, EPS growth, revenue trends, and 
        debt-to-equity ratio.

        Your final report MUST expand on the report provided
        but now including a clear assessment of the stock's
        financial standing, its strengths and weaknesses, 
        and how it fares against its competitors in the current
        market scenario.
        Be verbose!
        
        {self.__tip_section()}

        Make sure to use the most recent data possible.
      """),
      agent=agent
    )
  
  def timeseries_analysis(self, agent): 
    return Task(description=dedent(f"""
        Conduct a thorough analysis of the stock's price performances.
        ALWAYS analyze the stock's price and return performance also in comparison 
        to its industry peers and overall market trends.
                                   
        You HAVE to look at least at year to date, 1 year, 3 years and 5 years performances!

        Your final report MUST expand on the report provided
        but now including a clear assessment of the stock's
        past performances expecially YTD, 1 year, 3 and 5 years
        Be verbose!
        
        {self.__tip_section()}

        Make sure to use the most recent data possible.
      """),
      agent=agent
    )

  def filings_analysis(self, agent):
    return Task(description=dedent(f"""
        Analyze the latest 10-Q and 10-K filings from EDGAR for
        the stock in question. 
        Focus on key sections like Management's Discussion and
        Analysis, financial statements, insider trading activity, 
        and any disclosed risks.
        Provide in you report punctual data you have found and insights that could influence
        the stock's future performance.

        Your final answer MUST be an expanded report that now
        also highlights significant findings from these filings,
        including any red flags or positive indicators for
        your customer.
                                   
        you MUST NOT delete any previous information in the report, just add your informations, just add your informations and report the full analysys that your colleague gave you
        {self.__tip_section()}        
      """),
      agent=agent
    )

  def recommend(self, agent):
    return Task(description=dedent(f"""
        Review an organize the report provided by the
        Financial Analyst, the Timeseries Analyst, the Research Analyst and the filings analyst.
        Combine these insights to form a comprehensive report for a equity analyst.
        I want a long and detailed report.
         
        You MUST Consider all aspects, including financial
        health, market sentiment, qualitative data from
        EDGAR filings and stock performances. If you have report them!

        Make sure to include a section that shows insider 
        trading activity, and upcoming events like earnings.

        Make it pretty and well formatted for your analyst.
        
        Start with an executive summary with the key points and then summarize the iformation provided.

        you MUST NOT include any parts of the prompt in the final report.                                                
        {self.__tip_section()}
      """),
      agent=agent
    )

  def __tip_section(self):
    return "If you do your BEST WORK, I'll give you a $1,000,000 commission!"
