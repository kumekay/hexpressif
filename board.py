import json


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY_50 = (127, 127, 127)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class Layout:
    """
    Layout stores mapping of the LED sequence to the 2d array
    """

    def __init__(self, pixels=None):  # type: (list[tuple[int,int]]) -> None
        if pixels is None:
            pixels = []
        self.pixels = pixels

    def __len__(self):
        return len(self.pixels)

    def __iter__(self):
        return iter(self.pixels)

    def to_json(self):
        return self.pixels

    @classmethod
    def from_json(cls, data):  # type: (str) -> Layout
        return cls([tuple(v) for v in json.loads(data)])

    @classmethod
    def from_file(cls, path):  # type: (str) -> Layout
        with open(path) as f:
            return cls.from_json(f.read())
