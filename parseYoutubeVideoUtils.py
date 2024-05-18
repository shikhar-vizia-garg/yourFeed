from youtube_transcript_api import YouTubeTranscriptApi
from isodate import parse_duration
import re

def get_video_id(url):
  """Extracts the video ID from a YouTube URL, including shared links.

  Args:
    url: The YouTube video URL.

  Returns:
    The extracted video ID or None if not found.
  """
  # Two patterns for standard and shared links
  regex_standard = r"(?:https?:\/\/)?(?:www\.)?youtu(?:\.be|be\.com)\/(?:watch\?v=)?([^\?&\"\;\ ]+)"
  regex_shared = r"(?:https?:\/\/)?(?:www\.)?youtu(?:\.be|be\.com)\/(?:shared\?ci=)([^\?&\"\;\ ]+)"

  match = re.search(regex_standard, url)
  if not match:
    match = re.search(regex_shared, url)

  if match:
    return match.group(1)
  else:
    return None


def fetch_transcript(video_id, start_seconds, end_seconds):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    # print(transcript)
    return transcript
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return []

    # Extract the portion of the transcript between start_seconds and end_seconds
    start_index = find_nearest_index(transcript, start_seconds)
    end_index = find_nearest_index(transcript, end_seconds)

    return transcript[start_index:end_index]
def find_nearest_index(transcript, target_seconds):
    # Find the index in the transcript closest to the target time
    for i, entry in enumerate(transcript):
        if entry['start'] >= target_seconds:
            return i
    return len(transcript)
