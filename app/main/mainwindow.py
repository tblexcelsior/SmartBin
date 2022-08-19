from pkgutil import get_data
from re import A
import sys
import random
import mysql.connector as mdb
from PySide2.QtCore import QTimer, Qt, SIGNAL, Slot
from PySide2.QtWidgets import *
from PySide2 import QtUiTools, QtWidgets
from PySide2extn.RoundProgressBar import roundProgressBar
from PySide2.QtCharts import QtCharts
from PySide2.QtGui import QPainter, QMovie
from chart import Bar_Chart, Bar_Chart2
from datetime import datetime
HOST = 'localhost'
DATABASE = 'smart_bin'
USER = 'tblexcel'
PASSWORD = 'tblexcelsior'
a = datetime.today().strftime('%Y-%m-%d')
b = a.split('-')
temp = 0
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

        ## Processing animation frame
        self.processing_animation_frame = self.window.findChild(QWidget, 'Processing')
        self.label = self.window.findChild(QLabel, 'loading')
        self.movie = QMovie("./app/component/Loading.gif")
        self.label.setMovie(self.movie)
        self.movie.start()
        if temp ==0:   
            self.processing_animation_frame.setVisible(False)
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
        self.chart_widget_daily = self.window.findChild(QWidget, 'chart_widget_daily')
        self.chart_widget_monthly = self.window.findChild(QWidget, 'chart_widget_monthly')

        ## Status text
        self.status = self.window.findChild(QLabel, 'status')

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
        self.data_for_daily_type1 = self.get_daily_data(1)
        self.type_chart = Bar_Chart(self.data_for_daily_type1)
        self.type_chart.setParent(self.chart_widget_daily)
        self._type_chart_view = QtCharts.QChartView(self.type_chart)
        self._type_chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_layout = QtWidgets.QHBoxLayout(self.chart_widget_daily)
        self.chart_layout.setContentsMargins(0, 0, 0, 0)
        self.chart_layout.addWidget(self._type_chart_view)

        self.data_for_mothly_type1 = self.get_montly_data(1)
        self.type_chart2 = Bar_Chart2(self.data_for_mothly_type1)
        self.type_chart2.setParent(self.chart_widget_monthly)
        self._type_chart_view2 = QtCharts.QChartView(self.type_chart2)
        self._type_chart_view2.setRenderHint(QPainter.Antialiasing)
        self.chart_layout2 = QtWidgets.QHBoxLayout(self.chart_widget_monthly)
        self.chart_layout2.setContentsMargins(0, 0, 0, 0)
        self.chart_layout2.addWidget(self._type_chart_view2)

       



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
        self.sheet_1_btn.connect(self.sheet_1_btn, SIGNAL('clicked()'), self.open_chart1)

        self.sheet_2_btn = QPushButton()
        self.sheet_2_btn.setParent(self.sheet_2)
        self.sheet_2_btn.setGeometry(0, 0, 250, 400)
        self.sheet_2_btn.setStyleSheet('background-color: rgba(255, 255, 255, 0);')
        self.sheet_2_btn.connect(self.sheet_2_btn, SIGNAL('clicked()'), self.open_chart2)

        self.sheet_3_btn = QPushButton()
        self.sheet_3_btn.setParent(self.sheet_3)
        self.sheet_3_btn.setGeometry(0, 0, 250, 400)
        self.sheet_3_btn.setStyleSheet('background-color: rgba(255, 255, 255, 0);')
        self.sheet_3_btn.connect(self.sheet_3_btn, SIGNAL('clicked()'), self.open_chart3)
        ## Statistic Button
        self.stat_btn = QPushButton()
        self.stat_btn.setParent(self.stat_frame)
        self.stat_btn.setGeometry(0, 0, 200, 60)
        self.stat_btn.setStyleSheet('background-color: rgba(255, 255, 255, 0);')
        self.stat_btn.connect(self.stat_btn, SIGNAL('clicked()'), self.open_chart3)

        ## Exit button
        self.exit_btn.connect(self.exit_btn, SIGNAL('clicked()'), self.exit)
    # Callback function
    ##----------------- Need to update ------------------------##
    def open_chart1(self):
        self.main_frame.setVisible(False)
        self.chart_frame.setVisible(True)
        self.chart_widget_monthly.setVisible(False)
        # self.data_for_daily_type1 = self.getdata(1)
        # self.type_chart.bar_value = self.data_for_daily_type1
        # self.type_chart.hour_bar.append(self.type_chart.bar_value)
        # self.type_chart._bar_series = QtCharts.QBarSeries()
        # self.type_chart._bar_series.append(self.type_chart.hour_bar)


    def open_chart2(self):
        self.main_frame.setVisible(False)
        self.chart_frame.setVisible(True)
        # self.data_for_daily_type2 = self.getdata(2)
        # self.type_chart.bar_value = self.data_for_daily_type2


    def open_chart3(self):
        self.main_frame.setVisible(False)
        self.chart_frame.setVisible(True)
        # self.data_for_daily_type3 = self.getdata(3)
        # self.type_chart.bar_value = self.data_for_daily_type3
    
    def toggle_clicked(self):
        if self.toggle_status == 0:
            self.toggle_status = 1
            self.toggle_month.setVisible(True)
            self.toggle_day.setVisible(False)
            self.day_picker.setVisible(False)
            self.chart_widget_daily.setVisible(False)
            self.chart_widget_monthly.setVisible(True)
        elif self.toggle_status == 1:
            self.toggle_status = 0
            self.toggle_month.setVisible(False)
            self.toggle_day.setVisible(True)
            self.day_picker.setVisible(True)
            self.chart_widget_daily.setVisible(True)
            self.chart_widget_monthly.setVisible(False)
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

    def get_daily_data(self, type):
        try:
            conn = mdb.connect(host = HOST,
                    database = DATABASE,
                    user = USER,
                    password = PASSWORD)
            curr = conn.cursor()
            query = """SELECT * FROM (
            SELECT * FROM daily_statistic ORDER BY id DESC LIMIT 3) as r ORDER BY id"""
            curr.execute(query)
            current_date = list(curr.fetchall())
            data = list(current_date[type - 1])[2:]
            curr.close()
            conn.close()
        except:
            data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        return data
    
    def get_montly_data(self, type):
        conn = mdb.connect(host = HOST,
                    database = DATABASE,
                    user = USER,
                    password = PASSWORD)
        curr = conn.cursor()
        query = """SELECT * FROM (
            SELECT * FROM monthly_statistic ORDER BY id DESC LIMIT 3) as r ORDER BY id"""
        curr.execute(query)
        current_date = list(curr.fetchall())
        data = list(current_date[type - 1])[1:]
        curr.close()
        conn.close()
        return data
