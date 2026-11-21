# Chapter 3: data.
import json

scores = [0.82, 0.91, 0.40, 0.77]
doc = {"id": "returns", "pages": 3}

passed = [s for s in scores if s >= 0.5]
print(passed)

print(doc.get("author", "unknown"))
print(scores[:2], scores[::-1])

text = json.dumps(doc)
print(json.loads(text) == doc)
