# agent.py - With timeout support

import time
import threading
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.astar import astar

class PuzzleAgent:
    def __init__(self):
        self.algorithms = {
            'BFS': bfs,
            'DFS': dfs,
            'A*': astar
        }
        self.is_running = False
        self.result = None
    
    def analyze_problem(self, puzzle_type):
        if puzzle_type == '8-puzzle':
            return 'A*', "A* uses Manhattan distance heuristic (fastest for 8-puzzle)"
        elif puzzle_type == 'maze':
            return 'A*', "A* finds shortest path efficiently"
        else:
            return 'BFS', "BFS guarantees shortest path"
    
    def solve_async(self, problem, algorithm_name, puzzle_type, callback, progress_callback=None):
        def solve_task():
            self.is_running = True
            
            # Set timeout (5 seconds max)
            start_time = time.time()
            timeout = 10  # 10 seconds timeout
            
            try:
                if puzzle_type == '8-puzzle':
                    initial_state = problem.get_random_state()
                else:
                    initial_state = problem.start
                
                if algorithm_name is None:
                    algorithm_name, reason = self.analyze_problem(puzzle_type)
                else:
                    reason = f"User selected {algorithm_name}"
                
                if progress_callback:
                    progress_callback(f"Running {algorithm_name}...", 30)
                
                algorithm = self.algorithms.get(algorithm_name)
                
                if algorithm:
                    # Run with timeout check
                    solution = None
                    nodes_explored = 0
                    time_taken = 0
                    
                    # Use a flag to check timeout
                    def run_algorithm():
                        nonlocal solution, nodes_explored, time_taken
                        solution, nodes_explored, time_taken = algorithm(problem, initial_state)
                    
                    algo_thread = threading.Thread(target=run_algorithm)
                    algo_thread.daemon = True
                    algo_thread.start()
                    algo_thread.join(timeout=timeout)
                    
                    if algo_thread.is_alive():
                        # Timeout occurred
                        self.result = {
                            'success': False,
                            'solution': None,
                            'nodes_explored': 0,
                            'time': timeout,
                            'path_length': 0,
                            'algorithm_used': algorithm_name,
                            'decision_reason': f"{algorithm_name} took too long (timeout after {timeout}s)",
                            'initial_state': initial_state
                        }
                        self.add_log_callback(progress_callback, "⚠️ Timeout! Try a simpler puzzle or different algorithm", 100)
                    else:
                        path_length = len(solution) - 1 if solution else 0
                        self.result = {
                            'success': solution is not None,
                            'solution': solution,
                            'nodes_explored': nodes_explored,
                            'time': round(time_taken, 4),
                            'path_length': path_length,
                            'algorithm_used': algorithm_name,
                            'decision_reason': reason,
                            'initial_state': initial_state
                        }
                else:
                    self.result = {
                        'success': False,
                        'solution': None,
                        'nodes_explored': 0,
                        'time': 0,
                        'path_length': 0,
                        'algorithm_used': algorithm_name,
                        'decision_reason': f"Algorithm {algorithm_name} not found"
                    }
                
                if progress_callback:
                    progress_callback("Complete!", 100)
                
            except Exception as e:
                self.result = {
                    'success': False,
                    'solution': None,
                    'nodes_explored': 0,
                    'time': 0,
                    'path_length': 0,
                    'algorithm_used': algorithm_name if algorithm_name else "Unknown",
                    'decision_reason': f"Error: {str(e)[:50]}"
                }
            
            self.is_running = False
            callback(self.result)
        
        thread = threading.Thread(target=solve_task)
        thread.daemon = True
        thread.start()
    
    def add_log_callback(self, callback, message, value):
        """Helper to call progress callback"""
        if callback:
            callback(message, value)
    
    def solve(self, problem, algorithm_name=None, puzzle_type=None):
        """Synchronous solve (for comparison)"""
        try:
            if puzzle_type == '8-puzzle':
                initial_state = problem.get_random_state()
            else:
                initial_state = problem.start
            
            if algorithm_name is None:
                algorithm_name, reason = self.analyze_problem(puzzle_type)
            else:
                reason = f"User selected {algorithm_name}"
            
            algorithm = self.algorithms.get(algorithm_name)
            
            if algorithm:
                solution, nodes_explored, time_taken = algorithm(problem, initial_state)
                path_length = len(solution) - 1 if solution else 0
                
                return {
                    'success': solution is not None,
                    'solution': solution,
                    'nodes_explored': nodes_explored,
                    'time': round(time_taken, 4),
                    'path_length': path_length,
                    'algorithm_used': algorithm_name,
                    'decision_reason': reason,
                    'initial_state': initial_state
                }
            else:
                return {
                    'success': False,
                    'solution': None,
                    'nodes_explored': 0,
                    'time': 0,
                    'path_length': 0,
                    'algorithm_used': algorithm_name,
                    'decision_reason': f"Algorithm not found"
                }
        except Exception as e:
            return {
                'success': False,
                'solution': None,
                'nodes_explored': 0,
                'time': 0,
                'path_length': 0,
                'algorithm_used': algorithm_name if algorithm_name else "Unknown",
                'decision_reason': f"Error: {str(e)[:50]}"
            }
    
    def compare_algorithms(self, problem, puzzle_type):
        """Compare algorithms with limits"""
        results = {}
        
        for algo_name in ['BFS', 'DFS', 'A*']:
            result = self.solve(problem, algo_name, puzzle_type)
            results[algo_name] = {
                'nodes_explored': result['nodes_explored'],
                'time': result['time'],
                'path_length': result['path_length'],
                'success': result['success']
            }
        
        return results
    
    def is_busy(self):
        return self.is_running