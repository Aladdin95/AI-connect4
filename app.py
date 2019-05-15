import numpy as np
import time
import math

class Connect4:
    def __init__(self, width=7, height=6, player1='player1', player2='player2'):
        self.__board = np.full((height, width), None)
        self.__pos = width * [height - 1]
        self.__player1 = player1
        self.__player2 = player2
        self.__width = width
        self.__height = height
        self.__last_move = None
        self.__last_played = None
        self.__score = [276, 276]  #aywa hardcode


    def restart(self, width=7, height=6):
        self.__board = np.full((height, width), None)
        self.__pos = width * [height - 1]
        self.__width = width
        self.__height = height
        self.__last_move = None
        self.__last_played = None
        self.__score = [276, 276]  #aywa hardcode

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
        self.__score[(index+1)%2] = self.__score[(index+1)%2] - cost
        ret = self.is_winner(self.get_full_state())
        if ret == 1:
            print('game ended,', self.__last_played, 'is winner!')
            return 1
        elif ret == -1:
            print('game ended, there is no winner!!!')
            return 0
        if index:
            return self.AI_play()


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
            if board[0][j] == None:
                col_free_flag = 0
                for i in range(1,height):
                    if board[i][j] != None:
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
        c = 4 - math.ceil(abs(posh-2.5))
        c += 4 - abs(posw-3)
        if posw == 0 or posw == 6:
            c += 1
        elif posw == 1 or posw == 5:
            c += 4 - math.ceil(abs(posh-2.5))
        elif posw == 2 or posw == 4:
            c += 6 - 2*abs(posh-2.5)
        elif posw == 3:
            c += 2 * (4 - math.ceil(abs(posh-2.5)))
        return int(c)


    def dfs(self, state, path, alpha, beta ,depth, AI):
        #print(path)
        modefied = False
        if depth > 0:
            ret = self.is_winner(state)
            if ret == 1:
                if AI:
                    alpha = -1000*depth
                else:
                    beta = 1000*depth

            else:
                cut_off = False
                best_path = path
                for i, n in enumerate(self.next_state(state)):
                    new_path, new_alpha, new_beta = self.dfs(n, path+[i], alpha, beta, depth-1, not AI)
                    if AI:
                        if new_beta > alpha:
                            alpha = new_beta
                            modefied = True
                    else:
                        if new_alpha < beta:
                            beta = new_alpha
                            modefied = True
                    if modefied:
                        best_path = new_path
                        modefied = False
                    if alpha >= beta:    #cut off
                        cut_off = True
                        break
                #if not cut_off:
                path = best_path

        else:
            score = self.eval_state(state, depth+1)
            #print('score', score)
            if AI:
                if score > alpha:
                    alpha = score
            else:
                if score < beta:
                    beta = score
            #print(alpha, beta)
        return path, alpha, beta


    def AI_play(self):
        state = self.get_full_state()
        alpha, beta = -float("inf"), float("inf")
        path = []
        depth = 4
        path, new_alpha, new_beta = self.dfs(state, path, alpha, beta, depth, True)
        #print(path, new_alpha, new_beta)
        n_states = self.next_state(state)
#         scores = []
#         for s in n_states:
#             scores.append(self.eval_state(s))
#         print(scores)
        index = path[0]
#         try:
#             index = path[1]
#         except:
#             index = 0
#         print(new_alpha, new_beta)
        self.play(self.__player1, n_states[index][1][1])

        ret = self.is_winner(self.get_full_state())
        if ret == 1:
            print('game ended,', self.__last_played, 'is winner!')
            return 1
        elif ret == -1:
            print('game ended, there is no winner!!!')
            return 0


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


game = Connect4()
game.set_player1('AI')
game.set_player2('You')


import sys
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtWidgets import QApplication, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QFileDialog, QLineEdit

color1='red'
color2='yellow'





