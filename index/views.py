from django.shortcuts import render,redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from userTable import *
from django.views.decorators.csrf import csrf_exempt
from phase2 import *
from socket import *
import json
from index.map_creator import * 

from threading import *
from django.contrib import messages

color_map = {'brown':'#641e16',
         'light-blue':'#85c1e9',
         'pink':'#ff56d1',
         'orange': '#ef5921',
         'red': '#ff0000',
         'yellow': '#fcallback_print7ff00',
         'green': '#23ff00',
         'dark-blue': '#000478',
         }

#variable for socket connection port
a = 1447
game_over = False
board_prop = []
positions = []
user_names = []
user_balances =  []
user_props =  {}
userprop_levels =  {}
curr_turn =  []
msg = ""
mutex = Lock()
input_available = Condition(lock=mutex)
data_available = Condition(lock=mutex)

input_msg = ""
is_in_board = False
#create and connect global socket
sock = socket(AF_INET, SOCK_STREAM)
sock.connect(('localhost', a))
#check authantication
def authenticate(username, password):
    is_auth = login(username,password)

    return True if is_auth else False

#views getten redirect attığında token yazdırır urlde.
def go_back_view(request):
    if request.method == 'POST':
        return redirect('dashboard')
    else:
        pass
def create_game_view(request):
    global sock
    if request.method == 'POST':
        game_name = request.POST.get('gameName')
        joinable_users = request.POST.get('users')
        share_status = request.POST.get('share_status')

        city_names = []
        city_colors = []
        city_prices = []

        # users gives as a [price1,price2,price3,price4,price5], use eval to convert it to list.
        city_level_prices = []

        # WE have 26 cities in the game, so we need to get all the cities from the form.
        for i in range(1,27):
            city_names.append(request.POST.get(f'cityName{i}', ''))
            city_colors.append(request.POST.get(f'cityColor{i}', ''))
            city_prices.append(int(request.POST.get(f'cityBuyPrice{i}', 0)))
            city_level_prices.append(eval(request.POST.get(f'cityLevelPrices{i}', 0)))

        # Create a map with the given parameters.
        basic_map = creator(game_name, city_names,city_colors,city_prices,city_level_prices)
        data = json.dumps(basic_map)

        msg = f'new game {game_name} {share_status} {joinable_users} '.format(game_name=game_name, share_status=share_status, joinable_users=joinable_users)
        
        msg += data
        
        sock.send(msg.encode())
        
        msg = sock.recv(1024).decode()
        
        if msg == "Created":
            
            messages.success(request, 'Game created successfully.')
        else:
            messages.error(request, 'Game could not be created.')
        
        return redirect('dashboard')
            
        
        #template = loader.get_template('dashboard.html')
        #return HttpResponse(template.render({{'show_popup': show_popup}}, request))

    if request.method == 'GET':
        if request.session.get('username') is None:
            return redirect('login')
    
        template = loader.get_template('new_game.html')
        return HttpResponse(template.render({'city_size':[i + 1 for i in range(26)],'auth': True if request.session['username'] else False}, request))
  
  
def logout_view(request):
    request.session.flush()
    return JsonResponse({'message': 'Logged out successfully'})

  
@csrf_exempt
def register_view(request):
    
    # Change this view authenticate the user to the server.
    
    message = ""
    global sock
    if request.method == 'POST':
        username = request.POST.get('username')
        name = request.POST.get('name')
        email = request.POST.get('email')
        
        password1 = request.POST.get('password1')
        password2 =  request.POST.get('password2')
        
        # Create socket content to send to the server.
        
        
        
        if password1 == password2:
            msg = f"register {username} {email} {name} {password1} {password2}".format(username,email,name,password1)
            sock.send(msg.encode())
            data = sock.recv(1024).decode()
            
            if data == "registered":
                return redirect('login')
            else:
                # redirtct to register page with error message,
                # username or email is already taken.
                context = {
                    'message': message
                }
                
                template = loader.get_template('register.html')
                return render(request, 'register.html', context)
        
        else:
            # passwords does not match. 
            message = "Passwords does not match."
            
            
    context = {
        'message': message
    }
    template = loader.get_template('register.html')
    return render(request, 'register.html', context)



