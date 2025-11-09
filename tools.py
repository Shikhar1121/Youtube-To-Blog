from crewai_tools import YoutubeChannelSearchTool, YoutubeVideoSearchTool
import os
from dotenv import load_dotenv

load_dotenv()

def get_yt_tool(channel_name):
    """Create and return a YouTube tool for the given channel."""
    try:
        # Clean the channel name
        channel_name = channel_name.strip()
        
        # Extract just the handle from various formats
        if channel_name.startswith('https://www.youtube.com/@'):
            channel_name = channel_name.replace('https://www.youtube.com/@', '')
        elif channel_name.startswith('https://www.youtube.com/'):
            channel_name = channel_name.replace('https://www.youtube.com/', '')
        elif channel_name.startswith('@'):
            channel_name = channel_name[1:]
        
        print(f"Attempting to initialize YouTube tool with handle: {channel_name}")
        
        # Try method 1: Direct channel handle
        try:
            tool = YoutubeChannelSearchTool(youtube_channel_handle=channel_name)
            print(f"✓ Successfully initialized with handle: {channel_name}")
            return tool
        except Exception as e1:
            print(f"✗ Failed with handle '{channel_name}': {str(e1)}")
        
        # Try method 2: With @ prefix
        try:
            tool = YoutubeChannelSearchTool(youtube_channel_handle=f"@{channel_name}")
            print(f"✓ Successfully initialized with @{channel_name}")
            return tool
        except Exception as e2:
            print(f"✗ Failed with @{channel_name}: {str(e2)}")
        
        # Try method 3: Use YoutubeVideoSearchTool as alternative
        # This tool searches for videos instead of channel-specific content
        try:
            print(f"Trying alternative: YoutubeVideoSearchTool")
            tool = YoutubeVideoSearchTool()
            print(f"✓ Successfully initialized YoutubeVideoSearchTool (will search all YouTube)")
            return tool
        except Exception as e3:
            print(f"✗ Failed with YoutubeVideoSearchTool: {str(e3)}")
        
        # If all methods fail, raise error with helpful message
        raise Exception(
            f"Could not initialize YouTube tool for channel '{channel_name}'.\n\n"
            f"Troubleshooting steps:\n"
            f"1. Verify the channel exists: https://www.youtube.com/@{channel_name}\n"
            f"2. Try using the channel ID instead of handle (found in channel's 'About' page)\n"
            f"3. Check your internet connection\n"
            f"4. Install/update packages: pip install --upgrade crewai-tools youtube-transcript-api\n"
            f"5. The channel might not have transcripts enabled on their videos"
        )
        
    except Exception as e:
        print(f"Fatal error: {str(e)}")
        raise

# For backward compatibility
yt_tool = None
