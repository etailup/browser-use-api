import os
import asyncio
from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

from browser_use import Agent, ChatOpenAI

app = FastAPI()

class RunPayload(BaseModel):
    task: str = Field(..., description="What the agent should do")
    model: str = Field(default="gpt-4.1-mini", description="LLM model name")
    start_url: Optional[str] = None
    max_actions: int = 30
    extra_instructions: Optional[str] = None

@app.get("/health")
async def health():
    return {"ok": True}

@app.post("/run")
async def run_agent(payload: RunPayload):
    llm = ChatOpenAI(model=payload.model)

    task_text = payload.task
    if payload.start_url:
        task_text += f"\nStart from: {payload.start_url}"
    if payload.extra_instructions:
        task_text += f"\nExtra: {payload.extra_instructions}"

    agent = Agent(task=task_text, llm=llm, max_actions=payload.max_actions)
    result = await agent.run()

    return {
        "status": "ok",
        "summary": getattr(result, "final_result", str(result)),
        "raw": str(result)
    }

