'''

    This file contains the impementation of the Card class.
    When a player picks a chance card, then actions is taken in the action overrided method.
'''

from abc import ABC, abstractmethod
def callbackCaller(usr,str,callback):
    return callback(usr,str)

class AbstractChanceCard(ABC):
    def __init__(self, text):
        self.text = text

    @abstractmethod
    def action(self, user, board):
        pass

    def __str__(self):
        return self.text


class UpgradePropertyCard(AbstractChanceCard):
    def __init__(self, text):
        super().__init__(text)

    def action(self, user, board):
        #ask user the property to upgrade
        temp = ('{username} pick upgrade property chance card'.format(username=user.userName))
        incr = 1
        temp += ("Which Property Do You Want to Upgrade?")
        #print all property cells name 
        for cell in board.property_cells:
            string = '{number}. {property_name}'.format(number=incr,property_name=cell.name)
            incr += 1
            temp += string + "\n"
        (callbackCaller(user,temp+'2',user.callback_print))

        index = int(callbackCaller(user,temp,user.callback_inp))
        index -= 1
        prop = board.property_cells[index]
        #if level is not max upgrade
        if(prop.current_level<5):
            prop.upgrade_level()
            temp = ("Property cells with name {name} is upgraded.".format(name=prop.name ))
            callbackCaller(user,temp+'1',user.callback_print)
        else:
            temp = ("Property cells with name {name}, cannot be upgraded because it is max level.".format(name=prop.name ))
            callbackCaller(user,temp+'1',user.callback_print)
        return False,True

class DowngradePropertyCard(AbstractChanceCard):
    def __init__(self, text):
        super().__init__(text)

    def action(self, user, board):
        #ask user the property to downgrade
        temp = ('{username} picks downgrade property chance card'.format(username=user.userName))
        # callbackCaller(user,temp,user.callback_print)
        incr = 1
        temp += ("Which Property Do You Want to Downgrade?")
        #print all props
        for cell in board.property_cells:
            string = '{number}. {property_name}'.format(number=incr,property_name=cell.name)
            incr += 1
            temp += string + "\n"
        (callbackCaller(user,temp+'2',user.callback_print))
        index = int(callbackCaller(user,temp,user.callback_inp))
        index -= 1
        prop = board.property_cells[index]
        #if selected prop is not min level downgrade
        if(prop.current_level > 1):
            prop.downgrade_level()
            temp = ("Property cells with name {name} is downgraded.".format(name=prop.name ))
            callbackCaller(user,temp+'1',user.callback_print)
        else:
            temp = ("Property cells with name {name}, cannot be downgraded because it is min level.".format(name=prop.name))
            callbackCaller(user,temp+'1',user.callback_print)
        return False,True

class ColorUpgradeCard(AbstractChanceCard):
    def __init__(self, text):
        super().__init__(text)

    def action(self, user, board):
        temp = ('{username} picks color upgrade chance card'.format(username=user.userName))
        # callbackCaller(user,temp,user.callback_print)
        keys = list(user.prop.keys())  #take colors from board
        #ask user color to upgrade all color props that user at least own one of them
        if(keys):
            temp += ("Which Color Do You Want to Upgrade?")
            incr = 1
            for key in keys:
                string = '{number}. {property_name}'.format(number=incr,property_name=key)
                incr += 1
                temp += string + "\n"
            (callbackCaller(user,temp+'2',user.callback_print))
            index = int(callbackCaller(user,temp,user.callback_inp))
            index -= 1
            selectedColor = keys[index]
            props = board.filter_property_by_color(selectedColor)
            #upgrade all prop levels of color if it is not max
            for prop in props:
                if(prop.current_level<5):
                    prop.upgrade_level()
            temp = ("Property cells with color {color}, are upgraded if it is not max level.".format(color=selectedColor))
            
            callbackCaller(user,temp+'1',user.callback_print)
        else:
            temp = ('{username} do not have any property cell. Turn is Passed!'.format(username=user.userName))
            callbackCaller(user,temp+'1',user.callback_print)
        return False,True

