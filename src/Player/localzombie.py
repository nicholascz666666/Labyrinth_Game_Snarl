import sys
sys.path.insert(1, sys.path[1]+'../Common/')
import player
sys.path.insert(1, sys.path[1]+'../Observer/')
import localobserver
import random

import heapq

class LocalZombie(player.Player):

    def __init__(self, name):
        self.name = name
        self.state = None

    def update(self, state):
        self.state = state

    def get_action(self): 

        #find character adversary
        for char in self.state.adversaries:
            if char.name == self.name:
                self.adver_char = char
                break
        
        path = self._path_to_player()
        if path:
            return path

        return self._random_move()
        

    def _path_to_player(self, search_range=5):
        start = self.adver_char.pos

        target = None
        for p in self.state.players:
            if abs(p.pos[0] - self.adver_char.pos[0]) + abs(p.pos[1] - self.adver_char.pos[1]) < search_range:
                target = p
        if target:
            path = dijkstra(start, target.pos, self.state, self.adver_char)
            
            if path:
                return path[-2]

        return None

    def _random_move(self):
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        start = self.adver_char.pos
        moves = [(start[0] + d[0], start[1] + d[1]) for d in moves]
        moves = [d for d in moves if self.adver_char.valid_moves(d, self.state) == 1]

        if len(moves) > 0:
            return random.choice(moves)
        return start
       
def dijkstra(start, target, state, adver_char):
    d = {start: 0}
    parent = {start: None}
    pq = [(0, start)]
    visited = set()
    while pq:
        cost, pos = heapq.heappop(pq)
        if pos in visited: 
            continue
        if pos == target:
            path = []
            curr = pos
            while curr:
                path.append(curr)
                curr = parent[curr]
            return path

        visited.add(pos)
        for p in adj(pos, state, adver_char):
            if p not in d or d[p] > cost + 1:
                d[p] = cost + 1
                parent[p] = pos
                heapq.heappush(pq, (d[p], p))
    return None

def adj(pos, state, adver_char):
    direction = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    ret = []
    for d in direction:
        new_pos = (pos[0] + d[0], pos[1] + d[1])
        if adver_char.valid_moves(new_pos, state, -1) == 1:
            ret.append(new_pos)

    return ret

