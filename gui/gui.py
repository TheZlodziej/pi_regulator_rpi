import sys
import json
import paho.mqtt.client as mqtt
from datetime import datetime
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout,
                               QLineEdit, QSpinBox, QPushButton, QLabel, QWidget)
from PySide6 import QtCharts
from PySide6.QtCore import Qt, QDateTime

data_points = []

class MQTTApp(QMainWindow):
    def __init__(self):
        super().__init__()

        # Initial MQTT setup
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_message = self.on_message

        # GUI setup
        self.setWindowTitle("MQTT Chart")
        self.setGeometry(100, 100, 800, 600)

        layout = QVBoxLayout()
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        central_widget.setLayout(layout)

        # Hostname and Port setup
        connection_layout = QHBoxLayout()
        layout.addLayout(connection_layout)

        connection_layout.addWidget(QLabel("Hostname:"))
        self.hostname_input = QLineEdit("192.168.0.21")
        connection_layout.addWidget(self.hostname_input)

        connection_layout.addWidget(QLabel("Port:"))
        self.port_input = QLineEdit("1883")
        connection_layout.addWidget(self.port_input)

        self.connect_btn = QPushButton("Połącz")
        self.connect_btn.clicked.connect(self.connect_to_broker)
        connection_layout.addWidget(self.connect_btn)

        # Chart setup
        self.chart = QtCharts.QChart()
        self.chart_view = QtCharts.QChartView(self.chart)
        layout.addWidget(self.chart_view)

        self.temp_set_series = QtCharts.QLineSeries()
        self.temp_series = QtCharts.QLineSeries()
        self.chart.addSeries(self.temp_set_series)
        self.chart.addSeries(self.temp_series)

        self.axisX = QtCharts.QDateTimeAxis()
        self.axisX.setTitleText("Time")
        self.axisX.setFormat("hh:mm:ss")
        self.axisY = QtCharts.QValueAxis()
        self.axisY.setTitleText("Temperature (°C)")
        self.axisY.setRange(0, 50)

        self.chart.addAxis(self.axisX, Qt.AlignBottom)
        self.chart.addAxis(self.axisY, Qt.AlignLeft)

        self.temp_set_series.attachAxis(self.axisX)
        self.temp_set_series.attachAxis(self.axisY)
        self.temp_series.attachAxis(self.axisX)
        self.temp_series.attachAxis(self.axisY)

        layout.addWidget(QLabel("Zadaj temperaturę:"))

        self.spin_box = QSpinBox(self)
        self.spin_box.setRange(22, 40)
        layout.addWidget(self.spin_box)

        self.set_temp_btn = QPushButton("Zadaj temperaturę")
        self.set_temp_btn.clicked.connect(self.on_set_temp_button_pressed)
        layout.addWidget(self.set_temp_btn)

        self.save_data_btn = QPushButton("Zapisz dane")
        self.save_data_btn.clicked.connect(self.on_save_data_button_pressed)
        layout.addWidget(self.save_data_btn)

    def connect_to_broker(self):
        if self.mqtt_client.is_connected():
            self.mqtt_client.disconnect()
        hostname = self.hostname_input.text()
        port = int(self.port_input.text())
        self.mqtt_client.connect(hostname, port, 60)
        self.mqtt_client.subscribe("uC/get")
        self.mqtt_client.loop_start()

    def on_message(self, client, userdata, msg):
        payload = json.loads(msg.payload.decode())
        temp_set = payload['temp_set']
        temp = payload['temp']
        timestamp = QDateTime.currentDateTime()

        # Update chart
        self.temp_set_series.append(timestamp.toMSecsSinceEpoch(), temp_set)
        self.temp_series.append(timestamp.toMSecsSinceEpoch(), temp)

        # Adjust the X axis range
        if len(self.temp_set_series.points()) > 1:
            self.axisX.setMin(self.temp_set_series.at(0).x())
            self.axisX.setMax(self.temp_set_series.at(-1).x())

        # Store data
        data_points.append({"temp": temp, "temp_set": temp_set, "t": timestamp.toString('yyyy-MM-dd hh:mm:ss')})

    def on_set_temp_button_pressed(self):
        temp_set_value = self.spin_box.value()
        payload = {"temp_set": temp_set_value}
        self.mqtt_client.publish("uC/set", json.dumps(payload))

    def on_save_data_button_pressed(self):
        with open('data_points.json', 'w') as f:
            json.dump(data_points, f, indent=4)

    def closeEvent(self, event):
        if self.mqtt_client.is_connected():
            self.mqtt_client.disconnect()
            self.mqtt_client.loop_stop()

if __name__ == '__main__':
    app = QApplication([])
    window = MQTTApp()
    window.show()
    sys.exit(app.exec_())
