#!/usr/bin/env python3
"""
Text Summarization Script
Summarizes text using AI models (OpenAI or HuggingFace)
"""

import argparse
import os
import sys
from pathlib import Path

try:
    from transformers import pipeline
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


def summarize_with_transformers(text, model_name="facebook/bart-large-cnn", max_length=150):
    """
    Summarize text using HuggingFace transformers
    
    Args:
        text (str): Text to summarize
        model_name (str): HuggingFace model name
        max_length (int): Maximum summary length
    
    Returns:
        str: Generated summary
    """
    try:
        summarizer = pipeline("summarization", model=model_name)
        result = summarizer(text, max_length=max_length, min_length=30, do_sample=False)
        return result[0]['summary_text']
    except Exception as e:
        print(f"Error with transformers summarization: {e}")
        return None


def summarize_with_openai(text, model="gpt-3.5-turbo", max_tokens=150):
    """
    Summarize text using OpenAI API
    
    Args:
        text (str): Text to summarize
        model (str): OpenAI model to use
        max_tokens (int): Maximum tokens in summary
    
    Returns:
        str: Generated summary
    """
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that creates concise summaries."},
                {"role": "user", "content": f"Please summarize the following text:\n\n{text}"}
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error with OpenAI summarization: {e}")
        return None


def summarize_text(input_file, output_dir="./summaries", method="transformers", max_length=150):
    """
    Summarize text from file
    
    Args:
        input_file (str): Path to input text file
        output_dir (str): Output directory for summaries
        method (str): Summarization method ('transformers' or 'openai')
        max_length (int): Maximum summary length
    
    Returns:
        str: Generated summary
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Read input text
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            text = f.read().strip()
    except Exception as e:
        print(f"Error reading input file: {e}")
        return None
    
    # Generate summary based on method
    if method == "transformers":
        if not TRANSFORMERS_AVAILABLE:
            print("Error: transformers not installed. Run: pip install transformers torch")
            return None
        summary = summarize_with_transformers(text, max_length=max_length)
    elif method == "openai":
        if not OPENAI_AVAILABLE:
            print("Error: openai not installed. Run: pip install openai")
            return None
        summary = summarize_with_openai(text, max_tokens=max_length)
    else:
        print(f"Unknown summarization method: {method}")
        return None
    
    if summary:
        # Save summary to file
        base_name = Path(input_file).stem
        summary_file = os.path.join(output_dir, f"{base_name}_summary.txt")
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(summary)
        
        print(f"Summary saved to: {summary_file}")
        return summary
    
    return None


def main():
    parser = argparse.ArgumentParser(description='Summarize text using AI models')
    parser.add_argument('input_file', help='Path to input text file')
    parser.add_argument('--method', '-m', default='transformers',
                       choices=['transformers', 'openai'],
                       help='Summarization method (default: transformers)')
    parser.add_argument('--output', '-o', default='./summaries',
                       help='Output directory (default: ./summaries)')
    parser.add_argument('--max-length', '-l', type=int, default=150,
                       help='Maximum summary length (default: 150)')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: Input file not found: {args.input_file}")
        sys.exit(1)
    
    result = summarize_text(args.input_file, args.output, args.method, args.max_length)
    if not result:
        sys.exit(1)


if __name__ == "__main__":
    main()
