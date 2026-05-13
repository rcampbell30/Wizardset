"""Agent 004: Wizardset Release Checker.

This agent checks basic release readiness: package metadata, tests, exports,
README presence, and common repository files. It writes a markdown report.
"""

from __future__ import annotations

from pathlib import Path

from agents.common import (
    PYPROJECT_FILE,
    README_FILE,
    ROOT,
    TEST_FILE,
    exported_names,
    read_text,
    run_command,
    top_level_functions,
    write_report,
)


REPORT_NAME = "release_check.md"


REQUIRED_FILES = [
    "README.md",
    "pyproject.toml",
    "LICENSE",
    "tests/test_wizardset.py",
    "wizardset_enhanced/__init__.py",
    "wizardset_enhanced/wizardset.py",
]


def file_exists(relative_path: str) -> bool:
    """Check whether a file exists relative to the repository root."""
    return (ROOT / relative_path).exists()


def pyproject_has_required_metadata(pyproject_text: str) -> list[str]:
    """Return missing important pyproject fields."""
    required_markers = [
        "[project]",
        "name =",
        "version =",
        "description =",
        "readme =",
        "requires-python =",
        "license =",
        "authors =",
        "classifiers =",
    ]
    return [marker for marker in required_markers if marker not in pyproject_text]


def build_release_report() -> str:
    """Build a release readiness report."""
    functions = top_level_functions()
    exports = exported_names()
    readme_text = read_text(README_FILE)
    pyproject_text = read_text(PYPROJECT_FILE)
    test_text = read_text(TEST_FILE)

    missing_files = [path for path in REQUIRED_FILES if not file_exists(path)]
    missing_metadata = pyproject_has_required_metadata(pyproject_text)
    unexported_functions = [name for name in functions if name not in exports]
    stale_exports = [name for name in exports if name not in functions]
    untested_functions = [name for name in functions if name not in test_text]

    pytest_code, pytest_stdout, pytest_stderr = run_command(["python", "-m", "pytest", "-q"])

    score = 100
    score -= 10 * len(missing_files)
    score -= 5 * len(missing_metadata)
    score -= 5 * len(unexported_functions)
    score -= 5 * len(stale_exports)
    score -= 2 * len(untested_functions)
    if pytest_code != 0:
        score -= 25
    if "learning" not in readme_text.lower():
        score -= 5
    score = max(score, 0)

    lines: list[str] = []
    lines.append("# Wizardset Release Check")
    lines.append("")
    lines.append(f"Release readiness score: **{score}/100**")
    lines.append("")

    lines.append("## Required Files")
    lines.append("")
    if missing_files:
        for path in missing_files:
            lines.append(f"- Missing: `{path}`")
    else:
        lines.append("All required files are present.")
    lines.append("")

    lines.append("## Package Metadata")
    lines.append("")
    if missing_metadata:
        for marker in missing_metadata:
            lines.append(f"- Missing marker in `pyproject.toml`: `{marker}`")
    else:
        lines.append("Core package metadata appears present.")
    lines.append("")

    lines.append("## Export Health")
    lines.append("")
    if not unexported_functions and not stale_exports:
        lines.append("Exports match source functions.")
    else:
        if unexported_functions:
            lines.append("### Source functions not exported")
            for name in unexported_functions:
                lines.append(f"- `{name}()`")
        if stale_exports:
            lines.append("### Exports not found in source")
            for name in stale_exports:
                lines.append(f"- `{name}`")
    lines.append("")

    lines.append("## Test Coverage Signal")
    lines.append("")
    if untested_functions:
        lines.append("These functions are not clearly mentioned in the test file:")
        for name in untested_functions:
            lines.append(f"- `{name}()`")
    else:
        lines.append("Every function name appears in the test file.")
    lines.append("")

    lines.append("## Pytest Result")
    lines.append("")
    if pytest_code == 0:
        lines.append("`python -m pytest -q` passed.")
    else:
        lines.append("`python -m pytest -q` failed or could not run.")
    lines.append("")
    lines.append("```text")
    lines.append((pytest_stdout + pytest_stderr).strip() or "No pytest output captured.")
    lines.append("```")
    lines.append("")

    lines.append("## Recommended Next Action")
    lines.append("")
    if pytest_code != 0:
        lines.append("Fix the test command first.")
    elif untested_functions:
        lines.append("Add focused tests for the untested functions before the next tagged release.")
    elif missing_metadata or missing_files:
        lines.append("Fix repository/package metadata before publishing.")
    else:
        lines.append("Ready for a small release after a final manual README scan.")

    return "\n".join(lines)


def main() -> None:
    """Run the release checker."""
    path = write_report(REPORT_NAME, build_release_report())
    print(f"Release check created: {path}")


if __name__ == "__main__":
    main()
