from pkgutil import get_data
from re import A, S
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
from functools import partial
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

        ## Processing animation frame
        self.processing_animation_frame = self.window.findChild(QWidget, 'Processing')
        self.label = self.window.findChild(QLabel, 'loading')
        self.movie = QMovie("./app/component/Loading.gif")
        self.label.setMovie(self.movie)
        self.movie.start()  
        self.processing_animation_frame.setVisible(False)
        self.processing_status()
        self._timer4 = QTimer()    
        self._timer4.setInterval(500)
        self._timer4.timeout.connect(self.processing_status)
        self._timer4.start()

        
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



        self.type_chart = Bar_Chart()
        self.type_chart.setParent(self.chart_widget_daily)
        self._type_chart_view = QtCharts.QChartView(self.type_chart)
        self._type_chart_view.setRenderHint(QPainter.Antialiasing)
        self.chart_layout = QtWidgets.QHBoxLayout(self.chart_widget_daily)
        self.chart_layout.setContentsMargins(0, 0, 0, 0)
        self.chart_layout.addWidget(self._type_chart_view)

        # self.update_chart()
        self._timer1 = QTimer()    
        self._timer1.setInterval(1000)
        self._timer2 = QTimer()    
        self._timer2.setInterval(1000)
        self._timer3 = QTimer()    
        self._timer3.setInterval(1000)
        self._timer5 = QTimer()    
        self._timer5.setInterval(1000)


        self.type_chart2 = Bar_Chart2()
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
        self.sheet_1_btn.connect(self.sheet_1_btn, SIGNAL('clicked()'), partial(self.open_chart, 'type1'))

        self.sheet_2_btn = QPushButton()
        self.sheet_2_btn.setParent(self.sheet_2)
        self.sheet_2_btn.setGeometry(0, 0, 250, 400)
        self.sheet_2_btn.setStyleSheet('background-color: rgba(255, 255, 255, 0);')
        self.sheet_2_btn.connect(self.sheet_2_btn, SIGNAL('clicked()'), partial(self.open_chart, 'type2'))

        self.sheet_3_btn = QPushButton()
        self.sheet_3_btn.setParent(self.sheet_3)
        self.sheet_3_btn.setGeometry(0, 0, 250, 400)
        self.sheet_3_btn.setStyleSheet('background-color: rgba(255, 255, 255, 0);')
        self.sheet_3_btn.connect(self.sheet_3_btn, SIGNAL('clicked()'), partial(self.open_chart, 'type3'))
        ## Statistic Button
        self.stat_btn = QPushButton()
        self.stat_btn.setParent(self.stat_frame)
        self.stat_btn.setGeometry(0, 0, 200, 60)
        self.stat_btn.setStyleSheet('background-color: rgba(255, 255, 255, 0);')
        self.stat_btn.connect(self.stat_btn, SIGNAL('clicked()'), partial(self.open_chart, 'sta'))

        ## Exit button
        self.exit_btn.connect(self.exit_btn, SIGNAL('clicked()'), self.exit)
    # Callback function
    ##----------------- Need to update ------------------------##
    def open_chart(self, type):
        if type == 'type1':
            self.main_frame.setVisible(False)
            self.chart_frame.setVisible(True)
            # if self.chart_widget_monthly.isVisible():
            if self.toggle_status == 0:
                self.chart_widget_monthly.setVisible(False)
            self.type_chart._axis_x.setRange('8:00', '17:00')
            self.update_chart(type)
            self._timer1.timeout.connect(partial(self.update_chart, type))
            self._timer1.start()
        elif type == 'type2':
            self.main_frame.setVisible(False)
            self.chart_frame.setVisible(True)
            if self.toggle_status == 0:
                self.chart_widget_monthly.setVisible(False)
            self.type_chart._axis_x.setRange('8:00', '17:00')
            self.update_chart(type)
            self._timer2.timeout.connect(partial(self.update_chart, type))
            self._timer2.start()
        elif type == 'type3':
            self.main_frame.setVisible(False)
            self.chart_frame.setVisible(True)
            if self.toggle_status == 0:
                self.chart_widget_monthly.setVisible(False)
            self.type_chart._axis_x.setRange('8:00', '17:00')
            self.update_chart(type)
            self._timer3.timeout.connect(partial(self.update_chart, type))
            self._timer3.start()
        else:
            self.main_frame.setVisible(False)
            self.chart_frame.setVisible(True)
            if self.toggle_status == 0:
                self.chart_widget_monthly.setVisible(False)
            self.type_chart._axis_x.setRange('Type1', 'Type3')
            self.update_chart(type)
            self._timer5.timeout.connect(partial(self.update_chart, type))
            self._timer5.start()


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
        self.chart_widget_monthly.setVisible(True)
        self._timer1.stop()
        self._timer2.stop()
        self._timer3.stop()
        self._timer5.stop()
    ##-------------Get date date from this-----------------##
    def day_picked(self):
        self.today = datetime.today().strftime('%y,%m,%d').split(',')
        self.today = [int(i) for i in self.today]
        self.picked_day = list(str(self.day_picker.date())[-11:-1].split(','))
        self.picked_day = [int(i) for i in self.picked_day]
        print(self.today==self.picked_day)

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

    def update_chart(self, type):
        self.sum_data_daily = []
        self.data_for_monthly_type1 =  self.num_garbage('1', 'monthly')
        self.data_for_monthly_type2 =  self.num_garbage('2', 'monthly')
        self.data_for_monthly_type3 =  self.num_garbage('3', 'monthly')
        self.sum_data_monthly = [e1 + e2 + e3 for e1,e2,e3 in zip(self.data_for_monthly_type1, self.data_for_monthly_type2, self.data_for_monthly_type3)]
        self.data_for_daily_type1 =  self.num_garbage('1', 'daily')
        self.sum_data_daily.append(sum(self.data_for_daily_type1))
        self.data_for_daily_type2 =  self.num_garbage('2', 'daily')
        self.sum_data_daily.append(sum(self.data_for_daily_type2))
        self.data_for_daily_type3 =  self.num_garbage('3', 'daily') 
        self.sum_data_daily.append(sum(self.data_for_daily_type3))

        if type == 'type1':
            self.type_chart.update_data(self.data_for_daily_type1)
            self.type_chart2.update_data(self.data_for_monthly_type1)
            # print(self.data_for_daily_type1)
        elif type == 'type2':
            self.type_chart.update_data(self.data_for_daily_type2)
            self.type_chart2.update_data(self.data_for_monthly_type2)
            # print(self.data_for_daily_type2)
        elif type == 'type3':
            self.type_chart.update_data(self.data_for_daily_type3)
            self.type_chart2.update_data(self.data_for_monthly_type3)
            # print(self.data_for_daily_type3)
        else:
            self.type_chart.update_data(self.sum_data_daily)
            self.type_chart2.update_data(self.sum_data_monthly)
    def num_garbage(seft, type, time):
        if time == 'daily':
            idx = 8
            init_data = [0,0,0,0,0,0,0,0,0,0]
            query = """select g_type, hour(updated_time) as hour, count(g_type) as 
                total from garbage_statistic where day(updated_time) = day(current_date()) 
                and hour(updated_time) between 8 and 19 group by g_type, hour(updated_time);"""
        elif time == 'monthly':
            idx = 1
            query = """select g_type, month(updated_time) as month, count(g_type) as total 
           from garbage_statistic where year(updated_time) = year(current_date())  
           group by  g_type, month(updated_time);"""
            init_data = [0,0,0,0,0,0,0,0,0,0,0,0]
        conn = mdb.connect(host = HOST,
                        database = DATABASE,
                        user = USER,
                        password = PASSWORD)
        curr = conn.cursor()        
        curr.execute(query)
        current_date = list(curr.fetchall())
        curr.close()
        conn.close()
        data_list = {'1':init_data, '2':init_data, '3': init_data}
        for item in current_date:
            if item[0] == type:
                data_list[type][item[1] - idx] = item[2]
        return data_list[type]

    def processing_status(self):
        conn = mdb.connect(host = HOST,
                    database = DATABASE,
                    user = USER,
                    password = PASSWORD)
        curr = conn.cursor()
        query = """SELECT * FROM processing"""
        curr.execute(query)
        status = list(curr.fetchall()[0])[1]
        if status == 1:
            self.processing_animation_frame.setVisible(True)
        else:
            self.processing_animation_frame.setVisible(False)


test = MainWindow()
test.window.show()

sys.exit(test.app.exec_())
