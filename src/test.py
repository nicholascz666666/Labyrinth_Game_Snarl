import unittest
import level
import view
import gamestate
import character
import gamemanager

class TestGameManager(unittest.TestCase):
    def test_accept_character(self):
        manager = gamemanager.GameManager()

        self.assertEqual(manager.players, [])

        manager.accept_character("p1", (0, 0), "player")

        self.assertEqual(manager.players, [character.Player((0,0), "p1")])

        manager.accept_character("a1", (0, 0), "zombie")

        self.assertEqual(manager.players, [character.Player((0,0), "p1")])
        self.assertEqual(manager.adversaries, [character.Adversary((0,0), "a1")])

    def test_start_game_player_between1_4_exception(self):
        manager = gamemanager.GameManager()

        room = {}
        room["position"] = (0, 0)
        room["size"] = (4, 4)
        room["walls"] = [(0, 0), (0, 1), (0, 2), (0, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
        room["doors"] = [(1, 0), (2, 0), (1, 3), (2, 3)]
        room["objects"] = {"key": (2, 1)}

        l_ = {"rooms": [room], "hallways" : []}
        l_ = level.Level(l_)

        self.assertRaises(Exception, manager.start_game, l_)

    def test_start_game_player_unique_name_exception(self):
        manager = gamemanager.GameManager()

        room = {}
        room["position"] = (0, 0)
        room["size"] = (4, 4)
        room["walls"] = [(0, 0), (0, 1), (0, 2), (0, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
        room["doors"] = [(1, 0), (2, 0), (1, 3), (2, 3)]
        room["objects"] = {"key": (2, 1)}

        l_ = {"rooms": [room], "hallways" : []}
        l_ = level.Level(l_)

        manager.accept_character("p1", (1, 0), "player")
        manager.accept_character("p1", (2, 0), "player")
        self.assertRaises(Exception, manager.start_game, l_)

    def test_start_game_player_pos_overlap_exception(self):
        manager = gamemanager.GameManager()

        room = {}
        room["position"] = (0, 0)
        room["size"] = (4, 4)
        room["walls"] = [(0, 0), (0, 1), (0, 2), (0, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
        room["doors"] = [(1, 0), (2, 0), (1, 3), (2, 3)]
        room["objects"] = {"key": (2, 1)}

        l_ = {"rooms": [room], "hallways" : []}
        l_ = level.Level(l_)

        manager.accept_character("p1", (1, 0), "player")
        manager.accept_character("p2", (1, 0), "player")
        self.assertRaises(Exception, manager.start_game, l_)
    



class TestGameState(unittest.TestCase):
    def test_move_character_pos(self):
        room = {}
        room["position"] = (0, 0)
        room["size"] = (4, 4)
        room["walls"] = [(0, 0), (0, 1), (0, 2), (0, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
        room["doors"] = [(1, 0), (2, 0), (1, 3), (2, 3)]
        room["objects"] = {"key": (2, 1)}


        l_ = {"rooms": [room], "hallways" : []}
        l_ = level.Level(l_)
        
        p1 = character.Player((1, 2), "p1")
        a1 = character.Adversary((2, 2), "a1")
        
        state_ = gamestate.GameState(l_, [p1], [a1],1)
        state_.move_character_pos((2,3))
        self.assertEqual(a1.pos,(2,3))
    
    def test_move_character_pos_invalid(self):
        room = {}
        room["position"] = (0, 0)
        room["size"] = (4, 4)
        room["walls"] = [(0, 0), (0, 1), (0, 2), (0, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
        room["doors"] = [(1, 0), (2, 0), (1, 3), (2, 3)]
        room["objects"] = {"key": (2, 1)}


        l_ = {"rooms": [room], "hallways" : []}
        l_ = level.Level(l_)
        
        p1 = character.Player((1, 2), "p1")
        a1 = character.Adversary((2, 2), "a1")
        
        state_ = gamestate.GameState(l_, [p1], [a1],1)
        state_.move_character_pos((100,3))
        self.assertEqual(a1.pos,(100,3))
        
    def test_turn_two_character(self):
        room = {}
        room["position"] = (0, 0)
        room["size"] = (4, 4)
        room["walls"] = [(0, 0), (0, 1), (0, 2), (0, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
        room["doors"] = [(1, 0), (2, 0), (1, 3), (2, 3)]
        room["objects"] = {"key": (2, 1)}


        l_ = {"rooms": [room], "hallways" : []}
        l_ = level.Level(l_)
        
        p1 = character.Player((1, 2), "p1")
        a1 = character.Adversary((2, 2), "a1")
        
        state_ = gamestate.GameState(l_, [p1], [a1],1)
        state_.move_character_pos((2,3))
        self.assertEqual(state_.turn,0)
    
    def test_turn_four_character(self):
        room = {}
        room["position"] = (0, 0)
        room["size"] = (4, 4)
        room["walls"] = [(0, 0), (0, 1), (0, 2), (0, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
        room["doors"] = [(1, 0), (2, 0), (1, 3), (2, 3)]
        room["objects"] = {"key": (2, 1)}


        l_ = {"rooms": [room], "hallways" : []}
        l_ = level.Level(l_)
        
        p1 = character.Player((1, 2), "p1")
        a1 = character.Adversary((2, 2), "a1")
        a2 = character.Adversary((1, 0), "a2")
        a3 = character.Adversary((2, 0), "a3")
        
        state_ = gamestate.GameState(l_, [p1], [a1,a2,a3],1)
        state_.move_character_pos((2,3))
        self.assertEqual(state_.turn,2)

class TestView(unittest.TestCase):
    def test_render_with_player(self):
        v_ = view.View()
        room = {}
        room["position"] = (0, 0)
        room["size"] = (4, 4)
        room["walls"] = [(0, 0), (0, 1), (0, 2), (0, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
        room["doors"] = [(1, 0), (2, 0), (1, 3), (2, 3)]
        room["objects"] = {"key": (2, 1)}


        l_ = {"rooms": [room], "hallways" : []}
        l_ = level.Level(l_)
        
        p1 = character.Player((1, 2), "p1")
        a1 = character.Adversary((2, 2), "a1")
        
        state_ = gamestate.GameState(l_, [p1], [a1])
        v_.set_game_state(state_)
        #print("")
        #print(v_.render())
        
    def test_render_level(self):
        room1 = {}
        room1["position"] = (0, 0)
        room1["size"] = (4, 4)
        room1["walls"] = [(0, 0), (0, 1), (0, 2), (0, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
        room1["doors"] = [(1, 0), (2, 0), (1, 3), (2, 3)]
        room1["objects"] = {"key": (2, 1)}

        hallway = {}
        hallway = {"posFrom": (1, 3), "posTo": (2, 7), "waypoints" : [(1, 5), (2, 5)]}

        room2 = {}
        room2["position"] = (0, 7)
        room2["size"] = (4, 4)
        room2["walls"] = [(0, 0), (0, 1), (0, 2), (0, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
        room2["doors"] = [(1, 0), (2, 0), (1, 3), (2, 3)]
        room2["objects"] = {"exit": (1, 1), "key": (2, 1)}

        l = {"rooms": [room1, room2], "hallways" : [hallway]}
        level_ = level.Level(l)
        
        v = view.View()
        v.set_level(level_.toJSON())
        #print("")
        #print(v.render())
        


class TestHallway(unittest.TestCase):
    
    def test_hallway_to_json(self):
        construct_hallway = level.Level.Hallway((1, 3), (2, 7), [(1, 5), (2, 5)])
        self.assertEqual(construct_hallway.toJSON(), 
        {"posFrom": (1, 3), "posTo": (2, 7), "waypoints" : [(1, 5), (2, 5)]})


class TestRoom(unittest.TestCase):
    def test_room_constructor_negative_size(self):
        self.assertRaises(Exception, level.Level.Room, (0, 0), (-1, 3), [], [], {})

    def test_room_constructor_door_not_at_broundary(self):
        self.assertRaises(Exception, level.Level.Room, (0, 0), (4, 4), [], [2, 2], {})

    def test_room_to_json(self):
        position = (0, 0)
        size = (4, 4)
        walls = [(0, 0), (0, 1), (0, 2), (0, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
        doors = [(1, 0), (2, 0), (1, 3), (2, 3)]
        objects = {"person": (1, 1), "key": (2, 1)}

        construct_room = level.Level.Room(position, size, walls, doors, objects)
        self.assertEqual(construct_room.toJSON(), 
        {"position": (0, 0), "size": (4, 4), "walls" : [(0, 0), (0, 1), (0, 2), (0, 3), (3, 0), (3, 1), (3, 2), (3, 3)], 
        "doors": [(1, 0), (2, 0), (1, 3), (2, 3)], "objects": {"person": (1, 1), "key": (2, 1)}})

class TestLevel(unittest.TestCase):
    def test_hallway_not_connects_two_rooms(self):
        room1 = {}
        room1["position"] = (0, 0)
        room1["size"] = (4, 4)
        room1["walls"] = [(0, 0), (0, 1), (0, 2), (0, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
        room1["doors"] = [(1, 0), (2, 0), (1, 3), (2, 3)]
        room1["objects"] = {"person": (1, 1), "key": (2, 1)}

        hallway = {}
        hallway = {"posFrom": (10, 4), "posTo": (2, 6), "waypoints" : [(1, 5), (2, 5)]}

        room2 = {}
        room2["position"] = (0, 7)
        room2["size"] = (4, 4)
        room2["walls"] = [(0, 0), (0, 1), (0, 2), (0, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
        room2["doors"] = [(1, 0), (2, 0), (1, 3), (2, 3)]
        room2["objects"] = {"person": (1, 1), "key": (2, 1)}

        l = {"rooms": [room1, room2], "hallways" : [hallway]}

        self.assertRaises(Exception, level.Level, l)


    def test_hallway_not_perpendicular(self):
        room1 = {}
        room1["position"] = (0, 0)
        room1["size"] = (4, 4)
        room1["walls"] = [(0, 0), (0, 1), (0, 2), (0, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
        room1["doors"] = [(1, 0), (2, 0), (1, 3), (2, 3)]
        room1["objects"] = {"person": (1, 1), "key": (2, 1)}

        hallway = {}
        hallway = {"posFrom": (1, 3), "posTo": (2, 7), "waypoints" : [(10, 5), (2, 5)]}

        room2 = {}
        room2["position"] = (0, 7)
        room2["size"] = (4, 4)
        room2["walls"] = [(0, 0), (0, 1), (0, 2), (0, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
        room2["doors"] = [(1, 0), (2, 0), (1, 3), (2, 3)]
        room2["objects"] = {"person": (1, 1), "key": (2, 1)}

        l = {"rooms": [room1, room2], "hallways" : [hallway]}

        self.assertRaises(Exception, level.Level, l)

    def test_level_room_overlap(self):
        room1 = {}
        room1["position"] = (0, 0)
        room1["size"] = (4, 4)
        room1["walls"] = [(0, 0), (0, 1), (0, 2), (0, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
        room1["doors"] = [(1, 0), (2, 0), (1, 3), (2, 3)]
        room1["objects"] = {"person": (1, 1), "key": (2, 1)}

        hallway = {}
        hallway = {"posFrom": (1, 3), "posTo": (2, 7), "waypoints" : [(1, 5), (2, 5)]}

        room2 = {}
        room2["position"] = (1, 1)
        room2["size"] = (4, 4)
        room2["walls"] = [(0, 0), (0, 1), (0, 2), (0, 3), (3, 0), (3, 1), (3, 2), (3, 3)]
        room2["doors"] = [(1, 0), (2, 0), (1, 3), (2, 3)]
        room2["objects"] = {"person": (1, 1), "key": (2, 1)}

        l = {"rooms": [room1, room2], "hallways" : [hallway]}

        self.assertRaises(Exception, level.Level, l)


if __name__ == '__main__':
    unittest.main()