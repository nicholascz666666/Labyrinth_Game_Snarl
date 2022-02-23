import json

# the interface to represent the character.
class Character:
    name = ""
    pos = ()
    # the constructor for the Character.
    def __init__(self, pos, name):
        self.pos = pos
        self.name = name
        self.exited_num = 0
        self.ejected_num = 0
        self.key_found_num = 0

    # the current character interact with the current game state
    def interact(self, game_state):
        raise NotImplementedError('subclasses must override this method')

    # check valid moves for the current character with the current game state
    def valid_moves(self, pos, game_state, move_num):
        raise NotImplementedError('subclasses must override this method')

    def get_player_score(self):
        player_score = { "type": "player-score", "name": self.name, "exits": self.exited_num, "ejects": self.ejected_num,  "keys": self.key_found_num}
        return player_score

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.name == other.name
        else:
            return False

# the calss to represent Player.
class Player(Character):

    # the constructor for the Player. 
    def __init__(self, pos, name = "Player"):
        super().__init__(pos, name)
    
    #The order of interaction for a player is: interact with the enemy, interact with the key, and, finally, interact with the exit.
    def interact(self, game_state):
        #ejected
        for adversary in game_state.adversaries:
            if adversary.pos == self.pos:
                game_state.players.remove(self)

                game_state.ejected_player.append(self.name)
                self.ejected_num += 1

        all_tiles_pos = game_state.level.all_tiles_pos
        tile = all_tiles_pos[self.pos]

        #found key
        if tile == "key": 
            game_state.key_found = True
            game_state.level.all_tiles_pos[self.pos] = "empty"

            game_state.who_pick_up_key = self.name
            self.key_found_num += 1
            
        #exit
        if tile == "exit" and game_state.key_found:
            game_state.players.remove(self)
            game_state.level_win = True

            game_state.exited_players.append(self.name)
            self.exited_num += 1

        

    def valid_moves(self, pos, game_state, move_num=2):
        if move_num != -1 and abs(pos[0] - self.pos[0]) + abs(pos[1] - self.pos[1]) > move_num:
            return 5

        all_tiles_pos = game_state.level.all_tiles_pos
        
        if pos not in all_tiles_pos or all_tiles_pos[pos] == "wall":
            return 5

        for player in game_state.players:
            if player.name != self.name and player.pos == pos:
                return 5
        
        for adversary in game_state.adversaries:
            if adversary.pos == pos:
                return 2
        

        if all_tiles_pos[pos] == "exit" and game_state.key_found:
            return 3

        if all_tiles_pos[pos] == "key":
            return 0

        return 1

    def __str__(self):
        s = {"type": "player" ,"name": self.name,"position": [self.pos[1], self.pos[0]]}
        return json.dumps(s)

    
# the calss to represent Adversary.
class Adversary(Character):
    def __init__(self, pos, name = "Adversary"):
        super().__init__(pos, name)

    def valid_moves(self, pos, game_state, move_num=1):
        if move_num != -1 and abs(pos[0] - self.pos[0]) + abs(pos[1] - self.pos[1]) > move_num:
            return 5

        all_tiles_pos = game_state.level.all_tiles_pos

        if pos not in all_tiles_pos or all_tiles_pos[pos] == "wall":
            return 5

        for adversary in game_state.adversaries:
            if adversary.name != self.name and adversary.pos == pos:
                return 5

        if all_tiles_pos[pos] == "exit":
            return 5

        if all_tiles_pos[pos] == "door":
            return 5


        return 1

    def interact(self, game_state):
        for player in game_state.players:
            if player.pos == self.pos:
                game_state.players.remove(player)

                game_state.ejected_player.append(player.name)
                player.ejected_num += 1
        return

    def __str__(self):
        s = {"type": "zombie" ,"name": self.name,"position": [self.pos[1], self.pos[0]]}
        return json.dumps(s)


class Ghost(Adversary):
    def __init__(self, pos, name = "Ghost"):
        super().__init__(pos, name)

    def valid_moves(self, pos, game_state, move_num=1):
        if move_num != -1 and abs(pos[0] - self.pos[0]) + abs(pos[1] - self.pos[1]) > move_num:
            return 5
            
        all_tiles_pos = game_state.level.all_tiles_pos

        if pos not in all_tiles_pos:
            return 5

        for adversary in game_state.adversaries:
            if adversary.name != self.name and adversary.pos == pos:
                return 5

        if all_tiles_pos[pos] == "exit":
            return 5

        return 1

    def interact(self, game_state):

        if game_state.level.all_tiles_pos[self.pos] == "wall":
            self.pos = game_state._valid_placement()


        super().interact(game_state)

    def __str__(self):
        s = {"type": "ghost" ,"name": self.name,"position": [self.pos[1], self.pos[0]]}
        return json.dumps(s)
