from typing import Annotated, List, Dict, Any, Optional
from langchain_core.tools import tool
from dotenv import load_dotenv
import requests
import os
import json

# load environment variables from .env file
load_dotenv()

@tool
def ollama_model() -> Annotated[dict, "JSON response with running models information"]:
    """Gets the list of running ollama models."""
    OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:31434')
    response = requests.get(f"{OLLAMA_HOST}/api/ps")
    response.raise_for_status()  # Raises an HTTPError for bad responses
    return response.json()

@tool
def ollama_model_details(model_name: Annotated[str, "The name of the model to get details for"]) -> Annotated[dict, "JSON response with model details"]:
    """Gets model details."""
    OLLAMA_HOST = os.getenv('OLLAMA_HOST', 'http://localhost:31434')
    response = requests.post(f"{OLLAMA_HOST}/api/show", json={"model": model_name})
    response.raise_for_status()  # Raises an HTTPError for bad responses
    return response.json()

if __name__ == "__main__":

    import pprint
    pp = pprint.PrettyPrinter(indent=1, width=200, sort_dicts=False)

    # results = ollama_model.invoke(input={})
    results = ollama_model_details.invoke(input={'model_name':'qwen3:14b'})
    pp.pprint(results)
