from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from starlette.websockets import WebSocketState
from fastapi.responses import HTMLResponse

app = FastAPI()

HTML = ""

connections: list[WebSocket] = []


@app.get("/")
async def get():
    return HTMLResponse(HTML)


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_json()
            match data[0]:
                case "sub":
                    connections.append(ws)
                case "board" | "layout":
                    for con in connections:
                        if con.client_state == WebSocketState.CONNECTED:
                            await con.send_json(data)
    except WebSocketDisconnect:
        if ws in connections:
            connections.remove(ws)
