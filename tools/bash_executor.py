from langchain_core.tools import tool
from typing import Annotated, List, Dict, Any, Optional
import subprocess


@tool
def execute_bash(command: Annotated[str, "The bash command to execute"], 
    timeout: Annotated[Optional[int], "Timeout in seconds."] = 60
    ) -> Annotated[dict, "Output object of the command {command, return_code, stdout, stderr}"]:
    """Execute a bash command."""
    try:
        # Run the command
        result = subprocess.run(command,shell=True,timeout=timeout,capture_output=True,text=True)
                
        return {"command": command,"return code": result.returncode,
            "stdout": result.stdout.strip(),"stderr": result.stderr.strip(),
        }
    except subprocess.TimeoutExpired:
        return {"command": command,"return code": -1,"stdout": None,
            "stderr": f"Error executing command: Command timed out after {timeout} seconds",
        }
    except Exception as e:
        return {"command": command,"return code": -1,"stdout": None,
            "stderr": f"Error executing command: {str(e)}",
        }
