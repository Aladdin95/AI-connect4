from game_class import Connect4

import sys
from PySide2 import QtGui, QtCore, QtWidgets
from PySide2.QtWidgets import QApplication, QPushButton, QWidget, QHBoxLayout, QVBoxLayout, QFileDialog, QLineEdit


game = Connect4()
game.set_player1('AI')
game.set_player2('You')


class MainGUI(QWidget):
    started = QtCore.Signal()
    finished = QtCore.Signal()

    def __init__(self):
        super(MainGUI, self).__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 770, 700)
        self.setWindowTitle('Colors')

        # buttons = []
        x = 115

        self.clickbutton0 = QPushButton("Click", self)
        self.clickbutton0.setFixedSize(50, 32)
        # clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.clickbutton0.clicked.connect((lambda :self.col(0)))
        self.clickbutton0.move(x,120)
        x += 82

        self.clickbutton1 = QPushButton("Click", self)
        self.clickbutton1.setFixedSize(50, 32)
        # clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.clickbutton1.clicked.connect((lambda :self.col(1)))
        self.clickbutton1.move(x,120)

        x += 82
        self.clickbutton2 = QPushButton("Click", self)
        self.clickbutton2.setFixedSize(50, 32)
        # clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.clickbutton2.clicked.connect((lambda: self.col(2)))
        self.clickbutton2.move(x, 120)

        x += 82

        self.clickbutton3 = QPushButton("Click", self)
        self.clickbutton3.setFixedSize(50, 32)
        # clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.clickbutton3.clicked.connect((lambda: self.col(3)))
        self.clickbutton3.move(x,120)

        x += 82

        self.clickbutton4 = QPushButton("Click", self)
        self.clickbutton4.setFixedSize(50, 32)
        # clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.clickbutton4.clicked.connect((lambda: self.col(4)))
        self.clickbutton4.move(x, 120)

        x += 82

        self.clickbutton5 = QPushButton("Click", self)
        self.clickbutton5.setFixedSize(50, 32)
        # clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.clickbutton5.clicked.connect((lambda: self.col(5)))
        self.clickbutton5.move(x, 120)

        x += 82

        self.clickbutton6 = QPushButton("Click", self)
        self.clickbutton6.setFixedSize(50, 32)
        # clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.clickbutton6.clicked.connect((lambda: self.col(6)))
        self.clickbutton6.move(x, 120)

        self.clickbutton0.setEnabled(False)
        self.clickbutton1.setEnabled(False)
        self.clickbutton2.setEnabled(False)
        self.clickbutton3.setEnabled(False)
        self.clickbutton4.setEnabled(False)
        self.clickbutton5.setEnabled(False)
        self.clickbutton6.setEnabled(False)

        self.restartbtn = QPushButton("Restart", self)
        self.restartbtn.setFixedSize(50, 32)
        # clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.restartbtn.clicked.connect((lambda: self.restart()))
        self.restartbtn.move(10,10)
        # self.restartbtn.hide()

        self.aistartbtn = QPushButton("AI Start", self)
        self.aistartbtn.setFixedSize(50, 32)
        # clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.aistartbtn.clicked.connect((lambda: self.aistart()))
        self.aistartbtn.move(10, 50)
