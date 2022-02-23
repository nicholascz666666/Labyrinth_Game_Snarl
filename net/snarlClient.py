#!/usr/bin/env python3
# coding: utf-8
import argparse
import socket 
import json
import sys
sys.path.insert(1, '../src/')
sys.path.insert(1, '../src/Player/')
sys.path.insert(1, '../src/Common/')
import localplayer
from utils import decode_json


class ClientPlayer():

    def __init__(self, conn):
        
        self.player = localplayer.LocalPlayer(None, True)

        self.conn = conn
    
    def __del__(self):
        print("close connection")
        self.conn.close()


    def update(self):
        conn = self.conn

        data = conn.recv(1024).decode('utf-8')
        data_list = decode_json(data)
        
        for data in data_list:
            #print(data)

            if data == "null":
                continue
            elif data == "name":
                self.player.set_name()
                name = self.player.name
                conn.sendall(name.encode('utf-8'))

            elif data == "move":
                move = self.player.get_action()
                player_move = json.dumps({"type": "move", "to": [move[1], move[0]]})
                
                conn.sendall(player_move.encode('utf-8'))


            elif isinstance(data, dict):
                type_ = data["type"]
                if type_ == "welcome":
                    info = data["info"]
                    self.player.message("server info:", info)
                    
                if type_ == "start-level":
                    level = data["level"]
                    players = data["players"]
                    self.player.message("starting level " + str(level), "players: " + str(players))
                    
                if type_ == "player-update":
                    message = data["message"]
                    if message:
                        self.player.message(message)
                    
                    self.player.update(data)
                    

                if type_ == "end-level":
                    key = data["key"]
                    exits = data["exits"]
                    ejects = data["ejects"]

                    self.player.message("level end")
                    self.player.message(', '.join(key) + " found key")
                    self.player.message(', '.join(exits) + " exited")
                    self.player.message(', '.join(ejects) + " ejected")
                    

                if type_ == "end-game":
                    self.player.message("game end")
                    scores = data["scores"]
                    for score in scores:
                        self.player.message("player " + str(score["name"]), "exits: " + str(score["exits"]), "ejects: " + str(score["ejects"]) , "keys: " + str(score["keys"]))

            else:
                self.player.message("move result: " + str(data))
        




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--address", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=45678)

    args = parser.parse_args()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        try:
            s.connect((args.address, args.port))

            player = ClientPlayer(s)

            while True:
                player.update()

        except socket.timeout:
            exit()   

main()

