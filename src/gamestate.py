import json
import rulechecker
import random
class GameState:

    def __init__(self, level, players, adversaries, turn = 0, key_found = False, level_win = False):
        self.key_found = False
        self.level = level
        self.players = players.copy()
        self.adversaries = adversaries.copy()
        for char in self.players + self.adversaries:
            if char.pos == None:
                char.pos = self._valid_placement()

        self.turn = turn
        self.key_found = key_found
        self.level_win = level_win

        self.who_pick_up_key = None
        self.exited_players = []
        self.ejected_player = []

    
    #when reaching the turn of the current character, move the character to the position and interact with the object
    def move_character_pos(self, pos):
        characters = self.players + self.adversaries
        character = characters[self.turn]

        #move character
        character.pos = pos
        
        # interacts with an object
        character.interact(self)

        self.turn = (self.turn + 1) % len(characters)
            
    
    #move the character of the given name to the position and interact with the object
    def move_character_pos_by_name(self, pos, name):
        characters = self.players + self.adversaries
        
        for c in characters:
            if c.name == name:
                character = c
                break
        
        if pos != None:
            character.pos = pos
        
        character.interact(self)
        



    #return a list of valid move position for the character of the current turn
    def valid_moves(self):
        characters = self.players + self.adversaries
        character = characters[self.turn]
        return character.valid_moves(self)
        
    
    def __str__(self):
        
        player_list = [json.loads(str(player)) for player in self.players]
        adversary_list = [json.loads(str(player)) for player in self.adversaries]
        level = json.loads(str(self.level))
        #s = {"type": "state", "level": level, "players": player_list, "adversaries": adversary_list, "exit-locked": not self.key_found}

        s = {"exit-locked": not self.key_found, "players": player_list,"type": "state",  "adversaries": adversary_list, "level": level }
        return json.dumps(s)

    def player_view(self, pos):
        actor_position_list = []

        for row in range(-2, 3, 1):
            for col in range(-2, 3, 1):
                p = (pos[0] + col, pos[1] + row)

                for character in self.players + self.adversaries:
                    if p == character.pos and p != pos:
                        actor_position_list.append(json.loads(str(character)))
        
        result = {"type": "player-update", "position": [pos[1], pos[0]], "actors": actor_position_list}

        level_view = self.level.player_view(pos)
        result.update(level_view)

        return result

    def _valid_placement(self):
        valid_pos = set()
        for p, t in self.level.all_tiles_pos.items():
            if t == "room":
                valid_pos.add(p)
                
        for char in self.players + self.adversaries:
            if char.pos != None and char.pos in valid_pos:
                valid_pos.remove(char.pos)
        return random.choice(list(valid_pos))
                




   