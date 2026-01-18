from mcp.server.fastmcp import FastMCP
from langchain_core.tools import tool
from langchain_mcp_adapters.tools import to_fastmcp
from web_operations import scrape_webpages, web_search
from file_operations import read_file, write_file
from bash_executor import execute_bash

@tool()
def get_current_time():
    """Returns current system time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

tools=[
    to_fastmcp(get_current_time),
    to_fastmcp(web_search),
    to_fastmcp(scrape_webpages),
    to_fastmcp(read_file),
    to_fastmcp(write_file),
    to_fastmcp(execute_bash),
    ]

if __name__ == "__main__":

    # print(web_search("Create custom components langflow"))
    # print(web_scrape("https://docs.langflow.org/components-custom-components"))
    # print(execute_bash.invoke("pwd"))
    # print(web_search.invoke(input={'query':'langchain local ollama multi-agent deep research system'}))
    # print(scrape_webpages.invoke(input={'urls':['https://discuss.streamlit.io/t/build-a-multi-agent-ai-researcher-using-ollama-langgraph-and-streamlit/116726']}))

    FastMCP("mcp", tools=tools).run(transport="stdio")
    
