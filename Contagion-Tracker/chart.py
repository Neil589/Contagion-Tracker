import sys 
from typing import Dict, List
from projects.pj02.model import Model, Cell
from projects.pj02 import constants

"""Hypothesis: the cells won't all get infected as rate of infection isn't as fast as recovery period chosen."""
"""It was interesting using a cell speed means that infection rate is faster while the recovery period relies on real time."""

def main() -> None:
    """Entrypoint of the scene."""
    args: Dict[str, str] = read_args()
    int_vals = strs_to_ints(args["total cells"], args["infected cells"], args["immune cells"])
    x = int_vals[0]
    model = Model(int_vals[0], constants.CELL_SPEED, int_vals[1], int_vals[2])
    list_time = []
    list_immune = []
    list_infected = []
    for _ in range(0, int_vals[0]):
        model.tick()
        list_time.append(model.time)
        if Cell.is_infected:
            list_infected.append(Cell)
        if Cell.is_immune:
            list_immune.append(Cell)
    chart_data(x, list_time, list_infected, list_immune)
    print(args)

def read_args() -> Dict[str, str]: 
    """Reads arguements and allows input of arguements. If expected number of args are not provided exits."""
    if len(sys.argv) != 4:
        print("Usage: [TOTALCELLS] [INFECTEDCELLS] [IMMUNECELLS]")
        exit()
    return {
        "total cells": sys.argv[1],
        "infected cells": sys.argv[2],
        "immune cells": sys.argv[3] 
    }

def strs_to_ints(string_val1: str, string_val2: str, string_val3: str) -> List[int]:
    """Function that converts string elements in a list to floats."""
    a: int = int(string_val1)
    b: int = int(string_val2)
    c: int = int(string_val3)
    list_1 = []
    list_1.append(a)
    list_1.append(b)
    list_1.append(c)
    return list_1

def chart_data(total_cells: int, time: List[int], infected_cells: List[int], immune_cells: List[int]) -> None:
    """Charts data with time on x axis and data on y axis."""
    import matplotlib.pyplot as plt
    plt.title("Chart depicting time vs the number of infected and immune cells.")
    plt.plot(time, infected_cells)
    plt.plot(time, immune_cells)
    plt.xlabel("Ticks in simulation")
    plt.ylabel(str(total_cells))
    plt.show()

if __name__ == "__main__":
    main()