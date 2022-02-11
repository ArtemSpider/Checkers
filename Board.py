from typing import Dict, List, Tuple

Position = Tuple[int, int]

class Board(object):
    def in_bounds(pos : Position) -> bool:
        return pos[0] >= 0 and pos[0] < 10 and pos[1] >= 0 and pos[1] < 10

    def can_take(self, pos : Position) -> bool:
        return len(self._get_takes(pos)) > 0

    def move(self, pos1: Position, pos2: Position):
        self.grid[pos2[1]][pos2[0]] = self.grid[pos1[1]][pos1[0]]
        self.grid[pos1[1]][pos1[0]] = 0

        self.upgraded[pos2[1]][pos2[0]] = self.upgraded[pos1[1]][pos1[0]]
        self.upgraded[pos1[1]][pos1[0]] = False

        last_line = 9 if self.grid[pos2[1]][pos2[0]] == 1 else 0
        if pos2[1] == last_line:
            self.upgraded[pos2[1]][pos2[0]] = True

    def remove(self, pos: Position):
        self.grid[pos[1]][pos[0]] = 0
        self.upgraded[pos[1]][pos[0]] = False

    def _get_takes(self, pos) -> List[Position]:
        res = []
        if self.upgraded[pos[1]][pos[0]]:
            for dir in [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]:
                d = 1
                while True:
                    npos = (pos[0] + dir[0] * d, pos[1] + dir[1] * d)
                    if Board.in_bounds(npos):
                        if self.grid[npos[1]][npos[0]] == 3 - self.grid[pos[1]][pos[0]]:
                            nnpos = (npos[0] + dir[0], npos[1] + dir[1])
                            if Board.in_bounds(nnpos) and self.grid[nnpos[1]][nnpos[0]] == 0:
                                res.append(nnpos)
                            break
                    else:
                        break
                    d += 1
        else:
            for dir in [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]:
                npos = (pos[0] + dir[0], pos[1] + dir[1])
                if Board.in_bounds(npos):
                    if self.grid[npos[1]][npos[0]] == 3 - self.grid[pos[1]][pos[0]]:
                        nnpos = (npos[0] + dir[0], npos[1] + dir[1])
                        if Board.in_bounds(nnpos) and self.grid[nnpos[1]][nnpos[0]] == 0:
                            res.append(nnpos)
        return res

    def _get_moves(self, pos : Position) -> List[Position]:
        res = self._get_takes(pos)

        if len(res) > 0:
            return res

        if self.upgraded[pos[1]][pos[0]]:
            for dir in [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]:
                d = 1
                while True:
                    npos = (pos[0] + dir[0] * d, pos[1] + dir[1] * d)
                    if Board.in_bounds(npos) and self.grid[npos[1]][npos[0]] == 0:
                        res.append(npos)
                    else:
                        break
                    d += 1
        else:
            dir = +1 if self.grid[pos[1]][pos[0]] == 1 else -1

            npos = (pos[0] + 1, pos[1] + dir)
            if Board.in_bounds(npos) and self.grid[npos[1]][npos[0]] == 0:
                res.append(npos)

            npos = (pos[0] - 1, pos[1] + dir)
            if Board.in_bounds(npos) and self.grid[npos[1]][npos[0]] == 0:
                res.append(npos)
        return res

    def get_all_moves(self) -> Dict[Position, List[Position]]:
        ct = False
        for i in range(10):
            for j in range(10):
                if self.grid[i][j] == self.turn:
                    ct = ct or self.can_take((j, i))

        res = {}
        if ct:
            for i in range(10):
                for j in range(10):
                    if self.grid[i][j] == self.turn:
                        if (j, i) not in res:
                            res[(j, i)] = []

                        p_moves = self._get_takes((j, i))
                        for p in p_moves:
                            res[(j, i)].append(p)
        else:
            for i in range(10):
                for j in range(10):
                    if self.grid[i][j] == self.turn:
                        if (j, i) not in res:
                            res[(j, i)] = []

                        p_moves = self._get_moves((j, i))
                        for p in p_moves:
                            res[(j, i)].append(p)
        return res

    def __init__(self):
        self.grid = [[0 for j in range(10)] for i in range(10)]
        self.upgraded = [[False for j in range(10)] for i in range(10)]
        self.turn = 1

        for i in range(4):
            for j in range(0, 10, 2):
                self.grid[i][(i % 2) + j] = 1

        for i in range(9, 5, -1):
            for j in range(1, 10, 2):
                self.grid[i][(i % 2) - 1 + j] = 2