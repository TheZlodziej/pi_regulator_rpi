from mainwindow import Ui_MainWindow
from PySide6.QtWidgets import QMainWindow, QApplication
from paho.mqtt.client import Client
from json import dumps, loads
from time import time
from PySide6.QtCharts import QScatterSeries, QLineSeries, QChart
from PySide6.QtGui import QPainter

class RegBackend():
    def __init__(self):
        self.__client = Client()
        self.__client.subscribe("uC/get")
       
    def set_on_message_cb(self, cb):
        self.__client.on_message = cb

    def connect(self, host, port):
        self.__client.loop_stop()
        print("Connecting to broker...")
        try:
            self.__client.connect(host, port)
            self.__client.subscribe("uC/get")
            self.__client.loop_start()
        except ConnectionError:
            print("Error connecting to broker")
            return False
        except Exception:
            print("Unknown error when connecting to broker")
            return False
        print("Connected.")
        return True

    def send_new_value(self, value):
        # format
        # { "temp_set": <value> }
        if self.__client.is_connected():
            self.__client.publish("uC/set", dumps({"temp_set": value}))

class RegMainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self, backend):
        super(RegMainWindow, self).__init__()
        self.setupUi(self)

        self.__temp_series = QScatterSeries()
        self.__temp_series.setMarkerSize(8)
        self.__temp_series.setColor("#ff0000")
        self.__temp_series.setName("Current temperature")
        self.__temp_set_series = QLineSeries()
        self.__temp_set_series.setColor("#0000ff")
        #self.__temp_set_series.setBorderColor("#000000")
        self.__temp_set_series.setName("Set temperature")
        self.live_chart = QChart()
        self.live_chart.addSeries(self.__temp_set_series)
        self.live_chart.addSeries(self.__temp_series)
        self.live_chart.createDefaultAxes()
        self.chart.setChart(self.live_chart)
        self.chart.setRenderHint(QPainter.RenderHint.Antialiasing)
        x_axe, y_axe = self.live_chart.axes()
        x_axe.setTitleText("Time [s]")
        y_axe.setTitleText("Temperature [°C]")
        self.__start = time()

        self.__points = [] # list of { "temp_set": float, "temp": float, "t": time }
        self.__backend = backend
        self.__backend.set_on_message_cb(self.__on_message)
        self.__setup_connects()

    def __on_message(self, client, userdata, message):
        def validate(d):
            if d.get("temp_set") and d.get("temp"):
                return True
            return False
        
        data = loads(message.payload)
        if not validate(data):
            return
        
        temp_set = data.get("temp_set")
        temp = data.get("temp")
        t = time() - self.__start
        self.__points.append({
            "temp_set": temp_set,
            "temp": temp,
            "t": t
        })
        self.__temp_series.append(t, temp)
        self.__temp_set_series.append(t, temp_set)
        x_ax, y_ax = self.live_chart.axes()

        min_x = self.__points[0]["t"] if len(self.__points) > 0 else 0
        x_ax.setRange(min_x, t)
        y_ax.setRange(min_x, 45)
        
        
    def __setup_connects(self):
        def on_connect_btn_clicked():
            if self.__backend.connect(self.broker_hostname.text(), self.broker_port.value()):
                self.__points.clear()
                self.__start = time()
            
        def on_set_temp_btn_clicked():
            self.__backend.send_new_value(self.set_temp_input.value())

        def on_save_data_btn_clicked():
            with open("output.json", "w") as output:
                output.write(dumps(self.__points))
                self.__points.clear()

        self.broker_connect_btn.clicked.connect(on_connect_btn_clicked)
        self.set_temp_btn.clicked.connect(on_set_temp_btn_clicked)
        self.save_data_btn.clicked.connect(on_save_data_btn_clicked)

if __name__ == '__main__':
    try:
        app = QApplication()
        window = RegMainWindow(RegBackend())
        window.show()
        app.exec()
    except KeyboardInterrupt:
        app.quit()
    except Exception as e:
        print(e)