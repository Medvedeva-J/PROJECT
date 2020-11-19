import sys
from time import *
from PyQt5.QtWidgets import QDialog, QMainWindow, QApplication, QPushButton, QLabel, QLineEdit
from PyQt5 import uic
from PyQt5.QtCore import QTimer, QTime


class Stopwatch(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('stopwatch.ui', self)
        self.btn_stop.hide()
        self.btn_pause.hide()
        self.btn_start.clicked.connect(self.run)
        self.btn_stop.clicked.connect(self.stop)
        self.btn_pause.clicked.connect(self.pause)

    def run(self):
        self.flags.clear()
        self.history = []
        self.begin = round(time(), 2)
        self.last_stop = self.label.text()
        self.btn_start.hide()
        self.btn_stop.show()
        self.btn_pause.show()
        self.tmr = QTimer(self)
        self.tmr.setInterval(10)
        self.tmr.timeout.connect(self.frame)
        self.tmr.start()

    def frame(self):
        m_seconds = (round(time(), 2) - self.begin) % 60
        seconds = (round(time(), 2) - self.begin) % 60
        minutes = (round(time(), 2) - self.begin) // 60
        m_seconds = (str(round(m_seconds, 2)).split('.')[-1]).rjust(2, '0')
        seconds = str(round(seconds)).rjust(2, '0')
        minutes = str(round(minutes)).rjust(2, '0')
        self.label.setText(f'{minutes}:{seconds}:{m_seconds}')

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
            m_seconds = self.label.text().split(':')
            m_seconds = list(map(lambda x: int(x), m_seconds))
            m_seconds = m_seconds[0] * 60 * 100 + m_seconds[1] * 100 + m_seconds[-1]

            m_seconds2 = self.last_stop.split(':')
            m_seconds2 = list(map(lambda x: int(x), m_seconds2))
            m_seconds2 = (m_seconds2[0] * 60 * 100) + (m_seconds2[1] * 100) + m_seconds2[-1]
            
            m = m_seconds - m_seconds2
            minutes2 = m // 6000
            seconds2 = (m % 6000) // 100
            m_seconds2 = (m % 6000) % 100

            a.append(f'+ {int(minutes2)}:{int(seconds2)}:{int(m_seconds2)}')
            a.append(self.label.text())
            self.last_stop = self.label.text()
            a = '\t'.join(a)
            self.history.append(a)
            self.flags.setText('\n'.join(self.history))
        else:
            self.btn_pause.setText('PAUSE')
            self.tmr.start()

    def sw_main(self):
        if __name__ == '__main__':
            app = QApplication(sys.argv)
            sw = Stopwatch()
            sw.show()
            sys.exit(app.exec())