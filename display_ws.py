import json

from websockets import connect

from display import BaseDisplay


class Display(BaseDisplay):
    def __init__(self, addr: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.addr = addr

    async def init(self) -> BaseDisplay:
        self.ws = await connect(f"ws://{self.addr}/ws")
        await super().init()

        # Send layout
        msg = json.dumps(["layout", self.layout])
        await self.ws.send(msg)

        # Set default color
        if self.color is not None:
            await self.fill(self.color)

        return self

    async def write(
        self, board: list[tuple[tuple[int, int], tuple[int, int, int]]]
    ) -> None:
        await super().write(board)

        msg = json.dumps(["board", board])
        await self.ws.send(msg)
