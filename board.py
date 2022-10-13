import json


class Hex:
    def __init__(self, q, r):  # type: (int, int) -> None
        self.q = q
        self.r = r

    def __hash__(self):  # type: () -> int
        return hash((self.q, self.r))

    def __eq__(self, other):
        return self.to_json() == other.to_json()

    @property
    def s(self):  # type: () -> int
        return -self.q - self.r

    def to_json(self):  # type: () -> tuple[int, int]
        return (self.q, self.r)


class Color:
    def __init__(self, r=0, g=0, b=0):  # type: (int, int, int) -> None
        self.r = r
        self.g = g
        self.b = b

    def to_json(self):  # type: () -> tuple[int, int, int]
        return (self.r, self.g, self.b)


BLACK = Color()
WHITE = Color(255, 255, 255)
GRAY_50 = Color(127, 127, 127)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)


class Board:
    def __init__(self, pixels=None):  # type: (dict[Hex, Color] | None) -> None
        if pixels is None:
            self.pixels = {}
        else:
            self.pixels = dict(pixels)

    def __iter__(self):
        return iter(self.pixels)

    def to_json(self):
        return [(k.to_json(), v.to_json()) for (k, v) in self.pixels.items()]


class Layout:
    """
    Layout stores mapping of the LED sequence to the 2d array
    """

    def __init__(self, pixels=None):  # type: (list[Hex]) -> None
        if pixels is None:
            pixels = []
        self.pixels = pixels

    def __len__(self):
        return len(self.pixels)

    def __iter__(self):
        return iter(self.pixels)

    def to_json(self):
        return [h.to_json for h in self.pixels]

    @classmethod
    def from_json(cls, path):
        with open(path) as f:
            return cls([Hex(q, r) for (q, r) in json.loads(f.read())])