# Auto create 3 new rows for the new day
def auto_update_new_date():
    conn = mdb.connect(host = HOST,
                    database = DATABASE,
                    user = USER,
                    password = PASSWORD)
    curr = conn.cursor()
    query = """select * from daily_statistic where id = (select max(id) from daily_statistic);"""
    curr.execute(query)
    current_date = curr.fetchall()
    if len(current_date) == 0:
        current_date = "None"
    else:
        current_date = str(list(current_date[0])[1])
    a = datetime.today().strftime('%Y-%m-%d')
    if a != current_date:
        query = """insert into daily_statistic (time, g8, g9, g10, g11, g12, g13, g14, g15, g16, g17) 
                                    values (%s, 14, 32, 13, 15, 34, 53, 61, 13, 43, 33);"""
        row = curr.execute(query, (a,))
        conn.commit()
        query = """insert into daily_statistic (time, g8, g9, g10, g11, g12, g13, g14, g15, g16, g17) 
                                    values (%s, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);"""
        row = curr.execute(query, (a,))
        conn.commit()
        query = """insert into daily_statistic (time, g8, g9, g10, g11, g12, g13, g14, g15, g16, g17) 
                                    values (%s, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0);"""
        row = curr.execute(query, (a,))
        conn.commit()
    curr.close()
    conn.close()


auto_update_new_date()
test = MainWindow()
test.window.show()

sys.exit(test.app.exec_())
