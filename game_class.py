import numpy as np
import math
import pickle

class Connect4:
    def __init__(self, width=7, height=6, player1='player1', player2='player2'):
        self.__board = np.full((height, width), None)
        self.__pos = width * [height - 1]   # list of next available move in each column
        self.__player1 = player1
        self.__player2 = player2
        self.__width = width
        self.__height = height
        self.__last_move = None             # position of last move played
        self.__last_played = None           # name of last player played
        self.__score = [276, 276]           # initial score for each player "hard code"
        self.__depth = 4                    # for difficulty


    def restart(self, width=7, height=6):
        self.__board = np.full((height, width), None)
        self.__pos = width * [height - 1]
        self.__width = width
        self.__height = height
        self.__last_move = None
        self.__last_played = None
        self.__score = [276, 276]           #aywa hard code


    def save(self):
        try:
            dict = {}
            with open('state.p', 'wb') as handle:
                dict['board']  = self.__board
                dict['pos'] = self.__pos
                dict['player1'] = self.__player1
                dict['player2'] = self.__player2
                dict['width'] = self.__width
                dict['height'] = self.__height
                dict['last_move'] = self.__last_move
                dict['last_played'] = self.__last_played
                dict['score'] = self.__score
                pickle.dump(dict, handle)
                return 1
        except:
            return 0


    def load(self):
        try:
            with open('state.p', 'rb') as handle:
                dict = pickle.load(handle)
                self.__board = dict['board']
                self.__pos = dict['pos']
                self.__player1 = dict['player1']
                self.__player2 = dict['player2']
                self.__width = dict['width']
                self.__height = dict['height']
                self.__last_move = dict['last_move']
                self.__last_played = dict['last_played']
                self.__score = dict['score']
                return 1
        except:
            return 0


    def play(self, player, col):
        row = self.__pos[col]
        assert row >= 0, 'this column is full can\'t put more pieces in it'
        assert player in [self.__player1, self.__player2], '{} is not a player in this game'.format(player)
        self.__board[row][col] = player
        self.__pos[col] -= 1
        self.__last_move = (row, col)
        self.__last_played = player
        cost = self.cost(row, col)
        index = player is self.__player2
        self.__score[(index+1)%2] -= cost
        ret = self.is_winner(self.get_full_state())
        if ret == 1:
            print('game ended,', self.__last_played, 'is winner!')
            return 1
        elif ret == -1:
            print('game ended, there is no winner!!!')
            return 0
        elif index:
            return self.AI_play()


    def set_depth(self, d):
        self.__depth = d


    def get_state(self):
        return self.__board


    def get_full_state(self):
        return self.__last_played, self.__last_move, self.__score, self.__board


    def get_player1(self):
        return self.__player1


    def get_player2(self):
        return self.__player2


    def set_player1(self, player_name):
        assert not self.__board.any(), 'player name can\'t be set during the game'
        self.__player1 = player_name


    def set_player2(self, player_name):
        assert not self.__board.any(), 'player name can\'t be set during the game'
        self.__player2 = player_name


    def is_winner(self, state):
        player, (posh, posw),_ , board = state
        height, width = board.shape

        #detect vertical
        if posh < height-3:
            i = 0
            while i < 4:
                if board[posh+i][posw]!=player:
                    break
                i+=1
            else:
                return 1

        #detect horizontal
        i = max(0, posw-3)
        j = min(width, posw+4)
        count = 0
        while i < j:
            if board[posh][i] != player:
                count = 0
            else:
                count += 1
            i+=1
            if count >= 4:
                return 1

        #detect diagonal /
        low = min(height-posh-1, posw, 3)
        #i, j = posh+low, posw-low
        high = min(posh, width-posw-1, 3)
        #i, j = posh-high, posw+high
        if high + low > 2:
            count = 0
            i, j = posh+low, posw-low
            while i >= posh-high:
                if board[i][j] != player:
                    count = 0
                else:
                    count += 1
                i-=1; j+=1
                if count >= 4:
                    return 1

        #detect diagonal \
        low = min(height-posh-1, width-posw-1, 3)
        #i, j = posh+low, posw+low
        high = min(posh, posw, 3)
        #i, j = posh-high, posw-high
        if high + low > 2:
            count = 0
            i, j = posh+low, posw+low
            while i >= posh-high:
                if board[i][j] != player:
                    count = 0
                else:
                    count += 1
                i-=1; j-=1
                if count >= 4:
                    return 1

        if None in board: return 0
        return -1


    def next_state(self, state):
        players = self.__player1, self.__player2
        index = state[0] is self.__player1
        player_name = players[index]
        initial_board = state[3]
        height, width = initial_board.shape
        boards = []
        for j in range(width):
            board = initial_board.copy()
            if board[0][j] is None:
                col_free_flag = 0
                for i in range(1,height):
                    if board[i][j] is not None:
                        col_free_flag = 1 #the column not empty
                        board[i-1][j] = player_name
                        cost = self.cost(i-1, j)
                        score = [None, None]
                        score[(index+1)%2] = state[2][(index+1)%2] - cost
                        score[index] = state[2][index]
                        boards.append(( player_name, (i-1, j), score, board ))
                        break
                if col_free_flag==0:
                    board[height-1][j] = player_name
                    cost = self.cost(height-1, j)
                    score = [None, None]
                    score[(index+1)%2] = state[2][(index+1)%2] - cost
                    score[index] = state[2][index]
                    boards.append(( player_name, (height-1, j), score, board ))
        return boards


    def eval_state(self, state, depth):
        player = state[0]
        ret = self.is_winner(state)
        if ret == 1:
            if player == self.__player1:
                return 1000*depth
            else:
                return -1000*depth
        elif ret == -1:
            return 0
        else:
            cost = ((player is self.__player1)*2-1) * self.cost(*state[1])
            return state[2][0] - state[2][1] + cost


    def cost(self, posh, posw):
        c = 4 - math.ceil(abs(posh-2.5))   # all destroyed vertical patterns
        c += 4 - abs(posw-3)               # all destroyed horizontal patterns
        if posw == 0 or posw == 6:         # following conditions to get all destroyed diagonal patterns
            c += 1
        elif posw == 1 or posw == 5:
            c += 4 - math.ceil(abs(posh-2.5))
        elif posw == 2 or posw == 4:
            c += 6 - 2*abs(posh-2.5)
        elif posw == 3:
            c += 2 * (4 - math.ceil(abs(posh-2.5)))
        return int(c)


    def dfs(self, state, path, alpha, beta ,depth, AI):
        if depth > 0:
            if self.is_winner(state) == 1:
                if AI:
                    alpha = max(alpha, -1000*(depth+1))
                else:
                    beta = min(beta, 1000*(depth+1))

            else:
                best_path = path
                modified = False
                for i, s in enumerate(self.next_state(state)):
                    new_path, new_alpha, new_beta = self.dfs(s, path+[i], alpha, beta, depth-1, not AI)
                    if AI:
                        if new_beta > alpha:
                            alpha = new_beta; modified = True
                    else:
                        if new_alpha < beta:
                            beta = new_alpha; modified = True
                    if alpha >= beta:    #cut off
                        break
                    if modified:
                        best_path = new_path; modified = False

                path = best_path
        else:
            score = self.eval_state(state, depth+1)
            if AI:
                alpha = max(alpha, score)
            else:
                beta = min(beta, score)

        return path, alpha, beta


    def AI_play(self):
        state = self.get_full_state()
        alpha, beta = -float("inf"), float("inf")
        path = []
        depth = self.__depth
        path, new_alpha, new_beta = self.dfs(state, path, alpha, beta, depth, True)
        n_states = self.next_state(state)
        index = path[0]
        return self.play(self.__player1, n_states[index][1][1])


    def start(self, first_play, col=None):
        assert not self.__board.any(), 'the game have already started'
        if first_play == self.__player1:
            self.play(first_play, np.random.randint(self.__width))
        else:
            assert col in range(self.__width), 'invalid column to play'
            self.play(first_play, col)


    def show(self):
        p1 = self.__player1
        p2 = self.__player2
        length = max(len(p1), len(p2), 4)
        for i in self.__board:
            for j in i:
                print(str(j).ljust(length), end="   ")
            print()
