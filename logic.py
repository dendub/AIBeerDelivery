import math
from simpleai.search import SearchProblem, astar
from draw import *
import numpy as np

class MazeSolver(SearchProblem):
    # Initialize the class
    def __init__(self, board):
        self.board = board
        self.goal = (0, 0)

        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x].lower() == 'o':
                    self.initial = (x, y)
                elif self.board[y][x].lower() == 'x':
                    self.goal = (x, y)

        super(MazeSolver, self).__init__(initial_state=self.initial)
    def actions(self, state):
        actions = []
        for action in COSTS.keys():
            newx, newy = self.result(state, action)
            if self.board[newy][newx] != '#':
                actions.append(action)
        return actions

    def result(self, state, action):
        x,y = state
        if action.count('up'):
            y-=1
        if action.count('down'):
            y+=1
        if action.count('left'):
            x-=1
        if action.count('right'):
            x+=1
        new_state = (x,y)
        return new_state

    def is_goal(self, state):
        return state == self.goal

    def cost(self, state, action, state2):
        return COSTS[action]

    def heuristic(self, state):
        x,y = state
        gx, gy = self.goal
        return math.sqrt((x - gx) ** 2 + (y - gy) ** 2)

if __name__ == '__main__':
    MAP = """
##############################
#                        #   #
######    ########       ## ##
#  o #    #  #           #   #
#    ###     #####  ######   #
#      #   ###      #        #
#      #     #   #  #  #   ###
#     ## ##   #     #  #     #
#              #       #   x #
##############################"""



    # print(MAP)
    MAP = [list(x) for x in MAP.split("\n") if x]
    print(MAP)
    cost_regular = 1.0
    COSTS = {
        "up": cost_regular,
        "down": cost_regular,
        "left": cost_regular,
        "right": cost_regular
    }
    problem = MazeSolver(MAP)
    result = astar(problem, graph_search=True)

    path = [x[1] for x in result.path()]


    print(MAP, path)
