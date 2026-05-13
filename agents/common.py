"""Shared helpers for Wizardset local agents.

These agents are intentionally simple. They inspect the local repository,
produce markdown reports, and help keep Wizardset useful as both a Python
utility package and a learning project.
"""

from __future__ import annotations

import ast
import subprocess
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
SOURCE_FILE = ROOT / "wizardset_enhanced" / "wizardset.py"
INIT_FILE = ROOT / "wizardset_enhanced" / "__init__.py"
TEST_FILE = ROOT / "tests" / "test_wizardset.py"
README_FILE = ROOT / "README.md"
PYPROJECT_FILE = ROOT / "pyproject.toml"
REPORTS_DIR = ROOT / "reports"


FUNCTION_EXPLANATIONS: dict[str, str] = {
    "best": "Teaches max(items, key=rule). Finds the item with the highest custom score.",
    "worst": "Teaches min(items, key=rule). Finds the item with the lowest custom score.",
    "rank": "Teaches sorted(items, key=rule). Sorts items using a custom rule.",
    "count_where": "Teaches conditional counting. Counts items that pass a test.",
    "any_match": "Teaches any(). Checks whether at least one item passes a condition.",
    "all_match": "Teaches all(). Checks whether every item passes a condition.",
    "unique": "Teaches sets and order-preserving filtering. Removes repeated items.",
    "frequencies": "Teaches collections.Counter. Counts how often each item appears.",
    "pair": "Teaches zip(). Pairs values from two iterables.",
    "numbered": "Teaches enumerate(). Adds index numbers to items.",
    "average_score": "Scores every item with a rule, then returns the average score.",
    "explain_best": "Shows the winner, runner-up, their scores, and the gap between them.",
    "flatten": "Turns a nested list-like structure into one flat list.",
    "chunk": "Splits a sequence into smaller fixed-size groups.",
    "group_by": "Groups items into a dictionary using a key function.",
    "duplicates": "Finds items that appear more than once.",
    "transpose": "Swaps rows and columns in a matrix-like structure.",
    "map_values": "Teaches map-style thinking. Transforms every item.",
    "filter_values": "Teaches filter-style thinking. Keeps only matching items.",
    "safe_get": "Safely reads nested dictionary values without KeyError crashes.",
    "merge": "Combines two dictionaries, with the second overriding the first.",
    "nested_merge": "Combines dictionaries recursively.",
    "intersection": "Finds items shared by two sequences.",
    "difference": "Finds items in the first sequence but not the second.",
    "prefix_sum": "Builds a running total across a sequence of numbers.",
    "flatten_dict": "Turns nested dictionary keys into dotted flat keys.",
    "unflatten_dict": "Turns dotted flat dictionary keys back into nested dictionaries.",
}


BASIC_EXAMPLES: dict[str, str] = {
    "best": "best([1, 4, 2], lambda n: n)  # 4",
    "worst": "worst([1, 4, 2], lambda n: n)  # 1",
    "rank": "rank(['cat', 'elephant', 'dog'], len)  # ['cat', 'dog', 'elephant']",
    "count_where": "count_where([1, 2, 3, 4], lambda n: n > 2)  # 2",
    "any_match": "any_match(['cat', 'dog'], lambda word: word.startswith('c'))  # True",
    "all_match": "all_match([2, 4, 6], lambda n: n % 2 == 0)  # True",
    "unique": "unique(['a', 'b', 'a'])  # ['a', 'b']",
    "frequencies": "frequencies(['a', 'b', 'a'])  # Counter({'a': 2, 'b': 1})",
    "pair": "pair(['Amy', 'Ben'], [90, 80])  # [('Amy', 90), ('Ben', 80)]",
    "numbered": "numbered(['a', 'b'], start=1)  # [(1, 'a'), (2, 'b')]",
    "average_score": "average_score(['cat', 'elephant'], len)  # 5.5",
    "explain_best": "explain_best(['cat', 'elephant', 'dog'], len)",
    "flatten": "flatten([[1, 2], [3, 4]])  # [1, 2, 3, 4]",
    "chunk": "chunk([1, 2, 3, 4, 5], 2)  # [[1, 2], [3, 4], [5]]",
    "group_by": "group_by(['hi', 'cat', 'dog'], len)  # {2: ['hi'], 3: ['cat', 'dog']}",
    "duplicates": "duplicates(['cat', 'dog', 'cat'])  # ['cat']",
    "transpose": "transpose([[1, 2], [3, 4]])  # [[1, 3], [2, 4]]",
    "map_values": "map_values([1, 2, 3], lambda n: n * 2)  # [2, 4, 6]",
    "filter_values": "filter_values([1, 2, 3, 4], lambda n: n % 2 == 0)  # [2, 4]",
    "safe_get": "safe_get({'a': {'b': 1}}, ['a', 'b'])  # 1",
    "merge": "merge({'a': 1}, {'b': 2})  # {'a': 1, 'b': 2}",
    "nested_merge": "nested_merge({'a': {'x': 1}}, {'a': {'y': 2}})  # {'a': {'x': 1, 'y': 2}}",
    "intersection": "intersection([1, 2, 3], [2, 3, 4])  # [2, 3]",
    "difference": "difference([1, 2, 3], [2])  # [1, 3]",
    "prefix_sum": "prefix_sum([1, 2, 3])  # [1.0, 3.0, 6.0]",
    "flatten_dict": "flatten_dict({'user': {'name': 'Rory'}})  # {'user.name': 'Rory'}",
    "unflatten_dict": "unflatten_dict({'user.name': 'Rory'})  # {'user': {'name': 'Rory'}}",
}


