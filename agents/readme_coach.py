"""Agent 003: Wizardset README Coach.

This agent does not overwrite README.md. It reads the current README and
creates a coaching report with practical improvements for the next edit.
"""

from __future__ import annotations

from agents.common import README_FILE, exported_names, read_text, top_level_functions, write_report


REPORT_NAME = "readme_coach.md"


RECOMMENDED_SECTIONS = [
    "What Wizardset teaches",
    "Quick start",
    "Beginner examples",
    "Dinosaur examples",
    "Function map",
    "Testing",
    "Release checklist",
]


def section_missing(readme: str, title: str) -> bool:
    """Return True when a recommended section heading is missing."""
    return title.lower() not in readme.lower()


def build_readme_coach_report() -> str:
    """Build a markdown report suggesting README improvements."""
    readme = read_text(README_FILE)
    functions = top_level_functions()
    exports = exported_names()

    missing_function_mentions = [name for name in functions if f"`{name}" not in readme]
    missing_sections = [title for title in RECOMMENDED_SECTIONS if section_missing(readme, title)]

    lines: list[str] = []
    lines.append("# Wizardset README Coach Report")
    lines.append("")
    lines.append("## Current README Positioning")
    lines.append("")
    lines.append("Wizardset is strongest when presented as a learning-first utility package: small functions that teach important Python patterns.")
    lines.append("")

    lines.append("## Recommended One-Line Pitch")
    lines.append("")
    lines.append("> Wizardset is a beginner-friendly Python utility package that teaches powerful built-in patterns through readable helper functions.")
    lines.append("")

    lines.append("## Missing Recommended Sections")
    lines.append("")
    if missing_sections:
        for title in missing_sections:
            lines.append(f"- {title}")
    else:
        lines.append("No major recommended sections are missing.")
    lines.append("")

    lines.append("## Function Mention Check")
    lines.append("")
    lines.append(f"- Source functions: **{len(functions)}**")
    lines.append(f"- Public exports: **{len(exports)}**")
    lines.append(f"- Functions not clearly mentioned with backticks in README: **{len(missing_function_mentions)}**")
    lines.append("")
    if missing_function_mentions:
        for name in missing_function_mentions:
            lines.append(f"- `{name}()`")
    else:
        lines.append("Every source function appears to be clearly mentioned in the README.")
    lines.append("")

    lines.append("## Suggested README Additions")
    lines.append("")
    lines.append("### What Wizardset teaches")
    lines.append("```markdown")
    lines.append("Wizardset is not trying to replace Python's built-ins. It helps beginners understand them by wrapping common patterns in clear, named functions.")
    lines.append("")
    lines.append("- `best()` teaches `max(items, key=rule)`")
    lines.append("- `worst()` teaches `min(items, key=rule)`")
    lines.append("- `rank()` teaches `sorted(items, key=rule)`")
    lines.append("- `count_where()` teaches conditional counting")
    lines.append("- `frequencies()` teaches `collections.Counter`")
    lines.append("- `pair()` teaches `zip()`")
    lines.append("- `numbered()` teaches `enumerate()`")
    lines.append("```")
    lines.append("")

    lines.append("### Beginner example block")
    lines.append("```markdown")
    lines.append("```python")
    lines.append("from wizardset_enhanced import best, group_by, count_where")
    lines.append("")
    lines.append("words = ['cat', 'elephant', 'dog', 'python']")
    lines.append("")
    lines.append("print(best(words, len))")
    lines.append("print(group_by(words, len))")
    lines.append("print(count_where(words, lambda word: len(word) > 3))")
    lines.append("```")
    lines.append("```")
    lines.append("")

    lines.append("## Next README Edit")
    lines.append("")
    lines.append("Add the learning-first positioning near the top, then add one compact examples section. Keep the full generated examples in `reports/beginner_examples.md` rather than bloating the README.")

    return "\n".join(lines)


def main() -> None:
    """Run the README coach."""
    path = write_report(REPORT_NAME, build_readme_coach_report())
    print(f"README coach report created: {path}")


if __name__ == "__main__":
    main()