#         self.vbox = QVBoxLayout(self)
#         self.vbox.addWidget(self.restartbtn)

        self.savebtn = QPushButton("Save", self)
        self.savebtn.setFixedSize(50, 32)
        # clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.savebtn.clicked.connect((lambda :game.save()))
        self.savebtn.move(10,90)

        self.loadbtn = QPushButton("Load", self)
        self.loadbtn.setFixedSize(50, 32)
        # clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.loadbtn.clicked.connect((lambda :self.load()))
        self.loadbtn.move(10,130)

        self.difficultybtn1 = QPushButton("Very Easy", self)
        self.difficultybtn1.setFixedSize(80, 32)
        # clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.difficultybtn1.clicked.connect((lambda :self.set_difficulty('ve')))
        self.difficultybtn1.move(680,10)

        self.difficultybtn2 = QPushButton("Easy", self)
        self.difficultybtn2.setFixedSize(80, 32)
        # clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.difficultybtn2.clicked.connect((lambda: self.set_difficulty('e')))
        self.difficultybtn2.move(680, 50)

        self.difficultybtn3 = QPushButton("Medium", self)
        self.difficultybtn3.setFixedSize(80, 32)
        # clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.difficultybtn3.clicked.connect((lambda: self.set_difficulty('m')))
        self.difficultybtn3.move(680, 90)

        self.difficultybtn4 = QPushButton("Hard", self)
        self.difficultybtn4.setFixedSize(80, 32)
        # clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.difficultybtn4.clicked.connect((lambda: self.set_difficulty('h')))
        self.difficultybtn4.move(680, 130)

        self.difficultybtn5 = QPushButton("Very Hard", self)
        self.difficultybtn5.setFixedSize(80, 32)
        # clickbutton.setStyleSheet("QPushButton{border-radius: 5px;background: #C71585; font:bold 16px;color: white;}")
        self.difficultybtn5.clicked.connect((lambda: self.set_difficulty('vh')))
        self.difficultybtn5.move(680, 170)

        self.label = QtWidgets.QLabel(self)
        # self.label.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.label.setText("first line\nsecond line")
        self.label.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.AlignRight)
        self.label.move(350,50)
        self.label.setStyleSheet("QLabel{font:bold 29px;color:#6A5ACD}")
        self.label.hide()

        self.aistartbtn.hide()
        self.savebtn.hide()
        self.loadbtn.hide()

        self.show()

    def aistart(self):
        game.start('AI')
        self.update()
        self.aistartbtn.hide()

    def load(self):
        game.load()
        self.update()
        self.aistartbtn.hide()

    def set_difficulty(self,diff):
        if diff == 've':
            game.set_depth(1)
        elif diff == 'e':
            game.set_depth(2)
        elif diff == 'm':
            game.set_depth(4)
        elif diff == 'h':
            game.set_depth(5)
        elif diff == 'vh':
            game.set_depth(7)

        self.aistartbtn.show()
        self.savebtn.show()
        self.loadbtn.show()

        self.difficultybtn1.hide()
        self.difficultybtn2.hide()
        self.difficultybtn3.hide()
        self.difficultybtn4.hide()
        self.difficultybtn5.hide()

        self.clickbutton0.setDisabled(False)
        self.clickbutton1.setDisabled(False)
        self.clickbutton2.setDisabled(False)
        self.clickbutton3.setDisabled(False)
        self.clickbutton4.setDisabled(False)
        self.clickbutton5.setDisabled(False)
        self.clickbutton6.setDisabled(False)

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

            # self.restartbtn.setEnabled(True)

            self.clickbutton0.setEnabled(False)
            self.clickbutton1.setEnabled(False)
            self.clickbutton2.setEnabled(False)
            self.clickbutton3.setEnabled(False)
            self.clickbutton4.setEnabled(False)
            self.clickbutton5.setEnabled(False)
            self.clickbutton6.setEnabled(False)

        elif result == -1:
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
        x, y, w, h = 110, 570, 70, 70

        # print(game.get_state())
        for i in range (6):
            for j in range(7):
                if game.get_state()[5-i][j] == game.get_player1():
                    qp.setBrush(QtGui.QColor(255, 0, 0))
                elif game.get_state()[5-i][j] == game.get_player2():
                    qp.setBrush(QtGui.QColor(255, 255, 0))
                else:
                    qp.setBrush(QtGui.QColor(255, 255, 255))
                qp.drawEllipse(x, y, w, h)
                x += 80
                # print(x)
            x = 110
            y -= 80

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

        self.difficultybtn1.show()
        self.difficultybtn2.show()
        self.difficultybtn3.show()
        self.difficultybtn4.show()
        self.difficultybtn5.show()

        self.aistartbtn.hide()
        self.savebtn.hide()
        self.loadbtn.hide()

        self.label.hide()

        game.restart()

        self.update()

        print('done restarting')

        # print(game.get_state())


def main():
    app = QApplication(sys.argv)
    ex = MainGUI()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
