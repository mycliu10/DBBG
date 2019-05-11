import gnubg as bg
import numpy as np


def PlayGame(board, num_games=8):
    command_set_board = "set board simple " + ' '.join(str(x) for x in board)
    for count in range(num_games):
        bg.command("new game")
        gnubg.command('set automatic game off')
        bg.command(command_set_board)
        print("BOARD IS SET!!!")        
        board = bg.board()
#        simple_board = BoardPositionToSimple(board)
#        print(board)
#        print(simple_board)

        bg.command("end game")

#    bg.command("end match")
    match_info = bg.match(0,1,0,0)['games']
    
    
    for game_info in match_info:
        print(game_info['info'])
        winner = game_info['info']['winner']
        if winner is None:
            points_won = 0
        elif winner=='X':
            points_won = game_info['info']['points-won']
        elif winner=='O':
            points_won = - game_info['info']['points-won']
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


PlayGame((1, 0, 0, 1, 2, 0, 5, 0, 2, 0, -1, 0, -3, 3, 0, 0, 0, -2, -2, -5, 0, 1, -2, 0, 0, 0), num_games=4)