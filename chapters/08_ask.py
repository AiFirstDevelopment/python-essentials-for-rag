# Chapter 8: async and calling a model. async/await as in JavaScript; asyncio.run starts the loop.
import asyncio

from anthropic import AsyncAnthropic


async def ask(client: AsyncAnthropic, question: str) -> str:
    response = await client.messages.create(
        model="claude-opus-5-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": question}],
    )
    if response.stop_reason == "refusal":
        return "The model declined."
    return "".join(block.text for block in response.content if block.type == "text")


async def main():
    client = AsyncAnthropic()                     # reads ANTHROPIC_API_KEY
    answers = await asyncio.gather(               # like Promise.all
        ask(client, "In one sentence: what is RAG?"),
        ask(client, "In one sentence: what is an embedding?"),
    )
    for a in answers:
        print(a)


if __name__ == "__main__":                        # runs only when this file is run, not when it is imported
    asyncio.run(main())
