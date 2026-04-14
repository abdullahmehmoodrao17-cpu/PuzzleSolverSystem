# data_structures.py - Simple data structures

class Queue:
    
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop(0)
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)


class Stack:
   
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None
    
    def is_empty(self):
        return len(self.items) == 0
    
    def size(self):
        return len(self.items)


class PriorityQueue:
   
    def __init__(self):
        self.items = []
    
    def push(self, item, priority):
        self.items.append((priority, item))
        self.items.sort(key=lambda x: x[0])
    
    def pop(self):
        if not self.is_empty():
            return self.items.pop(0)[1]
        return None
    
    def is_empty(self):
        return len(self.items) == 0