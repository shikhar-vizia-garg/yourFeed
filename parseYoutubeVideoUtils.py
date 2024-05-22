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


def fetch_transcript(video_id):
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return transcript

def find_nearest_index(transcript, target_seconds):
    # Find the index in the transcript closest to the target time
    for i, entry in enumerate(transcript):
        if entry['start'] >= target_seconds:
            return i
    return len(transcript)


def getStringTranscript(transcript):
    transcript_str = ''
    for line in transcript:
        transcript_str = transcript_str + '\n' + line["text"]
    return transcript_str