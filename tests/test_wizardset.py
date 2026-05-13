import pytest

from wizardset_enhanced import (
    all_match,
    any_match,
    average_score,
    best,
    chunk,
    count_where,
    difference,
    duplicates,
    explain_best,
    filter_values,
    flatten,
    flatten_dict,
    frequencies,
    group_by,
    intersection,
    map_values,
    merge,
    nested_merge,
    numbered,
    pair,
    prefix_sum,
    rank,
    safe_get,
    transpose,
    unflatten_dict,
    unique,
    worst,
)


def test_core_wizard_functions():
    words = ["cat", "elephant", "dog", "python"]

    assert best(words, len) == "elephant"
    assert worst(words, len) == "cat"
    assert rank(words, len) == ["cat", "dog", "python", "elephant"]
    assert rank(words, len, reverse=True) == ["elephant", "python", "cat", "dog"]
    assert count_where(words, lambda word: len(word) > 3) == 2
    assert any_match(words, lambda word: len(word) > 7) is True
    assert any_match(words, lambda word: len(word) > 20) is False
    assert all_match(words, lambda word: len(word) >= 3) is True
    assert all_match(words, lambda word: "a" in word) is False


def test_collection_helpers():
    items = ["cat", "dog", "cat", "bird", "dog"]

    assert unique(items) == ["cat", "dog", "bird"]
    assert frequencies(items)["cat"] == 2
    assert frequencies(items)["bird"] == 1
    assert pair(["Amy", "Ben"], [90, 80]) == [("Amy", 90), ("Ben", 80)]
    assert pair(["Amy", "Ben", "Cara"], [90, 80]) == [("Amy", 90), ("Ben", 80)]
    assert numbered(["a", "b"], start=1) == [(1, "a"), (2, "b")]
    assert duplicates(items) == ["cat", "dog"]
    assert duplicates(["a", "b", "c"]) == []


def test_scoring_helpers():
    words = ["cat", "elephant", "dog"]

    assert average_score(words, len) == 14 / 3

    result = explain_best(words, len)

    assert result["best"] == "elephant"
    assert result["best_score"] == 8
    assert result["second"] == "cat"
    assert result["second_score"] == 3
    assert result["gap"] == 5


def test_scoring_helpers_raise_clear_errors():
    with pytest.raises(ValueError, match="Cannot compute average"):
        average_score([], len)

    with pytest.raises(ValueError, match="Need at least two items"):
        explain_best(["only-one"], len)


def test_structure_helpers():
    assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]
    assert flatten([[], [1], [], [2, 3]]) == [1, 2, 3]
    assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
    assert chunk([1, 2, 3], 10) == [[1, 2, 3]]
    assert group_by(["hi", "cat", "dog"], len) == {2: ["hi"], 3: ["cat", "dog"]}


def test_chunk_rejects_non_positive_sizes():
    with pytest.raises(ValueError, match="positive integer"):
        chunk([1, 2, 3], 0)

    with pytest.raises(ValueError, match="positive integer"):
        chunk([1, 2, 3], -1)


def test_matrix_and_transform_helpers():
    assert transpose([[1, 2], [3, 4]]) == [[1, 3], [2, 4]]
    assert transpose([[1, 2, 3], [4, 5, 6]]) == [[1, 4], [2, 5], [3, 6]]
    assert transpose([[1, 2], [3]]) == [[1, 3]]

    assert map_values([1, 2, 3], lambda number: number * 2) == [2, 4, 6]
    assert map_values(["cat", "elephant"], len) == [3, 8]

    assert filter_values([1, 2, 3, 4], lambda number: number % 2 == 0) == [2, 4]
    assert filter_values(["cat", "elephant", "dog"], lambda word: len(word) > 3) == ["elephant"]


def test_dictionary_helpers():
    data = {
        "user": {
            "profile": {
                "name": "Rory"
            }
        }
    }

    flat = flatten_dict(data)

    assert safe_get(data, ["user", "profile", "name"]) == "Rory"
    assert safe_get(data, ["user", "profile", "age"], default="missing") == "missing"
    assert safe_get(data, ["user", "profile", "name", "extra"], default=None) is None
    assert flat == {"user.profile.name": "Rory"}
    assert flatten_dict(data, sep="_") == {"user_profile_name": "Rory"}
    assert unflatten_dict(flat) == data
    assert unflatten_dict({"user_profile_name": "Rory"}, sep="_") == data


def test_merge_helpers():
    left = {"name": "Rory", "score": 10}
    right = {"score": 20, "level": "wizard"}

    assert merge(left, right) == {"name": "Rory", "score": 20, "level": "wizard"}
    assert left == {"name": "Rory", "score": 10}

    base = {
        "agent": {
            "name": "Auditor",
            "checks": {
                "tests": True,
                "docs": False,
            },
        },
        "version": "0.1.0",
    }
    override = {
        "agent": {
            "checks": {
                "docs": True,
            },
        },
        "version": "0.2.0",
    }

    assert nested_merge(base, override) == {
        "agent": {
            "name": "Auditor",
            "checks": {
                "tests": True,
                "docs": True,
            },
        },
        "version": "0.2.0",
    }


def test_set_style_sequence_helpers():
    assert intersection([1, 2, 3], [2, 3, 4]) == [2, 3]
    assert intersection([1, 2, 2, 3], [2]) == [2, 2]
    assert intersection(["cat", "dog"], ["bird"]) == []

    assert difference([1, 2, 3], [2]) == [1, 3]
    assert difference([1, 2, 2, 3], [2]) == [1, 3]
    assert difference(["cat", "dog"], []) == ["cat", "dog"]


def test_prefix_sum():
    assert prefix_sum([1, 2, 3]) == [1.0, 3.0, 6.0]
    assert prefix_sum([1.5, 2.5, -1.0]) == [1.5, 4.0, 3.0]
    assert prefix_sum([]) == []
