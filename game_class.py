import numpy as np


class Connect4:
    def __init__(self, width=7, height=6, player1='player1', player2='player2'):
        self.__board = np.full((height, width), None)
        self.__pos = width * [height - 1]
        self.__lists = []
        self.__player1 = player1
        self.__player2 = player2
        self.__width = width
        self.__height = height

    def play(self, player, col):
        row = self.__pos[col]
        assert row >= 0, 'this column is full can\'t put more pieces in it'
        assert player in [self.__player1, self.__player2], '{} is not a player in this game'.format(player)
        self.__board[row][col] = player
        self.__pos[col] -= 1

    def get_state(self):
        return self.__board

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

    def is_winner():
        pass

    def next_state(self,state , player_name):
        boards = []
        for j in range(7):
            board = state.copy()
            if board[0][j] == None:

                col_free_flag = 0
                for i in range(1,6):
                    if board[i][j] != None:
                        col_free_flag = 1 #the column not empty
                        board[i-1][j] = player_name
                        boards.append(board)
                        break
                if col_free_flag==0:
                    board[5][j] = player_name
                    boards.append(board)

        return boards


    def show(self):
        p1 = self.__player1
        p2 = self.__player2
        length = max(len(p1), len(p2), 4)
        for i in self.__board:
            for j in i:
                print(str(j).ljust(length), end="   ")
            print()
