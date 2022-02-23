class RuleChecker:

    #based on the name and position, searching for that character and check validation of that movement and coresponding interaction. 
    #return int: 1: Success 2: ejected 3. exited 4: Player is not a part of the game 5.destination tile is not traversable 
    @staticmethod
    def check_valid_movement_interaction(game_state, name, position):
        for character in (game_state.players + game_state.adversaries):
            if character.name == name:
                if position == None:
                    return character.valid_moves(character.pos, game_state)
                else:
                    return character.valid_moves(position, game_state)
        
        return 4

    #check the given name is unique or not. Return a boolean.
    @staticmethod
    def check_unique_name(character_name, name, type_):  
        if type_ == "player" and (name.startswith("zombie") or name.startswith("ghost")):
            return False
        # check characters' names
        for char_name in character_name:
            if name == char_name:
                return False

        return True

    #check the given game_state is valid or not. Return a boolean.
    @staticmethod
    def check_input_game_states(game_state):  
        # check players' number
        if len(game_state.players) > 4 or len(game_state.players) < 1:
            raise NotImplementedError('players num need to be between 1 and 4')

        # check characters' names
        character = game_state.players + game_state.adversaries
        unique_name = set()
        for c in character:
            if c.name in unique_name:
                raise NotImplementedError('names not unique')
            unique_name.add(c.name)
            
        # check players' position
        for player in game_state.players:
            if player.valid_moves(player.pos, game_state) >= 4:
                raise NotImplementedError('player not at the right position')
        
        # check adversaries' position
        for adversary in game_state.adversaries:
            if adversary.valid_moves(adversary.pos, game_state) >= 4:
                raise NotImplementedError('adversary not at the right position')



    # return the status of the current game state. 0: lose ; 1: win; 2: in-progress      
    @staticmethod  
    def check_status(game_state):
        #check_input_game_states(game_state)
        if len(game_state.players) == 0:
            if game_state.level_win:
                return 1
            else:
                return 0
        return 2

        

        

    
    
