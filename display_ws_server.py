from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML = ""


@app.get("/")
async def get():
    return HTMLResponse(HTML)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_json()
        # await websocket.send_text(f"Message text was: {data}")
        print(data)
