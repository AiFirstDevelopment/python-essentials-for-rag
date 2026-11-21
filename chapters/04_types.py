# Chapter 4: type hints, dataclasses, Pydantic (like TypeScript interfaces, and Zod at runtime).
from dataclasses import dataclass

from pydantic import BaseModel, ValidationError


@dataclass
class Chunk:                        # like: interface Chunk { file: string; page: number; text: string }
    file: str                       # the same fields as rag/chunks.py, which adds seq for widening
    page: int
    text: str


class Question(BaseModel):          # like a Zod schema: checked when the data arrives
    text: str
    top: int = 3


chunk = Chunk(file="returns.txt", page=1, text="You can return any unused item within 30 days.")
print(chunk)

print(Question.model_validate({"text": "How long is the return window?"}))
try:                                # try/except is try/catch
    Question.model_validate({"text": "Hi", "top": "lots"})
except ValidationError as e:
    print("rejected:", e.errors()[0]["msg"])
