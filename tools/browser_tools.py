import json
import os

import requests
from crewai import Agent, Task
from langchain.tools import tool
from unstructured.partition.html import partition_html
from aws_utilis import get_aws_parameter
from langchain.chat_models import ChatOpenAI

# Recupera le chiavi API da AWS Systems Manager Parameter Store
browserless_api_key = get_aws_parameter("BROWSERLESS_API_KEY", decrypt=True)
openai_api_key = get_aws_parameter("OPENAI_API_KEY", decrypt=True)

# Ora puoi utilizzare queste variabili dove necessario nel tuo codice
llm = ChatOpenAI(model="gpt-3.5-turbo-16k", openai_api_key=openai_api_key)



class BrowserTools():

  @tool("Scrape website content")
  def scrape_and_summarize_website(website):
    """Useful to scrape and summarize a website content"""
    url = f"https://chrome.browserless.io/content?token={browserless_api_key}"
    payload = json.dumps({"url": website})
    headers = {'cache-control': 'no-cache', 'content-type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)
    elements = partition_html(text=response.text)
    content = "\n\n".join([str(el) for el in elements])
    content = [content[i:i + 8000] for i in range(0, len(content), 8000)]
    summaries = []
    for chunk in content:
      agent = Agent(
          role='Principal Researcher',
          goal=
          'Do amazing research and summaries based on the content you are working with',
          backstory=
          "You're a Principal Researcher at a big company and you need to do research about a given topic.",
          llm = llm,
          allow_delegation=False)
      task = Task(
          agent=agent,
          description=
          f'Analyze and summarize the content below, make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}'
      )
      summary = task.execute()
      summaries.append(summary)
    return "\n\n".join(summaries)
