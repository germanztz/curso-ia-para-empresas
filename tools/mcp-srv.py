from mcp.server.fastmcp import FastMCP
from langchain_core.tools import tool
from langchain_mcp_adapters.tools import to_fastmcp
import web_operations
import file_operations
import bash_operations
import datetime

@tool()
def get_current_time():
    """Returns current system time."""
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

tools=[
    to_fastmcp(get_current_time),
    ]

for module in [web_operations, file_operations, bash_operations]:
    for func in dir(module):
        # check if func is a tool method of the module
        if (type(getattr(module, func)).__name__ == 'StructuredTool'):
            tools.append(to_fastmcp(getattr(module, func)))


if __name__ == "__main__":

    # print(execute_bash.invoke("pwd"))
    # print(web_search.invoke(input={'query':'langchain local ollama multi-agent deep research system'}))
    # print(scrape_webpages.invoke(input={'url':'https://discuss.streamlit.io/t/build-a-multi-agent-ai-researcher-using-ollama-langgraph-and-streamlit/116726'}))
    # print(bash_operations.ollama_model.invoke(input=''))
    # print(bash_operations.check_port_open.invoke(input={'destination':'localhost', 'port':'8080'}))
    # print(web_operations.ollama_model.invoke(input=''))
    # print(web_operations.ollama_model_details.invoke(input={'model_name':'qwen3:14b'}))
    FastMCP("mcp", tools=tools).run(transport="stdio")


    
