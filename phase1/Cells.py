""""

Impementation of the Cell class in a monopoly game.


AbstractCell: Abstract class for a cell in a monopoly game.

PropertyCell: Class for a property cell in a monopoly game.
TaxCell: Class for a tax cell in a monopoly game.
TeleportCell: Class for a teleport cell in a monopoly game.
JailCell: Class for a jail cell in a monopoly game.
GoToJailCell: Class for a go to jail cell in a monopoly game. Teleports the player to the jail cell.
StartCell: Class for a start cell in a monopoly game.
ChanceCell: Class for a chance cell in a monopoly game. Note that it is an abstract class.

UpgradeChanceCell: Class for a chance cell that upgrades a property.
DowngradeChanceCell: Class for a chance cell that downgrades a property.



Every cell has to implement action method which takes 3 arguments, user, board and action.
action argument is just a Python Enum class, to gain more info tou can look at the Enums.py
Cells takes action according to passed action enum.





"""
from abc import ABC, abstractmethod
from phase1.Enums import Actions,CellTypes
from phase1.User import User
import phase1.ChanceCards as ChanceCards

import random

def callbackCaller(usr,str,callback):
    return callback(usr,str)


class AbstractCell():
    def __init__(self, next, prev,cell_no):
        self.next = next
        self.prev = prev
        self.cell_number = cell_no

    @abstractmethod
    def action(self, user,board,action):
        pass

class PropertyCell(AbstractCell):
    def __init__(self, next, prev,cell_no, name, price, color, rents):
        super().__init__(next, prev,cell_no)
        self.name = name
        self.price = price
        self.color = color
        self.rents = rents
        self.owner = None
        self.current_level = 1
        self.type = CellTypes.PROPERTY
        
        
        

    def set_owner(self, user):
        self.owner = user

    def upgrade_level(self):
        self.current_level += 1

    def downgrade_level(self):
        self.current_level -= 1
    def props_for_board(self):
        return (self.name,self.price,self.color)
    def __str__(self):
        string = ""
        string += "Name: " + self.name + "\n"
        string += "Current level: " + str(self.current_level) + "\n"
        string += "Price: " + str(self.price) + "\n"
        string += "Color: " + self.color + "\n"
        string += "Owner: " + (str(self.owner) if self.owner != None else "None") + "\n"
        string += "Current Rent: " + str(self.rents[self.current_level - 1]) + "\n"

        return string

    def action(self,user:User,board,action):

        if action.value == 1:
            
            if self.price <= user.getUserBalance():
                self.owner = user
                user.addProp(self)
                user.balance -= self.price
                temp = ('{username} have just purchased the {cell_name}'.format(username=user.userName,cell_name=self.name))
                callbackCaller(user,temp+'1',user.callback_print)
            else:
                temp = ('{username} has not enough credit.'.format(username=user.userName))
                callbackCaller(user,temp+'1',user.callback_print)
                
        elif action.value == 2:
            if self.owner == user:
                if self.current_level < 5 and board.upgrade_cost <= user.balance:
                    user.balance -= board.upgrade_cost
                    self.upgrade_level()
                    temp = ('{username} has upgraded the {name} to the  level {level}'.format(username=user.userName,name=self.name,level=self.current_level))
                    callbackCaller(user,temp+'1',user.callback_print)
                elif self.current_level < 5 and board.upgrade_cost > user.balance:
                    temp = ('{username} has not enough money to upgrade {property}'.format(username=user.userName,property=self.name))
                    callbackCaller(user,temp+'1',user.callback_print)
                elif self.current_level >= 5:
                    temp = ('{name} property is maximum level. You can not upgrade it.'.format(name=self.name))
                    callbackCaller(user,temp+'1',user.callback_print)
            else:
                print('{username} has not the property. Passed!'.format(user.userName))
                    
        elif action.value == 7 and self.owner != user:
            rent = self.rents[self.current_level - 1]
            if not self.owner.isInJail:
                # Owner is in the jail, no exchange.
                if user.getUserBalance() < rent:
                    # User Must be eliminated due to lack of money.
                    temp = ("Cannot pay rent balance is not enought.")
                    callbackCaller(user,temp+'1',user.callback_print)
                    return True,True
                else:
                    user.pay_rent(self.owner, rent)
                    temp = ("{user_1} pays {rent} to {user_2}".format(user_1 = user.userName, rent = rent, user_2= self.owner.userName))
                    callbackCaller(user,temp+'1',user.callback_print)
            else:
                temp = ('{user} is in the jail so {other_user} do not pay the rent.'.format(user=self.owner.userName,other_user=user.userName))
                callbackCaller(user,temp+'1',user.callback_print)
        return False,True
    
class TaxCell(AbstractCell):
    def __init__(self, next, prev,cell_no):
        super().__init__(next, prev,cell_no)
        self.type = CellTypes.TAX
        
    def __str__(self):
        return "Tax Cell with amount " 

    def action(self,user:User,board,action): 

        amount = user.get_property_count() * board.tax
        
        
        if user.balance < amount:
            temp = ('{username} has not enough money.'.format(username=user.userName))
            callbackCaller(user,temp+'1',user.callback_print)
            return True,True
        
        user.balance -= amount
        
        
        temp = ('{username} is at the tax cell, {amount_f} is taken from the account.'.format(username=user.userName,amount_f=amount))
        callbackCaller(user,temp+'1',user.callback_print)
        #callbackCaller(user,temp,user.callback_print)
        
        return False,True


