import gnubg as bg
np = bg
class Player:
    def __init__(self):

        return

    def reset(self):
        bg.command("new match")
        bg.command("set automatic game off") # Auto play
        bg.command("set jacoby off") # I don't know, I just turned it off anyway...
        bg.command("set crawford off") # I don't know, I just turned it off anyway...
        bg.command("set automatic crawford off")
        bg.command("set automatic roll off")
        bg.command("set automatic move off")
        bg.command("set matchlength 0")

        bg.command("set cube use off")
        bg.command("set player 0 name O")
        bg.command("set player 1 name X")
        bg.command("new game")
        bg.command("end game")

        game_info = bg.match(0,1,0,1)['games']
        print(len(game_info))
        game_info = game_info[0]
        self._moves = [move for move in game_info['game'] if move.get('board') and move['player']=='X']

        self._num_moves = len(self._moves)
        self._move_count = 0

        #for move in self._moves:
        #    print(move)
        observation = bg.positionfromid(self._moves[self._move_count]['board'])
        obs = observation[0] + observation[1]
        observation = obs
        return observation
        
    def step(self, action):
        move = self._moves[self._move_count]
        bg.command("new match")
        bg.command("set cube use on")
        bg.command("new game")
        bg.command("set board " + move['board'])
        bg.command("set turn " +  move['player'])
                
        if action==1:
            bg.command("double")
        bg.command("end game")
        
        game_info = bg.match(0,1,0,0)['games'][0]['info']
        winner = game_info['winner']

        if winner=='X':
            points_won = -game_info['points-won']
        elif winner=='O':
            points_won = game_info['points-won']
        reward = points_won

        self._move_count += 1
        if self._move_count==self._num_moves:
            done = True
            observation = bg.positionfromid(move['board'])
        else:
            done = False
            observation = bg.positionfromid(self._moves[self._move_count]['board'])
        
        info = bg.positionfromid(move['board'])
        obs = info[0] + info[1]
        info = obs
 

        return observation, reward, done, info
    
    def episode(self, count_eps, dir_out="season01/"):
        filename = "".join((dir_out,'eps',count_eps.__str__().zfill(8),'.dat'))
        with open(filename, 'w+') as fh:
            self.reset()
            done = False
            while not done:
#                action = np.random.randint(2)
                _, reward0, done, info = self.step(0)
                self._move_count -= 1
                _, reward1, done, info = self.step(1)
                fh.write(" ".join(bit.__str__() for bit in info))
                fh.write(" ".join((" ",reward0.__str__())))
                fh.write(" ".join((" ",reward1.__str__(),"\n")))
            

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

with open("counter.dat", 'r') as fh:
    n0 = fh.readline()
    n1 = fh.readline()
print n0,n1
n0 = int(n0)
n1 = int(n1)
player = Player()
for count in range(n0, n1):
    player.episode(count, dir_out="season09/")



