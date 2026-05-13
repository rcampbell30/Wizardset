"""Agent 001: Wizardset Function Auditor.

This agent checks whether Wizardset's public functions are documented,
exported, and mentioned in the test suite. It produces a markdown report
that is useful before a new release or README update.
"""

from __future__ import annotations

from agents.common import (
    FUNCTION_EXPLANATIONS,
    TEST_FILE,
    docstring_for_function,
    exported_names,
    names_mentioned_in_text,
    read_text,
    top_level_functions,
    write_report,
)


REPORT_NAME = "wizardset_audit.md"


def build_audit_report() -> str:
    """Build a markdown report about Wizardset's function health."""
    functions = top_level_functions()
    exports = exported_names()
    test_text = read_text(TEST_FILE)
    tested = names_mentioned_in_text(functions, test_text)

    missing_exports = [name for name in functions if name not in exports]
    stale_exports = [name for name in exports if name not in functions]
    missing_tests = [name for name in functions if name not in tested]
    missing_explanations = [name for name in functions if name not in FUNCTION_EXPLANATIONS]
    missing_docstrings = [name for name in functions if not docstring_for_function(name)]

    lines: list[str] = []
    lines.append("# Wizardset Audit Report")
    lines.append("")
    lines.append("## Summary")
    lines.append("")
    lines.append(f"- Source functions found: **{len(functions)}**")
    lines.append(f"- Public exports found: **{len(exports)}**")
    lines.append(f"- Functions mentioned in tests: **{len(tested)}**")
    lines.append(f"- Missing/weak test mentions: **{len(missing_tests)}**")
    lines.append("")

    lines.append("## Function Index")
    lines.append("")
    for name in functions:
        lines.append(f"### `{name}()`")
        lines.append(FUNCTION_EXPLANATIONS.get(name, "No beginner explanation added yet."))
        lines.append("")

    lines.append("## Missing or Weak Test Coverage")
    lines.append("")
    if missing_tests:
        for name in missing_tests:
            lines.append(f"- `{name}()`")
    else:
        lines.append("Every source function appears in the test file.")
    lines.append("")

    lines.append("## Export Mismatches")
    lines.append("")
    if not missing_exports and not stale_exports:
        lines.append("No export mismatches found.")
    else:
        if missing_exports:
            lines.append("### Functions missing from `__all__`")
            for name in missing_exports:
                lines.append(f"- `{name}()`")
            lines.append("")
        if stale_exports:
            lines.append("### Names exported but not found in source")
            for name in stale_exports:
                lines.append(f"- `{name}`")
    lines.append("")

    lines.append("## Documentation Gaps")
    lines.append("")
    if missing_docstrings:
        lines.append("### Missing docstrings")
        for name in missing_docstrings:
            lines.append(f"- `{name}()`")
        lines.append("")
    else:
        lines.append("Every source function has a docstring.")
        lines.append("")

    if missing_explanations:
        lines.append("### Missing beginner explanations")
        for name in missing_explanations:
            lines.append(f"- `{name}()`")
    else:
        lines.append("Every source function has a beginner explanation in the agent knowledge map.")
    lines.append("")

    lines.append("## Recommended Next Action")
    lines.append("")
    if missing_tests:
        lines.append("Add tests for the missing/weakly covered functions first.")
    elif missing_exports or stale_exports:
        lines.append("Fix the export mismatch before publishing a new release.")
    else:
        lines.append("The package is ready for example expansion, README polish, or a patch release.")

    return "\n".join(lines)


def main() -> None:
    """Run the auditor and write the report."""
    path = write_report(REPORT_NAME, build_audit_report())
    print(f"Audit report created: {path}")


if __name__ == "__main__":
    main()
