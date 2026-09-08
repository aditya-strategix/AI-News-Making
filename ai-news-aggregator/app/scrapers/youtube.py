from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled,CouldNotRetrieveTranscript, NoTranscriptFound, VideoUnavailable
from feedparser import parse


def extract_id_from_rss_url(url):
    """Extract YouTube video ID from URL."""
    id=url.split("channel_id=")[-1]
    return id

def extract_video_details_from_channel(channel_id):
    """Extract video details from YouTube channel ID."""
    yt_channel_link=f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    feed=parse(yt_channel_link)
    videos=[]
    for entry in feed.entries:
        video={
            "title":entry.title,
            "link":entry.link,
            "published":entry.published,
            "video_id":entry.yt_videoid
        }
        videos.append(video)
    return videos

def fetch_transcript(video_id):
    """Fetch transcript for a given YouTube video ID."""
    yt_api=YouTubeTranscriptApi()
    try:
        transcript=yt_api.fetch(video_id,languages=['en','hi'],preserve_formatting=True)
        return transcript
    except (TranscriptsDisabled, CouldNotRetrieveTranscript, NoTranscriptFound, VideoUnavailable) as e:
        print(f"Error fetching transcript for video {video_id}: {e}")
        return None

def decoding_transcript(transcript):
    """Decode transcript into plain text."""
    if not transcript:
        return ""
    decoded_text=" ".join(entry.text for entry in transcript.snippets)
    return decoded_text

def pipeline(channel_id):
    """Complete pipeline to fetch and decode transcripts from a YouTube channel."""
    videos=extract_video_details_from_channel(channel_id)
    for video in videos:
        transcript=fetch_transcript(video['video_id'])
        decoded_text=decoding_transcript(transcript)
        video['transcript']=decoded_text
    return videos

def print_transcript_with_title(videos):
    """Print titles and transcripts of videos."""
    for video in videos:
        print(f"Title: {video['title']}")
        print(f"Transcript: {video['transcript']}...") 
        print("\n")

        
channel_id="UCXZCJLdBC09xxGZ6gcdrc6A"
videos=pipeline(channel_id)