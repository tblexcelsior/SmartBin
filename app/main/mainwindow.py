from re import S
from PySide2.QtCore import QTimer, Qt, SIGNAL
from PySide2.QtWidgets import *
from PySide2 import QtUiTools
import sys
import random
import mysql.connector as mdb
from PySide2extn.RoundProgressBar import roundProgressBar

HOST = 'localhost'
DATABASE = 'smart_bin'
USER = 'tblexcel'
PASSWORD = 'tblexcelsior'

class MainWindow(object):
    def __init__(self) -> None:
        super().__init__()
        self.app = QApplication(sys.argv)
        loader = QtUiTools.QUiLoader()
        self.window = loader.load('./app/component/MainGUI_t_2.ui', None)
        # Get main frame
        self.main_frame = self.window.findChild(QFrame, 'drop_shadow_frame')
        self.chart_frame = self.window.findChild(QFrame, 'Chart')
        self.chart_frame.setVisible(False)
        # Get child object
        ## Exit button
        self.exit_btn = self.window.findChild(QPushButton, 'exit_btn')
        ## Percent text
        self.org_percent = self.window.findChild(QLabel, 'org_percent')
        self.inorg_percent = self.window.findChild(QLabel, 'inorg_percent')
        self.other_percent = self.window.findChild(QLabel, 'other_percent')
        ## Percent progress bar
        self.prog_1 = self.window.findChild(QFrame, 'progress_bar_1')
        self.prog_2 = self.window.findChild(QFrame, 'progress_bar_2')
        self.prog_3 = self.window.findChild(QFrame, 'progress_bar_3')
        ## Sheet
        self.sheet_1 = self.window.findChild(QFrame, 'type_1')
        self.sheet_2 = self.window.findChild(QFrame, 'type_2')
        self.sheet_3 = self.window.findChild(QFrame, 'type_3')

        # Process Bar Design
        self.rpb_1 = roundProgressBar()
        self.rpb_1.setObjectName('prog_1')
        self.rpb_1.setParent(self.prog_1)
        self.rpb_1.setFixedHeight(180)
        self.rpb_1.setFixedWidth(180)
        self.rpb_1.rpb_setLineColor((58, 235, 52))
        self.rpb_1.rpb_enableText(False)
        self.rpb_1.rpb_setLineCap('RoundCap')
        self.rpb_1.rpb_setLineWidth(10)
        self.rpb_1.rpb_setPathWidth(10)
        self.rpb_1.rpb_setPathColor((255, 255, 255))

        self.rpb_2 = roundProgressBar()
        self.rpb_2.setObjectName('prog_2')
        self.rpb_2.setParent(self.prog_2)
        self.rpb_2.setFixedHeight(180)
        self.rpb_2.setFixedWidth(180)
        self.rpb_2.rpb_setLineColor((58, 235, 52))
        self.rpb_2.rpb_enableText(False)
        self.rpb_2.rpb_setLineCap('RoundCap')
        self.rpb_2.rpb_setLineWidth(10)
        self.rpb_2.rpb_setPathWidth(10)
        self.rpb_2.rpb_setPathColor((255, 255, 255))

        self.rpb_3 = roundProgressBar()
        self.rpb_3.setObjectName('prog_3')
        self.rpb_3.setParent(self.prog_3)
        self.rpb_3.setFixedHeight(180)
        self.rpb_3.setFixedWidth(180)
        self.rpb_3.rpb_setLineColor((58, 235, 52))
        self.rpb_3.rpb_enableText(False)
        self.rpb_3.rpb_setLineCap('RoundCap')
        self.rpb_3.rpb_setLineWidth(10)
        self.rpb_3.rpb_setPathWidth(10)
        self.rpb_3.rpb_setPathColor((255, 255, 255))

        # Setting text position
        self.other_percent.setAlignment(Qt.AlignCenter)
        self.inorg_percent.setAlignment(Qt.AlignCenter)
        self.org_percent.setAlignment(Qt.AlignCenter)
        self.set_percent()
        self._timer = QTimer()    
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self.set_percent)
        self._timer.start()

        # Button detect
        self.sheet_1_btn = QPushButton()
        self.sheet_1_btn.setParent(self.sheet_1)
        self.sheet_1_btn.setGeometry(0, 0, 250, 400)
        self.sheet_1_btn.setStyleSheet('background-color: rgba(255, 255, 255, 0);')
        self.sheet_1_btn.connect(self.sheet_1_btn, SIGNAL('clicked()'), self.test1)

        self.sheet_2_btn = QPushButton()
        self.sheet_2_btn.setParent(self.sheet_2)
        self.sheet_2_btn.setGeometry(0, 0, 250, 400)
        self.sheet_2_btn.setStyleSheet('background-color: rgba(255, 255, 255, 0);')
        self.sheet_2_btn.connect(self.sheet_2_btn, SIGNAL('clicked()'), self.test3)

        self.sheet_3_btn = QPushButton()
        self.sheet_3_btn.setParent(self.sheet_3)
        self.sheet_3_btn.setGeometry(0, 0, 250, 400)
        self.sheet_3_btn.setStyleSheet('background-color: rgba(255, 255, 255, 0);')
        self.sheet_3_btn.connect(self.sheet_3_btn, SIGNAL('clicked()'), self.test3)

        self.exit_btn.connect(self.exit_btn, SIGNAL('clicked()'), self.exit)

    def test1(self):
        self.main_frame.setVisible(False)
        self.chart_frame.setVisible(True)
    def exit(self):
        self.main_frame.setVisible(True)
        self.chart_frame.setVisible(False)
    def test3(self):
        print('check3')
    def set_percent(self):
        try:
            conn = mdb.connect(host = HOST,
                database = DATABASE,
                user = USER,
                password = PASSWORD)
            curr = conn.cursor()
            query = 'select * from percent where id = (select max(id) from percent);'
            row = curr.execute(query)
            percent = list(curr.fetchall()[0])[1:]
            self.org_percent.setText(f'{percent[0]}%')
            self.inorg_percent.setText(f'{percent[1]}%')
            self.other_percent.setText(f'{percent[2]}%')
            self.rpb_1.rpb_setValue(percent[0])
            self.rpb_2.rpb_setValue(percent[1])
            self.rpb_3.rpb_setValue(percent[2])
            curr.close()
            conn.close()
        except:
            print("Cannot connect to database")

test = MainWindow()
test.window.show()
sys.exit(test.app.exec_())
