import sys
import sqlite3
import pygame
import easygui
import datetime as dt
from PyQt5 import uic
from PyQt5.QtCore import QTimer, QModelIndex
from PyQt5.QtWidgets import QDialog, QWidget, QTableWidget, QSpinBox, \
    QTableWidgetItem, QMainWindow, QComboBox, QApplication, QPushButton, QLabel, QTextEdit


class Alarm(QDialog):
    def __init__(self):
        pygame.init()
        self.started = dict()
        super().__init__()
        self.q = ''
        uic.loadUi('alarm.ui', self)
        self.ok.hide()
        self.choose_ringtone.clicked.connect(self.select)
        self.confirm.clicked.connect(self.add_alarm)
        self.btn_delete.clicked.connect(self.delete_alarm)
        self.ok.clicked.connect(self.stop_music)

        self.con = sqlite3.connect('project_ringtones.sqlite')
        self.cur = self.con.cursor()
        self.result = self.cur.execute("""select * from start order by alarm_time""").fetchall()
        self.table_update()
        self.name()
        self.check_alarm()

    def name(self):
        b = []
        for i in range(self.table.rowCount()):
            if self.table.item(i, 0).text().startswith('Будильник_'):
                b.append(self.table.item(i, 0).text())
        if len(b) > 0:
            b = list(map(lambda x: int(x.split('_')[-1]), b))
            q = max(b) + 1
        else:
            q = 1
        self.alarm_name.setText(f'Будильник_{q}')

    def stop_music(self):
        self.sound.stop()
        self.ok.hide()
        if self.q != '':
            self.cur.execute(f"""delete from start where alarm_name = '{self.q}'""").fetchall()
        self.con.commit()
        self.table_update()

    def delete_alarm(self):
        a = self.table.selectionModel().selectedRows()
        for i in range(len(a) - 1, -1, -1):
            name = self.table.item(a[i].row(), 0).text()
            name = self.cur.execute(f"""select id from start
                        where alarm_name = '{name}'""").fetchone()
            name = name[0]
            self.cur.execute(f"""delete from start where id = {name}""").fetchone()
            self.started[name].stop()
            self.con.commit()
        self.table_update()
        self.name()

    def table_update(self):
        self.result = self.cur.execute("""select * from start order by alarm_time""").fetchall()
        self.table.setRowCount(len(self.result))
        for i, elem in enumerate(self.result):
            for j, val in enumerate(elem):
                if j != 0:
                    a = QTableWidgetItem(str(val))
                    self.table.setItem(i, j - 1, a)
        self.table.repaint()

    def add_alarm(self):
        b = []
        for i in range(self.table.rowCount()):
            b.append(self.table.item(i, 0).text())
        if self.alarm_name.text() == '' or self.choose_ringtone.text() == '------':
            self.label_6.setText('Заполните все поля')
            self.label_6.show()
        elif self.alarm_name.text() in b:
            self.label_6.setText('Введите уникальное имя')
            self.label_6.show()
        else:
            self.label_6.hide()
            row = []
            name = self.alarm_name.text()
            text = str(self.hours.value()).rjust(2, '0') + ':' + str(self.minutes.value()).rjust(2, '0')
            al_time = dt.datetime.strptime(text, '%H:%M').time()
            ringtone = self.choose_ringtone.text()
            repeat = self.repeat_ask.currentText()
            row.append(name)
            row.append(al_time)
            row.append(repeat)
            row.append(ringtone)
            row.append(repeat)
            self.cur.execute(f"""insert into start(alarm_name, alarm_time, sound,
                            alarm_repeat, song_path, on_off, today_day)
                            values ('{name}', '{al_time}', '{ringtone}', '{repeat}',
                            '{self.song_path}', 0, '{dt.datetime.now().strftime('%A')}')""")
        self.con.commit()
        self.table_update()
        self.name()
        self.check_alarm()

    def run(self):
        f = 0
        name = self.sender()
        for p in self.started:
            if self.started[p] == name:
                a = p
        al = self.cur.execute(f"""select alarm_time from start
                        where id = {a}""").fetchone()
        al = al[0]
        al = ':'.join(str(al).split(':')[:-1])
        rep = self.cur.execute(f"""select alarm_repeat from start
                        where id = {a}
                        order by id""").fetchone()[0]
        tod = self.cur.execute(f"""select today_day from start
                        where id = {a}
                        order by id""").fetchone()[0]
        oo = self.cur.execute(f"""select on_off from start
                        where id = {a}
                        order by id""").fetchone()[0]
        al_t = ':'.join(str(al).split(':')[:2])
        rn = ':'.join(str(dt.datetime.now().time()).split(':')[:2])
        if rep == 'Однократно':
            if al_t == rn:
                f = 1
                self.q = self.cur.execute(f"""select alarm_name from start
                        where id = {a}
                        order by id""").fetchone()[0]
                getattr(self, f'tmr_{a}').stop()

        elif rep == 'По будням':
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
            if dt.datetime.now().strftime('%A') in days and al_t == rn and oo == 0:
                f = 1
                oo = 1
            if tod != dt.datetime.now().strftime('%A'):
                oo = 0
                self.cur.execute(f"""update start
                            set today_day = '{dt.datetime.now().strftime('%A')}')
                            where id = {a}""")
            self.cur.execute(f"""update start
                            set on_off = {oo})
                            where id = {a}""")
        elif rep == 'Ежедневно':
            if al_t == rn and 00 == 0:
                f = 1
            if tod != dt.datetime.now().strftime('%A'):
                oo = 0
                self.cur.execute(f"""update start
                            set today_day = '{dt.datetime.now().strftime('%A')}')
                            where id = {a}""")
            self.cur.execute(f"""update start
                            set on_off = {oo})
                            where id = {a}""")

        if f == 1:
            path = self.cur.execute(f"""select song_path from start
                                    where id = {a}""").fetchone()[0]
            self.sound = pygame.mixer.Sound(path)
            self.sound.play(-1)
            self.ok.show()
        self.con.commit()
        self.table_update()

    def check_alarm(self):
        if len(self.result) > 0:
            for i in range(len(self.result)):
                f = self.result[i][0]
                if f not in self.started:
                    setattr(self, f'tmr_{self.result[i][0]}', QTimer(self))
                    self.started[self.result[i][0]] = getattr(self, f'tmr_{self.result[i][0]}')
                    getattr(self, f'tmr_{self.result[i][0]}').setInterval(1000)
                    setattr(self, f'k_{self.result[i][0]}', str(self))
                    getattr(self, f'tmr_{self.result[i][0]}').timeout.connect(self.run)
                    getattr(self, f'tmr_{self.result[i][0]}').start()

    def select(self):
        input_file = easygui.fileopenbox(default="рингтоны/*.mp3", filetypes=["*.mp3"])
        self.sound = pygame.mixer.Sound(input_file)
        self.song_path = input_file
        self.choose_ringtone.setText(input_file.split('\\')[-1])

    def a_main(self):
        if __name__ == '__main__':
            a_app = QApplication(sys.argv)
            al = Alarm()
            al.show()
            sys.exit(a_app.exec())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    al = Alarm()
    al.show()
    sys.exit(app.exec())
