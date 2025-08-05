"""
This file orchestrates the flow of our program
"""
from Transcriber.youtube_transcriber import YoutubeTranscriber


if __name__ == "__main__":
    yt = YoutubeTranscriber()

    video_id = yt.get_video_id("https://www.youtube.com/watch?v=2GZ2SNXWK-c")

    transcript = yt.get_transcript(video_id)