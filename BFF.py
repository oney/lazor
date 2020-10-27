def repr_board(m):
    return "\n".join(" ".join(line) for line in m)


class BFF:
    blockMap = ["A", "B", "C"]

    def __init__(self, fptr):
        self.board = []
        self.blocks = [0, 0, 0]
        self.lazors = []
        self.points = []
        self.griding = False
        self.read(fptr)

    def read(self, fptr):
        def handle(line):
            if line.startswith("#") or len(line) == 0:
                return
            if line == "GRID START":
                self.griding = True
            elif line == "GRID STOP":
                self.griding = False
            elif self.griding:
                line = line.replace(" ", "")
                self.board.append(list(line))
            elif line[0] in ["A", "B", "C"]:
                self.blocks[ord(line[0]) - ord("A")] = int(line[1:])
            elif line[0] in ["L", "P"]:
                items = filter(lambda x: len(x), line[1:].split(" "))
                res = tuple(map(lambda x: int(x), items))
                (self.lazors if line[0] == "L" else self.points).append(res)

        with open(fptr) as f:
            for line in f:
                handle(line.strip())

    def __str__(self):
        return "\n".join(
            map(str, [
                repr_board(self.board),
                self.blocks, self.lazors, self.points]))
