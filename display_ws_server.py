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
    subscribed = False
    while True:
        data = await websocket.receive_json()
        match data[0]:
            case "sub":
                subscribed = True
            case "board" | "layout":
                if subscribed:
                    await websocket.send_json(data)
