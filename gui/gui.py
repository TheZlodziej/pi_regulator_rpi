import sys
import json
import paho.mqtt.client as mqtt
from datetime import datetime
from PySide6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QSpinBox, QLabel
from PySide6.QtCharts import QtCharts
from PySide6.QtCore import Qt

data_points = []

class MQTTApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # MQTT setup
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_message = self.on_message
        self.mqtt_client.connect("192.168.0.21", 1883, 60)
        self.mqtt_client.subscribe("uC/get")
        self.mqtt_client.loop_start()

        # GUI setup
        self.setWindowTitle("MQTT Chart")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)

        self.chart = QtCharts.QChart()
        self.chart_view = QtCharts.QChartView(self.chart)
        layout.addWidget(self.chart_view)

        self.temp_set_series = QtCharts.QLineSeries()
        self.temp_series = QtCharts.QLineSeries()
        self.chart.addSeries(self.temp_set_series)
        self.chart.addSeries(self.temp_series)

        self.axisX = QtCharts.QDateTimeAxis()
        self.axisX.setFormat("hh:mm:ss")
        self.axisY = QtCharts.QValueAxis()
        self.axisY.setRange(0, 50)

        self.chart.addAxis(self.axisX, Qt.AlignBottom)
        self.chart.addAxis(self.axisY, Qt.AlignLeft)

        self.temp_set_series.attachAxis(self.axisX)
        self.temp_set_series.attachAxis(self.axisY)
        self.temp_series.attachAxis(self.axisX)
        self.temp_series.attachAxis(self.axisY)

        self.spin_box = QSpinBox(self)
        self.spin_box.setRange(22, 40)
        self.spin_box.valueChanged.connect(self.on_spin_value_changed)
        layout.addWidget(QLabel("Set Temperature:"))
        layout.addWidget(self.spin_box)

    def on_message(self, client, userdata, msg):
        payload = json.loads(msg.payload.decode())
        temp_set = payload['temp_set']
        temp = payload['temp']
        timestamp = datetime.now()

        # Update chart
        self.temp_set_series.append(timestamp.timestamp() * 1000, temp_set)
        self.temp_series.append(timestamp.timestamp() * 1000, temp)

        # Update axis
        self.axisX.setRange(timestamp.timestamp() * 1000 - 60 * 1000, timestamp.timestamp() * 1000)
        
        # Store data
        data_points.append({"temp": temp, "temp_set": temp_set, "t": timestamp.strftime('%Y-%m-%d %H:%M:%S')})

    def on_spin_value_changed(self, value):
        payload = {"temp_set": value}
        self.mqtt_client.publish("uC/set", json.dumps(payload))

    def closeEvent(self, event):
        with open('data_points.json', 'w') as f:
            json.dump(data_points, f, indent=4)
        self.mqtt_client.disconnect()
        self.mqtt_client.loop_stop()


if __name__ == '__main__':
    app = QApplication([])
    window = MQTTApp()
    window.show()
    sys.exit(app.exec_())
    