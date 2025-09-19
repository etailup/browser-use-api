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
    """
    Avvia un task con browser-use e restituisce risultati JSON-serializzabili.
    """
    try:
        agent = Agent(
            task=body.task,
            llm=ChatOpenAI(model=body.model),
            max_actions=body.max_actions,
        )
        result = await agent.run()

        # Chiamare i metodi per ottenere i valori reali
        final_result = None
        extracted_content = None
        intermediate_steps = None

        try:
            if callable(getattr(result, "final_result", None)):
                final_result = result.final_result()
        except Exception:
            pass

        try:
            if callable(getattr(result, "extracted_content", None)):
                extracted_content = result.extracted_content()
        except Exception:
            pass

        try:
            if hasattr(result, "intermediate_steps"):
                intermediate_steps = result.intermediate_steps
        except Exception:
            pass

        return {
            "final_result": final_result,
            "extracted_content": extracted_content,
            "intermediate_steps": intermediate_steps,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
