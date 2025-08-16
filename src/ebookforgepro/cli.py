import sys
import traceback

from .app import App
from .core import scaffold_from_meta, autonomous_generation
from .exporters import Exporter
from .ai import Expander
from .core import PROJECT_DIR
import re

def run_cli_test():
    """Run tests without GUI"""
    print("Running CLI self-check...")
    try:
        # Test 1: Standard exports
        ex = Exporter(PROJECT_DIR)
        sample = scaffold_from_meta("Sample Book", "", "Intro, Core, Finale", "Quick self-test", topic="Generic")
        md = ex.export_md(sample, "Sample Book")
        ep = ex.export_epub(sample, "Sample Book", "Test Author")
        pdf = ex.export_pdf(sample, "Sample Book", "Test Author")
        print(f"Test 1 (Standard Exports): PASSED")

        # Test 2: Dynamic content generation from training data
        topic = "Digital Marketing Strategy"
        dyn_sample = scaffold_from_meta("Dynamic Book", "", "SEO,PPC,Email", "Dynamic test", topic=topic)
        if "buyer personas" in dyn_sample and "SEO" in dyn_sample:
            print(f"Test 2 (Dynamic Draft Generation): PASSED")
        else:
            print(f"Test 2 (Dynamic Draft Generation): FAILED")
            sys.exit(1)

        # Test 3: Autonomous generation with a mock expander
        class MockExpander:
            def expand(self, manuscript: str) -> str:
                match = re.search(r'You are writing the chapter: "(.+?)"', manuscript)
                ch_title = match.group(1) if match else "Unknown Chapter"
                return f"## {ch_title}\n\nThis is the mock-generated content for the chapter."

        mock_expander = MockExpander()
        auto_sample = autonomous_generation("Auto Book", "", "Chapter 1,Chapter 2", "Test autonomous", {}, expander=mock_expander)

        if "## Chapter 1" in auto_sample and "## Chapter 2" in auto_sample and "mock-generated content" in auto_sample:
            print("Test 3 (Autonomous Generation Logic): PASSED")
        else:
            print("Test 3 (Autonomous Generation Logic): FAILED")
            sys.exit(1)

        print("\nAll CLI self-checks finished successfully.")

    except Exception as e:
        print(f"CLI self-check error: {e}", file=sys.stderr)
        traceback.print_exc()
        sys.exit(1)

def main():
    """Main entry point for the application."""
    if "--self-check" in sys.argv:
        run_cli_test()
        return

    try:
        app = App()
        app.mainloop()
    except Exception as exc:
        # Fallback for fatal errors
        try:
            from tkinter import messagebox as mb
            mb.showerror("Fatal Error", f"A fatal error occurred: {exc}\n\n{traceback.format_exc()}")
        except (ImportError, RuntimeError):
            print(f"A fatal error occurred: {exc}", file=sys.stderr)
            traceback.print_exc()
