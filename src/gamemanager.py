import character
import gamestate
import rulechecker
import math
import sys
import json
sys.path.insert(1, '../src/Player/')
import localzombie
import localghost
from serverplayer import ClientDisconnectError

class GameManager:

    players = []
    adversaries = []
    state = None
    observers = {}
    clients = {}
    manager_trace = []

    def __init__(self, state=None):
        self.players = []
        self.adversaries = []
        self.observers = []
        self.clients = {}
        self.state = state
        self.manager_trace = []
        

    #accept a string as the name of the new gamer. Create a Player object based on the name.
    def accept_character(self, name, pos=None, type_="player", client=None):
        character_name = [char.name for char in self.players + self.adversaries]
        if not rulechecker.RuleChecker().check_unique_name(character_name, name, type_):
            return False

        self.clients[name] = client

        if type_ == "player":
            player = character.Player(pos, name)
            self.players.append(player)
            
        elif type_ == "zombie":
            adversary = character.Adversary(pos, name)
            self.adversaries.append(adversary)

        elif type_ == "ghost":
            adversary = character.Ghost(pos, name)
            self.adversaries.append(adversary)
            
        return True

    def add_obsever(self, observer):
        self.observers.append(observer)

    #construct a gamestate object with a Level and the list of Players and Adversaries. Use rulechecker to check validity
    def start_game(self, level=None):
        if level == None:
            level = self.levels[self.level_num]
        
        if self.adversaries == []:
            #populate it with a number of adversaries
            current_level = self.level_num + 1

            zombie_num = math.floor(current_level / 2) + 1
            for i in range(zombie_num):
                name = "zombie" + str(i+1)
                zombie = localzombie.LocalZombie(name)
                self.accept_character(name=name, type_="zombie", client=zombie)

            ghost_num = math.floor((current_level - 1) / 2)
            for i in range(ghost_num):
                name = "ghost" + str(i+1)
                ghost = localghost.LocalGhost(name)
                self.accept_character(name=name, type_="ghost", client=ghost)


        state = gamestate.GameState(level, self.players, self.adversaries)
        
        #check_input_game_states
        rulechecker.RuleChecker().check_input_game_states(state)

        self._send_start_level()

        self.state = state
        self.send_player_update()

        self.supervise_game()
    
    def _send_start_level(self):
        name_list = [player.name for player in self.players]
        start_level = { "type": "start-level", "level": self.level_num + 1, "players": name_list}
        self.send_message_to_client(start_level)


    def _send_result(self, name, result):
        if result == 1:
            self.send_message_to_client("OK", name)
        elif result == 2:
            self.send_message_to_client("Eject", name)
        elif result == 3:
            self.send_message_to_client("Exit", name)
        elif result == 0:
            self.send_message_to_client("Key", name)
        else:
            self.send_message_to_client("Invalid", name)

    def set_levels(self, levels, level_num = 1):
        self.levels = levels
        self.level_num = level_num - 1


    def supervise_game(self):
        turn = 0
        while True:
            characters = self.state.players + self.state.adversaries

            character = characters[turn]
            name = character.name
            
            if turn >= len(self.state.players):
                self.send_adversary_update(name)

            client = self.clients[name]

            try:
                pos = client.get_action()
                result = self.move_character_pos_by_name(pos, name)
                
                if result >= 4:
                    continue

            except ClientDisconnectError as err:
                self._disconnect_client(err.name)
                turn = turn % len(self.state.players + self.state.adversaries)
                continue

            event_message = self._player_event_message(name, result)
            self.send_player_update(event_message)
        
            if rulechecker.RuleChecker.check_status(self.state) == 0:
                level_win = False
                break
            elif rulechecker.RuleChecker.check_status(self.state) == 1:
                level_win = True
                break
                
            if len(characters) == len(self.state.players + self.state.adversaries):
                turn = (turn + 1) % len(characters)
            else:
                turn = turn % len(self.state.players + self.state.adversaries)
        

        self._send_end_level()

        if level_win:
            self.level_num += 1
            if self.level_num == len(self.levels):
                self._send_end_game()
                
                # self.send_message_to_client("player win")
                # for player in self.players:
                #     self.send_message_to_client(player.name + " successfully exited " + str(player.exited_num) + " times.")
                #     self.send_message_to_client(player.name + " found key " + str(player.key_found_num) + " times.")
            else:
                #reseting player positoin
                for player in self.players:
                    player.pos = None
                self.adversaries = []
                self.start_game()
        else:
            self._send_end_game()
            #self.send_message_to_client("player lose. " + "Failed in level " + str(self.level_num+1))
            
        
    
    def _send_end_level(self):
        end_level = { "type": "end-level", "key": self.state.who_pick_up_key, "exits": self.state.exited_players, "ejects": self.state.ejected_player}

        self.send_message_to_client(end_level)

    def _send_end_game(self):
        player_score_list = []
        for player in self.players:
            player_score = player.get_player_score()
            player_score_list.append(player_score)

        end_game = { "type": "end-game",  "scores": player_score_list}
        self.send_message_to_client(end_game)
    
    def _disconnect_client(self, name):
        #remove from self.players
        for player in self.players:
            if player.name == name:
                self.players.remove(player)

        #remove from self.state.players
        for player in self.state.players: 
            if player.name == name:
                self.state.players.remove(player)

        #destroy client object
        del(self.clients[name])

        event =  "Player " + name + " disconnected"
        self.send_player_update(event)


        

    #check whether the movement is valid. If valid, move the character of the given name to the position and interact with the object
    #return int: 0: key 1: Success 2: ejected 3. exited 4: Player is not a part of the game 5.destination tile is not traversable 
    def move_character_pos_by_name(self, pos, name):
        result = rulechecker.RuleChecker().check_valid_movement_interaction(self.state, name, pos)
        
        self._send_result(name, result)
        
        event_message = self._player_event_message(name, result)
        actor_pos = [pos[1], pos[0]] if pos != None else None
        actor_move = {"type": "move", "to": actor_pos}
        manager_trace_entry = [name, actor_move, event_message]
        self.manager_trace.append(manager_trace_entry)

        if result < 4:
            self.state.move_character_pos_by_name(pos, name)

        return result

    def _player_event_message(self, name, result):
        if result == 1:
            return "Player " + name + " moved"
        elif result == 2:
            return "Player " + name + " was expelled"
        elif result == 3:
            return "Player " + name + " exited"
        elif result == 0:
            return "Player " + name + " found the key"

        
    def notify_oberver(self):
        for observer in self.observers:
            observer.update(self.state)

    def send_player_update(self, event_message=None):
        for player in self.players:
            name = player.name

            pos = player.pos

            player_update = self.state.player_view(pos)
            player_update.update({"message": event_message})

            try:
                self.clients[name].update(player_update)
            except ClientDisconnectError:
                pass

            manager_trace_entry = [name, player_update]

            self.manager_trace.append(manager_trace_entry)

        self.notify_oberver()

    def send_adversary_update(self, name):
        self.clients[name].update(self.state)

    def send_message_to_client(self, message, client_name=None):
        for player in self.players:
            name = player.name

            if client_name and client_name != name:
                continue
            client = self.clients[name]

            try:
                client.message(message)
            except ClientDisconnectError:
                pass
