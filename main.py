"""
This file orchestrates the flow of our program
"""
from Transcriber.youtube_transcriber import YoutubeTranscriber
from Summarizer.transcript_summarizer import TranscriptSummarizer


if __name__ == "__main__":
    print("📽️  Initializing YouTube Transcriber...")
    yt = YoutubeTranscriber()

    video_url = "https://www.youtube.com/watch?v=0CmtDk-joT4"
    print(f"🔗 Fetching video ID from URL: {video_url}")
    video_id = yt.get_video_id(video_url)

    print("\n📝 Generating transcript from YouTube video...")
    transcript = yt.get_transcript(video_id)
    print(f"📜 Transcript preview (first 100 chars):\n{transcript[:100]}")

    print("\n✂️  Splitting transcript into chunks...")
    ts = TranscriptSummarizer()
    chunks = ts.generate_chunks(transcript)
    print(f"📦 Generated {len(chunks)} chunks.\n")

    print("🧠 Generating summary from transcript chunks...\n")
    summary = ts.generate_summary(chunks)

    print("\n✅ Final Summary:\n")
    print(summary)