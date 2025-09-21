# To use Ollama for local LLM inference, follow these steps:

1. Download and install Ollama from https://ollama.com/download (Windows, Mac, Linux supported).
2. Open a terminal and run:
   ollama run codellama
   # or for general Llama2:
   ollama run llama2
3. Wait for the model to download and start. Ollama will listen on http://localhost:11434 by default.

Once Ollama is running, the code will use it for AI feedback instead of OpenAI.
