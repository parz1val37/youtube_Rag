## Function of this RAG model
- Acts as an assistant which when prompted provides summary or answer related to the video.

## How to use:
- Clone this repo or run main.py after installing necessary modules.
- Read (Python Notebooks) or go through (all functions files) to understand how it works
- ! Must have an API_KEY


## How it works:
1. using youtube transcript api it fetches the transcript of the video(default language of transcript is english)
2. Internally it creates embedding of processed transcript
3. Creates embedding of query asked by user.
4. Using cosine similarity the most relevant chunk of transcript is pulled from database
5. The query and relevant chunk is passed to LLM with prompt.
6. LLM provides answer based on query of user and context in the chunk.

## Note:
1. Use any free LLM agent api or paid api if you have (I used gemini api)
2. Use an Embedding model(Ollama nomic-text-embed is used).

## Potential use case:
- A chrome extension can be made which answers the query related to the playing YouTube video.
