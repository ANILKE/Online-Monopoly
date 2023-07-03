# Online-monopoly
CEng445 Term Project
Kemal Anil Kekevi 2380608
Emin Sak 2380830
Phase1:

    Game Engin is running the game and stores board as , users as circular linked list. 
    User file includes user attributes and basic crud funtions.
    Grid file includes cells of the board and given fixed values like tax value or star money...
    Cell file has an abstruct cllas for cells on the board and specifies the cells by their action methodes
    Chance card file has an abstruct cllas for card and specifies the cards by their action methodes
    Demo file is a basic demo of the game to run it in powershell.
    Grid creator file creates grrid.
    Enums stores all enums for actions and game.

Phase2:
    userTable.py file creates the users.db which includes users table to and use login function to authantications by using sqlite3
    phase2_demo.py file starts the server thread to call it "python3 phase2_demo.py --port 1432"
    phase2_demo_client.py file starts one user thread to call it "python3 phase2_demo_client.py --port 1432"
    gameInstance.py file includes an class derived from Thread to create board thread.
    MonopolyClient.py file creates the socket that cominicate with MonopolyServer.
    MonopolyServer.py:
        read_socket_content receives the coming message and return the decoded message as string.
        game_str reads all ongoing games and create a string including game names and return a this string.
        game_starter thread is checking user counts tha atteched to boards and starts game engine game.
        game_status_checker thread checks the games and removes the finished games.
        question_slave thread listens the users and give the corresponding respons to client thread.
        MonopolyServer includes and controls the threads.


