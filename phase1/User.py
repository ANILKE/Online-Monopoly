import hashlib
import json
def print_callback():
    def callback_printer(usr,data):
        response = json.dumps("*")
        response += json.dumps(data)
        response = response.encode()
        print(response)
        print("asdasdasdasdasd")
        usr.sock.send(response)

    return  callback_printer 
def get_callback():
    def callback_getter(usr,data):
        # response = data + '2'
        # response = response.encode()
        # usr.sock.send(response)
        
        byte_data = usr.sock.recv(16300)
        inp = byte_data.decode()
        
        return inp
    return callback_getter  
# def callback_getter(usr,str):
# inp = input(str+"\n")
# return inp
class User:
    #Constructor for user class
    def __init__(self, uname,mail, fname, passwd, balance ,sock=None, locate = None ):
        self.userName = uname
        self.email = mail
        self.fullName = fname
        self.password =  hashlib.sha256(passwd.encode()).hexdigest()
        self.sock = sock
        self.not_money_to_teleport = False
        self.callback_inp = None
        self.callback_print = None


        
        self.currLocation = locate
        self.balance = balance
        self.prop = {}
        self.isInJail = False # if user is in jail true
        self.jailTime = -1 # time passed in jail
        self.isReady = False # check if the user is ready for the game
        self.jailFreeCardCount = 0 # stors escape from jail chance card count of user
        self.escapebyDoubleDice = False #if user is bail out by rolling a double dice
        
        
        
    def __str__(self):
        string = ""
        string += "Username: " + self.userName + "\n"
        string += "Email: " + self.email + "\n"
        string += "fullName: " + str(self.fullName) + "\n"
        string += "password: " + self.password + "\n"
        string += "isInJail: " + str(self.isInJail) + "\n"
        string += "jailFreeCardCount : " + str(self.jailFreeCardCount) + "\n"

        return string
   

        
    # Get Operations on Attributes Starts Here.
    
    def getUserName(self):
        return self.userName

    def getUserToken(self):
        return self.token

    def getUserProp(self):
        return self.prop

    def getUserBalance(self):
        return self.balance

    def getUserLocation(self):
        return self.currLocation
    
    # Get Operations on Attributes Ends Here.


    
    


    # Property Rent Operations Starts Here.
    
    def pay_rent(self,user,rent):
        self.balance -= rent
        user.balance += rent
    
     # Property Rent Operations Ends Here.
    
    
    
    def get_property_count(self):
        count = 0
        
        for key,val in self.prop.items():
            count += len(val)
            
        return count
    
    def isJailFree(self):
        if (self.jailTime == 3 or self.jailTime == -1):
            return True
        else:
            return False

    def getuserstate(self):
        uName = self.userName
        userMoney = self.balance
        properties = ""  # takes all properties that are owned by user owned
        for key, val in self.prop.items:
            for item in val:
                properties += item.name()
                properties += ","
        properties = properties[0:(len(properties) - 1)]  # to delete the unneccessary comma
        print("Username: {}, Balance: {}, Properties: {}".format(uName, userMoney, properties))

    #General Update operations for class attributes

    def gototheJail(self): #set user jail status and turn info
        self.isInJail = True
        self.jailTime = 0
    def jailTurn(self): # increase time passed in jail 
        self.jailTime +=1
    def getOutJail(self): # Bail out the user
        self.jailTime = -1
        self.isInJail = False
    def updateUserName(self,uname):
        self.userName = uname

    def updateCurrLocation(self,location):
        self.currLocation = location

    def updateToken(self,toke):
        self.token = toke

    #Property CRUD operations
    def addProp(self,property): #add prop cel to users property set
        if(property.color in self.prop.keys()):
            self.prop[property.color].append(property)
        else:
            self.prop[property.color] = []
            self.prop[property.color].append(property)

    def upgradeProperty(self,key,prop): 
        index = self.prop[key].index(prop)
        self.prop[key][index].level += 1


    def downgradeProperty(self,key,prop):
        index = self.prop[key].index(prop)
        self.prop[key][index].level -= 1

    def deleteProperty(self,key,prop): #delete property from user prop set
        self.prop[key].remove(prop)
    def turnComeToYou(self,callback):
        return callback(self.userName)
    

    #Destructer
    def __del__(self):
        print("Destructer called")

    #Check whether password for user is true.
    def auth(self, plainpass):
        return

    #Start a session for the user, return a random token to be used during the session
    def login(self):
        return

    #Check if the token is valid, returned by the last login
    def checksession(token):
        return

    #End the session invalidating the token
    def logout(self):
        return