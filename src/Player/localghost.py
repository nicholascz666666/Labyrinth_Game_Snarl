import sys
import localzombie
sys.path.insert(1, sys.path[1]+'../Common/')
import player
sys.path.insert(1, sys.path[1]+'../Observer/')
import localobserver
import random
class LocalGhost(localzombie.LocalZombie):

        
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
        
        path = self._path_to_player(10)
        if path:
            return path

        return self._random_move()
        
       