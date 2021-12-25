"""The model classes maintain the state and logic of the simulation."""

from __future__ import annotations
from typing import List
from random import random
from projects.pj02 import constants
from math import sin, cos, pi 
import math


__author__ = "730363127"


class Point:
    """A model of a 2-d cartesian coordinate Point."""
    x: float
    y: float

    def __init__(self, x: float, y: float):
        """Construct a point with x, y coordinates."""
        self.x = x
        self.y = y

    def add(self, other: Point) -> Point:
        """Add two Point objects together and return a new Point."""
        x: float = self.x + other.x
        y: float = self.y + other.y
        return Point(x, y)

    def distance(self, point1: Point) -> float:
        """Find the distance between two points."""
        diff_x = point1.x - self.x
        diff_y = point1.y - self.y
        square_x = diff_x ** 2
        square_y = diff_y ** 2
        sum_xy = square_x + square_y
        return math.sqrt(sum_xy)
        

class Cell:
    """An individual subject in the simulation."""
    location: Point
    direction: Point
    sickness: int = 0

    def __init__(self, location: Point, direction: Point):
        """Construct a cell with its location and direction."""
        self.location = location
        self.direction = direction

    # Part 1) Define a method named `tick` with no parameters.
    # Its purpose is to reassign the object's location attribute
    # the result of adding the self object's location with its
    # direction. Hint: Look at the add method.
    def tick(self) -> None:
        """Changes the sickness attribute and checks it with recovery time if immune."""
        self.location = self.location.add(self.direction)
        if self.is_infected():
            self.sickness = self.sickness + 1
        if self.sickness > constants.RECOVERY_PERIOD:
            self.immunize()

    def color(self) -> str:
        """Return the color representation of a cell."""
        if self.is_vulnerable():
            return "gray"
        if self.is_infected():
            return "blue"
        elif self.is_immune():
            return "green"
        return "red"

    def contract_disease(self) -> None:
        """Function to set the infected cell constant to the cell."""
        self.sickness = constants.INFECTED
    
    def is_vulnerable(self) -> bool:
        """Function to check if a cell is vulnerable."""
        if self.sickness == constants.VULNERABLE:
            return True
        else:
            return False
    
    def is_infected(self) -> bool:
        """Function to check if a cell is infected."""
        if self.sickness >= constants.INFECTED:
            return True
        else:
            return False

    def contact_with(self, cell2: Cell) -> None:
        """Function to make a cell infected if it meets an infected cell."""
        if self.is_vulnerable() and cell2.is_infected():
            self.contract_disease()
        if self.is_infected() and cell2.is_vulnerable():
            cell2.contract_disease()

    def immunize(self) -> None:
        """Function to set the immune cell constant to the cell."""
        self.sickness = constants.IMMUNE

    def is_immune(self) -> bool:
        """Function to check if a cell is immune."""
        if self.sickness == constants.IMMUNE:
            return True
        else:
            return False


class Model:
    """The state of the simulation."""
    population: List[Cell]
    time: int = 0

    def __init__(self, cells: int, speed: float, infected_cells: int, immune_cells: int = 0):
        """Initialize the cells with random locations and directions."""
        self.population = []
        if infected_cells < 1 or infected_cells >= cells:
            raise ValueError("There needs to be some cells that start infected.")
        if immune_cells < 0 or immune_cells >= cells:
            raise ValueError("Number of immune cells exceeds number of total cells.")
        for _ in range(0, cells):
            start_loc = self.random_location()
            start_dir = self.random_direction(speed)
            self.population.append(Cell(start_loc, start_dir))
        for x in range(0, infected_cells):
            self.population[x].contract_disease()
        for x in range(infected_cells, infected_cells + immune_cells):
            self.population[x].immunize()

    def tick(self) -> None:
        """Update the state of the simulation by one time step."""
        self.time += 1
        for cell in self.population:
            cell.tick()
            self.enforce_bounds(cell)
        self.check_contacts()

    def random_location(self) -> Point:
        """Generate a random location."""
        start_x = random() * constants.BOUNDS_WIDTH - constants.MAX_X
        start_y = random() * constants.BOUNDS_HEIGHT - constants.MAX_Y
        return Point(start_x, start_y)

    def random_direction(self, speed: float) -> Point:
        """Generate a 'point' used as a directional vector."""
        random_angle = 2.0 * pi * random()
        dir_x = cos(random_angle) * speed
        dir_y = sin(random_angle) * speed
        return Point(dir_x, dir_y)

    def enforce_bounds(self, cell: Cell) -> None:
        """Cause a cell to 'bounce' if it goes out of bounds."""
        if cell.location.x > constants.MAX_X:
            cell.location.x = constants.MAX_X
            cell.direction.x *= -1
        if cell.location.x < constants.MIN_X:
            cell.location.x = constants.MIN_X
            cell.direction.x *= -1
        if cell.location.y > constants.MAX_Y:
            cell.location.y = constants.MAX_Y
            cell.direction.y *= -1
        if cell.location.y < constants.MIN_Y:
            cell.location.y = constants.MIN_Y
            cell.direction.y *= -1

    def check_contacts(self) -> None:
        """Function to check if theres contact between two cells using cell radius."""
        len_population: int = len(self.population)
        x: int = 0
        while x < len_population:
            y: int = x + 1
            while y < len_population: 
                location_x = self.population[x].location
                location_y = self.population[y].location
                distance: float = location_x.distance(location_y)
                if distance < constants.CELL_RADIUS:
                    self.population[x].contact_with(self.population[y])
                y = y + 1
            x = x + 1       

    def is_complete(self) -> bool:
        """Method to indicate when the simulation is complete."""
        for x in range(0, len(self.population)):
            if self.population[x].is_infected():
                return False
        return True