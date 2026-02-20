# 1. get query from user
# 2. using Cosine Similarity find the most relevant chunk(2 or more)
# 3. make a prompt and feed to LLM with relevant chunk and query.

from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import ollama


def fetch_relevant_chunk(user_query: str, dataframe, top_result=3):
  def embed_query(user_query):
    response = ollama.embed(
      model="nomic-embed-text",
      input=[user_query])
    
    return response.embeddings[0]
  
  embedded_query = embed_query(user_query)

  similarity = cosine_similarity(np.vstack(dataframe["embedding"]), [embedded_query]).flatten() # type: ignore

  top_similar_indx = similarity.argsort()[-top_result:][::-1]

  relevant_chunk = dataframe.loc[top_similar_indx][["text", "start", "duration"]]

  return relevant_chunk.to_json(orient="records")