import json
from board import Layout, Board, BLACK, Color


class BaseDisplay:
    def __init__(self, layout, fill=BLACK):  # type: (Layout, Color) -> None
        self.layout = {v: k for (k, v) in enumerate(layout)}

        board = Board({hex: fill for hex in layout})
        self.write(board)

    def write(self, board):  # type: (Board) -> None
        raise NotImplemented
