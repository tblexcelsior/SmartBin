import sys
import random
import mysql.connector as mdb
from PySide2.QtCore import QTimer, Qt, SIGNAL, Slot
from PySide2.QtWidgets import *
from PySide2 import QtUiTools, QtWidgets
from PySide2extn.RoundProgressBar import roundProgressBar
from PySide2.QtCharts import QtCharts
from PySide2.QtGui import QPainter
from chart import Bar_Chart
HOST = 'localhost'
DATABASE = 'smart_bin'
USER = 'tblexcel'
PASSWORD = 'tblexcelsior'

class MainWindow(object):
    def __init__(self) -> None:
        super().__init__()
        self.app = QApplication(sys.argv)
        loader = QtUiTools.QUiLoader()
        self.window = loader.load('./SmartBin/app/component/MainGUI_t_2.ui', None)

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
        self.stat_frame = self.window.findChild(QFrame, 'stat_frame')
        ## Chart Frame
        self.chart_widget = self.window.findChild(QWidget, 'chart_widget')

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

        # Bar Graph Setting
        self.type_chart = Bar_Chart()
        self.type_chart.setParent(self.chart_widget)
        self._type_chart_view = QtCharts.QChartView(self.type_chart)
        self._type_chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_layout = QtWidgets.QHBoxLayout(self.chart_widget)
        self.chart_layout.setContentsMargins(0, 0, 0, 0)
        self.chart_layout.addWidget(self._type_chart_view)


        # Setting text position
        self.other_percent.setAlignment(Qt.AlignCenter)
        self.inorg_percent.setAlignment(Qt.AlignCenter)
        self.org_percent.setAlignment(Qt.AlignCenter)
        self.set_percent()
        self._timer = QTimer()    
        self._timer.setInterval(1000)
        self._timer.timeout.connect(self.set_percent)
        self._timer.start()

        # Toggle Button
        self.toggle_status = 0
        self.toggle_btn_frame = self.window.findChild(QWidget, 'Toggle_Btn')
        self.toggle_slider = self.window.findChild(QWidget, 'pos_1')
        self.toggle_day = self.window.findChild(QLabel, 'Day')
        self.toggle_month = self.window.findChild(QLabel, 'Month')
        self.toggle_month.setVisible(False)
        self.toggle_day.setVisible(True)
        self.toggle_btn = QPushButton()
        self.toggle_btn.setParent(self.toggle_btn_frame)
        self.toggle_btn.setGeometry(0, 0, 100, 40)
        self.toggle_btn.setStyleSheet('background-color: rgba(255, 255, 255, 0);')
        self.toggle_btn.connect(self.toggle_btn, SIGNAL('clicked()'), self.toggle_clicked)

        # Date picker
        self.day_picker = self.window.findChild(QDateEdit, 'dateEdit')
        self.day_picker.editingFinished.connect(self.day_picked)

        # Button detect
        self.sheet_1_btn = QPushButton()
        self.sheet_1_btn.setParent(self.sheet_1)
        self.sheet_1_btn.setGeometry(0, 0, 250, 400)
        self.sheet_1_btn.setStyleSheet('background-color: rgba(255, 255, 255, 0);')
        self.sheet_1_btn.connect(self.sheet_1_btn, SIGNAL('clicked()'), self.open_chart)

        self.sheet_2_btn = QPushButton()
        self.sheet_2_btn.setParent(self.sheet_2)
        self.sheet_2_btn.setGeometry(0, 0, 250, 400)
        self.sheet_2_btn.setStyleSheet('background-color: rgba(255, 255, 255, 0);')
        self.sheet_2_btn.connect(self.sheet_2_btn, SIGNAL('clicked()'), self.open_chart)

        self.sheet_3_btn = QPushButton()
        self.sheet_3_btn.setParent(self.sheet_3)
        self.sheet_3_btn.setGeometry(0, 0, 250, 400)
        self.sheet_3_btn.setStyleSheet('background-color: rgba(255, 255, 255, 0);')
        self.sheet_3_btn.connect(self.sheet_3_btn, SIGNAL('clicked()'), self.open_chart)
        ## Statistic Button
        self.stat_btn = QPushButton()
        self.stat_btn.setParent(self.stat_frame)
        self.stat_btn.setGeometry(0, 0, 200, 60)
        self.stat_btn.setStyleSheet('background-color: rgba(255, 255, 255, 0);')
        self.stat_btn.connect(self.stat_btn, SIGNAL('clicked()'), self.open_chart)

        ## Exit button
        self.exit_btn.connect(self.exit_btn, SIGNAL('clicked()'), self.exit)
    # Callback function
    ##----------------- Need to update ------------------------##
    def open_chart(self):
        self.main_frame.setVisible(False)
        self.chart_frame.setVisible(True)
    
    def toggle_clicked(self):
        if self.toggle_status == 0:
            self.toggle_status = 1
            self.toggle_month.setVisible(True)
            self.toggle_day.setVisible(False)
            self.day_picker.setVisible(False)
        elif self.toggle_status == 1:
            self.toggle_status = 0
            self.toggle_month.setVisible(False)
            self.toggle_day.setVisible(True)
            self.day_picker.setVisible(True)
        self.toggle_slider.setGeometry(self.toggle_status * 50, 0, 50, 40)

    def exit(self):
        self.main_frame.setVisible(True)
        self.chart_frame.setVisible(False)
    ##-------------Get date date from this-----------------##
    def day_picked(self):
        print(str(self.day_picker.date()))

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
