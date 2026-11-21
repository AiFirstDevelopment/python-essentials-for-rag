# Chapter 4: types.
from dataclasses import dataclass

from pydantic import BaseModel, ValidationError


def first_words(text: str, n: int = 5) -> str:
    return " ".join(text.split()[:n])


@dataclass
class Chunk:
    file: str
    page: int
    text: str

    def preview(self) -> str:
        return f"{self.file} p.{self.page}: {first_words(self.text)}"


class Question(BaseModel):
    text: str
    top: int = 3


print(Chunk("returns.txt", 1, "You can return any unused item within 30 days.").preview())
try:
    Question.model_validate({"text": "Hi", "top": "lots"})
except ValidationError as e:
    print(e.errors()[0]["msg"])
