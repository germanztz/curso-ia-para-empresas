#!/usr/bin/env python3
"""
ollama-cli.py: CLI para interactuar con un LLM (Ollama) + MCP tools.
Uso: python ollama-cli.py "tu prompt aquí"
"""

import argparse
import subprocess
import sys
import time

from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MCPClient
from langchain_core.messages import HumanMessage


def create_mcp_client():
    """Inicia el servidor MCP como subproceso y devuelve un cliente MCP."""
    # Ruta al script MCP
    mcp_script = "/home/daimler/workspaces/curso-ia-para-empresas/tools/mcp-srv.py"
    
    # Inicia el servidor MCP en stdin/stdout
    process = subprocess.Popen(
        [sys.executable, mcp_script],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    # Esperar 2 segundos para que el servidor MCP inicie
    time.sleep(2)
    if process.poll() is not None:
        raise RuntimeError(f"MCP server failed to start. Error:\n{process.stderr.read()}")

    # Crea y conecta el cliente MCP
    client = MCPClient(process.stdout, process.stdin)
    return client, process


def stream_response(client, prompt: str):
    """Llama al modelo con herramientas MCP y muestra la respuesta en streaming."""
    try:
        # Crea el LLM conectado al cliente MCP
        llm = ChatOllama(
            model="qwen3.3:0.8b",  # ajusta el modelo según tu entorno
            mcp_client=client,
            temperature=0.7,
        )

        # Invoca el modelo en modo streaming
        for chunk in llm.stream([HumanMessage(content=prompt)]):
            # Muestra solo el contenido textual (evita tool calls en stream)
            if hasattr(chunk, "content") and chunk.content:
                print(chunk.content, end="", flush=True)

    except Exception as e:
        print(f"Error durante la generación: {e}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(
        description="Consulta a un LLM (Ollama) con herramientas MCP vía CLI."
    )
    parser.add_argument("prompt", nargs="*", help="Prompt a enviar al modelo")
    args = parser.parse_args()

    # Combina todos los argumentos en un solo prompt
    prompt = " ".join(args.prompt) if args.prompt else ""
    if not prompt:
        print("⚠️  Error: Se requiere un prompt. Ejemplo:\n", file=sys.stderr)
        print("  python ask_ollama_cli.py \"¿cuál es la fecha actual?\"", file=sys.stderr)
        sys.exit(1)

    # Inicia cliente MCP
    try:
        client, process = create_mcp_client()
    except Exception as e:
        print(f"❌ Error al iniciar MCP: {e}", file=sys.stderr)
        sys.exit(1)

    # Genera y muestra respuesta en streaming
    try:
        print("🤖 Respuesta: ", end="", flush=True)
        stream_response(client, prompt)
        print()  # salto de línea final
    finally:
        # Cierra el subproceso MCP
        try:
            process.terminate()
            process.wait(timeout=3)
        except Exception:
            process.kill()


if __name__ == "__main__":
    main()