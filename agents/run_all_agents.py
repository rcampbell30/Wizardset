"""Run all local Wizardset agents.

Use from the repository root:

    python -m agents.run_all_agents

The agents write markdown reports into the reports/ directory.
"""

from __future__ import annotations

from agents import example_generator, readme_coach, release_checker, wizardset_auditor


AGENTS = [
    ("Function Auditor", wizardset_auditor.main),
    ("Example Generator", example_generator.main),
    ("README Coach", readme_coach.main),
    ("Release Checker", release_checker.main),
]


def main() -> None:
    """Run every Wizardset agent in sequence."""
    print("Running Wizardset local agents...\n")

    for name, agent_main in AGENTS:
        print(f"== {name} ==")
        agent_main()
        print("")

    print("Done. Check the reports/ directory for generated markdown reports.")


if __name__ == "__main__":
    main()
