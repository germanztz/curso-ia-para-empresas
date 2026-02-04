from typing import Annotated, List, Dict, Any, Optional
from langchain_core.tools import tool
import os
# load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from ddgs import DDGS
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document
import requests
from bs4 import BeautifulSoup
import json
import re

@tool
def scrape_webpages(url: Annotated[str, "The URL of the webpage to scrape"],
    extract_links: Annotated[bool, "Whether to extract links from the content"]=False,
    min_words_per_line: Annotated[int, "Minimum number of words per line to include in the document"] = 5,
    ) -> Annotated[List[Document], "Tha page document"]:
    """Scrape and read the provided web page url for detailed information"""
    loader = WebBaseLoader(url, raise_for_status=True)
    docs = loader.load()

    # def get_root_host(url):
    #     parsed_url = urlparse(url)
    #     hostname = parsed_url.hostname
    #     parts = hostname.split('.')
    #     # Return the last two parts joined by a dot
    #     return '.'.join(parts[-2:])

    # internal_host = get_root_host(response.url)     

    for doc in docs:
        if extract_links:
            doc.metadata['links'] = list(set(re.findall(r'https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w.])*)?(?:#(?:[\w.])*)?)?', doc.page_content)))
        text = [line.strip() for line in doc.page_content.split('\n') if len(line.strip().split()) >= min_words_per_line]
        doc.page_content = '\n'.join(text)        
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

    import pprint
    pp = pprint.PrettyPrinter(indent=1, width=200, sort_dicts=False)

    # results = web_search.invoke(input={'query':'langchain local ollama multi-agent deep research system', 'num_results':3})
    results = scrape_webpages.invoke(input={'url':'https://en.wikipedia.org/wiki/LangChain'})
    pp.pprint(results)
