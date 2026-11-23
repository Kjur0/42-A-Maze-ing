from app.config import MazeConfig
from mazegen.mazegen import BaseMazeGen


class KruskalMazeGen(BaseMazeGen):
    def __init__(self,
                 config: MazeConfig) -> None:
        raise NotImplementedError
