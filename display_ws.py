from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML = ''

@app.get("/")
async def get():
    return HTMLResponse(HTML)


