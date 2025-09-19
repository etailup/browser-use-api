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

        # Converti attributi in tipi serializzabili
        final_result = getattr(result, "final_result", None)
        extracted_content = getattr(result, "extracted_content", None)
        intermediate_steps = getattr(result, "intermediate_steps", None)

        # Se sono oggetti, trasformali in stringhe
        if final_result is not None and not isinstance(final_result, (str, int, float, dict, list)):
            final_result = str(final_result)
        if extracted_content is not None and not isinstance(extracted_content, (str, int, float, dict, list)):
            extracted_content = str(extracted_content)
        if intermediate_steps is not None and not isinstance(intermediate_steps, (str, int, float, dict, list)):
            intermediate_steps = str(intermediate_steps)

        return {
            "final_result": final_result,
            "extracted_content": extracted_content,
            "intermediate_steps": intermediate_steps,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
