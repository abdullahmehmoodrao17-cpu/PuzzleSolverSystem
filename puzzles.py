# puzzles.py - More challenging puzzles

import random

class EightPuzzle:
    """8-Puzzle - 15-25 moves to solve"""
    
    def __init__(self):
        self.goal = [[1, 2, 3],
                     [4, 5, 6],
                     [7, 8, 0]]
    
    def get_puzzle(self):
        """Generate puzzle with 20-25 random moves (challenging)"""
        state = [row[:] for row in self.goal]
        
        # Make 20-25 random moves from goal (creates challenging puzzle)
        moves_count = random.randint(20, 30)
        for _ in range(moves_count):
            neighbors = self.get_neighbors(state)
            if neighbors:
                state = random.choice(neighbors)
        
        return state
    
    def get_blank_position(self, state):
        for i in range(3):
            for j in range(3):
                if state[i][j] == 0:
                    return i, j
        return 0, 0
    
    def get_neighbors(self, state):
        blank_i, blank_j = self.get_blank_position(state)
        neighbors = []
        
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        
        for di, dj in moves:
            new_i, new_j = blank_i + di, blank_j + dj
            if 0 <= new_i < 3 and 0 <= new_j < 3:
                new_state = [row[:] for row in state]
                new_state[blank_i][blank_j], new_state[new_i][new_j] = new_state[new_i][new_j], new_state[blank_i][blank_j]
                neighbors.append(new_state)
        
        return neighbors
    
    def is_goal(self, state):
        return (state[0][0] == 1 and state[0][1] == 2 and state[0][2] == 3 and
                state[1][0] == 4 and state[1][1] == 5 and state[1][2] == 6 and
                state[2][0] == 7 and state[2][1] == 8 and state[2][2] == 0)
    
    def manhattan_distance(self, state):
        distance = 0
        for i in range(3):
            for j in range(3):
                value = state[i][j]
                if value != 0:
                    goal_i = (value - 1) // 3
                    goal_j = (value - 1) % 3
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance


class Maze:
    """5x5 Maze - More complex, looks different from 8-puzzle"""
    
    def __init__(self):
        # 5x5 maze with clear walls (#) and paths (.)
        self.maze = [
            ['S', '.', '.', '#', '.'],
            ['.', '#', '.', '#', '.'],
            ['.', '#', '.', '.', '.'],
            ['.', '.', '#', '#', '.'],
            ['#', '.', '.', '.', 'G']
        ]
        self.start = (0, 0)
        self.goal = (4, 4)
        self.rows = 5
        self.cols = 5
    
    def get_neighbors(self, pos):
        i, j = pos
        neighbors = []
        
        # Up
        if i > 0 and self.maze[i-1][j] != '#':
            neighbors.append((i-1, j))
        # Down
        if i < 4 and self.maze[i+1][j] != '#':
            neighbors.append((i+1, j))
        # Left
        if j > 0 and self.maze[i][j-1] != '#':
            neighbors.append((i, j-1))
        # Right
        if j < 4 and self.maze[i][j+1] != '#':
            neighbors.append((i, j+1))
        
        return neighbors
    
    def is_goal(self, pos):
        return pos == self.goal
    
    def manhattan_distance(self, pos):
        return abs(pos[0] - self.goal[0]) + abs(pos[1] - self.goal[1])