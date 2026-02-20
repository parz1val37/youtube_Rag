from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np
import json
import math
from google import genai
from api_key import API_KEY
import ollama


class YoutubeRagAssistant:
  # gives transcript of video in format-- list[dict]
  def __fetch_transcript(self, url: str):
    # extracting video_id from the given url.
    try:
      def extract_video_id(url: str):
        video_id = url.split("?")[0].split("/")[-1]
        return video_id
      video_id = extract_video_id(url)
  
      yt_api = YouTubeTranscriptApi()
      formatter = JSONFormatter()
      raw_transcript = yt_api.fetch(video_id)
      pre_transcript = formatter.format_transcript(transcript=raw_transcript)
      transcript = json.loads(pre_transcript)
      return transcript
  
    except Exception as e:
      print(f"Facing Error: {e}")

  # this function group number of chunk(5 or 6) to a single chunk which preserves the context
  ''' parameters->
  # 1. transcript: video transcript,
  # 2. group_chunk_num(int): number of chunk to be grouped into one.'''

  def __merge_chunks(self, transcript: list[dict], group_chunk_num: int= 6):
    new_chunk = []
    no_chunk = len(transcript)
    # num of groups of chunk possible
    num_groups = math.ceil(no_chunk/group_chunk_num)

    for i in range(num_groups):
      # start and end index of chunk
      start_indx = i*group_chunk_num
      end_indx = min((i+1)*group_chunk_num, no_chunk)
      # group of chunks
      chunk_group = transcript[start_indx:end_indx]
      # refining the text format(removing \n from text)
      text = " ".join(c["text"] for c in chunk_group).replace("\n", " ")
      # adding metadata to new_chunk
      new_chunk.append({
        "text": text,
        "start": chunk_group[0]["start"],
        "duration": round((chunk_group[-1]["start"] - chunk_group[0]["start"]), 3) if start_indx!=end_indx else 1
      })
    
    # saving the content of video for creating summary.
    summary = " ".join(chunk["text"] for chunk in new_chunk)
    # saving new_chunk as json
    
    return new_chunk, summary
  
  #-----------------x
  # 1. Make array of chunks.
  # 2. Using ollama embedding model(nomic-embed-text), make embeddings of this array.
  # 3. Itterate over every chunk and add embedding of corresponding chunk in key ["embedding"]
  # 4. save new json data or update the previous json and use it.
  # Parameter: Json data
  def __create_embeddings(self, transcript: list[dict]):
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

  #----------------------X
  # 1. get query from user
  # 2. using Cosine Similarity find the most relevant chunk(2 or more)
  # 3. make a prompt and feed to LLM with relevant chunk and query.
  def __fetch_relevant_chunk(self, user_query: str, dataframe, top_result=3):
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

  # getting the response from LLM-Agentss
  def __LLM_response(self, query, metadata, summary):
    prompt = f'''
    note: Given Below is a query and some data(contains- start time in seconds, duration in seconds, and text)
    and you have to answer the query using the data and mention the time stamp after converting seconds into minute(example if start time in seconds is 60.000 it will be  1:00 in minutes)
    # if query says to summarise then give the short summary in 100-150 words using this:[{summary}] 
    #important message: don't ask any question at end.

    query: {query}

    data: {metadata}'''
    
    client = genai.Client(api_key=API_KEY)
    response = client.models.generate_content(
      model="gemini-3-flash-preview",
      contents=prompt)
    
    return response.text


  # save dataframe to use it without making it again and again
  def initiate_dataframe(self, url):
    # fetch transcript
    transcript = self.__fetch_transcript(url)
    # merge chunks of transcript and get summary
    transcript, summary = self.__merge_chunks(transcript) #type: ignore
    # create embeddings of chunk in transcript
    transcript = self.__create_embeddings(transcript)
    
    dataframe = pd.DataFrame(transcript)
    return dataframe
    
  



  def youtube_rag_assistant(self):
    pass