from fastapi import FastAPI  # type: ignore
from fastapi.responses import StreamingResponse  # type: ignore
from openai import OpenAI  # type: ignore

app = FastAPI()

MAX_CHARS = 500

@app.get("/api")
def idea():
    client = OpenAI()
    prompt = [{"role": "user", "content": f"Reply with a new business idea for AI Agents, formatted with headings, sub-headings and bullet points. Keep it under {MAX_CHARS} characters."}]
    stream = client.chat.completions.create(model="gpt-5-nano", messages=prompt, stream=True)

    def event_stream():
        sent = 0
        for chunk in stream:
            if sent >= MAX_CHARS:
                break
            text = chunk.choices[0].delta.content
            if text:
                text = text[: MAX_CHARS - sent]
                sent += len(text)
                lines = text.split("\n")
                for line in lines:
                    yield f"data: {line}\n"
                yield "\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream")