from fastapi import FastAPI, Request
from browser_use import Agent, Browser, BrowserConfig

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/run")
async def run_task(request: Request):
    body = await request.json()
    task = body.get("task", "No task provided")

    # Avvia il browser headless
    config = BrowserConfig(headless=True)
    browser = Browser(config)
    agent = Agent(browser=browser)

    # Esegui il task richiesto
    result = await agent.run(task)

    # Restituisci solo la parte "estratta"
    return {"result": result.extracted_content}
