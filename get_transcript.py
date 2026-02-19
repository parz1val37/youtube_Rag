from youtube_transcript_api import YouTubeTranscriptApi

yt = 'https://youtu.be/DFwppvrL_pE?si=wO5NE7e5jajBvXsX'

def fetch_transcript(url):
  def extract_video_id(url: str):
    video_id = url.split("?")[0].split("/")[-1]
    return video_id
  video_id = extract_video_id(url)
  
  try:
    yt_api = YouTubeTranscriptApi()
    transcript = yt_api.fetch(video_id)
    
    
    
    
    pass
  except Exception as e:
    print(f"Facing Error: {e}")






# fetch_transcript(yt)