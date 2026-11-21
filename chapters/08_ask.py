# Chapter 8: async, and calling a model.
import asyncio

from anthropic import AsyncAnthropic
from dotenv import load_dotenv

load_dotenv()            # ANTHROPIC_API_KEY from .env


async def ask(client, question):
    response = await client.messages.create(
        model="claude-opus-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": question}],
    )
    return "".join(b.text for b in response.content if b.type == "text")


async def main():
    client = AsyncAnthropic()
    answers = await asyncio.gather(
        ask(client, "In one sentence, what is RAG?"),
        ask(client, "In one sentence, what is an embedding?"),
    )
    print(answers)


if __name__ == "__main__":
    asyncio.run(main())
