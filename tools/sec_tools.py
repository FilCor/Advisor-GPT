import os

import requests

from langchain.tools import tool
from langchain.text_splitter import CharacterTextSplitter
#from langchain.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings

from sec_api import QueryApi
from unstructured.partition.html import partition_html
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


from aws_utilis import get_aws_parameter

# Recupera le chiavi API da AWS Systems Manager Parameter Store
sec_api_api_key = get_aws_parameter("SEC_API_API_KEY", decrypt=True)
openai_api_key = get_aws_parameter("OPENAI_API_KEY", decrypt=True)

# Ora puoi utilizzare queste variabili dove necessario nel tuo codice


# Ora puoi utilizzare queste variabili dove necessario nel tuo codice


class SECTools():
  @tool("Search 10-Q form")
  def search_10q(data):
    """
    Useful to search information from the latest 10-Q form for a
    given stock.
    The input to this tool should be a pipe (|) separated text of
    length two, representing the stock ticker you are interested and what
    question you have from it.
		For example, `AAPL|what was last quarter's revenue`.
    """
    stock, ask = data.split("|")
    queryApi = QueryApi(api_key=sec_api_api_key)
    query = {
      "query": {
        "query_string": {
          "query": f"ticker:{stock} AND formType:\"10-Q\""
        }
      },
      "from": "0",
      "size": "1",
      "sort": [{ "filedAt": { "order": "desc" }}]
    }

    fillings = queryApi.get_filings(query)['filings']
    if len(fillings) == 0:
      return "Sorry, I couldn't find any filling for this stock, check if the ticker is correct."
    link = fillings[0]['linkToFilingDetails']
    answer = SECTools.__embedding_search(link, ask)
    return answer

  @tool("Search 10-K form")
  def search_10k(data):
    """
    Useful to search information from the latest 10-K form for a
    given stock.
    The input to this tool should be a pipe (|) separated text of
    length two, representing the stock ticker you are interested, what
    question you have from it.
    For example, `AAPL|what was last year's revenue`.
    """
    stock, ask = data.split("|")
    queryApi = QueryApi(api_key=sec_api_api_key)
    query = {
      "query": {
        "query_string": {
          "query": f"ticker:{stock} AND formType:\"10-K\""
        }
      },
      "from": "0",
      "size": "1",
      "sort": [{ "filedAt": { "order": "desc" }}]
    }

    fillings = queryApi.get_filings(query)['filings']
    if len(fillings) == 0:
      return "Sorry, I couldn't find any filling for this stock, check if the ticker is correct."
    link = fillings[0]['linkToFilingDetails']
    answer = SECTools.__embedding_search(link, ask)
    return answer

  def __embedding_search(url, ask):
    text = SECTools.__download_form_html(url)
    elements = partition_html(text=text)
    content = "\n".join([str(el) for el in elements])
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 1000,
        chunk_overlap  = 150,
        length_function = len,
        is_separator_regex = False,
    )
    docs = text_splitter.create_documents([content])
    logger.info(f"Starting embedding search for {ask}")
    retriever = FAISS.from_documents(
      docs, OpenAIEmbeddings(openai_api_key=openai_api_key)
    ).as_retriever()
    answers = retriever.get_relevant_documents(ask, top_k=4)
    logger.info(f"Completed embedding search for {ask}")
    answers = "\n\n".join([a.page_content for a in answers])
    return answers

  def __download_form_html(url):
    headers = {
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
      'Accept-Encoding': 'gzip, deflate, br',
      'Accept-Language': 'en-US,en;q=0.9,pt-BR;q=0.8,pt;q=0.7',
      'Cache-Control': 'max-age=0',
      'Dnt': '1',
      'Sec-Ch-Ua': '"Not_A Brand";v="8", "Chromium";v="120"',
      'Sec-Ch-Ua-Mobile': '?0',
      'Sec-Ch-Ua-Platform': '"macOS"',
      'Sec-Fetch-Dest': 'document',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-Site': 'none',
      'Sec-Fetch-User': '?1',
      'Upgrade-Insecure-Requests': '1',
      'User-Agent':'Dummy Company anna.sassin@dummy.com',
      'Host':'www.sec.gov'
    }

    response = requests.get(url, headers=headers)
    return response.text
