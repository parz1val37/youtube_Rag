# 1. Make array of chunks.
# 2. Using ollama embedding model(nomic-embed-text), make embeddings of this array.
# 3. Itterate over every chunk and add embedding of corresponding chunk in key ["embedding"]
# 4. save new json data or update the previous json and use it.

import ollama
import json

# Parameter: Json data
def create_embeddings(transcript: list[dict]):
  arr_text = [chunk["text"] for chunk in transcript]

  def ollama_embed(arr_text):
    response = ollama.embed(
      model="nomic-embed-text",
      input=arr_text)
    return response.embeddings
  
  embeddings = ollama_embed(arr_text) # It's array of embeddings

  for i, chunk in enumerate(transcript):
    chunk["embedding"] = embeddings[i]

  return transcript


if __name__ == "__main__":

  with open("transcript.json", "r", encoding="utf-8") as json_file:
    transcript = json.load(json_file)

  embedded_transcript = create_embeddings(transcript)

  with open("embedded_transcript.json", "w", encoding="utf-8") as json_dump:
    json.dump(embedded_transcript, json_dump)

  print("Task  completed! check embedded_transcript.json file")