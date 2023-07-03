from phase1.Grid import * 
from phase1.GameEngine import *
from threading import * 


class GameInstance(Thread):

    def __init__(self,room_name,engine,share_status,applicable_usernames,owner):
        Thread.__init__(self)
        self.name = room_name
        self.engine = engine
        self.is_finished = False
        self.share_status = share_status
        self.applicable_usernames = applicable_usernames
        self.owner = owner
        self.anonymous_user_count = 0

    def register_user(self,user):
        self.engine.attach(user)
    
    def board_svg_creater(self):
        return self.engine.prop_board()

    def player_length(self):
        return self.engine.player_count

    def game_status(self):
        return self.engine.status 

    def run(self):
        self.engine.startGame()
        self.is_finished = True
        print("Game {room} is finished.".format(room=self.name))
        
