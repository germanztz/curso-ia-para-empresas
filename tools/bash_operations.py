from langchain_core.tools import tool
from typing import Annotated, List, Dict, Any, Optional
import subprocess
import json


def subproc_run(command, timeout = 60 ):
    """Execute a bash command."""

    return subprocess.run(command, shell=True, timeout=timeout, capture_output=True, text=True)


@tool
def execute_bash(command: Annotated[str, "The bash command to execute"], 
    timeout: Annotated[Optional[int], "Timeout in seconds."] = 60
    ) -> Annotated[dict, "Output object of the command {command, return_code, stdout, stderr}"]:
    """Execute a bash command."""

    return subproc_run(command, timeout=timeout)

@tool
def check_port_open(port: Annotated[int, "port number to check"], 
    destination: Annotated[str, "destination host to check"] = 'localhost'
    ) -> Annotated[subprocess.CompletedProcess, "check result"]:
    """Checks is an open port on the destination host."""

    return subproc_run(f"nc -zv -w 10 {destination} {port}", timeout=10)
