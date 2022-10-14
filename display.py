from board import Layout, Board, BLACK, Color


class Uninitialized(Exception):
    pass


class BaseDisplay:
    def __init__(self, layout, color=None):  # type: (Layout, Color | None) -> None
        self.layout = layout
        self.layout_dict = {v: k for (k, v) in enumerate(layout)}
        self.color = color
        self._initialized = False

    async def init(self):  # type: () -> BaseDisplay
        self._initialized = True
        return self

    async def write(self, board):  # type: (Board) -> None
        if not self._initialized:
            raise Uninitialized("You must await 'init()' before using display")

    async def fill(self, color=BLACK):  # type: (Color) -> None
        board = Board({hex: color for hex in self.layout_dict})
        await self.write(board)
