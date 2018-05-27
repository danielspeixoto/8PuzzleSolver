from typing import List, Tuple


class Config:

    correct_config = "012345678"

    def __init__(self, config, zero_x: int, zero_y: int, parent=None, depth=-1):
        self.config = config
        self.zero_x = zero_x
        self.zero_y = zero_y
        self.depth = depth
        self.parent = parent
        self.code = self.encode(config)

    def encode(self, config) -> str:
        code = ""
        for i in range(0, 3):
            for j in range(0, 3):
                code += str(config[i][j])
        return code

    def is_equal(self, config: str):
        return config == self.code

    def correct(self):
        return self.is_equal(Config.correct_config)

    # Verifies which directions the empty cell is able to move
    def variations(self) -> List[Tuple[int, int]]:
        variations_list = []
        if self.zero_x < 2:
            variations_list.append((1, 0))
        if self.zero_x > 0:
            variations_list.append((-1, 0))
        if self.zero_y < 2:
            variations_list.append((0, 1))
        if self.zero_y > 0:
            variations_list.append((0, -1))
        return variations_list

    def print(self):
        for i in range(0, 3):
            for j in range(0, 3):
                print(str(self.config[i][j]), end=' ')
            print()