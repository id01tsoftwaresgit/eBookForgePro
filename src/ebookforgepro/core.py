import os
import re
import textwrap
import random
import base64
from pathlib import Path

# Placeholder for a class that will be in a different module
# This avoids a circular import while allowing type hints or structure.
class Expander:
    pass

# --- Constants and Configuration ---

APP_NAME = "EebookForgePro" if False else "EbookForgePro"
APP_VERSION = "1.2.0"
APP_ID = "com.id01t.ebookforgepro"

BASE = Path.cwd()
PROJECT_DIR = (BASE / "EbookForgeProject").resolve()
EXPORTS = PROJECT_DIR / "exports"
BUILD = PROJECT_DIR / "build"
ASSETS = PROJECT_DIR / "assets"

# --- Embedded Data ---

EMBED_ICO = (
    b"AAABAAEAEBAAAAEAIABoBAAAFgAAACgAAAAQAAAAIAAAAAEAGAAAAAAAAAMAAAAAAAAAAAAAAAAAAAAA"
    b"AAAAAAD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////"
    b"AP///wD///8A////AP///wD///8A////AP///wD///8A////AAkJCQAZGRkAJCQkACUlJQAmJiYAKCgo"
    b"ACoqKgAuLi4AMDAwADExMQAyMjIANjY2ADg4OAA7OzsAPj4+AEBAQABDQ0MASEhIAE1NTQBPT08AVFRU"
    b"AFhYWABeXl4AYGBgAGNjYwBqam oAbGxsAHR0dAB+fn4AgICA AISEhACMjIwAlJSUAJyc nACwsLAAtLS0A"
    b"Li4uAC8vLwAwMDAAMTExADMzMwA0NDQANzc3ADg4OAA5OTkAOjo6ADs7OwA9PT0APj4+AEBAQABERERA"
    b"AEZGRgBJSUkATExMAE9PTwBVVVUAWVlZAF1dXQBfX18AYmJiAGZmZgBoaGgAbm5uAHBwcAB2dnYAenp6"
    b"AICCggCJiYkAkZGRAJWVlQCcnJwAn5+fAKGhoQCpqakArKysAK+vrwCwsLAAtra2ALa2tgC+vr4AwMDA"
    b"AMLCwgDFxcUAx8fHAMS EhADJycnA////wD///8A////AP///wD///8A////AP///wD///8A////AP//"
    b"/wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A////AP///wD///8A"
)

ICO_PATH = ASSETS / "app.ico"

TRAINING_DATA = {
  "Digital Marketing Strategy": {
    "introductions": [
      "This chapter will delve into the core principles of creating a successful digital marketing strategy. We will explore how to define your audience, set clear objectives, and choose the right channels to reach your goals.",
      "Building a digital marketing plan is the first step towards achieving online success. In this section, we'll cover the foundational elements of a robust strategy, from market research to performance measurement.",
      "A well-crafted digital marketing strategy acts as a roadmap for your business's online presence. This chapter will guide you through the process of creating a comprehensive plan that aligns with your business objectives."
    ],
    "core_concepts": [
      "Understanding your target audience is paramount. Develop detailed buyer personas to represent your ideal customers. Consider their demographics, psychographics, pain points, and online behavior. This will inform every aspect of your strategy.",
      "Setting SMART (Specific, Measurable, Achievable, Relevant, Time-bound) goals is crucial for success. Instead of a vague goal like 'increase online sales,' aim for something like 'achieve a 15% increase in e-commerce revenue in the next quarter.'",
      "The marketing funnel (Awareness, Consideration, Conversion, Loyalty) is a key concept. Your strategy should include tactics for each stage to guide potential customers on their journey from discovery to purchase and beyond.",
    ],
    "examples": [
      "For a local bakery, a good SMART goal would be: 'Increase online pre-orders for custom cakes by 25% within the next 6 months by running targeted Facebook ads and improving the website's SEO for local search terms.'",
      "A B2B software company might create a buyer persona named 'IT Manager Mike,' who is 35-45 years old, values efficiency and data security, and reads industry blogs and LinkedIn articles.",
    ],
    "exercises": [
      "Draft one complete buyer persona for your business. Include their demographics, goals, challenges, and preferred communication channels.",
      "Define three SMART goals for your next marketing campaign.",
    ],
    "takeaways": [
      "A successful digital marketing strategy is built on a deep understanding of your audience and clear, measurable goals.",
      "A multi-channel approach that integrates SEO, PPC, content, and email marketing is typically more effective than relying on a single tactic.",
    ]
  }
}

# --- Utility Functions ---

CLEAN_OPTS = {
    "replace_double_hyphen": True,
    "replace_emdash": True,
    "normalize_ws": True,
    "smart_quotes": True,
}

