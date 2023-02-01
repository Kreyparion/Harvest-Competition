from env.utils import Action, State
from env.environnement import Env
import sys
import numpy as np
import time
import copy
import random

class BruteForce:
    def __init__(self, solution:Env):
        self.solution = solution
        self.max_depth = solution.max_step
        self.best_cost = 0
        self.best_sol = None
        self.possible_action = self.solution.getPossibleActionsAsInt()
        self.n_children = len(self.possible_action)
        self.timer = time.time()
        self.time_limit = 10
    
    def brute_force(self,solution:Env):
        # stop the code after some time
        if time.time() - self.timer > self.time_limit:
            return
        # if at max depth, check if the solution is better
        if solution.step_num == self.max_depth:
            if solution.score > self.best_cost:
                self.best_cost = solution.score
                self.best_sol = solution
            return
        # else, try all possible actions
        for i in range(self.n_children):
            child = copy.deepcopy(solution)
            child.step(self.possible_action[i])
            self.brute_force(child)

if __name__ == "__main__":
    solution = Env(42)
    solution.reset()
    bf = BruteForce(solution)
    bf.brute_force(solution)
    print("Best solution found:")
    save = False
    if save:
        bf.best_sol.save_solution()
    render = False
    if render:
        bf.best_sol.final_render(speed=5)
    print("Score:",bf.best_sol.score)
    
        
