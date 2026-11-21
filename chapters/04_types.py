# Chapter 4: type hints, dataclasses, and Pydantic, which checks data at runtime.
from dataclasses import dataclass

from pydantic import BaseModel, ValidationError


@dataclass
class Chunk:                        # Python writes __init__(self, file, page, text) for you
    file: str                       # the same fields as rag/chunks.py, which adds seq for widening
    page: int
    text: str

    def preview(self) -> str:       # a method takes self first: the object it was called on
        return f"{self.file} p.{self.page}: {self.text[:30]}"


class Question(BaseModel):          # checked when the data arrives
    text: str
    top: int = 3


chunk = Chunk(file="returns.txt", page=1, text="You can return any unused item within 30 days.")
print(chunk)
print(chunk.preview())

print(Question.model_validate({"text": "How long is the return window?"}))
try:
    Question.model_validate({"text": "Hi", "top": "lots"})
except ValidationError as e:
    print("rejected:", e.errors()[0]["msg"])
