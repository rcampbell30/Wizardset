from wizardset_enhanced import (
    best,
    rank,
    count_where,
    group_by,
    flatten_dict,
    safe_get,
    explain_best,
)


words = ["cat", "elephant", "dog", "python", "hippopotamus"]

print("Best word:", best(words, len))

print("Ranked words:", rank(words, len, reverse=True))

print("Words longer than 4 letters:", count_where(words, lambda word: len(word) > 4))

print("Words grouped by length:", group_by(words, len))

print("Explained winner:", explain_best(words, len))


data = {
    "user": {
        "profile": {
            "name": "Rory",
            "skill": "Python"
        }
    }
}

print("Safe nested get:", safe_get(data, ["user", "profile", "name"]))

print("Flattened dictionary:", flatten_dict(data))
