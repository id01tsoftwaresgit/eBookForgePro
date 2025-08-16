# --------------------------------------------------------------------------
# Example: Using eBookForgePro as a Python Library
# --------------------------------------------------------------------------
#
# This script demonstrates how to import and use the core functions of the
# eBookForgePro package to generate an ebook manuscript from your own Python code.
#
# Before running, make sure you have installed the package, for example,
# by running `pip install .` in the root of this repository.
#
# You will also need to provide a valid API key for your chosen AI provider.
#
# --------------------------------------------------------------------------

import os
from ebookforgepro import autonomous_generation, scaffold_from_meta

def generate_ai_powered_book():
    """
    An example of using the autonomous_generation function to create a full
    ebook manuscript using an AI model.
    """
    print("--- Running Autonomous Generation Example ---")

    # 1. Configure your chosen AI provider.
    #    Supported modes: "openai", "gemini", "local" (Ollama)
    #    Make sure to set your API key. For local models, this may not be needed.
    api_cfg = {
        "mode": "openai",
        "openai_api_key": os.environ.get("OPENAI_API_KEY", "YOUR_API_KEY_HERE"),
        "openai_model": "gpt-4o-mini",
    }

    if api_cfg["openai_api_key"] == "YOUR_API_KEY_HERE":
        print("\nWARNING: No OpenAI API key found.")
        print("Please set the OPENAI_API_KEY environment variable or edit this script.")
        # We can't proceed, so we'll just generate a draft instead.
        generate_offline_draft()
        return

    # 2. Define the metadata for your book.
    book_title = "The Rise of the Machines"
    book_subtitle = "A History of Artificial Intelligence"
    book_toc = (
        "Chapter 1: The Dawn of Computing\n"
        "Chapter 2: The First AI Winters\n"
        "Chapter 3: The Deep Learning Revolution"
    )
    book_description = "A concise history of artificial intelligence, from the early theoretical work to the modern deep learning era."

    # 3. Call the generation function.
    #    This will call the AI model for each chapter, so it may take some time.
    print(f"Generating '{book_title}'... This may take several minutes.")
    manuscript = autonomous_generation(
        title=book_title,
        subtitle=book_subtitle,
        toc=book_toc,
        description=book_description,
        expander_cfg=api_cfg
    )

    # 4. Save the result.
    output_filename = "ai_generated_book.md"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(manuscript)

    print(f"\nSuccess! Manuscript saved to '{output_filename}'")
    print("-" * 40)


def generate_offline_draft():
    """
    An example of using the scaffold_from_meta function to create a draft
    using the built-in training data, without needing an AI provider.
    """
    print("\n--- Running Offline Draft Generation Example ---")

    # 1. Define the metadata for your book.
    book_title = "Mastering Digital Marketing"
    book_toc = "Introduction to SEO, Advanced PPC Tactics, Email Marketing Mastery"

    # 2. Call the scaffolding function.
    manuscript = scaffold_from_meta(
        title=book_title,
        toc=book_toc,
        description="A guide to digital marketing.",
        topic="Digital Marketing Strategy"
    )

    # 3. Save the result.
    output_filename = "offline_draft_book.md"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(manuscript)

    print(f"\nSuccess! Draft saved to '{output_filename}'")
    print("-" * 40)


if __name__ == "__main__":
    print("eBookForgePro Library Usage Examples")
    print("====================================")

    # Run the AI-powered example. It will fall back to the offline draft
    # if no API key is configured.
    generate_ai_powered_book()
