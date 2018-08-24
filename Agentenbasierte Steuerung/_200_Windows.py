import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtChart import *
from PyQt5 import QtWidgets , QtGui, QtCore, QtChart
from _000_Objektpool import Objektpool


class Fenster(QMainWindow,):

    def __init__(self,mainProgram):

        super().__init__()
        self.MainProgramm = mainProgram
        self.initMe()

    def initMe(self):
        self.counter = 0
        self.setObjectName("MainWindow")
        self.setWindowIcon(QIcon("lightbulb2.png"))
        self.resize(800,600)
        self.centralwidget = QtWidgets.QWidget(self)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.frame_3 = QtWidgets.QFrame(self.centralwidget)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame_3)
        self.verticalLayout.setObjectName("verticalLayout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.startButton = QtWidgets.QPushButton(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.startButton.setFont(font)
        self.cockpitButton = QtWidgets.QPushButton(self.frame_3)
        self.cockpitButton.setFont(font)
        self.cockpitButton.setObjectName("startButton")
        self.cockpitButton.setToolTip("Auswertung öffnen")
        self.verticalLayout.addWidget(self.cockpitButton)
        self.startButton.setObjectName("startButton")
        self.startButton.setToolTip("Startet den Simulationslauf")
        self.verticalLayout.addWidget(self.startButton)
        self.radioButton = QtWidgets.QRadioButton(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(False)
        font.setWeight(50)
        self.radioButton.setFont(font)
        self.radioButton.setObjectName("radioButton")
        self.radioButton.setToolTip("Deaktiviert die physischen Repräsentanten")
        self.radioButton.setChecked(True)
        self.verticalLayout.addWidget(self.radioButton)
        self.gridLayout.addWidget(self.frame_3, 2, 1, 1, 1)
        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView.setStyleSheet("background-image: url(C:/Users/Phili/Documents/Studium/Master/Thesis/03 Umsetzung/Python Software/Agentenbasierte Steuerung/Agentenbasierte Steuerung/Cozmo_Background.png);")
        self.gridLayout.addWidget(self.graphicsView, 1, 0, 2, 2)
        self.graphicsView.raise_()
        self.frame_3.raise_()
        self.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)
        self.statusBar().showMessage("Programmiert von Philip Diem")
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self)
        self.startButton.clicked.connect(self.StartSimulation)
        self.cockpitButton.clicked.connect(self.Auswertung)
        # Create a QTimer
        self.timer = QTimer(self)
        # Connect it to f
        self.timer.timeout.connect(self.Auswertung)
        # Call f() every 5 seconds
        self.show()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Agentenbasierte Produktionssteuerung"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.cockpitButton.setText(_translate("MainWindow", "Auswertung"))
        self.radioButton.setText(_translate("MainWindow", "Simu Modus"))

    def StartSimulation(self):
        Simulation = self.radioButton.isChecked()
        self.startButton.hide()
        self.MainProgramm.UseCozmo(Simulation)
        self.MainProgramm.SimuStart()

    def Auswertung(self):
        self.MainProgramm.Auswertung()
        print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        
    def OpenDBManupulation(self):
        pass


class CockpitWidget(QWidget):

    def __init__(self, mainProgram):
        super().__init__()
        self.DB = mainProgram
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
        self.productWaiting = QBarSet("Wartezeit")
        self.productWaiting.setColor(QColor("red"))
        self.productProcessing = QBarSet("Prozesszeit")
        self.productProcessing.setColor(QColor("green"))
        self.productTransport = QBarSet("Transportzeit")
        self.productTransport.setColor(QColor("yellow"))
       
        # Variablen hier einfügen ------------------------------------------------------------------------------
        for Eintrag in self.DB.produkte:
            Wartezeit = Eintrag.waitTime
            TransportZeit = Eintrag.transportTime
            ProzessZeit = Eintrag.processTime
            self.productWaiting.append(Wartezeit)
            self.productProcessing.append(ProzessZeit)
            self.productTransport.append(TransportZeit)
        
        # Variablen hier einfügen ------------------------------------------------------------------------------
        self.productSeries = QStackedBarSeries()
        self.productSeries.append(self.productWaiting)
        self.productSeries.append(self.productTransport)
        self.productSeries.append(self.productProcessing)
        self.machineIdle = QBarSet("Wartet")
        self.machineProcessing = QBarSet("Arbeitet")

        # Variablen hier einfügen ------------------------------------------------------------------------------
        self.machineIdle.append([self.DB.ressourcen[0].waitTime, self.DB.ressourcen[1].waitTime, self.DB.ressourcen[2].waitTime, self.DB.ressourcen[3].waitTime, self.DB.ressourcen[4].waitTime])
        self.machineProcessing.append([self.DB.ressourcen[0].processTime, self.DB.ressourcen[1].processTime, self.DB.ressourcen[2].processTime, self.DB.ressourcen[3].processTime, self.DB.ressourcen[4].processTime])

        # Variablen hier einfügen ------------------------------------------------------------------------------
        self.machineSeries = QPercentBarSeries()
        self.machineSeries.append(self.machineIdle)
        self.machineSeries.append(self.machineProcessing)
        self.productChart = QChart()
        self.machineChart = QChart()
        self.productChart.addSeries(self.productSeries)
        self.machineChart.addSeries(self.machineSeries)
        self.productChart.setTitle("Zusammensetzung der DLZ")
        self.machineChart.setTitle("Prozentuale Statusverteilung")
        self.productChart.setAnimationOptions(QChart.SeriesAnimations)
        self.machineChart.setAnimationOptions(QChart.SeriesAnimations)

        self.productCategories = []
        self.machineCategories = []

        for Eintraege in self.DB.produkte:
            Balkenbezeichnung = "Produkt " +str(Eintraege.ID)
            self.productCategories.append(Balkenbezeichnung)
        
        for Eintrag in self.DB.ressourcen:
            RessourcenBezeichnung = Eintrag.bezeichnung
            self.machineCategories.append(RessourcenBezeichnung)
        
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