def json_board_state(request):
    global sock
    global color_map
    global board_prop
    global positions

    global user_names
    global user_balances 
    global user_props 
    global userprop_levels 
    global curr_turn 
    global msg
    global input_msg
    global input_available
    global mutex
    
    
    
    curr_user_from_server = request.session.get('username')
    names = []
    color = []
    price = []
    for prop in board_prop:
        names.append(prop[0])
        price.append(str(prop[1])+'M')
        prop_color = color_map[prop[2]] 
        color.append(prop_color)
    context = {
        'names': names,
        'color': color,
        'price': price,
        'locations': positions,
        'user_names': user_names,
        'user_balances': user_balances,
        'user_props': user_props,
        'userprop_levels': userprop_levels,
        'curr_turn': curr_turn,
        'curr_user_server': curr_user_from_server,
        'msg': msg
    }    
    return JsonResponse(context)


def listen():
    global input_available
    global sock
    global color_map
    global board_prop
    global positions

    global user_names
    global user_balances 
    global user_props 
    global userprop_levels 
    global curr_turn 
    global msg
    global input_msg
    global mutex
    global game_over
    global data_available
    while True:
        
        data = sock.recv(16380)
        server_response = data.decode()

        
        splited = server_response.split("*")
        if(len(splited) == 2):
            try:

                server_response = splited[1][1:]
                whole_input = eval(server_response)

                positions = whole_input["user_locations"]
                user_names = whole_input["user_names"]
                user_balances =  whole_input["user_balances"]
                user_props =  whole_input["user_properties"]
                userprop_levels =  whole_input["user_property_levels"]
                curr_turn =  whole_input["current_turn"]
                
            except:
                msg = server_response[:-2]
                if(msg != ''):
                    if(server_response[-2]=='2'):

                        mutex.acquire()
                        while input_msg == "":
                            input_available.wait()
                        mutex.release()

                        sock.send(input_msg.encode())
                        input_msg = ""
                else:
                    game_over =True
                    break
        else:
            for data in splited:
                try:
                    server_response =data[1:]
                    server_response =server_response[:-1]
                    whole_input = eval(server_response)

                    positions = whole_input["user_locations"]
                    user_names = whole_input["user_names"]
                    user_balances =  whole_input["user_balances"]
                    user_props =  whole_input["user_properties"]
                    userprop_levels =  whole_input["user_property_levels"]
                    curr_turn =  whole_input["current_turn"] 
                   
                except:
                    server_response = data[1:]
            
                    server_response =server_response[:-1]
                    msg = server_response[:-2]
                    if(msg != ''):
                        if(server_response[-2]=='2'):

                            mutex.acquire()
                            while input_msg == "":
                                input_available.wait()
                            mutex.release()

                            sock.send(input_msg.encode())
                            input_msg = ""
                    else:
                        game_over =True
                        break
       

def ready_player_view(request):
    global sock
    global board_prop
    global is_in_board
    global color_map
    global positions
    global board_prop

    global user_names
    global user_balances 
    global user_props 
    global userprop_levels 
    global curr_turn 
    if request.method == 'POST':
        if(is_in_board):
            return redirect('/board')
        # if request.session.get('username') is None:
        #     return redirect('login')
            
        button_id = request.POST.get('id')
        if(button_id == '99999'):
            command = 'yes'
            sock.send(command.encode())
            names = []
            color = []
            price = []
            for prop in board_prop:
                names.append(prop[0])
                price.append(str(prop[1])+'M')
                prop_color = color_map[prop[2]] 
                color.append(prop_color)
            curr_user_from_server = request.session.get('username')

            context = {
            'names': names,
            'color': color,
            'price': price,
            'locations': positions,
            'user_names': [],
            'user_balances': [],
            'user_props': [],
            'userprop_levels': [],
            'curr_turn': "curr_turn",
            'curr_user_server': curr_user_from_server,
            'msg': msg
        }
            is_in_board = True
            template = loader.get_template('board.html')
            

            return (HttpResponse(template.render({'context':context}, request)))
        else:
            
            command = 'join '+ button_id
            sock.send(command.encode())
            data = sock.recv(1024)
            server_response = data.decode()
            whole_input = eval(server_response)
            board_prop = whole_input[0]
            positions = whole_input[1]
            listen_thread = Thread(target=listen,)
            listen_thread.start()
           
            template = loader.get_template('ready.html')
            return HttpResponse(template.render({}, request))
    if request.method == 'GET':
        # if request.session.get('username') is None:
        #     return redirect('login')
    
        template = loader.get_template('ready.html')
        return HttpResponse(template.render({}, request))
    
