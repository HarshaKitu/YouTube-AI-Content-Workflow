#!/usr/bin/env python3
"""
Video Download Script
Downloads YouTube videos using yt-dlp
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp not installed. Run: pip install yt-dlp")
    sys.exit(1)


def download_video(url, output_dir="./downloads", audio_only=False):
    """
    Download video from YouTube URL
    
    Args:
        url (str): YouTube video URL
        output_dir (str): Output directory for downloads
        audio_only (bool): Download audio only if True
    
    Returns:
        str: Path to downloaded file
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Configure yt-dlp options
    ydl_opts = {
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'format': 'bestaudio/best' if audio_only else 'best[height<=720]',
    }
    
    if audio_only:
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }]
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Get video info
            info = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info)
            
            # Download the video
            ydl.download([url])
            print(f"Successfully downloaded: {filename}")
            return filename
            
    except Exception as e:
        print(f"Error downloading video: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description='Download YouTube videos')
    parser.add_argument('url', help='YouTube video URL')
    parser.add_argument('--output', '-o', default='./downloads',
                       help='Output directory (default: ./downloads)')
    parser.add_argument('--audio-only', '-a', action='store_true',
                       help='Download audio only')
    
    args = parser.parse_args()
    
    result = download_video(args.url, args.output, args.audio_only)
    if not result:
        sys.exit(1)


if __name__ == "__main__":
    main()
