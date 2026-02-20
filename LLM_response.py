from google import genai
from api_key import API_KEY

def LLM_response(query, metadata, summary):
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