from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from browser_use import Agent, ChatOpenAI

app = FastAPI()


class RunRequest(BaseModel):
    task: str
    model: str = "gpt-4o-mini"
    max_actions: int = 15


@app.get("/")
async def root():
    return {"message": "Browser-use API is running"}


@app.get("/health")
async def health():
    return {"ok": True}


@app.post("/run")
async def run_task(body: RunRequest):
    try:
        agent = Agent(
            task=body.task,
            llm=ChatOpenAI(model=body.model),
            max_actions=body.max_actions,
        )
        result = await agent.run()

        return {
            "final_result": getattr(result, "final_result", None),
            "raw": str(result),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
