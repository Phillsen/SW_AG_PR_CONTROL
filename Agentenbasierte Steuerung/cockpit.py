import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets , QtGui, QtCore, QtChart
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtChart import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import threading
import time

class CockpitWidget(QWidget):

    def __init__(self, Objektpool):
        super().__init__()
        self.DB = Objektpool
        self.initMe()
        

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
         
        self.productWaiting = QBarSet("Waiting")
        self.productWaiting.setColor(QColor("red"))
        self.productProcessing = QBarSet("Processing")
        self.productProcessing.setColor(QColor("green"))
        self.productTransport = QBarSet("Transport")
        self.productTransport.setColor(QColor("yellow"))
        self.productBusy = QBarSet("Busy")
        self.productBusy.setColor(QColor("blue"))


        # Variablen hier einfügen ------------------------------------------------------------------------------
        
        self.productWaiting.append([self.DB.produkte[0].waitTime, self.DB.produkte[1].waitTime, self.DB.produkte[2].waitTime, self.DB.produkte[3].waitTime,self.DB.produkte[4].waitTime, self.DB.produkte[5].waitTime ])
        self.productProcessing.append([self.DB.produkte[0].processTime, self.DB.produkte[1].processTime, self.DB.produkte[2].processTime, self.DB.produkte[3].processTime, self.DB.produkte[4].processTime, self.DB.produkte[5].processTime])
        self.productTransport.append([self.DB.produkte[0].transportTime, self.DB.produkte[1].transportTime, self.DB.produkte[2].transportTime, self.DB.produkte[3].transportTime, self.DB.produkte[4].transportTime, self.DB.produkte[5].transportTime])
        self.productBusy.append([self.DB.produkte[0].busyTime, self.DB.produkte[1].busyTime, self.DB.produkte[2].busyTime, self.DB.produkte[3].busyTime, self.DB.produkte[4].busyTime, self.DB.produkte[5].busyTime])
                
        
        # Variablen hier einfügen ------------------------------------------------------------------------------
        
        self.productSeries = QStackedBarSeries()
        self.productSeries.append(self.productBusy)
        self.productSeries.append(self.productWaiting)
        self.productSeries.append(self.productTransport)
        self.productSeries.append(self.productProcessing)
        
        


        self.machineIdle = QBarSet("Idle")
        self.machineProcessing = QBarSet("Processing")
        self.machineBusy = QBarSet("Busy")


        # Variablen hier einfügen ------------------------------------------------------------------------------

        self.machineIdle.append([self.DB.ressourcen[0].waitTime, self.DB.ressourcen[1].waitTime, self.DB.ressourcen[2].waitTime, self.DB.ressourcen[3].waitTime, self.DB.ressourcen[4].waitTime])
        self.machineProcessing.append([self.DB.ressourcen[0].processTime, self.DB.ressourcen[1].processTime, self.DB.ressourcen[2].processTime, self.DB.ressourcen[3].processTime, self.DB.ressourcen[4].processTime])
        self.machineBusy.append([self.DB.ressourcen[0].busyTime, self.DB.ressourcen[1].busyTime, self.DB.ressourcen[2].busyTime, self.DB.ressourcen[3].busyTime, self.DB.ressourcen[4].busyTime])

        # Variablen hier einfügen ------------------------------------------------------------------------------



        self.machineSeries = QPercentBarSeries()
        self.machineSeries.append(self.machineIdle)
        self.machineSeries.append(self.machineProcessing)
        self.machineSeries.append(self.machineBusy)


        self.productChart = QChart()
        self.machineChart = QChart()

        self.productChart.addSeries(self.productSeries)
        self.machineChart.addSeries(self.machineSeries)

        self.productChart.setTitle("Zusammensetzung der DLZ")
        self.machineChart.setTitle("Prozentuale Statusverteilung")
        self.productChart.setAnimationOptions(QChart.SeriesAnimations)
        self.machineChart.setAnimationOptions(QChart.SeriesAnimations)

        self.productCategories = ["Produkt 1", "Produkt 2", "Produkt 3", "Produkt 4", "Produkt 5", "Produkt 6"]
        self.machineCategories = ["Schweissen", "Montieren", "Kalibrieren", "Prüfen", "Verpacken"]

        self.productAxis = QBarCategoryAxis()
        self.machineAxis = QBarCategoryAxis()

        self.productAxis.append(self.productCategories)
        self.machineAxis.append(self.machineCategories)
        self.machineChart.createDefaultAxes()
        self.machineChart.setAxisX(self.machineAxis,self.machineSeries)
        self.productChart.createDefaultAxes()
        self.productChart.setAxisX(self.productAxis, self.productSeries)

        self.productChart.legend().setVisible(True)
        self.machineChart.legend().setVisible(True)
        self.productChart.legend().setAlignment(Qt.AlignBottom)
        self.machineChart.legend().setAlignment(Qt.AlignBottom)

        self.productChartView = QChartView(self.productChart,self.machineFrame)
        self.verticalLayout_2.addWidget(self.productChartView)
        self.machineChartView = QChartView(self.machineChart,self.productFrame)
        self.verticalLayout_3.addWidget(self.machineChartView)
        
        self.productChartView.setRenderHint(QPainter.Antialiasing)
        self.machineChartView.setRenderHint(QPainter.Antialiasing)

        self.productChartView.resize(600, 300)
        self.machineChartView.resize(600, 300)
        self.productChartView.setWindowTitle("Produktstatus")
        self.machineChartView.setWindowTitle("Maschinenstatus")
        self.productChartView.setWindowIcon(QIcon("BarChart2.png"))
        self.machineChartView.setWindowIcon(QIcon("BarChart2.png"))
        self.productChartView.show()
        self.machineChartView.show()


        
    def retranslateUi(self, Cockpit):
        _translate = QtCore.QCoreApplication.translate
        Cockpit.setWindowTitle(_translate("Cockpit", "Cockpit"))

