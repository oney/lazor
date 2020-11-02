from BFF import BFF


class Lazor:
    def __init__(self, x, y, dx, dy):
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def __eq__(self, other):
        return other and self.x == other.x and self.y == other.y \
            and self.dx == other.dx and self.dy == other.dy

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.x, self.y, self.dx, self.dy))

    def hit_block(self, board):
        if self.x % 2 == 1:
            mx = (self.x - 1)//2
            my = self.y//2 - (1 if self.dy == -1 else 0)
        else:
            mx = self.x//2 - (1 if self.dx == -1 else 0)
            my = (self.y - 1)//2

        if mx < 0 or my < 0 or mx >= len(board[0]) or my >= len(board):
            return None
        return board[my][mx]

    def step(self):
        return Lazor(self.x + self.dx, self.y + self.dy, self.dx, self.dy)

    def reflect(s):
        if s.x % 2 == 1:
            return Lazor(s.x + s.dx, s.y - s.dy, s.dx, -s.dy)
        else:
            return Lazor(s.x - s.dx, s.y + s.dy, -s.dx, s.dy)


class Block:
    blockMap = ["A", "B", "C"]

    def __init__(self, type):
        self.type = type

    def placable(self):
        return self.type == "o"

    def place(self, type):
        self.type = type

    def react(self, lazor, dfs):
        if self.type == "o" or self.type == "x":
            dfs(lazor.step())
        elif self.type == "A":
            dfs(lazor.reflect())
        elif self.type == "C":
            dfs(lazor.step())
            dfs(lazor.reflect())


class Solver:
    def __init__(self, bff: BFF):
        self.bff = bff
        self.board = [[Block(t) for t in x] for x in bff.board]
        self.lazors = [Lazor(x, y, dx, dy) for x, y, dx, dy in bff.lazors]

    def solve(self):
        blocks = self.bff.blocks
        board = self.board
        h = len(board)
        w = len(board[0])

        def dfs(prv_b, prv_pos):
            b = next((i for i, v in enumerate(blocks) if v != 0), None)
            if b is None:
                return self.solved()
            blocks[b] -= 1
            for x in range(h):
                for y in range(w):
                    if prv_b == b and x * w + y <= prv_pos:
                        continue
                    if not board[x][y].placable():
                        continue
                    board[x][y].place(Block.blockMap[b])

                    if dfs(b, x * w + y):
                        return True
                    board[x][y].place("o")

            blocks[b] += 1
            return False
        return [[b.type for b in x] for x in board] if dfs(-1, -1) else None

    def solved(self):
        board = self.board
        points = set(self.bff.points)
        passed = set()

        def dfs(lazor):
            if not points:
                return
            if lazor in passed:
                return
            passed.add(lazor)

            if (lazor.x, lazor.y) in points:
                points.remove((lazor.x, lazor.y))

            block = lazor.hit_block(board)
            if block:
                block.react(lazor, dfs)

        for lazor in self.lazors:
            dfs(lazor)

        return not points
