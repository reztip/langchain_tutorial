
This is a simple tutorial for Streamlit and Ollama, toying with agentic
applications. , A simple tool to "create" your own LLM agents for simple conversations (that have no memory/context), this was mostly built by poking and prodding LLMs in VSCode.

It requires Ollama and llama3.1 running locally, as well as a Postgres and Redis instance.

There is not significant extensibility here to RAG, but it was fun for an hour or two, various issues include:
- SQL injection/input validation
- Single process/threaded
- Poor error handling

