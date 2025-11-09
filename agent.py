from crewai import Agent
from dotenv import load_dotenv
from litellm import completion
import os
from crewai import LLM

load_dotenv()

# Set the API key in environment
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

llm = "openai/gpt-5-2025-08-07"

def create_agents(yt_tool):
    """Create and return blog researcher and writer agents with the given tool."""
    
    ## Create a senior blog content researcher
    blog_researcher = Agent(
        role='Blog Researcher from Youtube Videos',
        goal='get the relevant video transcription for the topic {topic} from the provided Yt channel',
        verbose=True,
        memory=True,
        backstory=(
           "Expert in understanding videos in AI Data Science, Machine Learning And GEN AI and providing suggestion" 
        ),
        tools=[yt_tool],
        llm=llm,  # Direct model string
        allow_delegation=True
    )

    ## creating a senior blog writer agent with YT tool
    blog_writer = Agent(
        role='Blog Writer',
        goal='Narrate compelling tech stories about the video {topic} from YT video',
        verbose=True,
        memory=True,
        backstory=(
            "With a flair for simplifying complex topics, you craft "
            "engaging narratives that captivate and educate, bringing new "
            "discoveries to light in an accessible manner in 300 words."
        ),
        tools=[yt_tool],
        llm=llm,  # Direct model string
        allow_delegation=False
    )
    
    return blog_researcher, blog_writer