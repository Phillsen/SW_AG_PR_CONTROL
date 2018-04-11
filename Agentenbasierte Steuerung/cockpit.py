import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets , QtGui, QtCore, QtChart
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

class CockpitWidget(QWidget):

    def __init__(self, Objektpool):
        super().__init__()
        self.initMe()
        self.DB = Objektpool

    def initMe(self):

        self.setObjectName("CockpitWidget")
        self.setWindowIcon(QIcon("BarChart2.png"))
        self.resize(1000, 800)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.productFrame = QtWidgets.QFrame(self)
        self.productFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.productFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.productFrame.setObjectName("pruductFrame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.productFrame)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout.addWidget(self.productFrame)
        self.machineFrame = QtWidgets.QFrame(self)
        self.machineFrame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.machineFrame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.machineFrame.setObjectName("machineFrame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.machineFrame)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout.addWidget(self.machineFrame)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)


        self.setObjectName("Cockpit")
          
        
        
        




        productWaiting = QBarSet("Waiting")
        productWaiting.setColor(QColor("red"))
        productProcessing = QBarSet("Processing")
        productProcessing.setColor(QColor("green"))
        productTransport = QBarSet("Transport")
        productTransport.setColor(QColor("yellow"))
        productBusy = QBarSet("Busy")
        productBusy.setColor(QColor("blue"))


        # Variablen hier einfügen ------------------------------------------------------------------------------
        productWaiting.append([2,3,2,1,2,3])
        productProcessing.append([2,4,3,4,3,4])
        productTransport.append([1,1,1,1,1,1])
        productBusy.append([1,1,1,1,1,1])
        # Variablen hier einfügen ------------------------------------------------------------------------------


        productSeries = QStackedBarSeries()
        productSeries.append(productWaiting)
        productSeries.append(productProcessing)
        productSeries.append(productTransport)
        productSeries.append(productBusy)


        machineIdle = QBarSet("Idle")
        machineProcessing = QBarSet("Processing")
        machineBusy = QBarSet("Busy")


        # Variablen hier einfügen ------------------------------------------------------------------------------

        machineIdle.append([2,3,2,1,2,3])
        machineProcessing.append([2,3,2,1,2,3])
        machineBusy.append([2,3,2,1,2,3])

        # Variablen hier einfügen ------------------------------------------------------------------------------



        machineSeries = QPercentBarSeries()
        machineSeries.append(machineIdle)
        machineSeries.append(machineProcessing)
        machineSeries.append(machineBusy)


        productChart = QChart()
        machineChart = QChart()

        productChart.addSeries(productSeries)
        machineChart.addSeries(machineSeries)

        productChart.setTitle("Zusammensetzung der DLZ")
        machineChart.setTitle("Prozentuale Statusverteilung")
        productChart.setAnimationOptions(QChart.SeriesAnimations)
        machineChart.setAnimationOptions(QChart.SeriesAnimations)

        productCategories = ["Produkt 1", "Produkt 2", "Produkt 3", "Produkt 4", "Produkt 5", "Produkt 6"]
        machineCategories = ["Schweissen", "Montieren", "Kalibrieren", "Prüfen", "Verpacken"]

        productAxis = QBarCategoryAxis()
        machineAxis = QBarCategoryAxis()

        productAxis.append(productCategories)
        machineAxis.append(machineCategories)
        machineChart.createDefaultAxes()
        machineChart.setAxisX(machineAxis,machineSeries)
        productChart.createDefaultAxes()
        productChart.setAxisX(productAxis, productSeries)

        productChart.legend().setVisible(True)
        machineChart.legend().setVisible(True)
        productChart.legend().setAlignment(Qt.AlignBottom)
        machineChart.legend().setAlignment(Qt.AlignBottom)

        productChartView = QChartView(productChart,self.machineFrame)
        self.verticalLayout_2.addWidget(productChartView)
        machineChartView = QChartView(machineChart,self.productFrame)
        self.verticalLayout_3.addWidget(machineChartView)
        
        productChartView.setRenderHint(QPainter.Antialiasing)
        machineChartView.setRenderHint(QPainter.Antialiasing)

        productChartView.resize(600, 300)
        machineChartView.resize(600, 300)
        productChartView.setWindowTitle("Produktstatus")
        machineChartView.setWindowTitle("Maschinenstatus")
        productChartView.setWindowIcon(QIcon("BarChart2.png"))
        machineChartView.setWindowIcon(QIcon("BarChart2.png"))
        productChartView.show()
        machineChartView.show()
        
    def retranslateUi(self, Cockpit):
        _translate = QtCore.QCoreApplication.translate
        Cockpit.setWindowTitle(_translate("Cockpit", "Cockpit"))


