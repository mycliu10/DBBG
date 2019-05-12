import gnubg as bg
import numpy as np

class Player:
    def __init__(self):
        return

    def reset(self):
        bg.command("new match")
        bg.command("set automatic game on") # Auto play
        bg.command("set jacoby off") # I don't know, I just turned it off anyway...
        bg.command("set crawford off") # I don't know, I just turned it off anyway...
        bg.command("set automatic crawford off")
        bg.command("set automatic roll off")
        bg.command("set automatic move off")
        bg.command("set matchlength 0")

        bg.command("set cube use on")
        bg.command("set player 0 name O")
        bg.command("set player 1 name X")
        bg.command("new game")
        self._move_count = 0
        self._cube_owner = bg.cubeinfo()['cubeowner']

    def step(self, action):
        cube_info = bg.cubeinfo()
        cube_owner = cube_info['cubeowner']
        bg.command("swap players")
        bg.command("play")
        bg.command("swap players")
        bg.command("play")
        game_info = bg.match(0,1,0,0)['games'][0]['info']
        winner = game_info['winner']
        print(game_info)
#

def PlayGame(board, num_games=1):
    bg.command("set automatic game on") # Auto play
    bg.command("set jacoby off") # I don't know, I just turned it off anyway...
    bg.command("set crawford off") # I don't know, I just turned it off anyway...
    bg.command("set automatic crawford off")
    bg.command("set automatic roll off")
    bg.command("set automatic move off")
    bg.command("set matchlength 0")

    bg.command("set cube use on")
    bg.command("new match")
    bg.command("set player 0 name O")
    bg.command("set player 1 name X")

    command_set_board = "set board simple " + ' '.join(str(x) for x in board)
    for count in range(num_games):
        bg.command("new game")
#        bg.command(command_set_board)
#        print("BOARD IS SET!!!")        
#        board = bg.board()
#        simple_board = BoardPositionToSimple(board)
#        print(board)
#        print(simple_board)
        
        winner = None
        while winner is None:
            cube_info = bg.cubeinfo()
            cube_owner = cube_info['cubeowner']
#            whosmove = cube_info['move']
            bg.command("swap players")
            bg.command("play")
            bg.command("swap players")
            bg.command("play")
            game_info = bg.match(0,1,0,0)['games'][0]['info']
            winner = game_info['winner']
            print(game_info)
#            raw_input("Press Enter to continue...")
#        bg.command("end game")

#    bg.command("end match")
    match_info = bg.match(0,1,0,0)['games']
    
    
    for game_info in match_info:
        print(game_info['info'])
        winner = game_info['info']['winner']
        if winner is None:
            points_won = 0
        elif winner=='X':
            points_won = -game_info['info']['points-won']
        elif winner=='O':
            points_won = game_info['info']['points-won']
        else:
            raise KeyError("NO INFO!")
        print(winner, points_won)

def BoardPositionToSimple(board):
    p1, p2 = board
    p1 = np.array(p1) 
    p2 = np.array(p2)
    simple = np.zeros(26, dtype=np.int)
    simple[0] = p2[-1]
    simple[1:25] = p2[0:-1]
    simple[1:25] -= p1[:-1][::-1]
    simple[25] = p1[-1]
    return tuple(simple)


PlayGame((1, 0, 0, 1, 2, 0, 5, 0, 2, 0, -1, 0, -3, 3, 0, 0, 0, -2, -2, -5, 0, 1, -2, 0, 0, 0), num_games=1)
