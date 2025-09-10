from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import os, asyncio
from browser_use import Agent, Browser, BrowserConfig

app = FastAPI(title="browser-use-api")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

class RunBody(BaseModel):
    task: str
    model: str | None = None
    max_actions: int | None = 15

@app.get("/")
def root():
    return {"message": "Browser-use API is running", "endpoints": ["/health", "/run"]}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run")
async def run_agent(body: RunBody):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(500, "OPENAI_API_KEY is not set")
    browser = Browser(BrowserConfig(headless=True))
    agent = Agent(task=body.task, llm=body.model or "gpt-4o-mini", browser=browser, max_actions=body.max_actions or 15)
    try:
        result = await agent.run()
        return {"ok": True, "result": result}
    finally:
        await browser.close()
