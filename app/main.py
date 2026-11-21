"""Chapter 11: from script to chatbot. The same pipeline behind a web page: the index is built once, when the server
starts, and each question is one POST to /ask.    uv run fastapi dev app/main.py   then open http://localhost:8000"""
from contextlib import asynccontextmanager
from pathlib import Path

from anthropic import AsyncAnthropic
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from rag.pipeline import Index, answer, embedder, load

state = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    state["index"] = Index(load(), embedder())        # chunked and embedded once, at startup
    state["client"] = AsyncAnthropic()
    yield


app = FastAPI(lifespan=lifespan)


class Question(BaseModel):
    question: str


class Reply(BaseModel):
    answer: str
    sources: list[str]


@app.get("/")
async def page():
    return FileResponse(Path(__file__).parent / "index.html")


@app.post("/ask")
async def ask(body: Question) -> Reply:
    passages = await state["index"].retrieve(body.question, state["client"])
    text = await answer(body.question, passages, state["client"])
    return Reply(answer=text, sources=[f"{p.file}, page {p.first_page}" for p in passages])
