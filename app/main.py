from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from browser_use import Agent, ChatOpenAI  # simpler import; browser is handled internally

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
        result = await Agent(
            task=body.task,
            llm=ChatOpenAI(model=body.model),
            max_actions=body.max_actions or 15
        ).run()

        return {
            "status": "ok",
            "summary": getattr(result, "final_result", str(result)),
            "raw": str(result),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
