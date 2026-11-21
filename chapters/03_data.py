# Chapter 3: lists, dicts, comprehensions, JSON.
import json

scores = [0.82, 0.91, 0.40, 0.77]
passed = [s for s in scores if s >= 0.5]       # keep the scores of at least 0.5
doubled = [s * 2 for s in scores]              # every score, doubled

doc = {"id": "refunds", "pages": 3, "tags": ["policy", "returns"]}
print(doc["id"], doc.get("author", "unknown"))  # get gives a default for a missing key

by_id = {d["id"]: d for d in [doc, {"id": "shipping", "pages": 2, "tags": []}]}
print(list(by_id))                              # ['refunds', 'shipping']

print(scores[:2], scores[::-1])                 # a slice: the first two; the whole list reversed

text = json.dumps(doc)                          # dict to JSON text
back = json.loads(text)                         # JSON text to dict
print(passed, back == doc)