class ColorDowngradeCard(AbstractChanceCard):
    def __init__(self, text):
        super().__init__(text)

    def action(self, user, board):
        temp = ('{username} picks color downgrade chance card'.format(username=user.userName))
        # callbackCaller(user,temp,user.callback_print)
        keys = list(user.prop.keys()) #take colors from board
        #ask user color to upgrade all color props that user at least own one of them
        if(keys):
            temp += ("Which Color Do You Want to Downgrade?")
            
            incr = 1
            for key in keys:
                string = '{number}. {property_name}'.format(number=incr,property_name=key)
                incr += 1
                temp = ""
                temp += string + "\n"
            (callbackCaller(user,temp+'2',user.callback_print))
            index = int(callbackCaller(user,temp,user.callback_inp))
            index -= 1
            selectedColor = keys[index]
            props = board.filter_property_by_color(selectedColor)
             #downgrade all prop levels of color if it is not min
            for prop in props:
                if(prop.current_level>1):
                    prop.downgrade_level()
            temp = ("Property cells with color {color}, are downgrade if it is not min level.".format(color=selectedColor))
            callbackCaller(user,temp+'1',user.callback_print)
        else:
            temp = ('{username} do not have any property cell. Turn is Passed!'.format(username=user.userName))
            callbackCaller(user,temp+'1',user.callback_print)
        return False,True


class GotoJailCard(AbstractChanceCard):
    def __init__(self, text):
        super().__init__(text)

    def action(self, user, board):
        temp = ('{username} picks go to jail chance card. You are on the jail cell now.'.format(username=user.userName))
        callbackCaller(user,temp+'1',user.callback_print)
        #set users jail attributes and send to jail cell
        user.currLocation = board.jail
        user.gototheJail()
        return False,True


class JailFreeCard(AbstractChanceCard):
    def __init__(self, text):
        super().__init__(text)

    def action(self, user, board):
        #update jail free card count of user
        user.jailFreeCardCount += 1
        temp = ('{username} picks Jail Free chance card. You have {amount} jail free cards now.'.format(username=user.userName,amount = user.jailFreeCardCount))
        callbackCaller(user,temp+'1',user.callback_print)
        return False,True


class TeleportCard(AbstractChanceCard):
    def __init__(self, text):
        super().__init__(text)

    def action(self, user, board):
        #pick a property to go.
        temp = ('{username} picks teleport chance card.'.format(username=user.userName))
        #  callbackCaller(user,temp,user.callback_print)
        property_cells = board.teleporting_cells(user)
        temp += ('{username}, welcome. Where do you want to teleport. Please select the number and press the enter.'.format(username = user.userName))
        
        incr = 1
        #ask all props with no owner or curr users owned props.
        for property in property_cells:
            string = '{number}. {property_name}'.format(number=incr,property_name=property.name)
            incr += 1
            temp +=string + "\n"
        
        (callbackCaller(user,temp+'2',user.callback_print))
        index = int(callbackCaller(user,temp,user.callback_inp))
        index -= 1
        
        
        property_to_go = property_cells[index]
        
        turn = False
        #if user pass from start cell
        if property_to_go.cell_number < user.currLocation.cell_number:
            turn = True
                
                
        #set user location to this prop cell
        user.currLocation = property_to_go
        temp = ('{username} is successfully teleported.'.format(username=user.userName))
        callbackCaller(user,temp+'1',user.callback_print)
        #add balance if passed from start cell
        if turn:
            temp = ('{username} is completed 1 turn. Payload per turn is added to balance'.format(username=user.userName))
            callbackCaller(user,temp+'1',user.callback_print)
            user.balance += board.turn_money
            
        return False,False


class LotteryCard(AbstractChanceCard):
    def __init__(self, text):
        super().__init__(text)

    def action(self, user, board):
        #add balance to user
        amount = board.lottery
        temp = ('{username} picks lottery chance card, {amount_f} is added to the account.'.format(username=user.userName,amount_f=amount))
        callbackCaller(user,temp+'1',user.callback_print)
        user.balance += amount
        return False,True


class TaxCard(AbstractChanceCard):
    def __init__(self, text):
        super().__init__(text)

    def action(self, user, board):
        #take all user props and multiply with tax amount and update user balance.
        amount = user.get_property_count() * board.tax
        if user.balance < amount:
            temp=('{username} has not enough money.'.format(username=user.userName))
            callbackCaller(user,temp+'1',user.callback_print)
            return True,True
        
        user.balance -= amount
        
        
        temp = ('{username} picks tax chance card, {amount_f} is taken from the account.'.format(username=user.userName,amount_f=amount))
        temp += ('{username} has {credit} credit now.'.format(username=user.userName,credit=user.balance))
        callbackCaller(user,temp+'1',user.callback_print)
        return False,True