class TeleportCell(AbstractCell):
    def __init__(self, next, prev,cell_no):
        super().__init__(next, prev,cell_no)
        self.type = TeleportCell
        self.type = CellTypes.TELEPORT
    def __str__(self):
        return "Teleport Cell."

    def action(self,user:User,board,action):   
        if board.teleport_cost <= user.balance:
            property_cells = board.teleporting_cells(user)
            temp = ('{username}, welcome. Where do you want to teleport. Please select the number and press the enter.'.format(username = user.userName))
            #callbackCaller(user,temp,user.callback_print)
            incr = 1
            for property in property_cells:
                string = '{number}. {property_name}'.format(number=incr,property_name=property.name)
                incr += 1
                temp += (string)
                #callbackCaller(user,temp,user.callback_print)
            callbackCaller(user,temp+'2',user.callback_print)
            index = int(callbackCaller(user,temp,user.callback_inp))
            temp = ""
            index -= 1
            
            property_to_go = property_cells[index]

            turn = False
            if property_to_go.cell_number < user.currLocation.cell_number:
                turn = True
            
            
            user.currLocation = property_to_go
            temp = ('{username} is successfully teleported.'.format(username=user.userName))
            callbackCaller(user,temp+'1',user.callback_print)
            
            
            if turn:
                temp = ('{username} is completed 1 turn. Payload per turn is added to balance'.format(username=user.userName))
                callbackCaller(user,temp+'1',user.callback_print)
                user.balance += board.turn_money
            
        else:
            temp = ('{username}, you have not enough money to teleport. Teleport cost is {cost}'.format(username=user.userName,cost=board.teleport_cost))
            callbackCaller(user,temp+'1',user.callback_print)
            user.not_money_to_teleport = True
            return False,True
        
        
        return False,False

class JailCell(AbstractCell):
    def __init__(self, next, prev,cell_no):
        super().__init__(next, prev,cell_no)
        self.type = CellTypes.JAIL
    def __str__(self):
        return "Jail Cell"

    def action(self,user:User,board,action):
        if(user.isInJail):
            if action.value == 5:
                user.getOutJail()
                return False,False
                
                
            else:
                temp = ('What do you want to choose?')
                #callbackCaller(user,temp,user.callback_print)
                
                temp += ('Do you want to roll a double dice, press 1 and enter.')
                #callbackCaller(user,temp,user.callback_print)
                temp +=('Do you want to pay the redemption, press 2 and enter.')
                #callbackCaller(user,temp,user.callback_print)
                temp += ('Do you have a jail out chance card, if so press 3 and enter. ')
                callbackCaller(user,temp+'2',user.callback_print)
                
                selection = int(callbackCaller(user,temp,user.callback_inp))


                if selection == 1:
                    die1 = random.randint(1, 6)
                    die2 = random.randint(1, 6)
                    total = die1 +die2
                    temp = ('(Dice 1: {dice_1}, Dice 2: {dice_2}).'.format(dice_1=die1,dice_2=die2))
                    #callbackCaller(user,temp,user.callback_print)

                    if die1 == die2:
                        temp += ("You are Free")
                        callbackCaller(user,temp+'1',user.callback_print)
                        user.escapebyDoubleDice = True
                        for i in range(total):
                            user.currLocation =user.currLocation.next
                        user.getOutJail()
                        return False,False
                    
                    callbackCaller(user,temp+'1',user.callback_print)
                    return False,True       
                elif selection == 2:
                    if user.balance < board.jailbailcost:
                        temp = ('You do not have enough money to bail out.')
                        callbackCaller(user,temp+'1',user.callback_print)
                        return False, True
                    
                    user.balance -= board.jailbailcost
                    user.getOutJail()
                    
                    return False,False
                elif selection == 3:
                    if user.jailFreeCardCount > 0:
                        temp = ('You can go out.')
                        #callbackCaller(user,temp,user.callback_print)
                        user.jailFreeCardCount -= 1
                        board.chanceCards.put(ChanceCards.JailFreeCard("Jail Free Card"))
                        temp += ('Current jail free card count is {count}'.format(user.jailFreeCardCount))
                        callbackCaller(user,temp+'1',user.callback_print)
                        user.getOutJail()
                        return False,False

                    temp += ('You do not have enough jail free card to bail out.')
                    callbackCaller(user,temp+'1',user.callback_print)
                    return False,True
        return False,True

class GoToJailCell(AbstractCell):
    def __init__(self, next, prev,cell_no):
        super().__init__(next, prev,cell_no)
        self.type = CellTypes.GOTOJAIL

    def __str__(self):
        return "Go to Jail Cell"

    def action(self,user:User,board,action):
        user.currLocation = board.jail
        user.gototheJail()
        return False,True
    
class StartCell(AbstractCell):
    def __init__(self, next, prev,cell_no):
        super().__init__(next, prev,cell_no)
        self.type = CellTypes.START
    def __str__(self):
        return "Start Cell"

    def action(self,user:User,board,action):
        temp = ('{username} has completed 1 turn. Turn credit added to the account of {username} \n'.format(username=user.userName))

        user.balance += board.startup_money
        temp +=('{username} has {amount} credit now.'.format(username=user.userName,amount=user.balance))
        callbackCaller(user,temp+'1',user.callback_print)
        return False,True
    
class ChanceCell(AbstractCell):
    def __init__(self, next, prev,cell_no):
        super().__init__(next, prev,cell_no)
        self.type = CellTypes.CHANCE
        
        
    def __str__(self):
        return "Chance Cell"

    @abstractmethod
    def action(self,user,board,action):
        changeCard = board.chanceCards.get()
        isEliminate,turnFinished =changeCard.action(user, board)
        if(not isinstance(changeCard, ChanceCards.JailFreeCard)):
            board.chanceCards.put(changeCard)
        return isEliminate,turnFinished
       