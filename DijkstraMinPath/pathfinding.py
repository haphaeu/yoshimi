# Sample code from http://www.redblobgames.com/pathfinding/
# Copyright 2014 Red Blob Games <redblobgames@gmail.com>
#
# Feel free to use this code in your own projects, including commercial projects
# License: Apache v2.0 <http://www.apache.org/licenses/LICENSE-2.0.html>
#
# ##############################################################################
#
# Adapted to read images by Rafael Rossi, August 2016
# Created class GridFromImage
#
#

# ###############################################
# utility functions for dealing with square grids
# ###############################################


def from_id_width(id, width):
    return (id % width, id // width)


def draw_tile(graph, id, style, width):
    r = "."
    if 'number' in style and id in style['number']: r = "%d" % style['number'][id]
    if 'point_to' in style and style['point_to'].get(id, None) is not None:
        (x1, y1) = id
        (x2, y2) = style['point_to'][id]
        if x2 == x1 + 1: r = "\u2192"
        if x2 == x1 - 1: r = "\u2190"
        if y2 == y1 + 1: r = "\u2193"
        if y2 == y1 - 1: r = "\u2191"
    if 'start' in style and id == style['start']: r = "A"
    if 'goal' in style and id == style['goal']: r = "Z"
    if 'path' in style and id in style['path']: r = "@"
    if id in graph.walls: r = "#"  # * width
    return r


def draw_grid(graph, width=2, **style):
    for y in range(graph.height):
        for x in range(graph.width):
            print("%%-%ds" % width % draw_tile(graph, (x, y), style, width), end="")
        print()


class SquareGrid:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.walls = []

    def in_bounds(self, id):
        (x, y) = id
        return 0 <= x < self.width and 0 <= y < self.height

    def passable(self, id):
        return id not in self.walls

    def neighbors(self, id):
        (x, y) = id
        results = [(x+1, y), (x, y-1), (x-1, y), (x, y+1)]
        if (x + y) % 2 == 0: results.reverse()  # aesthetics
        results = filter(self.in_bounds, results)
        results = filter(self.passable, results)
        return results


class GridWithWeights(SquareGrid):
    def __init__(self, width, height):
        super().__init__(width, height)
        self.weights = {}

    def cost(self, from_node, to_node):
        return self.weights.get(to_node, 1)


diagram4 = GridWithWeights(10, 10)
diagram4.walls = [(1, 7), (1, 8), (2, 7), (2, 8), (3, 7), (3, 8)]
diagram4.weights = {loc: 5 for loc in [(3, 4), (3, 5), (4, 1), (4, 2),
                                       (4, 3), (4, 4), (4, 5), (4, 6),
                                       (4, 7), (4, 8), (5, 1), (5, 2),
                                       (5, 3), (5, 4), (5, 5), (5, 6),
                                       (5, 7), (5, 8), (6, 2), (6, 3),
                                       (6, 4), (6, 5), (6, 6), (6, 7),
                                       (7, 3), (7, 4), (7, 5)]}

from matplotlib import pylab
import numpy as np


class GridFromImage(GridWithWeights):
    def __init__(self, image_filename):
        self.figname = image_filename
        self.fig = pylab.imread(image_filename)
        h, w = len(self.fig), len(self.fig[0])
        super().__init__(w, h)
        self._find_walls()

    def _find_walls(self):
        """Converts the image into a matrix. Anything darker than medium grey will be a "wall"
        The rest is "walkable" area"""
        for y in range(self.height):
            for x in range(self.width):
                if self.fig[y][x][0] < 200:
                    self.walls.append((x, y))

    def ascii_print(self, stretch=1):
        for y in range(self.height):
            for x in range(self.width):
                tile = '#' if (x, y) in self.walls else '.'
                print(tile, end=' '*stretch)
            print('')

    def show_path(self, start, goal, came_from, save=False):
        fig2 = self.fig.copy()
        current = goal
        while not current == start:
            x, y = current
            fig2[y][x] = np.array([255, 0, 0], dtype=np.uint8)
            current = came_from[current]
        pylab.imshow(fig2)
        if save:
            pylab.imsave(arr=fig2, fname=self.figname[:-4]+'_minpath.png')


import heapq


class PriorityQueue:
    def __init__(self):
        self.elements = []

    def empty(self):
        return len(self.elements) == 0

    def put(self, item, priority):
        heapq.heappush(self.elements, (priority, item))

    def get(self):
        return heapq.heappop(self.elements)[1]


def dijkstra_search(graph, start, goal, verbose=False):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        if verbose: print(current)
        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far


def reconstruct_path(came_from, start, goal):
    current = goal
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    path.append(start)  # optional
    path.reverse()  # optional
    return path


def heuristic(a, b):
    (x1, y1) = a
    (x2, y2) = b
    return abs(x1 - x2) + abs(y1 - y2)


def a_star_search(graph, start, goal, verbose=False):
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from = {}
    cost_so_far = {}
    came_from[start] = None
    cost_so_far[start] = 0

    while not frontier.empty():
        current = frontier.get()
        if verbose: print(current, end='')
        if current == goal:
            break

        for next in graph.neighbors(current):
            new_cost = cost_so_far[current] + graph.cost(current, next)
            if next not in cost_so_far or new_cost < cost_so_far[next]:
                cost_so_far[next] = new_cost
                priority = new_cost + heuristic(goal, next)
                frontier.put(next, priority)
                came_from[next] = current

    return came_from, cost_so_far


if __name__ == '__main__':

    #    # A*
    #
    #    came_from, cost_so_far = a_star_search(diagram4, (1, 4), (7, 8))
    #    draw_grid(diagram4, width=3, point_to=came_from, start=(1, 4), goal=(7, 8))
    #    print()
    #    draw_grid(diagram4, width=3, number=cost_so_far, start=(1, 4), goal=(7, 8))
    #    print()
    #
    #    # Dijkstra
    #
    #    came_from, cost_so_far = dijkstra_search(diagram4, (1, 4), (7, 8))
    #    draw_grid(diagram4, width=3, point_to=came_from, start=(1, 4), goal=(7, 8))
    #    print()
    #    draw_grid(diagram4, width=3, number=cost_so_far, start=(1, 4), goal=(7, 8))
    #    print()
    #    draw_grid(diagram4, width=3, path=reconstruct_path(came_from, start=(1, 4), goal=(7, 8)))
    #    print()

    # from image
    grid = GridFromImage('plan_low.bmp')
    start, goal = (206, 117), (116, 193)
    came_from1, cost_so_far1 = a_star_search(grid, start, goal, verbose=False)
    # draw_grid(grid, width=3, point_to=came_from, start=start, goal=goal)

    # came_from2, cost_so_far2 = dijkstra_search(grid, start, goal, verbose=True)

    grid.show_path(start, goal, came_from1, save=True)
    # grid.show_path(start, goal, came_from2)
