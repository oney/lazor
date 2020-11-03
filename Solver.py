from BFF import BFF


class Lazor:
    '''
    The class to represent a moving lazor
    '''

    def __init__(self, x, y, dx, dy):
        '''
        The class initializer

        **Parameters**

            x: *int*
                x of the lazor's position
            y: *int*
                y of the lazor's position
            dx: *int*
                x of the lazor's diration
            dy: *int*
                y of the lazor's diration

        '''
        self.x = x
        self.y = y
        self.dx = dx
        self.dy = dy

    def __eq__(self, other):

        '''
        eq operator for this class, can be used in a set

        **Parameters**

            other: *Lazor class*
                comparing lazor

        **Returns**

            flag: *bool*
                If self euqals to other

        '''
        return other and self.x == other.x and self.y == other.y \
            and self.dx == other.dx and self.dy == other.dy

    def __ne__(self, other):
        '''
        ne operator for this class, can be used in a set

        **Parameters**

            other: *Lazor class*
                comparing lazor

        **Returns**

            flag: *bool*
                If self does not euqal to other

        '''
        return not self.__eq__(other)

    def __hash__(self):
        '''
        hash value for this class, can be used in a set

        **Returns**

            hash: *int*
                The hash value for the lazor

        '''
        return hash((self.x, self.y, self.dx, self.dy))

    def hit_block(self, board):
        '''
        The block that this lazor is going to hit

        **Parameters**

            board: *2-D list of Block class*
                The board

        **Returns**

            block: *Block class or None*
                The hit block

        '''
        # calculate the hit block's coordinates
        if self.x % 2 == 1:  # hit horizontally
            mx = (self.x - 1)//2
            my = self.y//2 - (1 if self.dy == -1 else 0)
        else:  # hit vertically
            mx = self.x//2 - (1 if self.dx == -1 else 0)
            my = (self.y - 1)//2

        # return None if the coordinates are outside of the board
        if mx < 0 or my < 0 or mx >= len(board[0]) or my >= len(board):
            return None
        return board[my][mx]

    def step(self):
        '''
        Return the lazor where self lazor moves straightforward

        **Returns**

            lazor: *Lazor class*
                The lazor where self lazor moves straightforward

        '''
        return Lazor(self.x + self.dx, self.y + self.dy, self.dx, self.dy)

    def reflect(s):
        '''
        Return the lazor where self lazor reflects

        **Returns**

            lazor: *Lazor class*
                The lazor where self lazor reflects

        '''
        if s.x % 2 == 1:  # reflect horizontally
            return Lazor(s.x + s.dx, s.y - s.dy, s.dx, -s.dy)
        else:  # reflect vertically
            return Lazor(s.x - s.dx, s.y + s.dy, -s.dx, s.dy)


class Block:
    '''
    The class to represent a block
    '''

    def __init__(self, type):
        '''
        The class initializer

        **Parameters**

            type: *str*
                the type of block

        '''
        self.type = type

    def placable(self):
        '''
        Return if the block can be placed something

        **Returns**

            flag: *bool*
                Indicate if the block can be placed something

        '''
        return self.type == "o"

    def place(self, type):
        '''
        Replace self's type with te type parameter

        **Parameters**

            type: *str*
                the type of block

        '''
        self.type = type

    def react(self, lazor, dfs):
        '''
        Call dfs to react what will happen according to the lazor and the block

        **Parameters**

            lazor: *Lazor class*
                The moving lazor
            dfs: *function*
                DFS function

        '''
        if self.type == "o" or self.type == "x":  # just go through
            dfs(lazor.step())
        elif self.type == "A":  # reflect
            dfs(lazor.reflect())
        elif self.type == "C":  # go through and reflect
            dfs(lazor.step())
            dfs(lazor.reflect())


class Solver:
    '''
    The class to solve a BFF puzzle
    '''
    def __init__(self, bff: BFF):
        '''
        The class initializer

        **Parameters**

            bff: *BFF class*
                the bff

        '''
        self.bff = bff
        # map to Block class
        self.board = [[Block(t) for t in x] for x in bff.board]
        # map to Lazor class
        self.lazors = [Lazor(x, y, dx, dy) for x, y, dx, dy in bff.lazors]

    def solve(self):
        '''
        Return a solution or None

        **Returns**

            board: *(2-D list of str) or None*
                A solution or None

        '''
        blockMap = ["A", "B", "C"]

        blocks = self.bff.blocks
        board = self.board
        h = len(board)
        w = len(board[0])

        def dfs(prv_b, prv_pos):
            # find the type of a remaining block that can be placed
            b = next((i for i, v in enumerate(blocks) if v != 0), None)

            # if not found(means blocks = [0,0,0]), it means we place all
            # blocks, so we can test whether the current board solve the puzzle
            if b is None:
                return self.solved()

            # When using a block, subtract it by 1
            blocks[b] -= 1
            for x in range(h):
                for y in range(w):
                    # This is to optimize the search by checking if previous
                    # used block is the same and the position has been searched
                    # If it is, we can skip
                    # This optimization can shrink time complexity by A!B!C!
                    if prv_b == b and x * w + y <= prv_pos:
                        continue

                    # If the (x, y) block is not placable, skip
                    if not board[x][y].placable():
                        continue
                    board[x][y].place(blockMap[b])

                    # Place a block and keep placing by doing DFS
                    if dfs(b, x * w + y):
                        # If dfs returns True, it means it found a solution,
                        # so stop searching
                        return True
                    board[x][y].place("o")

            # After current search finishes, add the block back
            blocks[b] += 1
            return False
        # The board's items are mapped back from Block class to str
        return [[b.type for b in x] for x in board] if dfs(-1, -1) else None

    def solved(self):
        '''
        Return if the current board is a solution

        **Returns**

            flag: *bool*
                Indicate if the current board is a solution

        '''
        board = self.board

        # record the remaining points that the lazors haven't passed
        points = set(self.bff.points)

        # coordinates of positions and directions that the lazors have passed
        passed = set()

        def dfs(lazor):
            # if the lazor is in passed, we should skip it
            # otherwise, it would cause an infinite cycle.
            if lazor in passed:
                return
            passed.add(lazor)

            hit_point = (lazor.x, lazor.y)
            # remove the current point from points
            if hit_point in points:
                points.remove(hit_point)
            # if the target points all have been passed, stop searching
            if not points:
                return

            # handle the lazor hitting the block
            block = lazor.hit_block(board)
            if block:
                block.react(lazor, dfs)

        for lazor in self.lazors:
            dfs(lazor)

        # If all points have been passed, the current board is a solution
        return not points
