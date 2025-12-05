# YouTube Video Summarizer AI Agent

An AI-powered Streamlit application that converts YouTube videos into detailed blog post summaries using OpenAI GPT and the Phi framework.

## Features

- Extract transcripts from any YouTube video (supports multiple languages)
- Automatic translation of non-English transcripts
- AI-powered blog post generation with structured summaries
- Handles auto-generated and manual captions
- Clean, intuitive web interface

## Tech Stack

- **Frontend**: Streamlit
- **AI Model**: OpenAI GPT-5-mini via Phi Agent framework
- **Transcript Extraction**: youtube-transcript-api
- **Search Integration**: DuckDuckGo (via Phi tools)
- **Environment Management**: python-dotenv

## Prerequisites

- Python 3.13+
- OpenAI API key
- UV package manager

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Shikhar1121/Youtube-To-Blog.git
cd youtube-to-blog
```

2. Install dependencies using UV:
```bash
uv add -r requirement.txt
```

3. Create a `.env` file in the root directory:
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your browser (usually auto-opens to `http://localhost:8501`)

3. Paste a YouTube video URL

4. Enter your analysis query or use the default prompt

5. Click "Analyze Video" to generate the blog post

## How It Works

1. **Video ID Extraction**: Parses YouTube URLs to extract video IDs
2. **Transcript Retrieval**: Fetches video transcripts using YouTube's API
3. **Language Detection**: Identifies transcript language and translation status
4. **AI Processing**: Uses OpenAI GPT model through Phi Agent to:
   - Translate non-English content
   - Fix transcription errors
   - Generate structured blog posts
5. **Output**: Displays formatted markdown blog post with metadata

## Project Structure
```
youtube-to-blog/
├── app.py              # Main Streamlit application
├── pyproject.toml      # UV/Python project configuration
├── requirement.txt     # Python dependencies
├── .env               # Environment variables (not in repo)
└── README.md          # This file
```

## Configuration

The AI agent is configured with:
- Model: `gpt-5-mini`
- Tools: DuckDuckGo search integration
- Output: Markdown formatted responses

## Error Handling

The application handles:
- Invalid YouTube URLs
- Disabled transcripts
- Missing transcripts
- Translation failures
- API errors

## Contributing

Contributions welcome! Please open an issue or submit a pull request.


## Author

Shikhar Srivastava