from PIL import Image


def repr_board(m):
    return "\n".join(" ".join(line) for line in m)


def get_colors():
    '''
    Colors map that the map will use:
        0 - No block
        1 - Fixed reflect block
        2 - Fixed opaque block
        3 - Fixed refract block

    **Returns**

        color_map: *dict, int, tuple, int*
            A dictionary that will correlate the integer key to
            a color.
    '''
    return {
        0: (211, 211, 211),
        1: (255, 20, 147),
        2: (0, 191, 255),
        3: (255, 255, 0),
    }


class Output:
    def __init__(self, bff, solution, block_size=50):
        self.bff = bff
        self.solution = solution
        self.txtname = "solution.txt"
        self.pngname = "solution.png"
        self.block_size = block_size
        self.output()
        self.output_PNG()

    def output(self):
        with open(self.txtname, 'w') as f:
            f.write(repr_board(self.solution)
                    if self.solution else "No solution!")

    def output_PNG(self):
        f = open(self.txtname, "r")
        f_lines = f.readlines()
        w = len(self.bff.board)
        h = len(self.bff.board[0])
        w_pixel = w * self.block_size
        h_pixel = h * self.block_size
        elements = []
        img = Image.new('RGB', (h_pixel, w_pixel), (211, 211, 211))
        colors = get_colors()
        solution = [[0 for x in range(h)] for y in range(w)]
        for element in f_lines:
            elements.append(element.strip())
            element.replace(' ', '')
        for i, x in enumerate(elements):
            color_list = []
            for j in x:
                if j == ' ':
                    j.replace(' ', '')
                elif j != ' ':
                    if j == 'A':
                        color_list.append(1)
                    elif j == 'B':
                        color_list.append(2)
                    elif j == 'C':
                        color_list.append(3)
                    elif j == 'x':
                        color_list.append(0)
                    elif j == 'o':
                        color_list.append(0)
            solution[i] = color_list
        for jx in range(h):
            for jy in range(w):
                x = jx * self.block_size
                y = jy * self.block_size
                for i in range(self.block_size):
                    for j in range(self.block_size):
                        img.putpixel((x + i, y + j), colors[solution[jy][jx]])
        img.save(self.pngname)
