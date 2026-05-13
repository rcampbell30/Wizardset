# Wizardset Local Agents

Wizardset now includes a small local agent set for maintaining the project as a beginner-friendly Python learning package.

These agents do **not** call an LLM. They inspect the local repo and generate markdown reports in `reports/`.

## Run all agents

From the repository root:

```bash
python -m agents.run_all_agents
```

## Run one agent

```bash
python -m agents.wizardset_auditor
python -m agents.example_generator
python -m agents.readme_coach
python -m agents.release_checker
```

## Agent 001: Function Auditor

File:

```txt
agents/wizardset_auditor.py
```

Creates:

```txt
reports/wizardset_audit.md
```

Checks:

- source functions
- exported names
- test mentions
- docstrings
- beginner explanations

## Agent 002: Example Generator

File:

```txt
agents/example_generator.py
```

Creates:

```txt
reports/beginner_examples.md
```

Generates:

- basic examples
- dinosaur examples
- beginner explanations

## Agent 003: README Coach

File:

```txt
agents/readme_coach.py
```

Creates:

```txt
reports/readme_coach.md
```

Suggests:

- stronger positioning
- missing README sections
- learning-first explanation blocks
- compact examples to add later

## Agent 004: Release Checker

File:

```txt
agents/release_checker.py
```

Creates:

```txt
reports/release_check.md
```

Checks:

- required files
- `pyproject.toml` metadata
- export health
- test coverage signal
- pytest result
- rough release-readiness score

## Intended workflow

1. Edit Wizardset source or tests.
2. Run:

```bash
python -m agents.run_all_agents
```

3. Read the reports in `reports/`.
4. Fix weak tests, docs, or release issues.
5. Commit the useful changes.

## Why these agents exist

Wizardset is not only a utility package. It is a Python learning package. The agents help keep that identity clear by checking whether functions are explained, tested, exported, and ready for release.
