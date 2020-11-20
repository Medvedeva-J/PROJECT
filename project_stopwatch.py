import sys
from time import *
import datetime as dt
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication, QPushButton, QLabel, QLineEdit
from PyQt5 import uic
from PyQt5.QtCore import QTimer, QTime


class Stopwatch(QDialog):
    def __init__(self):
        self.history = []
        super().__init__()
        uic.loadUi('stopwatch.ui', self)
        self.btn_stop.hide()
        self.btn_pause.hide()
        self.btn_start.clicked.connect(self.run)
        self.btn_stop.clicked.connect(self.stop)
        self.btn_pause.clicked.connect(self.pause)

    def run(self):
        if self.sender().text() == 'START':
            self.flags.clear()
            self.ALL = 0
            self.history = []
            self.begin = dt.datetime.now().time()
            self.last_start = self.begin
            self.last_stop = self.begin

        self.btn_start.hide()
        self.btn_stop.show()
        self.btn_pause.show()
        self.tmr = QTimer(self)
        self.tmr.setInterval(10)
        self.tmr.timeout.connect(self.frame)
        self.tmr.start()

    def frame(self):
        r1 = dt.datetime.now().time()
        r2 = self.last_start

        r1 = list(map(lambda x: float(x), str(r1).split(':')))
        r2 = list(map(lambda x: float(x), str(r2).split(':')))
        rm1 = int(str(r1[2] % 1).split('.')[-1][:2])
        rm2 = int(str(r2[2] % 1).split('.')[-1][:2])

        r = r1.pop(-1)
        r1.append(r // 1)
        r = r2.pop(-1)
        r2.append(r // 1)

        r1.append(rm1)
        r2.append(rm2)

        del r1[0]
        del r2[0]

        r1 = list(map(lambda x: int(x), r1))
        r2 = list(map(lambda x: int(x), r2))

        r1 = r1[0] * 6000 + r1[1] * 100 + r1[2]
        r2 = r2[0] * 6000 + r2[1] * 100 + r2[2]

        self.ALL += r1 - r2

        minutes = self.ALL // 6000
        seconds = (self.ALL % 6000) // 100
        m_seconds = (self.ALL % 6000) % 100
        self.label.setText(f'{str(minutes).rjust(2, "0")}:{str(seconds).rjust(2, "0")}:{str(m_seconds).rjust(2, "0")}')
        self.last_start = dt.datetime.now().time()
        if self.btn_pause.text() == 'PAUSE':
            self.tmr.start()

    def stop(self):
        self.tmr.stop()
        self.btn_stop.hide()
        self.btn_pause.setText('PAUSE')
        self.btn_pause.hide()
        self.btn_start.show()

    def pause(self):
        if self.btn_pause.text() == 'PAUSE':
            self.btn_pause.setText('CONTINUE')
            self.tmr.stop()
            a = []
            a.append(str(len(self.history)))

            r1 = dt.datetime.now().time()
            r2 = self.last_stop

            r1 = list(map(lambda x: float(x), str(r1).split(':')))
            r2 = list(map(lambda x: float(x), str(r2).split(':')))
            rm1 = int(str(r1[2] % 1).split('.')[-1][:2])
            rm2 = int(str(r2[2] % 1).split('.')[-1][:2])

            r = r1.pop(-1)
            r1.append(r // 1)
            r = r2.pop(-1)
            r2.append(r // 1)

            r1.append(rm1)
            r2.append(rm2)

            del r1[0]
            del r2[0]

            r1 = list(map(lambda x: int(x), r1))
            r2 = list(map(lambda x: int(x), r2))

            r1 = r1[0] * 6000 + r1[1] * 100 + r1[2]
            r2 = r2[0] * 6000 + r2[1] * 100 + r2[2]

            m = r1 - r2

            minutes2 = m // 6000
            seconds2 = (m % 6000) // 100
            m_seconds2 = (m % 6000) % 100

            a.append(f'+{str(minutes2).rjust(2, "0")}:{str(seconds2).rjust(2, "0")}:{str(m_seconds2).rjust(2, "0")}')
            a.append(self.label.text())
            a = '\t'.join(a)
            self.history.append(a)
            self.flags.setText('\n'.join(self.history))
        else:
            self.btn_pause.setText('PAUSE')
            self.last_stop = dt.datetime.now().time()
            self.last_start = self.last_stop
            self.run()
