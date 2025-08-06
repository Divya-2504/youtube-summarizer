"""
This file orchestrates the flow of our program
"""
from Transcriber.youtube_transcriber import YoutubeTranscriber
from Summarizer.transcript_summarizer import TranscriptSummarizer
from GoogleOAuth.quickstart import GoogleDocsClient

if __name__ == "__main__":

    # Youtube transcription
    print("📽️  Initializing YouTube Transcriber...")
    yt = YoutubeTranscriber()
    video_title = input("Enter your video title: ")
    video_url = input("Enter your video url: ")
    print(f"🔗 Fetching video ID from URL: {video_url}")
    video_id = yt.get_video_id(video_url)

    # transcription
    print("\n📝 Generating transcript from YouTube video...")
    transcript = yt.get_transcript(video_id)
    print(f"📜 Transcript preview (first 100 chars):\n{transcript[:100]}")

    # chunking
    print("\n✂️  Splitting transcript into chunks...")
    ts = TranscriptSummarizer()
    chunks = ts.generate_chunks(transcript)
    print(f"📦 Generated {len(chunks)} chunks.\n")

    print("🧠 Generating summary from transcript chunks...\n")
    summary = ts.generate_summary(chunks)

    print("\n✅ Final Summary:\n")
    print(summary)

    client = GoogleDocsClient()

    doc_id = client.create_document(video_title)

    content = (
        f"📺 Video Title: {video_title}\n\n"
        f"🔍 Summary:\n{summary}\n\n"
        f"📝 Full Transcript:\n{transcript}"
    )

    client.insert_text(doc_id, content)

    print(f"Click here : https://docs.google.com/document/d/{doc_id}/edit")

