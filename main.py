import time
from BFF import BFF
from Solver import Solver
from Output import Output


if __name__ == "__main__":
    bff = BFF("numbered_6.bff")
    print(bff)
    start = time.time()
    solver = Solver(bff)
    solution = solver.solve()
    print("solution", solution)
    Output(bff, solution)
