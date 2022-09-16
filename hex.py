from collections.abc import Mapping


class Hex:
    def __init__(self, q: int, r: int):
        self.q = q
        self.r = r

    def __hash__(self) -> int:
        return hash((self.q, self.r))

    @property
    def s(self) -> int:
        return -self.q - self.r


class Color:
    def __init__(self, q: int, r: int):
        self.q = q
        self.r = r

    @property
    def s(self) -> int:
        return -self.q - self.r


class Board:
    def __init__(self, hexes: Mapping[Hex, Color] = None):
        if hexes is None:
            self.hexes: dict[Hex, Color] = {}
        else:
            self.hexes = dict(hexes)
