from typing import Annotated, List, Dict, Any, Optional
from langchain_core.tools import tool
import os
import pprint
# load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from ddgs import DDGS
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
import requests
from bs4 import BeautifulSoup
pp = pprint.PrettyPrinter(indent=1, width=200, sort_dicts=False)


# @tool
# def web_scrape(url: str, elements: str = "p,h1,h2,h3,h4,h5,code,pre") -> str:
#     """
#     Scrape the content from a webpage.
    
#     Args:
#         url: The URL of the webpage to scrape
#         elements: Comma-separated list of HTML elements to extract (default: p,h1,h2,h3,h4,h5,code,pre)
        
#     Returns:
#         Extracted text content from the webpage
#     """
#     try:
#         headers = {
#             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
#         }
#         response = requests.get(url, headers=headers, timeout=10)
#         response.raise_for_status()
        
#         soup = BeautifulSoup(response.text, "html.parser")
        
#         # Extract text from the specified elements
#         element_list = elements.split(',')
#         content = []
        
#         for element_type in element_list:
#             element_type = element_type.strip()
#             for element in soup.find_all(element_type):
#                 text = element.get_text().strip()
#                 if text:
#                     # Add element type as a prefix for context
#                     content.append(f"[{element_type}] {text}")
        
#         return "\n".join(content)
#     except Exception as e:
#         return f"Error scraping {url}: {str(e)}"


# @tool
# def scrape_webpages(urls: Annotated[List[str], "The URLs list of the webpages to scrape"]
#     ) -> Annotated[List[Document], "Tha page document"]:
#     """Scrape and read the provided web pages urls for detailed information"""
#     loader = WebBaseLoader(urls)
#     docs = loader.load()
#     for doc in docs:
#         doc.page_content = doc.page_content.replace('\n'," ")
#     return docs


# @tool
# def web_search(queries: Annotated[List[str], "list of search queries to look up"], 
#     num_results: Annotated[Optional[int], "Max search results per query to return (default: 5)"] = 5
#     ) ->  Annotated[List[Dict[str, str]], "The search results"]:
#     """A Internet search engine. Useful for when you need to answer questions about current events"""
#     try:
#         with DDGS() as ddgs:
#             results = []
#             for query in queries:
#                 results += ddgs.text(query,max_results=num_results, backend='lite')
#             return results
#     except Exception as e:
#         return [{"Error": f"{str(e)}"}]


@tool
def scrape_webpages(url: Annotated[str, "The URL of the webpage to scrape"]
    ) -> Annotated[List[Document], "Tha page document"]:
    """Scrape and read the provided web page url for detailed information"""
    loader = WebBaseLoader(url)
    docs = loader.load()
    for doc in docs:
        doc.page_content = doc.page_content.replace('\n'," ")
    return docs


@tool
def web_search(query: Annotated[str, "search query to look up"], 
    num_results: Annotated[Optional[int], "Max search results per query to return (default: 5)"] = 5
    ) ->  Annotated[List[Dict[str, str]], "The search results"]:
    """A Internet search engine. Useful for when you need to answer questions about current events"""
    try:
        with DDGS() as ddgs:
            return ddgs.text(query,max_results=num_results, backend='lite')
    except Exception as e:
        return [{"Error": f"{str(e)}"}]

if __name__ == "__main__":

    # results = [web_search, scrape_webpages]
    # results = tavily_tool.invoke(input={'query':"langchain local ollama multi-agent deep research system"})  
    # pp.pprint(web_search.invoke(input={'query':'langchain local ollama multi-agent deep research system'}))
    pp.pprint(scrape_webpages.invoke(input={'url':'https://discuss.streamlit.io/t/build-a-multi-agent-ai-researcher-using-ollama-langgraph-and-streamlit/116726'}))
    # results = web_scrape.invoke(input={'url':'https://discuss.streamlit.io/t/build-a-multi-agent-ai-researcher-using-ollama-langgraph-and-streamlit/116726'})
    # pp.pprint(results)
    # from mcp.server.fastmcp import FastMCP
    # from langchain_mcp_adapters.tools import to_fastmcp

    # tools=[to_fastmcp(scrape_webpages), to_fastmcp(web_search)]
    # FastMCP("mcp_web_ops", tools=tools).run(transport="stdio")
