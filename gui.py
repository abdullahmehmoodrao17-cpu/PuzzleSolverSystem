# gui.py - Professional GUI

import tkinter as tk
from tkinter import ttk, messagebox
import time
from puzzles import EightPuzzle, Maze
from algorithms.bfs import bfs
from algorithms.dfs import dfs
from algorithms.astar import astar

class PuzzleSolverGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🧩 Intelligent Puzzle Solver System")
        self.root.geometry("1200x700")
        self.root.configure(bg='#1a1a2e')
        
        # Initialize
        self.eight_puzzle = EightPuzzle()
        self.maze = Maze()
        self.current_puzzle_type = "8-Puzzle"
        self.current_state = None
        self.current_solution = None
        self.animation_step = 0
        self.animation_id = None
        
        self.setup_gui()
        self.new_puzzle()
    
    def setup_gui(self):
        # Header
        header = tk.Frame(self.root, bg='#16213e', height=80)
        header.pack(fill='x')
        header.pack_propagate(False)
        
        tk.Label(header, text="🧩 INTELLIGENT PUZZLE SOLVER SYSTEM",
                font=('Segoe UI', 20, 'bold'), bg='#16213e', fg='#e94560').pack(pady=(15, 5))
        
        tk.Label(header, text="Autonomous Agent | BFS | DFS | A* Search Algorithm",
                font=('Segoe UI', 10), bg='#16213e', fg='#a0a0a0').pack()
        
        # Main container
        main = tk.Frame(self.root, bg='#1a1a2e')
        main.pack(fill='both', expand=True, padx=20, pady=20)
        
        # Left Panel - Controls
        left = tk.Frame(main, bg='#0f3460', width=280)
        left.pack(side='left', fill='y', padx=(0, 10))
        left.pack_propagate(False)
        
        # Center Panel - Display
        center = tk.Frame(main, bg='#16213e')
        center.pack(side='left', fill='both', expand=True, padx=(0, 10))
        
        # Right Panel - Results
        right = tk.Frame(main, bg='#0f3460', width=320)
        right.pack(side='right', fill='y')
        right.pack_propagate(False)
        
        self.setup_left_panel(left)
        self.setup_center_panel(center)
        self.setup_right_panel(right)
    
    def setup_left_panel(self, parent):
        tk.Label(parent, text="🎮 CONTROL PANEL", font=('Segoe UI', 14, 'bold'),
                bg='#0f3460', fg='#e94560').pack(pady=(20, 10))
        
        tk.Frame(parent, bg='#e94560', height=2).pack(fill='x', padx=20, pady=5)
        
        # Puzzle Selection
        card1 = tk.Frame(parent, bg='#16213e')
        card1.pack(fill='x', padx=20, pady=10)
        
        tk.Label(card1, text="📌 PUZZLE TYPE", font=('Segoe UI', 10, 'bold'),
                bg='#16213e', fg='#e94560').pack(pady=(10, 5))
        
        self.puzzle_var = tk.StringVar(value="8-Puzzle")
        puzzle_frame = tk.Frame(card1, bg='#16213e')
        puzzle_frame.pack(pady=5)
        
        tk.Radiobutton(puzzle_frame, text="8-Puzzle (3x3)", variable=self.puzzle_var,
                      value="8-Puzzle", bg='#16213e', fg='white',
                      selectcolor='#0f3460', command=self.new_puzzle).pack(side='left', padx=10)
        tk.Radiobutton(puzzle_frame, text="Maze (5x5)", variable=self.puzzle_var,
                      value="Maze", bg='#16213e', fg='white',
                      selectcolor='#0f3460', command=self.new_puzzle).pack(side='left', padx=10)
        
        # Algorithm Selection
        card2 = tk.Frame(parent, bg='#16213e')
        card2.pack(fill='x', padx=20, pady=10)
        
        tk.Label(card2, text="⚙️ ALGORITHM", font=('Segoe UI', 10, 'bold'),
                bg='#16213e', fg='#e94560').pack(pady=(10, 5))
        
        self.algo_var = tk.StringVar(value="A*")
        algo_frame = tk.Frame(card2, bg='#16213e')
        algo_frame.pack(pady=5)
        
        algorithms = [("A*", "A*"), ("BFS", "BFS"), ("DFS", "DFS"), ("🤖 Auto", "Auto")]
        for text, value in algorithms:
            tk.Radiobutton(algo_frame, text=text, variable=self.algo_var,
                          value=value, bg='#16213e', fg='white' if value != "Auto" else '#e94560',
                          selectcolor='#0f3460').pack(side='left', padx=8)
        
        # Action Buttons
        tk.Button(parent, text="🚀 SOLVE PUZZLE", command=self.solve_puzzle,
                 bg='#e94560', fg='white', font=('Segoe UI', 12, 'bold'),
                 padx=30, pady=10, cursor='hand2', relief='flat').pack(pady=15)
        
        tk.Button(parent, text="🔄 NEW PUZZLE", command=self.new_puzzle,
                 bg='#533483', fg='white', font=('Segoe UI', 10, 'bold'),
                 padx=20, pady=8, cursor='hand2', relief='flat').pack(pady=5)
        
        tk.Button(parent, text="📊 COMPARE ALL", command=self.compare_algorithms,
                 bg='#0f3460', fg='#e94560', font=('Segoe UI', 10, 'bold'),
                 padx=20, pady=8, cursor='hand2', relief='flat', bd=1).pack(pady=5)
        
        # Animation Controls
        card3 = tk.Frame(parent, bg='#16213e')
        card3.pack(fill='x', padx=20, pady=10)
        
        tk.Label(card3, text="🎬 SOLUTION ANIMATION", font=('Segoe UI', 10, 'bold'),
                bg='#16213e', fg='#e94560').pack(pady=(10, 5))
        
        btn_frame = tk.Frame(card3, bg='#16213e')
        btn_frame.pack(pady=5)
        
        self.play_btn = tk.Button(btn_frame, text="▶ PLAY", command=self.play_animation,
                                 bg='#27ae60', fg='white', font=('Segoe UI', 9, 'bold'),
                                 padx=15, pady=5, cursor='hand2', state='disabled')
        self.play_btn.pack(side='left', padx=5)
        
        self.reset_btn = tk.Button(btn_frame, text="🔄 RESET", command=self.reset_animation,
                                  bg='#e94560', fg='white', font=('Segoe UI', 9, 'bold'),
                                  padx=15, pady=5, cursor='hand2', state='disabled')
        self.reset_btn.pack(side='left', padx=5)
        
        # Speed Control
        speed_frame = tk.Frame(card3, bg='#16213e')
        speed_frame.pack(pady=10)
        tk.Label(speed_frame, text="Speed:", bg='#16213e', fg='white').pack(side='left')
        self.speed_var = tk.DoubleVar(value=0.5)
        speed_scale = tk.Scale(speed_frame, from_=0.2, to=1.5, orient='horizontal',
                               variable=self.speed_var, bg='#16213e', fg='white',
                               length=120, highlightthickness=0)
        speed_scale.pack(side='left', padx=5)
    
    def setup_center_panel(self, parent):
        tk.Label(parent, text="🎨 PUZZLE VISUALIZATION", font=('Segoe UI', 14, 'bold'),
                bg='#16213e', fg='#e94560').pack(pady=(20, 10))
        
        tk.Frame(parent, bg='#e94560', height=2).pack(fill='x', padx=20, pady=5)
        
        self.canvas = tk.Canvas(parent, bg='#0f3460', width=450, height=450,
                                highlightthickness=2, highlightbackground='#e94560')
        self.canvas.pack(pady=20)
        
        # Status
        self.status_frame = tk.Frame(parent, bg='#16213e')
        self.status_frame.pack(fill='x', padx=20, pady=10)
        
        self.status_label = tk.Label(self.status_frame, text="✅ Ready",
                                     font=('Segoe UI', 11), bg='#16213e', fg='#27ae60')
        self.status_label.pack()
        
        # Progress
        self.progress = ttk.Progressbar(parent, mode='determinate', length=350)
        self.progress.pack(pady=5)
        
        self.step_label = tk.Label(parent, text="", font=('Segoe UI', 9),
                                   bg='#16213e', fg='#a0a0a0')
        self.step_label.pack()
    
    def setup_right_panel(self, parent):
        tk.Label(parent, text="📊 PERFORMANCE METRICS", font=('Segoe UI', 14, 'bold'),
                bg='#0f3460', fg='#e94560').pack(pady=(20, 10))
        
        tk.Frame(parent, bg='#e94560', height=2).pack(fill='x', padx=20, pady=5)
        
        # Metrics
        metrics_frame = tk.Frame(parent, bg='#0f3460')
        metrics_frame.pack(fill='x', padx=20, pady=10)
        
        metrics = [
            ("🤖 Algorithm", "algo_val"),
            ("📊 Status", "status_val"),
            ("🔍 Nodes Explored", "nodes_val"),
            ("⏱️ Time Taken", "time_val"),
            ("📏 Path Length", "path_val"),
        ]
        
        self.metrics = {}
        for label, key in metrics:
            card = tk.Frame(metrics_frame, bg='#16213e')
            card.pack(fill='x', pady=4)
            
            tk.Label(card, text=label, font=('Segoe UI', 9, 'bold'),
                    bg='#16213e', fg='#a0a0a0', width=14, anchor='w').pack(side='left', padx=10, pady=8)
            
            self.metrics[key] = tk.Label(card, text="—", font=('Segoe UI', 9),
                                         bg='#16213e', fg='#e94560', anchor='w')
            self.metrics[key].pack(side='left', padx=5, pady=8, fill='x', expand=True)
        
        # Log
        tk.Label(parent, text="📋 EXECUTION LOG", font=('Segoe UI', 11, 'bold'),
                bg='#0f3460', fg='#e94560').pack(anchor='w', padx=20, pady=(15, 5))
        
        log_frame = tk.Frame(parent, bg='#16213e')
        log_frame.pack(fill='both', expand=True, padx=20, pady=5)
        
        self.log_text = tk.Text(log_frame, height=12, width=35,
                                bg='#0f3460', fg='#a0a0a0',
                                font=('Consolas', 9), wrap='word', relief='flat')
        self.log_text.pack(fill='both', expand=True, padx=5, pady=5)
        
        scrollbar = tk.Scrollbar(self.log_text)
        scrollbar.pack(side='right', fill='y')
        self.log_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.log_text.yview)
        
        self.add_log("🚀 System Initialized")
        self.add_log("🤖 Autonomous Agent Ready")
    
    def add_log(self, message):
        from datetime import datetime
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)
        self.root.update()
    
    def update_metrics(self, algorithm, status, nodes, exec_time, path_length):
        self.metrics['algo_val'].config(text=algorithm)
        self.metrics['status_val'].config(text=status, fg='#27ae60' if "✅" in status else '#e94560')
        self.metrics['nodes_val'].config(text=str(nodes))
        self.metrics['time_val'].config(text=f"{exec_time:.4f} sec")
        self.metrics['path_val'].config(text=str(path_length))
    
    def new_puzzle(self):
        """Generate new puzzle"""
        self.current_puzzle_type = self.puzzle_var.get()
        
        if self.current_puzzle_type == "8-Puzzle":
            self.current_state = self.eight_puzzle.get_puzzle()
            self.draw_8puzzle()
            self.add_log(f"🔄 New 8-Puzzle generated (20-30 moves to solve)")
        else:
            self.draw_maze()
            self.add_log(f"🔄 New 5x5 Maze generated")
        
        self.current_solution = None
        self.play_btn.config(state='disabled')
        self.reset_btn.config(state='disabled')
        self.progress['value'] = 0
        self.step_label.config(text="")
        
        for key in self.metrics:
            self.metrics[key].config(text="—")
        self.status_label.config(text="✅ Ready", fg='#27ae60')
    
    def draw_8puzzle(self):
        self.canvas.delete("all")
        size = 400
        cell = size // 3
        offset = 25
        
        colors = ['#e94560', '#533483', '#0f3460', '#27ae60', '#f39c12', '#3498db', '#1abc9c', '#9b59b6']
        
        for i in range(3):
            for j in range(3):
                val = self.current_state[i][j]
                x1 = offset + j * cell
                y1 = offset + i * cell
                x2 = x1 + cell - 3
                y2 = y1 + cell - 3
                
                if val == 0:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='#16213e', outline='#e94560', width=2)
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill=colors[(val-1)%8], outline='#e94560', width=2)
                    self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text=str(val),
                                           font=('Segoe UI', 28, 'bold'), fill='white')
    
    def draw_maze(self):
        self.canvas.delete("all")
        size = 400
        cell = size // 5
        offset = 25
        
        for i in range(5):
            for j in range(5):
                x1 = offset + j * cell
                y1 = offset + i * cell
                x2 = x1 + cell - 2
                y2 = y1 + cell - 2
                
                val = self.maze.maze[i][j]
                if val == '#':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='#16213e', outline='#e94560', width=1)
                elif val == 'S':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='#27ae60', outline='#e94560', width=2)
                    self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text="START",
                                           font=('Segoe UI', 10, 'bold'), fill='white')
                elif val == 'G':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='#e94560', outline='#e94560', width=2)
                    self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text="GOAL",
                                           font=('Segoe UI', 10, 'bold'), fill='white')
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='#0f3460', outline='#e94560', width=1)
    
    def solve_puzzle(self):
        """Solve the puzzle"""
        algo_choice = self.algo_var.get()
        
        if algo_choice == "A*":
            algorithm = astar
            algo_name = "A*"
        elif algo_choice == "BFS":
            algorithm = bfs
            algo_name = "BFS"
        elif algo_choice == "DFS":
            algorithm = dfs
            algo_name = "DFS"
        else:  # Auto
            algorithm = astar
            algo_name = "A* (Auto Selected)"
        
        if self.current_puzzle_type == "8-Puzzle":
            problem = self.eight_puzzle
            initial = self.current_state
        else:
            problem = self.maze
            initial = problem.start
        
        self.status_label.config(text=f"🤖 Solving with {algo_name}...", fg='#f39c12')
        self.add_log(f"🎯 Starting {algo_name} algorithm...")
        self.root.update()
        
        start_time = time.time()
        solution, nodes, exec_time = algorithm(problem, initial)
        total_time = time.time() - start_time
        
        if solution:
            path_length = len(solution) - 1
            self.current_solution = solution
            self.update_metrics(algo_name, "✅ SOLVED", nodes, total_time, path_length)
            self.status_label.config(text="✅ Solution Found!", fg='#27ae60')
            self.add_log(f"✅ Solution found in {exec_time:.3f} seconds!")
            self.add_log(f"📊 Explored {nodes} nodes, Path length: {path_length} moves")
            self.play_btn.config(state='normal')
            self.reset_btn.config(state='normal')
            self.progress['maximum'] = len(solution) - 1
        else:
            self.update_metrics(algo_name, "❌ FAILED", nodes, total_time, 0)
            self.status_label.config(text="❌ No solution found!", fg='#e94560')
            self.add_log(f"❌ No solution found after {nodes} nodes")
    
    def play_animation(self):
        """Animate solution"""
        if not self.current_solution:
            return
        
        self.animation_step = 0
        self.animate_next()
    
    def animate_next(self):
        if self.animation_step < len(self.current_solution):
            state = self.current_solution[self.animation_step]
            if self.current_puzzle_type == "8-Puzzle":
                self.current_state = state
                self.draw_8puzzle()
            else:
                self.draw_maze_with_path(state)
            
            self.step_label.config(text=f"Step {self.animation_step}/{len(self.current_solution)-1}")
            self.progress['value'] = self.animation_step
            self.animation_step += 1
            self.root.after(int(self.speed_var.get() * 300), self.animate_next)
        else:
            self.status_label.config(text="✅ Animation Complete!", fg='#27ae60')
    
    def draw_maze_with_path(self, position):
        """Draw maze with current position"""
        self.canvas.delete("all")
        size = 400
        cell = size // 5
        offset = 25
        
        for i in range(5):
            for j in range(5):
                x1 = offset + j * cell
                y1 = offset + i * cell
                x2 = x1 + cell - 2
                y2 = y1 + cell - 2
                
                val = self.maze.maze[i][j]
                if (i, j) == position:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='#f39c12', outline='#e94560', width=3)
                    self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text="🤖",
                                           font=('Segoe UI', 14, 'bold'), fill='white')
                elif val == '#':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='#16213e', outline='#e94560', width=1)
                elif val == 'S':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='#27ae60', outline='#e94560', width=2)
                    self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text="S",
                                           font=('Segoe UI', 12, 'bold'), fill='white')
                elif val == 'G':
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='#e94560', outline='#e94560', width=2)
                    self.canvas.create_text((x1+x2)//2, (y1+y2)//2, text="G",
                                           font=('Segoe UI', 12, 'bold'), fill='white')
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill='#0f3460', outline='#e94560', width=1)
    
    def reset_animation(self):
        """Reset animation"""
        self.animation_step = 0
        if self.current_puzzle_type == "8-Puzzle" and self.current_solution:
            self.current_state = self.current_solution[0]
            self.draw_8puzzle()
        elif self.current_solution:
            self.draw_maze()
        self.step_label.config(text="")
        self.progress['value'] = 0
        self.status_label.config(text="✅ Reset to start", fg='#27ae60')
    
    def compare_algorithms(self):
        """Compare all algorithms"""
        if self.current_puzzle_type == "8-Puzzle":
            problem = self.eight_puzzle
            initial = self.current_state
        else:
            problem = self.maze
            initial = problem.start
        
        self.add_log("")
        self.add_log("=" * 45)
        self.add_log("📊 ALGORITHM COMPARISON")
        self.add_log("=" * 45)
        
        results = {}
        for name, algo in [("A*", astar), ("BFS", bfs), ("DFS", dfs)]:
            solution, nodes, exec_time = algo(problem, initial)
            results[name] = {
                'nodes': nodes,
                'time': exec_time,
                'path': len(solution) - 1 if solution else 0,
                'solved': solution is not None
            }
            self.add_log(f"{name}: {nodes} nodes, {exec_time:.3f}s, {results[name]['path']} moves")
        
        self.add_log("")
        self.add_log("📈 Analysis:")
        fastest = min(results, key=lambda x: results[x]['time'])
        self.add_log(f"✓ {fastest} is fastest algorithm")
        self.add_log("✓ A* uses heuristic for guided search")
        self.add_log("✓ BFS guarantees shortest path")
        self.add_log("✓ DFS uses less memory")
        self.add_log("=" * 45)


def run_gui():
    root = tk.Tk()
    app = PuzzleSolverGUI(root)
    root.mainloop()

if __name__ == "__main__":
    run_gui()