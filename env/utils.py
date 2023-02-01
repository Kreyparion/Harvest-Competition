from typing import Dict, List, Optional, Tuple, Union
import numpy as np
from random import randrange, randint
import math
import copy

class Action(int):
    pass
    

class State:
    def __init__(self, map_ore:np.ndarray, map_seed: int= None):
        self.map = map_ore
        self.size = 10
        self.starting_ore = 10
        self.max_ore = 500
        self.seed = None

    def build_map(map_seed: int= None, size: int = 10): 
        # Set seed for random number generators
        np.random.seed(map_seed)
        map_ore = np.zeros((size,size))


        # Distribute Kore evenly into quartiles.

        grid = [[0] * size for _ in range(size)]

        # Randomly place a few kore "seeds".
        for i in range(size):
            # random distribution across entire quartile
            grid[np.random.randint(0, size - 1)][np.random.randint(0, size - 1)] = i ** 2

            # as well as a particular distribution weighted toward the center of the map
            grid[np.random.randint(size // 2, size - 1)][np.random.randint(size // 2, size - 1)] = i ** 2
        # Spread the seeds radially.
        radius_grid = copy.deepcopy(grid)
        for r in range(size):
            for c in range(size):
                value = grid[r][c]
                if value == 0:
                    continue

                # keep initial seed values, but constrain radius of clusters
                radius = min(round((value / size) ** 0.5), 1)
                for r2 in range(r - radius + 1, r + radius):
                    for c2 in range(c - radius + 1, c + radius):
                        if 0 <= r2 < size and 0 <= c2 < size:
                            distance = (abs(r2 - r) ** 2 + abs(c2 - c) ** 2) ** 0.5
                            radius_grid[r2][c2] += int(value / max(1, distance) ** distance)
        # add some random sprouts of kore
        radius_grid = np.asarray(radius_grid)
        add_grid = np.random.gumbel(0, 300.0, size=(size, size)).astype(int)
        sparse_radius_grid = np.random.binomial(1, 0.5, size=(size, size))
        add_grid = np.clip(add_grid, 0, a_max=None) * sparse_radius_grid
        radius_grid += add_grid

        # add another set of random locations to the center corner
        corner_grid = np.random.gumbel(0, 500.0, size=(size // 4, size // 4)).astype(int)
        corner_grid = np.clip(corner_grid, 0, a_max=None)
        radius_grid[size - (size // 4):, size - (size // 4):] += corner_grid
        # Normalize the available kore against the defined configuration starting kore.
        total = sum([sum(row) for row in radius_grid])
        for r, row in enumerate(radius_grid):
            for c, val in enumerate(row):
                if val != 0:
                    val = min(max(val /5,10),500)
                map_ore[r][c] = val
        return map_ore

    @classmethod
    def generate(self, map_seed: int= None, size: int = 10)-> "State":
        
        if map_seed == None:
            max_int_32 = (1 << 31) - 1
            map_seed = randrange(max_int_32)
        size = size
        map_ore = self.build_map(map_seed,size)
        return State(map_ore,map_seed)

