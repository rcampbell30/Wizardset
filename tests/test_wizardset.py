from wizardset_enhanced import (
    best,
    worst,
    rank,
    count_where,
    any_match,
    all_match,
    unique,
    frequencies,
    pair,
    numbered,
    average_score,
    explain_best,
    flatten,
    chunk,
    group_by,
    duplicates,
    safe_get,
    flatten_dict,
    unflatten_dict,
)


def test_core_wizard_functions():
    words = ["cat", "elephant", "dog", "python"]

    assert best(words, len) == "elephant"
    assert worst(words, len) == "cat"
    assert rank(words, len) == ["cat", "dog", "python", "elephant"]
    assert count_where(words, lambda word: len(word) > 3) == 2
    assert any_match(words, lambda word: len(word) > 7) is True
    assert all_match(words, lambda word: len(word) >= 3) is True


def test_collection_helpers():
    items = ["cat", "dog", "cat", "bird", "dog"]

    assert unique(items) == ["cat", "dog", "bird"]
    assert frequencies(items)["cat"] == 2
    assert pair(["Amy", "Ben"], [90, 80]) == [("Amy", 90), ("Ben", 80)]
    assert numbered(["a", "b"], start=1) == [(1, "a"), (2, "b")]
    assert duplicates(items) == ["cat", "dog"]


def test_scoring_helpers():
    words = ["cat", "elephant", "dog"]

    assert average_score(words, len) == 14 / 3

    result = explain_best(words, len)

    assert result["best"] == "elephant"
    assert result["best_score"] == 8
    assert result["gap"] == 5


def test_structure_helpers():
    assert flatten([[1, 2], [3, 4]]) == [1, 2, 3, 4]
    assert chunk([1, 2, 3, 4, 5], 2) == [[1, 2], [3, 4], [5]]
    assert group_by(["hi", "cat", "dog"], len) == {2: ["hi"], 3: ["cat", "dog"]}


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
    assert flat == {"user.profile.name": "Rory"}
    assert unflatten_dict(flat) == data
