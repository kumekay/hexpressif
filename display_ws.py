import json
from board import Layout, Board, BLACK
from display import BaseDisplay

# import asyncio
# from websockets import connect


class Display(BaseDisplay):
    def __init__(self, addr: str, *args, **kwargs) -> None:
        super(Display, self).__init__(*args, **kwargs)

        self.addr = addr

    def write(self, board):
        print(json.dumps(board.to_json()))
