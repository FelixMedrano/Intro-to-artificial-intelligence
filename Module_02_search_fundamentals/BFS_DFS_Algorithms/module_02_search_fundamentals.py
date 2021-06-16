# -*- coding: utf-8 -*-
"""Module_02_search_fundamentals

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/155upFmxS7OdgJbBiduJr1d7q6KhCNbUy
"""

import copy
import math
from collections import deque

# github repository by Rishal Hurbans
#https://github.com/rishal-hurbans/Grokking-Artificial-Intelligence-Algorithms/tree/master/ch02-search_fundamentals/uninformed_search
print('Hello this is the uninformed search algorithm with BFS and DFS, this code is not mine')
print('the only thing that was changed was implementing the algorithms into a single file, making it repeatable and')
print('allowing the user to chose which algorithm they would like to run')

#To run this source code in google colab use the following link:
# https://colab.research.google.com/drive/155upFmxS7OdgJbBiduJr1d7q6KhCNbUy?usp=sharing

again=True
while again== True:
  Algorithm_choice=input('Which algorithm would you like to run? BFS (Enter B) or DFS(Enter D)')
  Algorithm_choice= Algorithm_choice.capitalize()
  # This class is used to store the idea of a point in the maze and linking it to other points to create a path.
  class Point:
      def __init__(self, x=0, y=0):
          self.x = x
          self.y = y
          self.parent = None
          self.cost = math.inf

      def set_parent(self, p):
          self.parent = p

      def set_cost(self, c):
          self.cost = c

      def print(self):
          print(self.x, ',', self.y)


  # These constants are used to reference points on the maze that are in the respective direction of a point in question.
  NORTH = Point(0, 1)
  SOUTH = Point(0, -1)
  EAST = Point(1, 0)
  WEST = Point(-1, 0)


  # The MazePuzzle class contains the mechanics of the game
  class MazePuzzle:

      WALL = '#'
      EMPTY = '_'
      GOAL = '*'

      # Initialize the maze with a map containing; * at the goal, 0 as an empty unexplored point, and # as a point with
      # a wall.
      def __init__(self, maze_size_x=5, maze_size_y=5):
          self.maze_size_x = maze_size_x
          self.maze_size_y = maze_size_y
          self.maze = ['*0000',
                      '0###0',
                      '0#0#0',
                      '0#000',
                      '00000']

      def get_current_point_value(self, current_point):
          return self.maze[current_point.x][current_point.y]

      # Return all valid neighbors around a specific point, excluding points outside of the maze and walls.
      def get_neighbors(self, current_point):
          neighbors = []
          # potential_neighbors = [[0, 1], [0, -1], [1, 0], [-1, 0]]
          potential_neighbors = [[NORTH.x, NORTH.y], [SOUTH.x, SOUTH.y], [EAST.x, EAST.y], [WEST.x, WEST.y]]
          for neighbor in potential_neighbors:
              target_point = Point(current_point.x + neighbor[0], current_point.y + neighbor[1])
              if 0 <= target_point.x < self.maze_size_x and 0 <= target_point.y < self.maze_size_y:
                  if self.get_current_point_value(target_point) != '#':
                      neighbors.append(target_point)
          return neighbors

      # A function to visually show a set of points visited in the maze
      def overlay_points_on_map(self, points):
          overlay_map = copy.deepcopy(self.maze)
          for point in points:
              new_row = overlay_map[point.x][:point.y] + '@' + overlay_map[point.x][point.y + 1:]
              overlay_map[point.x] = new_row

          result = ''
          for x in range(0, self.maze_size_x):
              for y in range(0, self.maze_size_y):
                  result += overlay_map[x][y]
              result += '\n'
          print(result)

          return overlay_map

      def print_maze(self):
          result = ''
          for x in range(0, self.maze_size_x):
              for y in range(0, self.maze_size_y):
                  result += self.maze[x][y]
              result += '\n'
          print(result)


  # Utility to get a path as a list of points by traversing the parents of a node until the root is reached.
  def get_path(point):
      path = []
      current_point = point
      while current_point.parent is not None:
          path.append(current_point)
          current_point = current_point.parent
      return path


  # Utility to find the length of a specific path given a point.
  def get_path_length(point):
      path = []
      current_point = point
      total_length = 0
      while current_point.parent is not None:
          path.append(current_point)
          total_length += 1
          current_point = current_point.parent
      return total_length


  # Utility to calculate the cost of a path if an additional cost of movement exists.
  def get_path_cost(point):
      path = []
      current_point = point
      total_cost = 0
      while current_point.parent is not None:
          path.append(current_point)
          total_cost += get_cost(get_direction(current_point.parent, current_point))
          current_point = current_point.parent
      return total_cost


  # Utility to determine the cost of a specific move.
  def get_move_cost(origin, target):
      return get_cost(get_direction(origin, target))


  # Utility to determine the direction of movement given an origin and target point.
  def get_direction(origin, target):
      if target.x == origin.x and target.y == origin.y - 1:
          return 'N'
      elif target.x == origin.x and target.y == origin.y + 1:
          return 'S'
      elif target.x == origin.x + 1 and target.y == origin.y:
          return 'E'
      elif target.x == origin.x - 1 and target.y == origin.y:
          return 'W'


  # Utility to determine the cost of a move given a direction. In this case, North and South is 5, and East and West is 1.
  STANDARD_COST = 1
  GRAVITY_COST = 5


  def get_cost(direction):
      if direction == 'N' or direction == 'S':
          return GRAVITY_COST
      return STANDARD_COST



  if Algorithm_choice== 'B':
    # Function to find a route using the Breadth-first Search algorithm.
    # Breadth-first search is an algorithm used to traverse or generate a tree. This algorithm starts at a specific node
    # called the root and explores every node at that depth before exploring the next depth of nodes. It essentially visits
    # all children of nodes at a specific depth before visiting the next depth of child until it finds a goal leaf node.

    # The Breadth first search algorithm is best implemented using a first-in-first-out queue where the current depth of
    # nodes are processed and their children are queued to be processed later. This order of processing is exactly what
    # we require when implementing this algorithm.
    def run_bfs(maze_puzzle, current_point, visited_points):
        queue = deque()
        # Append the current node to the queue
        queue.append(current_point)
        visited_points.append(current_point)
        # Keep searching while there are nodes in the queue
        while queue:
            # Set the next node in the queue as the current node
            current_point = queue.popleft()
            # Get the neighbors of the current node
            neighbors = maze_puzzle.get_neighbors(current_point)
            # Iterate through the neighbors of the current node
            for neighbor in neighbors:
                # Add the neighbor to the queue if it hasn't been visited
                if not is_in_visited_points(neighbor, visited_points):
                    neighbor.set_parent(current_point)
                    queue.append(neighbor)
                    visited_points.append(neighbor)
                    # Return the path to the current neighbor if it is the goal
                    if maze_puzzle.get_current_point_value(neighbor) == '*':
                        return neighbor
        # In the case that no path to the goal was found
        return 'No path to the goal found.'


    # Function to determine if the point has already been visited
    def is_in_visited_points(current_point, visited_points):
        for visited_point in visited_points:
            if current_point.x == visited_point.x and current_point.y == visited_point.y:
                return True
        return False


    print('---Breadth-first Search---')

    # Initialize a MazePuzzle
    maze_game_main = MazePuzzle()

    # Run the breadth first search algorithm with the initialized maze
    starting_point = Point(2, 2)
    outcome = run_bfs(maze_game_main, starting_point, [])

    # Get the path found by the breadth first search algorithm
    bfs_path = get_path(outcome)

    # Print the results of the path found
    print('Path Length: ', len(bfs_path))
    maze_game_main.overlay_points_on_map(bfs_path)
    print('Path Cost: ', get_path_cost(outcome))
    for point in bfs_path:
        print('Point: ', point.x, ',', point.y)
    print('Would you like to go again?')
    check1=input('Press any key to continue or press 0 to exit')
    if check1=='0':
      again=False




  if Algorithm_choice=='D':
    # Function to find a route using the Depth-first Search algorithm.

    # Depth-first search is an algorithm used to traverse a tree or generate nodes and paths in a tree. This algorithm
    # starts at a specific node and explores paths of connected nodes of the first child and does this recursively until
    # it reaches the furthest leaf node before backtracking and exploring other paths to leaf nodes via other child nodes
    # that have been visited.

    # Although the Depth-first search algorithm van be implemented with a recursive function. This implementation is
    # achieved using a stack to better represent the order of operations as to which nodes get visited and processed.
    # It is important to keep track of the visited points so that the same nodes do not get visited unnecessarily and
    # create cyclic loops.
    def run_dfs(maze_game, current_point):
        # Append the current node to the stack
        visited_points = []
        stack = [current_point]
        # Keep searching while there are nodes in the stack
        while stack:
            # Set the next node in the stack as the current node
            next_point = stack.pop()
            # If the current node hasn't already been exploited, search it
            if not is_in_visited_points(next_point, visited_points):
                visited_points.append(next_point)
                # Return the path to the current neighbor if it is the goal
                if maze_game.get_current_point_value(next_point) == '*':
                    return next_point
                else:
                    # Add the current node's neighbors to the stack
                    neighbors = maze_game.get_neighbors(next_point)
                    for neighbor in neighbors:
                        neighbor.set_parent(next_point)
                        stack.append(neighbor)
        return 'No path to the goal found.'


    # Function to determine if the point has already been visited
    def is_in_visited_points(current_point, visited_points):
        for visited_point in visited_points:
            if current_point.x == visited_point.x and current_point.y == visited_point.y:
                return True
        return False


    print('---Depth-first Search---')

    # Initialize a MazePuzzle
    maze_game_main = MazePuzzle()

    # Run the depth first search algorithm with the initialized maze
    starting_point = Point(2, 2)
    outcome = run_dfs(maze_game_main, starting_point)

    # Get the path found by the depth first search algorithm
    dfs_path = get_path(outcome)

    # Print the results of the path found
    print('Path Length: ', len(dfs_path))
    maze_game_main.overlay_points_on_map(dfs_path)
    print('Path Cost: ', get_path_cost(outcome))
    for point in dfs_path:
        print('Point: ', point.x, ',', point.y)
    print('Would you like to go again?')
    check2=input('Press any key to continue or press 0 to exit')
    if check2=='0':
      again=False