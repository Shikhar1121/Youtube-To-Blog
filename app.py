import streamlit as st
import os
from dotenv import load_dotenv
from phi.agent import Agent
from phi.model.openai import OpenAIChat
from phi.tools.duckduckgo import DuckDuckGo
import re
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi , TranscriptsDisabled , NoTranscriptFound

load_dotenv()

openai_api_key = os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

if openai_api_key:
    genai.configure(api_key=openai_api_key)

# Page configuration
st.set_page_config(
    page_title="YouTube Video Summarizer AI Agent",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 YouTube Video Summarizer AI Agent")
st.header("Paste a YouTube link and get a detailed blog post summary! Powered by Gemini Pro.")


@st.cache_resource
def initialize_agent():
    return Agent(
        name="YouTube Summarizer Agent",
        model=OpenAIChat(id="gpt-5-mini-2025-08-07"),
        tools=[DuckDuckGo()],
        show_tool_calls=True,
        markdown=True
    )


def extract_video_id(youtube_url):
    """Extract video ID from YouTube URL"""
    patterns = [
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/watch\?v=([^&]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtu\.be\/([^?]+)',
        r'(?:https?:\/\/)?(?:www\.)?youtube\.com\/embed\/([^?]+)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, youtube_url)
        if match:
            return match.group(1)
    return None

PREFERRED_EN_LANGS = ["en", "en-US", "en-GB", "en-IN"]

def get_transcript(video_id: str, target_lang: str = "en"):
    """
    Works with youtube-transcript-api >= 1.2.3 (instance-based API).

    Returns:
        transcript_text: str
        language_code: str
        is_generated: bool
        is_translated: bool
    """
    try:
        ytt_api = YouTubeTranscriptApi()

        # Try to get an English (or translated-to-English) transcript first
        fetched = ytt_api.fetch(
            video_id,
            languages=[target_lang, *PREFERRED_EN_LANGS],
            preserve_formatting=False,
        )
        # fetched is a FetchedTranscript

        # Metadata (these attributes exist on FetchedTranscript in 1.2.3+)
        language_code = getattr(fetched, "language_code", "unknown")
        is_generated = bool(getattr(fetched, "is_generated", False))
        is_translated = bool(getattr(fetched, "is_translated", False))

        # Option 1: iterate snippets (FetchedTranscriptSnippet objects)
        # full_text = " ".join(
        #     snippet.text for snippet in fetched if snippet.text.strip()
        # )

        # Option 2: use raw dict data (closer to old API)
        raw_segments = fetched.to_raw_data()  # list[dict] with keys: text, start, duration, ...
        full_text = " ".join(
            seg["text"] for seg in raw_segments if seg["text"].strip()
        )

        return full_text, language_code, is_generated, is_translated

    except TranscriptsDisabled:
        raise Exception("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        raise Exception("No transcript (manual or auto-generated) was found for this video.")
    except Exception as e:
        raise Exception(f"Unexpected error while fetching transcript: {e}")
    

multimodal_agent = initialize_agent()

# YouTube link input
youtube_link = st.text_input(
    "Enter YouTube Video URL",
    placeholder="https://www.youtube.com/watch?v=...",
    help="Paste the full YouTube video URL here"
)

# Display video preview if link is provided
if youtube_link:
    try:
        st.video(youtube_link)
    except:
        st.warning("Invalid YouTube URL. Please check and try again.")

user_query = st.text_area(
    "What insights would you like to extract from the video?",
    placeholder="e.g., Provide a detailed blog post summarizing the key points discussed in the video.",
    help="Ask the agent to generate a comprehensive blog post based on the video's content.",
    value="Provide a detailed blog post summarizing the key points discussed in the video."
)

if st.button("Analyze Video", key="analyze_video_button"):
    if not youtube_link:
        st.warning("Please enter a YouTube URL.")
    elif not user_query:
        st.warning("Please enter a query to analyze the video.")
    else:
        try:
            with st.spinner("Fetching video transcript..."):
                # Extract video ID
                video_id = extract_video_id(youtube_link)
                if not video_id:
                    st.error("Invalid YouTube URL. Please provide a valid link.")
                else:
                    # Get transcript
                    transcript, lang_code, is_generated, is_translated = get_transcript(video_id)
                    
                    with st.spinner("Generating blog post..."):
                        analysis_prompt = f"""
                     You are an expert summarizer.

Transcript language code: {lang_code}
Auto-generated: {"yes" if is_generated else "no"}
Translated by YouTube: {"yes" if is_translated else "no"}

1. If the transcript is not in English, first translate it into fluent English.
2. Then, based on the (possibly translated) transcript, respond to this user request:

{user_query}

3. Write a detailed, well-structured, user-friendly blog post.
4. Fix obvious transcription errors and missing punctuation.

TRANSCRIPT:
{transcript}
                        """

                        response = multimodal_agent.run(analysis_prompt)

                        st.subheader("Generated Blog Post Summary:")
                        st.markdown(response.content)
                        
                        st.info(
    f"Transcript language: {lang_code} | "
    f"Auto-generated: {'yes' if is_generated else 'no'} | "
    f"Translated by YouTube: {'yes' if is_translated else 'no'}"
)
                
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")

st.markdown("""
<style>
.stTextArea textarea {
    height: 150px;
}
</style>
""", unsafe_allow_html=True)