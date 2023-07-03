import phase1.Grid as Grid
import phase1.User as User
import phase1.Cells as Cells
import phase1.ChanceCards as ChanceCards
from phase1.Enums import Actions,Status,CellTypes
import random
import time
        


class Node: #Node for circular linked list
    def __init__(self, data=None):

        self.data = data

        self.next = None

class CircularLinkedList: #circular linked list class to store users of game
    def __init__(self):
        self.head = None

    def insert(self, data):  #insert the given user to the doublelinkedlist
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.head.next = self.head
        else:
            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = new_node
            new_node.next = self.head

    def delete(self, user): #delete the given user from the doublelinkedlist
        if self.head is None:
            return
        print("{} is deatched from board".format(user.data.userName))
        if self.head.data.userName == user.data.userName:

            current = self.head
            while current.next != self.head:
                current = current.next
            current.next = self.head.next
            self.head = self.head.next
            
        else:
            current = self.head
            prev = None
            while current.next != self.head:
                prev = current
                current = current.next
                if current.data.userName == user.data.userName:
                    prev.next = current.next
                    current = current.next

                
        for key,value in user.data.prop.items():
            for prop in value:
                prop.owner = None
                user.data.deleteProperty(key,prop)
        

            

    def find(self, data): #find the given user in doublelinkedlist
        if self.head is None:
            return None
        current = self.head
        while True:
            if current.data == data:
                return current
            current = current.next
            if current == self.head:
                break
        return None

    def __len__(self): #length of user list in game engine
        count = 0
        if self.head is None:
            return count
        current = self.head
        while True:
            count += 1
            current = current.next
            if current == self.head:
                break
        return count
    def display(self): #prints the users
        if self.head is None:
            return
        current = self.head
        while True:
            print(current.data)
            current = current.next
            if current == self.head:
                break
    def __iter__(self): #for iterators
        current = self.head
        while current is not None:
            yield current.data
            current = current.next
            if current == self.head:
                break

def callbackforUserAttach(user): #callback funtion to print the user is attached to the board
    return str("User Name: {} is attached to board.".format(user.userName))
def callbackforUserTurn(user_name):
    result =  str("{}'s turn.".format(user_name))
    return result
def callbackCaller(usr,str,callback):
    return callback(usr,str)


def roll_dice(): #gives two dice number
    die1 = random.randint(1, 6)
    die2 = random.randint(1, 6)
    return (die1, die2)