class Example(QWidget):

    started = QtCore.Signal()
    finished = QtCore.Signal()

    def __init__(self):
        super(Example, self).__init__()



        self.initUI()







    def initUI(self):
        self.setGeometry(300, 300, 770, 700)
        self.setWindowTitle('Colors')

        #buttons = []
        x=115
        count=0


        self.clickbutton0 = QPushButton("Click", self)
        self.clickbutton0.setFixedSize(50, 32)
        #clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.clickbutton0.clicked.connect((lambda :self.col(0)))
        self.clickbutton0.move(x,120)
        x+=82

        self.clickbutton1 = QPushButton("Click", self)
        self.clickbutton1.setFixedSize(50, 32)
        #clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.clickbutton1.clicked.connect((lambda :self.col(1)))
        self.clickbutton1.move(x,120)

        x+=82
        self.clickbutton2 = QPushButton("Click", self)
        self.clickbutton2.setFixedSize(50, 32)
        #clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.clickbutton2.clicked.connect((lambda :self.col(2)))
        self.clickbutton2.move(x,120)

        x+=82

        self.clickbutton3 = QPushButton("Click", self)
        self.clickbutton3.setFixedSize(50, 32)
        #clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.clickbutton3.clicked.connect((lambda :self.col(3)))
        self.clickbutton3.move(x,120)


        x+=82

        self.clickbutton4 = QPushButton("Click", self)
        self.clickbutton4.setFixedSize(50, 32)
        #clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.clickbutton4.clicked.connect((lambda :self.col(4)))
        self.clickbutton4.move(x,120)


        x+=82

        self.clickbutton5 = QPushButton("Click", self)
        self.clickbutton5.setFixedSize(50, 32)
        #clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.clickbutton5.clicked.connect((lambda :self.col(5)))
        self.clickbutton5.move(x,120)
        x+=82

        self.clickbutton6 = QPushButton("Click", self)
        self.clickbutton6.setFixedSize(50, 32)
        #clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.clickbutton6.clicked.connect((lambda :self.col(6)))
        self.clickbutton6.move(x,120)


        self.restartbtn = QPushButton("Restart", self)
        self.restartbtn.setFixedSize(50, 32)
        #clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.restartbtn.clicked.connect((lambda :self.restart()))
        self.restartbtn.move(10,10)
        #self.restartbtn.hide()

        self.aistartbtn = QPushButton("AI Start", self)
        self.aistartbtn.setFixedSize(50, 32)
        #clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.aistartbtn.clicked.connect((lambda :self.aistart()))
        self.aistartbtn.move(10,50)
#         self.vbox = QVBoxLayout(self)
#         self.vbox.addWidget(self.restartbtn)


        self.label = QtWidgets.QLabel(self)
        #self.label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.label.setText("first line\nsecond line")
        self.label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.label.move(350,50)
        self.label.setStyleSheet("QLabel{font:bold 29px;color:#6A5ACD}")
        self.label.hide()

        self.show()


    def aistart(self):
        game.start('AI')
        self.update()
        self.aistartbtn.hide()


    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawRectangles(qp)
        qp.end()





    def col(self,n):
        print(n)
        result = game.play(game.get_player2(),n)
        self.update()
        self.aistartbtn.hide()

        if game.get_state()[0][n]!=None:
            if n == 0:
                self.clickbutton0.setEnabled(False)
            elif n == 1:
                self.clickbutton1.setEnabled(False)
            elif n == 2:
                self.clickbutton2.setEnabled(False)
            elif n == 3:
                self.clickbutton3.setEnabled(False)
            elif n == 4:
                self.clickbutton4.setEnabled(False)
            elif n == 5:
                self.clickbutton5.setEnabled(False)
            elif n == 6:
                self.clickbutton6.setEnabled(False)


        if result == 1:

            print(game.get_full_state()[0]+" Won !")

            self.label.setText(game.get_full_state()[0]+" Won !")
            self.label.show()

#             self._message_box = QtWidgets.QMessageBox()
#             self._message_box.setText(game.get_full_state()[0]+" Won !")
#             self._message_box.setStandardButtons(QtWidgets.QMessageBox.NoButton)
#             self.started.connect(self._message_box.show)
#             self.finished.connect(self._message_box.accept)


