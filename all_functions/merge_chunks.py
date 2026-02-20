import math

# this function group number of chunk(5 or 6) to a single chunk which preserves the context
''' parameters->
# 1. transcript: video transcript,
# 2. group_chunk_num(int): number of chunk to be grouped into one.'''

def merge_chunks(transcript: list[dict], group_chunk_num: int= 6):
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