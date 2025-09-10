from fastapi import FastAPI, Query
from pydantic import BaseModel
from typing import Optional

# importa la tua logica (browser agent, ecc.)
# se non ce l’hai ancora separata, puoi simulare la risposta
# sostituendo questa funzione con quella vera che hai già
async def run_browser_task(task: str, model: str, max_actions: int):
    """
    Finge di eseguire il task con browser-use e restituisce un risultato
    compatibile con il formato che hai già visto.
    """
    class Result:
        extracted_content = '{"checkbox1": false, "checkbox2": true}'
        full_output = {
            "all_results": [
                {
                    "is_done": True,
                    "success": True,
                    "extracted_content": '{"checkbox1": false, "checkbox2": true}'
                }
            ]
        }

    return Result()

# Pydantic model per validare la richiesta
class TaskRequest(BaseModel):
    task: str
    model: Optional[str] = "gpt-4.1-mini"
    max_actions: Optional[int] = 15

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/run")
async def run_task(
    req: TaskRequest,
    output: str = Query("full", description="Set 'content_only' per ottenere solo il contenuto estratto")
):
    result = await run_browser_task(req.task, req.model, req.max_actions)

    if output == "content_only":
        # 🔥 Restituisce solo l’estratto, in JSON puro
        return result.extracted_content

    # 🔥 Restituisce tutto (debug, metadati ecc.)
    return result.full_output
