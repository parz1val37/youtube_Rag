# getting transcript of youtube video using youtube-api
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter


def fetch_transcript(url):
  # extracting video_id from the given url.
  def extract_video_id(url: str):
    video_id = url.split("?")[0].split("/")[-1]
    return video_id
  video_id = extract_video_id(url)
  
  try:
    yt_api = YouTubeTranscriptApi()
    formatter = JSONFormatter()
    raw_transcript = yt_api.fetch(video_id)
    transcript = formatter.format_transcript(transcript=raw_transcript)
    return transcript
  
  except Exception as e:
    print(f"Facing Error: {e}")


if __name__== "__main__":

  yt = 'https://youtu.be/DFwppvrL_pE?si=wO5NE7e5jajBvXsX'
  transcript = fetch_transcript(yt)
  print(transcript)