# Chapter 4: type hints, dataclasses, Pydantic (like TypeScript interfaces, and Zod at runtime).
from dataclasses import dataclass

from pydantic import BaseModel, ValidationError


@dataclass
class Chunk:                        # like: interface Chunk { source: string; text: string; page?: number }
    source: str
    text: str
    page: int | None = None


class Question(BaseModel):          # like a Zod schema: checked when the data arrives
    text: str
    top_k: int = 3


chunk = Chunk(source="refunds.txt", text="Returns are accepted within 30 days.")
print(chunk)

print(Question.model_validate({"text": "How long is the return window?"}))
try:
    Question.model_validate({"text": "Hi", "top_k": "lots"})
except ValidationError as e:
    print("rejected:", e.errors()[0]["msg"])
