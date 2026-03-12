#!/usr/bin/env python3
import os
print(f"uid: {os.geteuid()}")
"""
CLI tool to interact with Qwen3 LLM using LangChain's ChatOllama and a custom MCP server.
"""

import argparse
import sys
import asyncio

from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.prompts import ChatPromptTemplate


def parse_args():
    parser = argparse.ArgumentParser(
        description="Chat with Qwen3 LLM using LangChain + MCP tools"
    )
    parser.add_argument("prompt", type=str, help="User prompt to send to the LLM")
    parser.add_argument(
        "--model", 
        default="qwen3.5", 
        help="Ollama model to use (default: qwen3)"
    )
    parser.add_argument(
        "--mcp-server", 
        default="/home/daimler/workspaces/curso-ia-para-empresas/tools/mcp-srv.py", 
        help="Path to MCP server script (default: /home/daimler/workspaces/curso-ia-para-empresas/tools/mcp-srv.py)"
    )
    parser.add_argument(
        "--verbose", 
        action="store_true", 
        help="Enable verbose output (debug info)"
    )
    return parser.parse_args()


async def run_async(args):
    try:
        # 1. Create MCP client connection (stdio transport)
        mcp_client = MultiServerMCPClient({"mcp": {"command": "python","args": [args.mcp_server], "transport": "stdio", }})

        # 2. Get available tools from MCP server (async)
        tools = await mcp_client.get_tools()

        if args.verbose:
            print(f"Connected to MCP server at {args.mcp_server}", file=sys.stderr)
            print(f"Available MCP tools: {[t.name for t in tools]}", file=sys.stderr)

        # 3. Initialize Ollama model
        llm = ChatOllama(
            model=args.model,
            reasoning=False,
            # temperature=0.7,
            # num_predict=1024
        )

        # 4. Bind tools to the LLM
        llm_with_tools = llm.bind_tools(tools)

        # 5. Prepare chat history (system + user prompt)
        system_prompt = f""". 
You are a helpful AI assistant with access to MCP tools. Use them when appropriate.
Answer only what is asked — no greetings, no explanations, no extra text. 
Be brief and precise.
- SO: Ubuntu 25
- PWD: {os.getcwd()}
- Language: Spanish 
"""
        messages = [
            SystemMessage(content=system_prompt),  # se incluye la info del sistema al inicio
            HumanMessage(content=args.prompt)
        ]
        # 6. Invoke the chain (async)
        response = await llm_with_tools.ainvoke(messages)

        # 7. Handle response: print content or execute tools
        if response.tool_calls:
            print("LLM wants to use tools:", response.tool_calls, file=sys.stderr)
            for tool_call in response.tool_calls:
                tool_name = tool_call["name"]
                tool_args = tool_call["args"]

                tool_to_call = next((t for t in tools if t.name == tool_name), None)
                if tool_to_call:
                    try:
                        # Try async invoke first
                        result = await tool_to_call.ainvoke(tool_args)
                    except AttributeError:
                        # Fall back to sync invoke in a thread
                        import asyncio
                        result = await asyncio.to_thread(tool_to_call.invoke, tool_args)

                    if args.verbose:
                        print(f"Executed tool '{tool_name}' with args {tool_args} → result: {result}", file=sys.stderr)

                    messages.append(AIMessage(content=f"Tool result: {result}"))
                    messages.append(HumanMessage(content="Please summarize the tool execution result."))
                    final_response = await llm_with_tools.ainvoke(messages)
                    print(final_response.content)
                else:
                    print(f"Unknown tool requested: {tool_name}", file=sys.stderr)
                    print(response.content)
        else:
            print(response.content)

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    args = parse_args()
    asyncio.run(run_async(args))


if __name__ == "__main__":
    main()