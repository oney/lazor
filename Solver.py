from BFF import BFF


class Solver:
    def __init__(self, bff: BFF):
        self.bff = bff

    def solve(self):
        blocks = self.bff.blocks
        board = self.bff.board
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
                    if board[x][y] != "o":
                        continue
                    board[x][y] = BFF.blockMap[b]

                    if dfs(b, x * w + y):
                        return True
                    board[x][y] = "o"

            blocks[b] += 1
            return False
        return board if dfs(-1, -1) else None

    def solved(self):
        board = self.bff.board
        points = set(self.bff.points)
        passed = set()

        def dfs(lazor):
            if not points:
                return
            if lazor in passed:
                return
            passed.add(lazor)

            x, y, dx, dy = lazor
            if (x, y) in points:
                points.remove((x, y))

            # if x < 0 or y < 0 or x > len(board[0])*2 or y > len(board)*2:
            #     return

            if x % 2 == 1:
                mx = (x - 1)//2
                my = y//2 - (1 if dy == -1 else 0)
            else:
                mx = x//2 - (1 if dx == -1 else 0)
                my = (y - 1)//2

            if mx < 0 or my < 0 or mx >= len(board[0]) or my >= len(board):
                return
            block = board[my][mx]

            def step():
                dfs((x + dx, y + dy, dx, dy))

            def reflect():
                if x % 2 == 1:
                    dfs((x + dx, y - dy, dx, -dy))
                else:
                    dfs((x - dx, y + dy, -dx, dy))

            if block == "o" or block == "x":
                step()
            elif block == "A":
                reflect()
            elif block == "C":
                step()
                reflect()

        for lazor in self.bff.lazors:
            dfs(lazor)

        return not points