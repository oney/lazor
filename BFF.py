import os


def repr_board(m):
    '''
    This will represent the board from a list to string

    Parameters
    ----------
    m : list
        A list representation of the board

    Returns
    -------
    str
        A string representation of the board

    '''
    return "\n".join(" ".join(line) for line in m)


class BFF:
    '''
    This BFF class will handle the .bff file that will be solved as the board
    '''
    blockMap = ["A", "B", "C"]

    def __init__(self, fptr):
        '''
        Initiate class variables

        Parameters
        ----------
        fptr : .bff file
            The .bff file of the board

        Returns
        -------
        None.

        '''
        self.ext = os.path.splitext(fptr)[-1].lower()
        if self.ext == '.bff':
            self.board = []
            self.blocks = [0, 0, 0]
            self.lazors = []
            self.points = []
            self.read(fptr)
        else:
            raise NotImplementedError('Wrong input data type, please load'
                                      ' the correct .bff file')

    def read(self, fptr):
        '''
        Read in the .bff file and handle each line in the file to assign
        values to the initiated class variables

        Parameters
        ----------
        fptr : .bff file
            The .bff file of the board

        Returns
        -------
        None.

        '''
        griding = False

        def handle(line):
            nonlocal griding
            '''
            This handles each line in the .bff file based on what they are and
            assign those line into the initiated class variables based on the
            information.

            Parameters
            ----------
            line : str
                Each str lines in the .bff file

            Returns
            -------
            None.

            '''
            if line.startswith("#") or len(line) == 0:
                return
            if line == "GRID START":
                griding = True
            elif line == "GRID STOP":
                griding = False
            elif griding:
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
        '''
        This will map the class variables into str type based on the define
        order

        Returns
        -------
        TYPE str
            str represenation of all of the class variabels based on the
            defined order.

        '''
        return "\n".join(
            map(str, [
                repr_board(self.board),
                self.blocks, self.lazors, self.points]))
