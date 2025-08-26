#!/usr/bin/env python3
"""
Audio Transcription Script
Transcribes audio files using OpenAI Whisper
"""

import argparse
import os
import sys
from pathlib import Path

try:
    import whisper
except ImportError:
    print("Error: whisper not installed. Run: pip install openai-whisper")
    sys.exit(1)


def transcribe_audio(audio_file, model_size="base", output_dir="./transcriptions"):
    """
    Transcribe audio file using OpenAI Whisper
    
    Args:
        audio_file (str): Path to audio file
        model_size (str): Whisper model size (tiny, base, small, medium, large)
        output_dir (str): Output directory for transcriptions
    
    Returns:
        dict: Transcription result with text and segments
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Load Whisper model
    print(f"Loading Whisper model: {model_size}")
    model = whisper.load_model(model_size)
    
    try:
        # Transcribe audio
        print(f"Transcribing: {audio_file}")
        result = model.transcribe(audio_file)
        
        # Save transcription to file
        base_name = Path(audio_file).stem
        transcript_file = os.path.join(output_dir, f"{base_name}_transcript.txt")
        
        with open(transcript_file, 'w', encoding='utf-8') as f:
            f.write(result['text'])
        
        # Save detailed segments if available
        segments_file = os.path.join(output_dir, f"{base_name}_segments.txt")
        with open(segments_file, 'w', encoding='utf-8') as f:
            for segment in result['segments']:
                start_time = segment['start']
                end_time = segment['end']
                text = segment['text']
                f.write(f"[{start_time:.2f} - {end_time:.2f}]: {text}\n")
        
        print(f"Transcription saved to: {transcript_file}")
        print(f"Segments saved to: {segments_file}")
        
        return result
        
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None


def main():
    parser = argparse.ArgumentParser(description='Transcribe audio files using Whisper')
    parser.add_argument('audio_file', help='Path to audio file')
    parser.add_argument('--model', '-m', default='base',
                       choices=['tiny', 'base', 'small', 'medium', 'large'],
                       help='Whisper model size (default: base)')
    parser.add_argument('--output', '-o', default='./transcriptions',
                       help='Output directory (default: ./transcriptions)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.audio_file):
        print(f"Error: Audio file not found: {args.audio_file}")
        sys.exit(1)
    
    result = transcribe_audio(args.audio_file, args.model, args.output)
    if not result:
        sys.exit(1)


if __name__ == "__main__":
    main()
