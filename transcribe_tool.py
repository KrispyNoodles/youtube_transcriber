# converting it into a langchain tool
from langchain_core.tools import tool
import re
from config import supadata

'''
Supadata is used instead of YouTubeTranscriptApi bcecasue:
YouTube is blocking requests from your IP. This usually is due to one of the following reasons:
- You have done too many requests and your IP has been blocked by YouTube
- You are doing requests from an IP belonging to a cloud provider (like AWS, Google Cloud Platform, Azure, etc.). Unfortunately, most IPs from cloud providers are blocked by YouTube.
'''

# the tool takes in a youtube in a string format and it transcribes back for the user
@tool(return_direct=False)
def youtube_transcriber(youtube_link: str) -> str:

    """
    Extract transcript with timestamps form a YouTube video URL and format it 
    for LLM consumption

    Args:
        url (str): YouTube video URL

    Returns:
        str: Formatted transcript with timestamps, where each entry
        is on a new line in the format: "[MM:SS] Text"
    """

    # extracting video id from url
    video_id_pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    video_id_match = re.search(video_id_pattern, youtube_link)

    # checking if the youtube url exists
    if not video_id_match:
        raise ValueError("Invalid Youtube Url")
    
    # id of the video like dQw4w9WgXcQ for example
    id_of_video = video_id_match.group(1)

    # if the video_id exists, try generating the transcript
    try:

        # finding alternative methods to transcribe
        transcript = supadata.youtube.transcript(video_id=id_of_video, lang="es")

        # Format each entry with timestamp and text
        formatted_entries = []

        for chunk in transcript.content:

            # convert seconds to MM:SS format

            # Division to get whole minutes
            minutes = int(chunk.duration//60)

            # Division to get remaining seconds
            seconds = int(chunk.duration % 60)
            timestamp = f"{minutes:02d}:{seconds:02d}"

            formatted_entry = f"{timestamp} {chunk.text}"
            formatted_entries.append(formatted_entry)

        # join all entries with newlines
        return "\n".join(formatted_entries)
    
    except Exception as e:
        raise Exception(f"Error fetching transcript: (str{e})")