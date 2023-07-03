from socket import *
from threading import *
import time 
import re
import json

from phase1 import GameEngine,User,grid_creator,Enums
from phase2 import GameInstance 
from game_map import basic_map
from userTable import *


def read_socket_content(socket:socket):

    content = ""
    part = socket.recv(10000)
    content += part.decode() 
    return content




def game_str(games,is_authenticated,username):
    game_list = []

    i = 0
    for game in games:
        tmp_dict = {}
        # Only given username can see the game.
        if game.share_status == "owner" and (username in game.applicable_usernames or username == game.owner):
            tmp_dict["name"] = game.name
            tmp_dict["id"] = i + 1
            game_list.append(tmp_dict)
        # Only authenticated users can see the game.
        elif game.share_status == "authenticated" and is_authenticated:
            tmp_dict["name"] = game.name
            tmp_dict["id"] = i + 1
            game_list.append(tmp_dict)
        # Everyone can see the game including anonymous users.
        elif game.share_status == "all":
            tmp_dict["name"] = game.name
            tmp_dict["id"] = i + 1
            game_list.append(tmp_dict)
        i += 1

    return game_list


def game_starter(games):

    while True:
        for game in games:
            if game is not None and game.player_length() >= 2 and game.game_status() == Enums.Status.CREATED and not game.is_alive():
                game.start()


def game_status_checker(games):

    while True:
        for game in games:
            if game.is_finished:
                games.remove(game)


def question_slave(new_socket,games):

    
    is_authenticated = None
    username = None
    dummy_user = None
    while True:
        socket_content = read_socket_content(new_socket)
        splitted = socket_content.split(" ",maxsplit=5)
        
        command = splitted[0]
        if command == "list":
            response = game_str(games,is_authenticated,username)
            response = json.dumps(response)
            new_socket.send(response.encode())
        
        elif command == "register":
            # Register user to database.
            # register username name email password1 password2
            username = splitted[1]
            name = splitted[2]
            email = splitted[3]
            pass1 = splitted[4]
            pass2 = splitted[5]
            
            if pass1 == pass2:
                is_registered,message = register(username,email,name,pass1)
                
                if is_registered:
                    "User registered send success message via socket"
                    msg = "registered" 
                    new_socket.send(msg.encode())
                else:
                    "User not registered send error message via socket"
                    msg = message
                    new_socket.send(msg.encode())
        elif command == "join":
            # join game_number
            numb = int(splitted[1])
            game = games[numb-1]
            if dummy_user is None:
                game.anonymous_user_count += 1

                usrn = "Anonymous" + str(game.anonymous_user_count)
                mail = usrn + "@anonymous.com"
                fname = usrn
                passwd = "1234"
                balance = 7000
                # balance =game.engine.board.startup_money
                dummy_user = User(usrn,mail,fname,passwd,balance,new_socket)


            games[numb-1].register_user(dummy_user)
            data = games[numb-1].board_svg_creater()
            dump_data = json.dumps(data)
            new_socket.send(dump_data.encode())
            break
        elif command == "new":
            "Command is new game game_name share_status, user1,user2,...(if share_status is authenticated) game_dict"
            
            try:
                game_name = splitted[2]
                share_status = splitted[3]

                usernames = splitted[4].split(",") if share_status == "authenticated" else []

                game_dict = eval(splitted[5])
                
                
                grid = grid_creator(game_dict)
                engine = GameEngine(grid)
                
                
                new_game_instance = GameInstance(game_name,engine,share_status,usernames,username)
                games.append(new_game_instance)
            except Exception as e:
                msg = "Error"
            msg = "Created"
            new_socket.send(msg.encode())
            
        elif command == "login":
            #Authentication
            #login username password
            
            if(len(splitted) == 3):
                is_authenticated = login(splitted[1],splitted[2])
                data = json.dumps(is_authenticated)
                new_socket.send(data.encode())
                if(is_authenticated == None):
                    new_socket.close()
                    return
            else:
                is_authenticated = cokkie_owner(str(splitted[1]))
            username = splitted[1]
            dummy_user = User(is_authenticated[0],is_authenticated[1],is_authenticated[2],is_authenticated[3],7000,new_socket)


class MonopolyServer:
    def __init__(self,port,queue_size):
        self.port_number = port
        self.listener_socket = socket(AF_INET,SOCK_STREAM)
        self.listener_socket.bind(('',self.port_number))
        self.listen_queue_number = queue_size
        self.games = [GameInstance("AnilinYeri",GameEngine(grid_creator(basic_map)),"all",[],"aniltest")]
        self.slave_threads = []
        self.game_start_controller = Thread(target=game_starter,args=(self.games,))
        self.game_finish_controller = Thread(target=game_status_checker,args = (self.games,))
        self.game_finish_controller.start()
        self.game_start_controller.start()




        """DATABASE STARTER SİLME !!"""
        start()
        
    def start_server(self):
        
        self.listener_socket.listen(self.listen_queue_number)
        try:
            while True:
                new_socket,peer_addr = self.listener_socket.accept()
                print("Player with {addr} {port} is connected to server.".format(addr=str(peer_addr[0]),port=str(peer_addr[1])))
                t = Thread(target=question_slave,args=(new_socket,self.games,),)
                t.start()
                self.slave_threads.append(t)

        except Exception as e:
            print(e)
        finally:
            self.listener_socket.close()


    def stop_server(self):
        self.listener_socket.close()
        for t in self.slave_threads:
            t.join()
        self.game_start_controller.join()
        self.game_finish_controller.join()
        print("Server is closed.")
