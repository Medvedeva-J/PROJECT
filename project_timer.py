import sys
import easygui
from time import *
from PyQt5.QtWidgets import QDialog, QCalendarWidget, QMainWindow, QApplication, QPushButton, QLabel, QLineEdit
from PyQt5 import uic
from PyQt5.QtCore import QTimer, QTime
import pygame


class Timer(QDialog):
    def __init__(self):
        pygame.init()
        self.song = pygame.mixer.Sound('рингтоны\hangouts.mp3')
        super().__init__()
        uic.loadUi('timer.ui', self)
        self.btn_start.clicked.connect(self.run)
        self.btn_stop.clicked.connect(self.end)
        self.btn_sound.clicked.connect(self.sound)

    def sound(self):
        input_file = easygui.fileopenbox(default="рингтоны/*.mp3", filetypes=["*.mp3"])
        self.song = pygame.mixer.Sound(input_file)

    def run(self):
        self.btn_sound.hide()
        self.begin = round(time())
        self.tmr = QTimer(self)
        self.tmr2 = QTimer(self)
        hour = self.hours.value()
        minute = self.minutes.value()
        second = self.seconds.value()
        self.allof = hour * 3600 + minute * 60 + second
        hour = str(hour).rjust(2, '0')
        minute = str(minute).rjust(2, '0')
        second = str(second).rjust(2, '0')
        self.tmr.setInterval(1000)
        self.tmr2.setInterval(self.allof * 1000)
        self.tmr2.timeout.connect(self.end)
        self.till.setText(f'{hour}:{minute}:{second}')
        self.tmr.timeout.connect(self.change)
        self.tmr.start()
        self.tmr2.start()

    def change(self):
        till_the_end = self.allof + self.begin - round(time())
        seconds = (till_the_end % 3600) % 60
        minutes = (till_the_end % 3600) // 60
        hours = till_the_end // 3600
        seconds = str(seconds).rjust(2, '0')
        minutes = str(minutes).rjust(2, '0')
        hours = str(hours).rjust(2, '0')
        self.till.setText(f'{hours}:{minutes}:{seconds}')
        
    def end(self):
        if self.btn_stop.text() == 'Сброс':
            self.tmr.stop()
            self.tmr2.stop()
            self.btn_sound.show()
            self.till.setText('00:00:00')
            if self.begin + self.allof == round(time()):
                self.btn_stop.setText('ОК')
                self.btn_start.setEnabled(False)
                self.song.play(-1)

        else:
            self.song.stop()
            self.btn_stop.setText('Сброс')
            self.btn_start.setEnabled(True)

    def t_main(self):
        app = QApplication(sys.argv)
        t = Timer()
        t.show()
        sys.exit(app.exec())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    t = Timer()
    t.show()
    sys.exit(app.exec())