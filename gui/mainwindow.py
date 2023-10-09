# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCharts import QChartView
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDoubleSpinBox, QHBoxLayout, QLabel,
    QLayout, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QSpacerItem, QSpinBox, QTabWidget,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(700, 500)
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        MainWindow.setDocumentMode(False)
        MainWindow.setTabShape(QTabWidget.Rounded)
        MainWindow.setDockOptions(QMainWindow.AllowTabbedDocks|QMainWindow.AnimatedDocks)
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setEnabled(True)
        self.centralwidget.setMinimumSize(QSize(0, 0))
        self.centralwidget.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.main_hlayout = QHBoxLayout()
        self.main_hlayout.setObjectName(u"main_hlayout")
        self.main_hlayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.main_hlayout.setContentsMargins(10, 10, 10, 10)
        self.left_vlayout = QVBoxLayout()
        self.left_vlayout.setObjectName(u"left_vlayout")
        self.broker_info_hlayout = QHBoxLayout()
        self.broker_info_hlayout.setObjectName(u"broker_info_hlayout")
        self.broker_lbl = QLabel(self.centralwidget)
        self.broker_lbl.setObjectName(u"broker_lbl")

        self.broker_info_hlayout.addWidget(self.broker_lbl)

        self.broker_hostname = QLineEdit(self.centralwidget)
        self.broker_hostname.setObjectName(u"broker_hostname")

        self.broker_info_hlayout.addWidget(self.broker_hostname)

        self.broker_port = QSpinBox(self.centralwidget)
        self.broker_port.setObjectName(u"broker_port")
        self.broker_port.setMaximum(65535)
        self.broker_port.setValue(1883)

        self.broker_info_hlayout.addWidget(self.broker_port)


        self.left_vlayout.addLayout(self.broker_info_hlayout)

        self.broker_connect_hlayout = QHBoxLayout()
        self.broker_connect_hlayout.setObjectName(u"broker_connect_hlayout")
        self.horizontalSpacer_2 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.broker_connect_hlayout.addItem(self.horizontalSpacer_2)

        self.broker_connect_btn = QPushButton(self.centralwidget)
        self.broker_connect_btn.setObjectName(u"broker_connect_btn")
        self.broker_connect_btn.setCursor(QCursor(Qt.PointingHandCursor))

        self.broker_connect_hlayout.addWidget(self.broker_connect_btn)


        self.left_vlayout.addLayout(self.broker_connect_hlayout)

        self.chart = QChartView(self.centralwidget)
        self.chart.setObjectName(u"chart")

        self.left_vlayout.addWidget(self.chart)

        self.temp_hlayout = QHBoxLayout()
        self.temp_hlayout.setObjectName(u"temp_hlayout")
        self.horizontalSpacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.temp_hlayout.addItem(self.horizontalSpacer)

        self.set_temp_lbl = QLabel(self.centralwidget)
        self.set_temp_lbl.setObjectName(u"set_temp_lbl")

        self.temp_hlayout.addWidget(self.set_temp_lbl)

        self.set_temp_input = QDoubleSpinBox(self.centralwidget)
        self.set_temp_input.setObjectName(u"set_temp_input")
        self.set_temp_input.setMinimum(22.000000000000000)
        self.set_temp_input.setMaximum(42.000000000000000)
        self.set_temp_input.setValue(36.000000000000000)

        self.temp_hlayout.addWidget(self.set_temp_input)

        self.set_temp_btn = QPushButton(self.centralwidget)
        self.set_temp_btn.setObjectName(u"set_temp_btn")

        self.temp_hlayout.addWidget(self.set_temp_btn)


        self.left_vlayout.addLayout(self.temp_hlayout)

        self.save_hlayout = QHBoxLayout()
        self.save_hlayout.setObjectName(u"save_hlayout")
        self.horizontalSpacer_3 = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.save_hlayout.addItem(self.horizontalSpacer_3)

        self.save_data_btn = QPushButton(self.centralwidget)
        self.save_data_btn.setObjectName(u"save_data_btn")

        self.save_hlayout.addWidget(self.save_data_btn)


        self.left_vlayout.addLayout(self.save_hlayout)


        self.main_hlayout.addLayout(self.left_vlayout)


        self.horizontalLayout.addLayout(self.main_hlayout)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Temperature monitor", None))
        self.broker_lbl.setText(QCoreApplication.translate("MainWindow", u"Broker", None))
#if QT_CONFIG(tooltip)
        self.broker_hostname.setToolTip(QCoreApplication.translate("MainWindow", u"Broker hostname", None))
#endif // QT_CONFIG(tooltip)
        self.broker_hostname.setText(QCoreApplication.translate("MainWindow", u"192.168.4.1", None))
        self.broker_hostname.setPlaceholderText(QCoreApplication.translate("MainWindow", u"hostname", None))
#if QT_CONFIG(tooltip)
        self.broker_port.setToolTip(QCoreApplication.translate("MainWindow", u"Broker port (1-65535)", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.broker_connect_btn.setToolTip(QCoreApplication.translate("MainWindow", u"Connect to broker", None))
#endif // QT_CONFIG(tooltip)
        self.broker_connect_btn.setText(QCoreApplication.translate("MainWindow", u"Connect to broker", None))
        self.set_temp_lbl.setText(QCoreApplication.translate("MainWindow", u"Temperature (\u00b0C)", None))
        self.set_temp_btn.setText(QCoreApplication.translate("MainWindow", u"Set", None))
        self.save_data_btn.setText(QCoreApplication.translate("MainWindow", u"Save data", None))
    # retranslateUi