def clean_text(s: str, opts: dict | None = None) -> str:
    """Core text cleaner."""
    opts = {**CLEAN_OPTS, **(opts or {})}
    if opts.get("replace_double_hyphen"):
        s = s.replace("--", ",")
    if opts.get("replace_emdash"):
        s = s.replace("—", ",")
    if opts.get("smart_quotes"):
        s = s.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    if opts.get("normalize_ws"):
        s = re.sub(r"[\t\r\f\v]", " ", s)
        s = re.sub(r"\n{3,}", "\n\n", s)
        s = re.sub(r"[ \t]{2,}", " ", s)
    return s.strip()

def slugify(s: str) -> str:
    """Convert a string to a filename-safe slug."""
    s = re.sub(r"[^A-Za-z0-9\-_ \.]", "", s)
    s = re.sub(r"\s+", "_", s).strip("_")
    return s or "ebook"


# --- Core Generation Logic ---

def scaffold_from_meta(title: str, subtitle: str, toc: str, description: str, seed: str = "", topic: str = "Digital Marketing Strategy") -> str:
    """Generate a robust Markdown manuscript using offline training data."""
    title = clean_text(title or "Untitled")
    subtitle = clean_text(subtitle or "")
    description = clean_text(description or "")
    if "\n" in toc:
        chapters = [clean_text(x) for x in toc.splitlines() if x.strip()]
    else:
        chapters = [clean_text(x) for x in toc.split(",") if x.strip()]
    if not chapters:
        chapters = ["Introduction", "Chapter 1", "Chapter 2", "Conclusion"]

    out = [f"# {title}"]
    if subtitle:
        out.append(f"\n**{subtitle}**\n")
    if description:
        out.append(f"\n> {description}\n")

    out.append("\n### Table of Contents\n")
    for i, ch in enumerate(chapters, 1):
        out.append(f"{i}. {ch}")

    if topic in TRAINING_DATA:
        td = TRAINING_DATA[topic]
        for i, ch in enumerate(chapters, 1):
            out.append(f"\n\n## {i}. {ch}\n")
            out.append(random.choice(td.get("introductions", [""])))
            concepts = random.sample(td.get("core_concepts", [""]), k=min(3, len(td.get("core_concepts", [""]))))
            out.extend(["\n", *concepts])
            out.append(f"\n\n**Example:** {random.choice(td.get('examples', ['']))}")
            out.append("\n\n### Exercises\n")
            exercises = random.sample(td.get("exercises", [""]), k=min(2, len(td.get("exercises", [""]))))
            for ex in exercises:
                out.append(f"1. {ex}")
            out.append("\n\n### Key Takeaways\n")
            out.append(random.choice(td.get("takeaways", [""])))
    else:
        seed_short = clean_text(seed)[:2000]
        for i, ch in enumerate(chapters, 1):
            out.append(f"\n\n## {i}. {ch}\n")
            # ... (original generic generator logic)
    return clean_text("\n".join(out))

def autonomous_generation(title: str, subtitle: str, toc: str, description: str, expander_cfg: dict, expander=None) -> str:
    """Generate a full eBook manuscript chapter by chapter using an AI expander."""
    if expander is None:
        from .ai import Expander  # Local import to avoid circular dependency at top level
        expander = Expander(expander_cfg)

    title = clean_text(title or "Untitled")
    subtitle = clean_text(subtitle or "")
    description = clean_text(description or "")
    if "\n" in toc:
        chapters = [clean_text(x) for x in toc.splitlines() if x.strip()]
    else:
        chapters = [clean_text(x) for x in toc.split(",") if x.strip()]
    if not chapters:
        return "# Error: Table of Contents is empty."

    out = [f"# {title}"]
    if subtitle:
        out.append(f"\n**{subtitle}**\n")
    if description:
        out.append(f"\n> {description}\n")

    out.append("\n### Table of Contents\n")
    full_toc_str = "\n".join(f"{i}. {ch}" for i, ch in enumerate(chapters, 1))
    out.append(full_toc_str)

    for i, ch_title in enumerate(chapters, 1):
        print(f"[generator] Generating chapter {i}/{len(chapters)}: {ch_title}...")
        prompt = f"You are an expert author writing a chapter for a book.\n\nBook Title: {title}\nFull ToC:\n{full_toc_str}\n\nYou are writing the chapter: \"{ch_title}\".\n\nWrite the full content for this chapter, starting with a Level 2 Markdown heading (`## {ch_title}`)."
        generated_content = expander.expand(prompt)
        out.append(f"\n\n{generated_content}")

    print("[generator] All chapters generated.")
    return clean_text("\n".join(out))
