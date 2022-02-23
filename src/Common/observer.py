"""
The Observer Component
We will use Python 3 to implement this observer and use observer pattern.

The subject of the observer pattern will be the server and observer is the client. Whenever a client send command to the server to move and change the gamestate, the server updates all its clients.

The Observer component will allow viewing a game and update the view for every change of the Gamestate.

Field:
GameState: a Gamestate object for rendering the view. It updates for every change.
Methods:
update(): It should be ensured that when subject changes state, this method will be called and the field GameState automatically.

render(): it will show the view of the game on the screen.

"""

class Observer():
    
    def update(self):
        raise NotImplementedError('subclasses must override this method')

    def render(self):
        raise NotImplementedError('subclasses must override this method')


