import sys
sys.path.insert(1, sys.path[1]+'../Common/')
import player
sys.path.insert(1, sys.path[1]+'../Observer/')
import localobserver
import render

import json
import socket
class ServerPlayer(player.Player):
    
        
    def __init__(self, name, conn):
        self.name = name

        self.conn = conn

    def __del__(self):
        self.conn.close()

    def set_name(self, name):
        self.name = name
        
    def get_action(self):
        self._send("move")

        data = self._recv()
        pos = data["to"]
        return (pos[1], pos[0])
        

    def message(self, message):
        self._send(message)

    def update(self, player_update_messgae):
        self._send(player_update_messgae)



    def render(self): 
        pass

    def _send(self, message):
        try:
            conn = self.conn
            conn.sendall(_json2bytes(message))
        except socket.error:
            raise(ClientDisconnectError(self.name)) 


    def _recv(self):
        conn = self.conn
        try:
            data = conn.recv(2048)
        except socket.error:
            raise(ClientDisconnectError(self.name)) 
        if not data:
            raise(ClientDisconnectError(self.name)) 
        data = _bytes2json(data)
        return data

def _json2bytes(json_object):
    message = json.dumps(json_object)
    message = message.encode('utf-8')
    return message

def _bytes2json(b):
    message = b.decode('utf-8')
    message = json.loads(message)
    return message

class ClientDisconnectError(Exception):
    def __init__(self, name): 
        self.name = name 