def board_view(request):
    global sock
    global color_map
    global board_prop
    global positions

    global user_names
    global user_balances 
    global user_props 
    global userprop_levels 
    global curr_turn 
    global msg
    global input_msg
    global input_available
    global mutex
    if request.method == 'POST':
        

        mutex.acquire()
        input_msg = request.POST.get('user-input')
        input_available.notify()
        mutex.release()

        return redirect('/board')
    
        # if request.session.get('username') is None:
        #     return redirect('login')
     

        # names = []
        # color = []
        # price = []
        # curr_user_from_server = request.session.get('username')
        # for prop in board_prop:
        #     names.append(prop[0])
        #     price.append(str(prop[1])+'M')
        #     prop_color = color_map[prop[2]] 
        #     color.append(prop_color)

        # context = {
        #     'names': names,
        #     'color': color,
        #     'price': price,
        #     'locations': positions,
        #     'user_names': user_names,
        #     'user_balances': user_balances,
        #     'user_props': user_props,
        #     'userprop_levels': userprop_levels,
        #     'curr_turn': curr_turn,
        #     'curr_user_server': curr_user_from_server,
        #     'msg': msg
        # }
        
        
        
        
        # template = loader.get_template('board.html')
        
        # return HttpResponse(template.render({'context':context}, request))
    elif request.method == 'GET':
        # if request.session.get('username') is None:
        #     return redirect('login')
        
       
        curr_user_from_server = request.session.get('username')
        names = []
        color = []
        price = []
        for prop in board_prop:
            names.append(prop[0])
            price.append(str(prop[1])+'M')
            prop_color = color_map[prop[2]] 
            color.append(prop_color)
        context = {
            'names': names,
            'color': color,
            'price': price,
            'locations': positions,
            'user_names': user_names,
            'user_balances': user_balances,
            'user_props': user_props,
            'userprop_levels': userprop_levels,
            'curr_turn': curr_turn,
            'curr_user_server': curr_user_from_server,
            'msg': msg
        }
        template = loader.get_template('board.html')
        return HttpResponse(template.render({'context':context}, request))

def list_games_view(request):
    global sock
    if request.method == 'GET':
        sock.send("list".encode())
        data = sock.recv(1024)
        server_response = data.decode()
        game_list = eval(server_response)

    
        template = loader.get_template('game_list.html')
        return HttpResponse(template.render({'games':game_list}, request,))

def dashboard_view(request):

    global sock
    if request.method == 'POST':
        if request.session.get('username') is None:
            return redirect('login')

        return redirect('create-game')

    
    if request.method == 'GET':
        if request.session.get('username') is None:
            return redirect('login')
    
        template = loader.get_template('dashboard.html')
        return HttpResponse(template.render({}, request))

@csrf_exempt
def login_view(request):

    global sock
    
    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')


        msg = "login " + username + " " + password
        msg = msg.encode()
        # Send username and password to server        
        sock.send(msg)

        # Receive response from server
        response = sock.recv(1024)
        response = response.decode()
        
        
        if response == "null":
            sock.close()

            sock = socket(AF_INET, SOCK_STREAM)
            sock.connect(('localhost', a))
            return redirect('login')
        else:
            request.session['username'] = username
            token = username
            
            response = redirect('dashboard')
            response.set_cookie('username',username)


            return response
    if request.method == 'GET':
        username = request.session.get('username')
        if username is not None:
            msg = "login " + username 

            sock.send(msg.encode())
            return redirect('dashboard')
        
        else:
            template = loader.get_template('login.html')
            return HttpResponse(template.render({}, request))