DINOSAUR_EXAMPLES: dict[str, str] = {
    "best": "best(dinosaurs, lambda dino: dino['mass_kg'])  # heaviest dinosaur",
    "worst": "worst(dinosaurs, lambda dino: dino['speed_kmh'])  # slowest dinosaur",
    "rank": "rank(dinosaurs, lambda dino: dino['length_m'], reverse=True)  # longest first",
    "count_where": "count_where(dinosaurs, lambda dino: dino['mass_kg'] > 1000)  # large dinosaurs",
    "any_match": "any_match(dinosaurs, lambda dino: dino['diet'] == 'carnivore')",
    "all_match": "all_match(dinosaurs, lambda dino: dino['era'] == 'Cretaceous')",
    "group_by": "group_by(dinosaurs, lambda dino: dino['diet'])  # group by herbivore/carnivore",
    "average_score": "average_score(dinosaurs, lambda dino: dino['speed_kmh'])",
    "explain_best": "explain_best(dinosaurs, lambda dino: dino['intelligence_score'])",
    "prefix_sum": "prefix_sum([12, 20, 35])  # cumulative fossil finds by dig site",
}


def ensure_reports_dir() -> None:
    """Create the reports directory when it does not exist."""
    REPORTS_DIR.mkdir(exist_ok=True)


def read_text(path: Path) -> str:
    """Read a UTF-8 text file, returning an empty string if it is missing."""
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8-sig")


def write_report(filename: str, content: str) -> Path:
    """Write a markdown report inside reports/."""
    ensure_reports_dir()
    path = REPORTS_DIR / filename
    path.write_text(content.rstrip() + "\n", encoding="utf-8")
    return path


def top_level_functions(path: Path = SOURCE_FILE) -> list[str]:
    """Return all top-level function names from a Python file."""
    source = read_text(path)
    tree = ast.parse(source)
    return [node.name for node in tree.body if isinstance(node, ast.FunctionDef)]


def exported_names(path: Path = INIT_FILE) -> list[str]:
    """Return names listed in __all__ from the package __init__.py file."""
    source = read_text(path)
    tree = ast.parse(source)

    for node in tree.body:
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name) and target.id == "__all__":
                    value = ast.literal_eval(node.value)
                    return list(value)

    return []


def docstring_for_function(function_name: str, path: Path = SOURCE_FILE) -> str:
    """Return a function's docstring from the source file."""
    source = read_text(path)
    tree = ast.parse(source)

    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == function_name:
            return ast.get_docstring(node) or ""

    return ""


def names_mentioned_in_text(names: Iterable[str], text: str) -> list[str]:
    """Return names that appear in a text blob."""
    return [name for name in names if name in text]


def run_command(command: list[str]) -> tuple[int, str, str]:
    """Run a shell command from the repo root and capture the result."""
    completed = subprocess.run(
        command,
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return completed.returncode, completed.stdout, completed.stderr
