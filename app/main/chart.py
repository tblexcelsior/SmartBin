from PySide2.QtCharts import QtCharts
import PySide2
from PySide2.QtCore import Qt
class Bar_Chart(QtCharts.QChart):
    def __init__(self) -> None:
        super().__init__()
        self.setGeometry(0, 0, 980, 550)
        self.hour_bar = QtCharts.QBarSet('Number of Wastes')
        self.bar_value =  [0,0,0,0,0,0,0,0,0,0,0,0]
        self.hour_bar.append(self.bar_value)
        self._bar_series = QtCharts.QBarSeries()
        self._bar_series.append(self.hour_bar)


        self.addSeries(self._bar_series)
        self.setTitle("Daily Statistic")

        self.hours = ['Type1', 'Type2', 'Type3','8:00', '9:00', '10:00', '11:00', '12:00', '13:00', '14:00', '15:00', '16:00', '17:00']
        self._axis_x = QtCharts.QBarCategoryAxis()
        self._axis_x.append(self.hours)
        self.setAxisX(self._axis_x, self._bar_series)
        self._axis_x.setRange('8:00', '17:00')

        self._axis_y = QtCharts.QValueAxis()
        self.setAxisY(self._axis_y, self._bar_series)
        # self._axis_y.setRange(0, max(self.bar_value))
        # self._axis_y.setRange(0, 30)

        self.legend().setVisible(True)
        self.legend().setAlignment(Qt.AlignBottom)

    def update_data(self, data):
        self.removeAllSeries()
        self.hour_bar = QtCharts.QBarSet('Number of Wastes')
        self.hour_bar.append(data)
        self._bar_series = QtCharts.QBarSeries()
        self._bar_series.append(self.hour_bar)
        self.addSeries(self._bar_series)
        self._axis_y.setRange(0, max(data))
    



class Bar_Chart2(QtCharts.QChart):
    def __init__(self) -> None:
        super().__init__()
        self.setGeometry(0, 0, 980, 550)
        self.hour_bar = QtCharts.QBarSet('Number of Wastes')
        self.bar_value =  [0,0,0,0,0,0,0,0,0,0,0,0]
        self.hour_bar.append(self.bar_value)

        self._bar_series = QtCharts.QBarSeries()
        self._bar_series.append(self.hour_bar)


        self.addSeries(self._bar_series)
        self.setTitle("Monthly Statistic")
        self.Month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        self._axis_x = QtCharts.QBarCategoryAxis()
        self._axis_x.append(self.Month)
        self.setAxisX(self._axis_x, self._bar_series)
        self._axis_x.setRange('Jan', 'Dec')

        self._axis_y = QtCharts.QValueAxis()
        self.setAxisY(self._axis_y, self._bar_series)
        # self._axis_y.setRange(0, max(self.bar_value))
        # self._axis_y.setRange(0, 30)

        self.legend().setVisible(True)
        self.legend().setAlignment(Qt.AlignBottom)

    def update_data(self, data):
        self.removeAllSeries()
        self.hour_bar = QtCharts.QBarSet('Number of Wastes')
        self.hour_bar.append(data)
        self._bar_series = QtCharts.QBarSeries()
        self._bar_series.append(self.hour_bar)
        self.addSeries(self._bar_series)
        self._axis_y.setRange(0, max(data))