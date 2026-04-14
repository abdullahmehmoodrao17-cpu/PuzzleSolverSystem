# algorithms/astar.py

def astar(problem, initial_state):
    import time
    start = time.time()
    
    if problem.is_goal(initial_state):
        return [initial_state], 1, 0.0
    
    frontier = []
    visited = {}
    g_scores = {}
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
    
    initial_key = to_key(initial_state)
    g_scores[initial_key] = 0
    h = problem.manhattan_distance(initial_state)
    frontier.append((h, 0, initial_state, [], initial_key))
    
    while frontier and nodes < 50000:
        frontier.sort(key=lambda x: x[0])
        f, g, state, path, key = frontier.pop(0)
        
        if key in visited:
            continue
        
        visited[key] = True
        nodes += 1
        
        if problem.is_goal(state):
            return path + [state], nodes, time.time() - start
        
        for neighbor in problem.get_neighbors(state):
            nkey = to_key(neighbor)
            
            if nkey in visited:
                continue
            
            new_g = g + 1
            
            if nkey not in g_scores or new_g < g_scores[nkey]:
                g_scores[nkey] = new_g
                h = problem.manhattan_distance(neighbor)
                f_score = new_g + h
                frontier.append((f_score, new_g, neighbor, path + [state], nkey))
    
    return None, nodes, time.time() - start