#             label1 = QtWidgets.QLabel(text=game.get_full_state()[0]+" Won !")
#             self.vbox.addWidget(label1)
#             #self.lineEdit.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
#             label1.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
#             label1.setStyleSheet("QLabel{font:bold 29px;color:#6A5ACD}")


            #self.restartbtn.setEnabled(True)

            self.clickbutton0.setEnabled(False)
            self.clickbutton1.setEnabled(False)
            self.clickbutton2.setEnabled(False)
            self.clickbutton3.setEnabled(False)
            self.clickbutton4.setEnabled(False)
            self.clickbutton5.setEnabled(False)
            self.clickbutton6.setEnabled(False)

        elif result == -1 :
            print('No one wins')

#             label1 = QtWidgets.QLabel(text="AI Wins !")
#             vbox = QVBoxLayout(self)
#             vbox.addWidget(label1)
#             #self.lineEdit.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
#             label1.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
#             label1.setStyleSheet("QLabel{font:bold 29px;color:#6A5ACD}")

            self.clickbutton0.setEnabled(False)
            self.clickbutton1.setEnabled(False)
            self.clickbutton2.setEnabled(False)
            self.clickbutton3.setEnabled(False)
            self.clickbutton4.setEnabled(False)
            self.clickbutton5.setEnabled(False)
            self.clickbutton6.setEnabled(False)



#             RestartButton = QPushButton("Restart", self)
#             RestartButton.setFixedSize(50, 32)
#             #clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
#             RestartButton.clicked.connect(self.restart())
#             vbox.addWidget(RestartButton)


#             ExitButton = QPushButton("Restart", self)
#             ExitButton.setFixedSize(50, 32)
#             #clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
#             ExitButton.clicked.connect(exit())
#             vbox.addWidget(ExitButton)


    def drawRectangles(self, qp):

        color = QtGui.QColor(0, 0, 0)
        color.setNamedColor('#0000FF')
        qp.setPen(color)

        qp.setBrush(QtGui.QColor(0,0,255))
        qp.drawRect(100, 160, 570, 500)

        qp.setBrush(QtGui.QColor(25,25,112))
        qp.drawRect(90, 650, 590, 20)


        color.setNamedColor('#FFFFFF')
        qp.setPen(color)
        qp.setBrush(QtGui.QColor(255,255,255))
        x,y,w,h=110,570,70,70

        #print(game.get_state())
        for i in range (6):
            for j in range(7):
                if(game.get_state()[5-i][j]==game.get_player1()):
                    qp.setBrush(QtGui.QColor(255,0,0))
                elif(game.get_state()[5-i][j]==game.get_player2()):
                    qp.setBrush(QtGui.QColor(255,255,0))
                else:
                    qp.setBrush(QtGui.QColor(255,255,255))
                qp.drawEllipse(x, y, w, h)
                x+=80
                #print(x)
            x=110
            y-=80


#         label = QtWidgets.QLabel(self)
#         label.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
#         label.setText("first line\nsecond line")
#         label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
#         label1 = QtWidgets.QLabel(text="Your turn !")
#         vbox = QVBoxLayout(self)
#         vbox.addWidget(label1)
#         #self.lineEdit.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
#         label1.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignHCenter)
#         label1.setStyleSheet("QLabel{font:bold 29px;color:#6A5ACD}")







#         label2 = QtWidgets.QLabel(text="his turn ?!")
#         vbox = QVBoxLayout(self)
#         vbox.addWidget(label2)
#         #self.lineEdit.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Sunken)
#         label2.setAlignment(QtCore.Qt.AlignBottom| QtCore.Qt.AlignHCenter)
#         label2.setStyleSheet("QLabel{font:bold 29px;color:#0000FF}")

    def restart(self):
        print('restaring ...')
        self.label.hide()
        self.aistartbtn.show()

        game.restart()

        self.clickbutton0.setDisabled(False)
        self.clickbutton1.setDisabled(False)
        self.clickbutton2.setDisabled(False)
        self.clickbutton3.setDisabled(False)
        self.clickbutton4.setDisabled(False)
        self.clickbutton5.setDisabled(False)
        self.clickbutton6.setDisabled(False)

        self.update()

        print('done restarting')

        #print(game.get_state())





def main():
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
