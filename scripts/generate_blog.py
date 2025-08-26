#!/usr/bin/env python3
"""
Blog Generation Script
Generates Markdown blog posts from summaries and content
"""

import argparse
import os
import sys
from datetime import datetime
from pathlib import Path

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


def generate_blog_with_openai(summary, title="", model="gpt-3.5-turbo", max_tokens=1000):
    """
    Generate blog post using OpenAI API
    
    Args:
        summary (str): Content summary to expand
        title (str): Blog post title
        model (str): OpenAI model to use
        max_tokens (int): Maximum tokens in blog post
    
    Returns:
        str: Generated blog post content
    """
    try:
        prompt = f"""
Create an engaging blog post from the following summary:

Summary: {summary}

Please format the blog post with:
- An engaging title (if not provided: "{title}")
- Introduction paragraph
- Main content sections with subheadings
- Conclusion
- Use markdown formatting

Make it informative, well-structured, and SEO-friendly.
"""
        
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a professional content writer who creates engaging blog posts."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error with OpenAI blog generation: {e}")
        return None


def generate_blog_template(summary, title="", video_url=""):
    """
    Generate basic blog post template
    
    Args:
        summary (str): Content summary
        title (str): Blog post title
        video_url (str): Original video URL
    
    Returns:
        str: Basic blog post template
    """
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    if not title:
        title = "Video Summary Blog Post"
    
    template = f"""---
title: "{title}"
date: {date_str}
tags: [video-summary, content]
author: AI Content Generator
---

# {title}

*Published: {date_str}*

## Overview

This blog post is generated from a video summary, providing key insights and information in an easily digestible format.

## Summary

{summary}

## Key Points

- Main topics covered in the video
- Important insights and takeaways
- Actionable information for readers

## Conclusion

This summary provides a comprehensive overview of the video content, making it accessible for those who prefer reading over watching.

---

*This content was automatically generated from video transcription and summarization.*
"""
    
    if video_url:
        template += f"\n\n**Original Video:** [{video_url}]({video_url})"
    
    return template


def generate_blog(input_file, output_dir="./blogs", title="", method="template", video_url=""):
    """
    Generate blog post from summary file
    
    Args:
        input_file (str): Path to summary text file
        output_dir (str): Output directory for blog posts
        title (str): Blog post title
        method (str): Generation method ('template' or 'openai')
        video_url (str): Original video URL
    
    Returns:
        str: Generated blog post content
    """
    # Create output directory if it doesn't exist
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Read summary text
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            summary = f.read().strip()
    except Exception as e:
        print(f"Error reading input file: {e}")
        return None
    
    # Generate blog content based on method
    if method == "openai":
        if not OPENAI_AVAILABLE:
            print("Error: openai not installed. Run: pip install openai")
            return None
        blog_content = generate_blog_with_openai(summary, title)
    else:  # template method
        blog_content = generate_blog_template(summary, title, video_url)
    
    if blog_content:
        # Save blog post to file
        base_name = Path(input_file).stem.replace('_summary', '')
        if not title:
            title = base_name.replace('_', ' ').title()
        
        safe_title = title.lower().replace(' ', '_').replace('/', '_')
        blog_file = os.path.join(output_dir, f"{safe_title}_blog.md")
        
        with open(blog_file, 'w', encoding='utf-8') as f:
            f.write(blog_content)
        
        print(f"Blog post saved to: {blog_file}")
        return blog_content
    
    return None


def main():
    parser = argparse.ArgumentParser(description='Generate blog posts from summaries')
    parser.add_argument('input_file', help='Path to summary text file')
    parser.add_argument('--title', '-t', default='',
                       help='Blog post title')
    parser.add_argument('--method', '-m', default='template',
                       choices=['template', 'openai'],
                       help='Generation method (default: template)')
    parser.add_argument('--output', '-o', default='./blogs',
                       help='Output directory (default: ./blogs)')
    parser.add_argument('--video-url', '-u', default='',
                       help='Original video URL for reference')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.input_file):
        print(f"Error: Input file not found: {args.input_file}")
        sys.exit(1)
    
    result = generate_blog(args.input_file, args.output, args.title, 
                          args.method, args.video_url)
    if not result:
        sys.exit(1)


if __name__ == "__main__":
    main()
