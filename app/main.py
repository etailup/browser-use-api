import asyncio
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

from browser_use.agent.service import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use import ChatOpenAI

app = FastAPI()

class RunBody(BaseModel):
    task: str
    model: Optional[str] = "gpt-4o-mini"
    max_actions: Optional[int] = 15

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/run")
async def run_agent(body: RunBody):
    try:
        # Browser configuration with Docker-safe flags
        browser = Browser(
            config=BrowserConfig(
                headless=True,
                args=[
                    "--no-sandbox",
                    "--disable-setuid-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-gpu",
                    "--no-first-run",
                    "--no-default-browser-check",
                    "--disable-features=IsolateOrigins,site-per-process",
                ],
                viewport={"width": 1280, "height": 800},
            )
        )

        llm = ChatOpenAI(model=body.model)

        agent = Agent(
            task=body.task,
            browser=browser,
            llm=llm,
            max_actions=body.max_actions or 15,
        )

        result = await agent.run()

        return {