class GameEngine:
    def __init__(self,grid = None,user = None):
        self.board = grid #Game Board
        self.users = CircularLinkedList() #takes users as a circular linked list to return back when all player play their turn
        self.spectator = CircularLinkedList() #takes users as a circular linked list to return back when all player play their turn
        self.status = Status(1) #game status
        self.currUser = user # user who will play now
        self.player_count = 0
        self.player_count_spect = 0

    def resetgame(self):
        self.users = CircularLinkedList()
        self.spectator = CircularLinkedList() 
        self.status = Status(1) #game status
        self.currUser = None # user who will play now
        self.player_count = 0
        self.player_count_spect = 0
    def setUserAsList(self,uList): #add game players as a list
        for user in uList:
            self.users.insert(user)

    def clearUsers(self): #when game is over clear users
        self.users = None
    def deleteUser(self,user): # delete user from linkedlist who leave the game
        self.users.delete(user)

    def attach(self, user):  # add only one player to game
        user.callback_inp = User.get_callback()
        user.callback_print = User.print_callback()
        if(self.status != Status.CREATED and self.status != Status.WAITING):
            self.spectator.insert(user)
            self.player_count_spect += 1
            # callbackCaller(user,"{} is attached to the board as spectator.".format(user.userName),user.callback_print)
        else:
            self.users.insert(user)
            self.player_count += 1
            # callbackCaller(user,"{} is attached to the board".format(user.userName),user.callback_print)
    def notify_all(self,temp):
        for user in self.users:
            callbackCaller(user,temp,user.callback_print)
        for user in self.spectator:
            callbackCaller(user,temp,user.callback_print)
    def detach(self,user): #detech the given user from board

        if (self.status == Status.STARTING or self.status == Status.WAITING):
            for key,val in user.prop:
                for cell in val:
                    cell.owner = None
        user.balance = 0
        self.users.delete(user)
        user.data.sock.close()



    def ready(self,user): #set user ready attribute to true
        user.isReady =True

    # turn function  will return 2 bools that state if the user is alive or not and the current users turn is over or not
    def turn(self, user, command):

      return user.currLocation.action(user, self.board, command)
    #prints all property cells with its information
    def getboardstate(self):
        # username, balance,location,properties
        # board state lazım
        state = {}
        board,user_locs = self.prop_board()

        state["board"] = board
        state["user_locations"] = user_locs
        state["user_names"] = [user.userName for user in self.users]
        state["user_balances"] = [user.balance for user in self.users]
        state["user_properties"] = {}

        for user in self.users:
            for key,props in user.prop.items():
                state["user_properties"][user.userName] = []
                for prop in props:
                    state["user_properties"][user.userName].append(prop.name)


        state["user_property_levels"] = {}
        for user in self.users:
            state["user_property_levels"][user.userName] = []
            for key,props in user.prop.items():
                for prop in props:
                    state["user_property_levels"][user.userName].append(prop.current_level)
        
        state["current_turn"] = self.currUser.data.userName

        return state
    def prop_board(self):
        board = []
        for cell in self.board.property_cells:
            board.append(cell.props_for_board())
        user_locs = []
        for user in self.users:
            try:
                curr_loc = user.currLocation
                if(curr_loc):
                    user_locs.append(curr_loc.cell_number-1)
                else:
                    user_locs.append(0)
            except:
                user_locs.append(0) 
        return board, user_locs
    def startGame(self):

        while True:
            # is all players are ready
            if (self.status == Status.WAITING):
                print("Waiting the playrs to be ready")
                for user in self.users: #ask the unready users if they are ready
                    if(user.isReady == False):
                        temp = ("{} are you ready to game? Yes or No".format(user.userName))
                        usersAnswer =  callbackCaller(user,temp,user.callback_inp)
                        if(usersAnswer.lower()== "yes"):
                            self.ready(user)
                        
                if(self.users.__len__()==0):
                    break

                isAllReady = True
                if(self.users == None or self.users.__len__() <2): #if there is no user in game wait
                    isAllReady = False
                for player in self.users: #if only one player is not ready wait
                    if(not player.isReady):
                        isAllReady = False
                if(isAllReady): #if all the users are ready start the game
                    # print("Game is starting")
                    for user in self.users: #assign start positions for users
                        user.currLocation = self.board.head
                        
                    self.currUser = self.users.head

                    self.status = Status.RUNNING

            # is board loaded
            elif (self.status == Status.CREATED):
                if(self.board):
                    temp = ("Board initilized game switch to waiting status")
                    #self.notify_all(temp)
                    
                    self.status = Status.WAITING #if board is ready go to wait phase


            # game is running
            elif (self.status == Status.RUNNING):
                print()
                temp = self.currUser.data.turnComeToYou(callbackforUserTurn)
                #self.notify_all(temp)

                # temp = self.getboardstate()
                # self.notify_all(temp)
                
                curr_cell = self.currUser.data.currLocation.cell_number
                new_cell = self.currUser.data.currLocation.cell_number
                isRollDice = False
                if (isinstance(self.currUser.data.currLocation, Cells.TeleportCell)): #user is on the teleport cell
                    if(self.currUser.data.not_money_to_teleport):
                        dice1, dice2 = roll_dice()
                        total = dice1+ dice2
                        isRollDice =True
                        new_cell =  self.currUser.data.currLocation.cell_number
                        temp = ("Dice 1 is: {} and dice 2 is: {}".format(dice1, dice2))
                        #self.notify_all(temp)
                        for i in range (total):  # self.currUser.currLocation update
                            self.currUser.data.currLocation = self.currUser.data.currLocation.next
                        self.currUser.data.not_money_to_teleport = False
                    else:
                        command = Actions.TELEPORT
                elif(not self.currUser.data.isInJail): #user is not in jail roll and go
                    if(not self.currUser.data.escapebyDoubleDice): #if user bail out
                        dice1, dice2 = roll_dice()
                        total = dice1+ dice2
                        isRollDice =True
                        new_cell =  self.currUser.data.currLocation.cell_number
                        temp = ("Dice 1 is: {} and dice 2 is: {}".format(dice1, dice2))
                        #self.notify_all(temp)
                        for i in range (total):  # self.currUser.currLocation update

                            self.currUser.data.currLocation = self.currUser.data.currLocation.next
                    else: 
                        self.currUser.data.escapebyDoubleDice = False
                    temp = ("{},is on the ".format(self.currUser.data.userName))
                    temp += str(self.currUser.data.currLocation)
                    #self.notify_all(temp)

                else: #user is in jail select given oppertunities to bail out
                    isRollDice = False
                    if(self.currUser.data.isJailFree()): #if jail turn is finished
                        command = Actions.BAIL_OUT
                    else: #if still in jail
                        self.currUser.data.jailTurn()
                        command = Actions.ROLL_DICE
                temp = self.getboardstate()
                self.notify_all(temp)
                time.sleep(2)
                if(isRollDice): #if user is rolled dice
                    if(not isinstance(self.currUser.data.currLocation, Cells.StartCell)): #if user is not on start check if he/she passed from start point
                        if(new_cell<curr_cell):
                            Cells.StartCell.action(self.currUser.data, self.board, Actions.ROLL_DICE)

                    if (isinstance(self.currUser.data.currLocation, Cells.TeleportCell)): #if user came teleport cell pass the turn and set curr user
                        self.currUser = self.currUser.next

                        continue
                    elif (isinstance(self.currUser.data.currLocation, Cells.GoToJailCell)): #if user came to go to the jail cell sent user to jail
                        self.currUser.data.gototheJail()
                        command = Actions.ROLL_DICE
                    elif (isinstance(self.currUser.data.currLocation, Cells.JailCell)): # if user came jail cell pass turn
                        command = Actions.ROLL_DICE

                    elif (isinstance(self.currUser.data.currLocation, Cells.PropertyCell)): #if property cell
                        
                        if (self.currUser.data.currLocation.owner == None): #if property do not have owner buy option
                            temp = ("Do you want to buy {} ? Yes or No".format(self.currUser.data.currLocation.name))
                            usersAnswer = callbackCaller(self.currUser.data,temp+'2',user.callback_print)
                            usersAnswer = callbackCaller(self.currUser.data,temp,user.callback_inp)
                            
                            if (usersAnswer.lower() == "yes"):
                                command = Actions.BUY_PROPERTY
                            else:
                                command = Actions.ROLL_DICE
                        elif(self.currUser.data.currLocation.owner.userName == self.currUser.data.userName): #if property's owner is curruserupgrade option
                            temp = ("Do you want to upgrade {}? Yes or No".format(self.currUser.data.currLocation.name))
                            usersAnswer = callbackCaller(self.currUser.data,temp+'2',user.callback_print)
                            usersAnswer =  callbackCaller(self.currUser.data,temp,user.callback_inp)
                            if (usersAnswer.lower()=="yes"):
                                command = Actions.UPGRADE_PROPERTY
                            else:
                                command = Actions.ROLL_DICE
                        else:
                            command = Actions.RENT
                    else: #if owner of property is another user pay rent
                        command = Actions.ROLL_DICE

                # turn function  will return 2 bools that state if the user is alive or not and the current users turn is over or not
                isEliminate,turnFinished = self.turn(self.currUser.data, command)
                if (isEliminate): #if user is elemineted detach user from board
                    temp = ("{}'s balance is finished".format(self.currUser.data.userName))
                    #self.notify_all(temp)
                    deletedUser = self.currUser
                    self.currUser = self.currUser.next
                    self.detach(deletedUser)
                    

                # check if the game is over or not
                if(self.users.__len__() == 1): # Last player is standing game is over
                    self.status = Status.FINISHED
                else: #continue
                    if(turnFinished): #if user is not teleported his/hir turn is finished
                        if( not isEliminate):

                            self.currUser = self.currUser.next

                    else:  #if user is teleported check if user wants to buy property and next step he/her continue

                        print("geldi")
                        if (isinstance(self.currUser.data.currLocation, Cells.PropertyCell)):
                            if (self.currUser.data.currLocation.owner == None):
                                temp = ("Do you want to buy {}? Yes or No".format(self.currUser.data.currLocation.name))
                                callbackCaller(self.currUser.data,temp+'2',user.callback_print)
                                usersAnswer =  callbackCaller(self.currUser.data,temp+'2',user.callback_inp)
                                if (usersAnswer.lower() == "yes"):
                                    command = Actions.BUY_PROPERTY
                            elif (self.currUser.data.currLocation.owner.userName == self.currUser.data.userName):
                                temp = ("Do you want to upgrade {}? Yes or No".format(self.currUser.data.currLocation.name))
                                callbackCaller(self.currUser.data,temp+'2',user.callback_print)
                                usersAnswer =  callbackCaller(self.currUser.data,temp+'2',user.callback_inp)
                                if (usersAnswer.lower() == "yes"):
                                    command = Actions.UPGRADE_PROPERTY
                        
                            isEliminate, turnFinished = self.turn(self.currUser.data, command)

            elif (self.status == Status.FINISHED): #if last player standing finished the game and clear the board(by deleting last player).
                temp = ("Game is over. User with username: {} is the winner".format(self.currUser.data.userName))
                self.notify_all(temp)
                self.detach(self.currUser)
                
                for user in self.spectator:
                    self.detach(user)

                self.users.head = None
                self.resetgame()
                return



