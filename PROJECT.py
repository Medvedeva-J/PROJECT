import sys
import sqlite3
import pygame
import easygui
import project_timer as pt
import project_stopwatch as psw
import project_alarm as pa
import datetime as dt
from PyQt5 import uic
from PyQt5.QtCore import QTimer, QModelIndex
from PyQt5.QtWidgets import QWidget, QTableWidget, QSpinBox,\
    QTableWidgetItem, QMainWindow, QComboBox, QApplication, QPushButton, QLabel, QTextEdit



class Watch(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('clocks.ui', self)
        self.tmr = QTimer(self)
        self.clock.setText(str(dt.datetime.now().time()).split('.')[0])
        self.btn_alarm.clicked.connect(self.alarm)
        self.btn_stopwatch.clicked.connect(self.stopwatch)
        self.btn_timer.clicked.connect(self.timer)
        self.tmr.setInterval(1000)
        self.tmr.timeout.connect(self.run)
        self.tmr.start()

    def stopwatch(self):
        Stopwatch.sw_main(self)

    def timer(self):
        Timer.t_main(self)

    def alarm(self):
        pa.Alarm.a_main(self)

    def run(self):
        self.clock.setText(str(dt.datetime.now().time()).split('.')[0])
        self.clock.repaint()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Watch()
    w.show()
    sys.exit(app.exec())