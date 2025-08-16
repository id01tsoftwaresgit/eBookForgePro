"""
EbookForgePro Package
=====================

A professional, all-in-one Python application for creating, compiling, and managing eBooks with AI-powered features.

This package can be used as a library to programmatically generate ebook content.

Example:
    from ebookforgepro import autonomous_generation

    # Configure your AI provider
    api_cfg = {
        "mode": "openai",
        "openai_api_key": "YOUR_API_KEY",
        "openai_model": "gpt-4o-mini",
    }

    # Generate a book
    manuscript = autonomous_generation(
        title="My Awesome Book",
        subtitle="An AI-Generated Story",
        toc="Chapter 1: The Beginning\\nChapter 2: The End",
        description="A short story written by an AI.",
        expander_cfg=api_cfg
    )

    with open("my_awesome_book.md", "w") as f:
        f.write(manuscript)

"""

# Make key functions available at the top level of the package
from .core import autonomous_generation, scaffold_from_meta, clean_text

__version__ = "1.3.0"
