# algorithms/dfs.py

def dfs(problem, initial_state, max_depth=50):
    import time
    start = time.time()
    
    if problem.is_goal(initial_state):
        return [initial_state], 1, 0.0
    
    stack = [(initial_state, [], 0)]
    visited = {}
    nodes = 0
    
    def to_key(state):
        if isinstance(state, tuple):
            return state
        elif isinstance(state, list):
            if len(state) == 3 and isinstance(state[0], list):
                return (state[0][0], state[0][1], state[0][2],
                        state[1][0], state[1][1], state[1][2],
                        state[2][0], state[2][1], state[2][2])
        return str(state)
    
    while stack and nodes < 30000:
        state, path, depth = stack.pop()
        key = to_key(state)
        
        if key in visited or depth > max_depth:
            continue
        
        visited[key] = True
        nodes += 1
        
        for neighbor in reversed(problem.get_neighbors(state)):
            nkey = to_key(neighbor)
            
            if nkey not in visited:
                if problem.is_goal(neighbor):
                    return path + [state, neighbor], nodes + 1, time.time() - start
                stack.append((neighbor, path + [state], depth + 1))
    
    return None, nodes, time.time() - start