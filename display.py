from board import Layout, BLACK


class Uninitialized(Exception):
    pass


class BaseDisplay:
    def __init__(
        self, layout, color=None
    ):  # type: (Layout, tuple[int, int, int] | None) -> None
        self.layout = [tuple(v) for v in layout]
        self.layout_dict = {v: k for (k, v) in enumerate(layout)}
        self.color = color
        self._initialized = False

    async def init(self):  # type: () -> BaseDisplay
        self._initialized = True
        return self

    async def write(
        self, board
    ):  # type: (list[tuple[tuple[int, int], tuple[int, int, int]]]) -> None
        if not self._initialized:
            raise Uninitialized("You must await 'init()' before using display")

    async def fill(self, color=BLACK):  # type: (tuple[int, int, int]) -> None
        await self.write([(h, color) for h in self.layout_dict.keys()])
