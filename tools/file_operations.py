"""Tools for file operations."""

from typing import Annotated, List, Dict, Any, Optional, Literal
# from langchain_experimental.utilities import PythonREPL
from langchain.tools import tool
import os

@tool
def write_file(
    file_path: Annotated[str, "The full path to the file where content will be written."],
    mode: Annotated[Literal['w', 'x', 'a'], "Mode in which the file is opened. 'w' for writing, 'x' for creating and writing to a new file, and 'a' for appending"],
    content: Annotated[str, "The content to be written to the file."],
    encoding: Annotated[Optional[str], "The encoding of the file."] = 'utf-8'
    ) -> Annotated[str, "Result message."]:
    """Writes text content to a file in append or overwrite mode."""
    try:
        content = '\n'+content if mode == 'a' else content
        with open(file_path, mode, encoding=encoding) as f:
            f.write(content)
        return f"Content successfully written to {file_path}"
    except Exception as e:
        return f"Error writing to file: {str(e)}"

@tool
def read_file(
    file_path: Annotated[str, "Path to the file to read"], 
    encoding: Annotated[Optional[str], "The encoding of the file."] = 'utf-8',
    start: Annotated[Optional[int], "The start line. Default is 0"] = 0,
    end: Annotated[Optional[int], "The end line. Default is None"] = None,    
    ) -> Annotated[str, "Content of the file"]:
    """Read content from a file."""
    try:
        with open(file_path, "r", encoding=encoding) as f:
            lines = f.readlines()
            return "".join(lines[start:end])
      
        return content
    except Exception as e:
        return f"Error reading {file_path}: {str(e)}"

@tool
def create_outline(
    points: Annotated[List[str], "List of main points or sections."],
    file_path: Annotated[str, "File path to save the outline."],
) -> Annotated[str, "Path of the saved outline file."]:
    """Create and save an outline."""
    with (file_path).open("w") as file:
        for i, point in enumerate(points):
            file.write(f"{i + 1}. {point}\n")
    return f"Outline saved to {file_path}"

@tool
def edit_document(
    file_path: Annotated[str, "Path of the document to be edited."],
    inserts: Annotated[
        Dict[int, str],
        "Dictionary where key is the line number (1-indexed) and value is the text to be inserted at that line.",
    ],
) -> Annotated[str, "Path of the edited document file."]:
    """Edit a document by inserting text at specific line numbers."""

    with (file_path).open("r") as file:
        lines = file.readlines()

    sorted_inserts = sorted(inserts.items())

    for line_number, text in sorted_inserts:
        if 1 <= line_number <= len(lines) + 1:
            lines.insert(line_number - 1, text + "\n")
        else:
            return f"Error: Line number {line_number} is out of range."

    with (file_path).open("w") as file:
        file.writelines(lines)

    return f"Document edited and saved to {file_name}"


# Warning: This executes code locally, which can be unsafe when not sandboxed
# repl = PythonREPL()
# @tool
# def python_repl_tool(
#     code: Annotated[str, "The python code to execute to generate your chart."],
# ):
#     """Use this to execute python code. If you want to see the output of a value,
#     you should print it out with `print(...)`. This is visible to the user."""
#     try:
#         result = repl.run(code)
#     except BaseException as e:
#         return f"Failed to execute. Error: {repr(e)}"
#     return f"Successfully executed:\n```python\n{code}\n```\nStdout: {result}"

if __name__ == "__main__":

    print(write_file.invoke(input={'content':'this is a test\n', 'file_path':'/tmp/file.txt', 'mode': 'w'}))
    print(read_file.invoke(input={'file_path':'/tmp/file.txt', 'start':0, 'end':9998}))
    
    # print(web_scrape("https://docs.langflow.org/components-custom-components"))
    # print(execute_bash.invoke("pwd"))

    # mcp = FastMCP("file-operations-mcp", tools=[write_file, read_file, ])
    # mcp.run(transport="stdio")
