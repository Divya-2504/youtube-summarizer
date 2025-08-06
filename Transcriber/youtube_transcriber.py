"""
This file generates transcripts based on youtube video links
"""
import re
from youtube_transcript_api import YouTubeTranscriptApi

class YoutubeTranscriber:
    def __init__(self):
        pass

    def get_video_id(self, url : str ) -> str:
        match = re.search(r"v=([^&]+)",url)
        if not match:
            raise ValueError("Invalid Youtube URL")
        
        video_id = match.group(1)
        return video_id

    def get_transcript(self,video_id : str) -> str:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.fetch(video_id, languages=['hi','en','en-US'])
        transcript = " ".join(snippet.text for snippet in transcript_list)
        return transcript