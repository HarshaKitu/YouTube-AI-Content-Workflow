# YouTube AI Content Workflow

Automated workflow for YouTube video summarization, blog generation, and podcast creation using open-source tools and n8n.

## Overview

This repository contains an end-to-end automated workflow that transforms YouTube videos into multiple content formats including summaries, blog posts, and podcasts. The workflow leverages AI technologies and open-source tools to create a comprehensive content pipeline.

## Workflow Components

### 1. Video Download
- **Tool**: [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- **Purpose**: Downloads YouTube videos in various formats
- **Features**: Supports playlists, subtitles, and metadata extraction

### 2. Audio Transcription
- **Tool**: [OpenAI Whisper](https://github.com/openai/whisper)
- **Purpose**: Converts video audio to text with high accuracy
- **Features**: Multi-language support, timestamp generation, speaker identification

### 3. Content Summarization
- **Tools**: 
  - HuggingFace Transformers (BART, T5, etc.)
  - OpenAI API (GPT models)
- **Purpose**: Generates concise summaries from transcriptions
- **Features**: Customizable summary length, key point extraction, topic analysis

### 4. Text-to-Speech (TTS)
- **Tool**: [Coqui TTS](https://github.com/coqui-ai/TTS)
- **Purpose**: Converts text summaries into podcast-quality audio
- **Features**: Multiple voice models, emotion control, speed adjustment

### 5. Blog Generation
- **Format**: Markdown
- **Purpose**: Creates SEO-optimized blog posts from video content
- **Features**: Automatic formatting, metadata generation, image placeholders

### 6. Podcast Creation
- **Process**: TTS conversion of summaries with intro/outro
- **Format**: MP3 with proper metadata
- **Features**: RSS feed generation, episode artwork, show notes

### 7. Publishing Platform
- **Framework**: [Next.js](https://nextjs.org/)
- **RSS Generation**: [FeedGen](https://github.com/lkiesow/python-feedgen)
- **Purpose**: Web interface for content management and RSS feed distribution
- **Features**: Responsive design, SEO optimization, analytics integration

### 8. Automation Engine
- **Tool**: [n8n](https://n8n.io/)
- **Purpose**: Orchestrates the entire workflow
- **Features**: Visual workflow editor, webhook triggers, error handling, scheduling

## Architecture

```
YouTube Video URL
        ↓
   [yt-dlp Download]
        ↓
   [Whisper Transcription]
        ↓
   [AI Summarization]
        ↓
    ┌───────────────┐
    ↓               ↓
[Blog Generation]  [TTS Podcast]
    ↓               ↓
[Markdown File]   [MP3 + RSS]
    ↓               ↓
    └─────→ [Next.js Publishing] ←─────┘
              ↓
         [Web Portal + RSS Feed]
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- Node.js 16+
- Docker (optional)
- API keys (OpenAI, HuggingFace)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/HarshaKitu/YouTube-AI-Content-Workflow.git
   cd YouTube-AI-Content-Workflow
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Node.js dependencies**
   ```bash
   cd web-app
   npm install
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys and configuration
   ```

5. **Setup n8n workflow**
   ```bash
   docker run -it --rm --name n8n -p 5678:5678 n8nio/n8n
   # Import the workflow from n8n-workflows/youtube-ai-workflow.json
   ```

## Configuration

### Environment Variables
```env
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# HuggingFace Configuration
HUGGINGFACE_API_KEY=your_huggingface_token

# Coqui TTS Configuration
TTS_MODEL_PATH=./models/tts

# Output Directories
OUTPUT_DIR=./output
BLOG_DIR=./output/blogs
PODCAST_DIR=./output/podcasts

# n8n Configuration
N8N_WEBHOOK_URL=http://localhost:5678/webhook/youtube-workflow
```

## Usage

### Manual Execution
```bash
python scripts/process_video.py --url "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Automated via n8n
1. Access n8n interface at `http://localhost:5678`
2. Import the workflow from `n8n-workflows/`
3. Configure webhook triggers
4. Activate the workflow

### Web Interface
```bash
cd web-app
npm run dev
# Access at http://localhost:3000
```

## File Structure

```
├── scripts/
│   ├── download_video.py      # yt-dlp wrapper
│   ├── transcribe_audio.py    # Whisper integration
│   ├── summarize_text.py      # AI summarization
│   ├── generate_blog.py       # Markdown blog creation
│   ├── create_podcast.py      # TTS and audio processing
│   └── process_video.py       # Main orchestration script
├── web-app/
│   ├── pages/                 # Next.js pages
│   ├── components/            # React components
│   ├── utils/                 # Utility functions
│   └── public/                # Static assets
├── n8n-workflows/
│   └── youtube-ai-workflow.json
├── templates/
│   ├── blog_template.md
│   └── podcast_template.xml
├── requirements.txt
├── package.json
└── README.md
```

## Features

- **Batch Processing**: Handle multiple videos simultaneously
- **Quality Control**: Automatic content validation and error handling
- **Customization**: Configurable templates and AI parameters
- **Analytics**: Track processing metrics and content performance
- **Scalability**: Containerized deployment support
- **Multi-format Output**: Blog posts, podcasts, and social media snippets

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenAI for Whisper and GPT models
- HuggingFace for transformer models
- Coqui AI for open-source TTS
- n8n team for the automation platform
- yt-dlp contributors for video downloading capabilities

## Support

For questions and support, please open an issue in this repository or contact [your-email@example.com](mailto:your-email@example.com).
