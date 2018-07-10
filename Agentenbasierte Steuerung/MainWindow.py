import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets , QtGui, QtCore, QtChart
from Objektpool import Objektpool
from cockpit import *


class Fenster(QMainWindow,):
    def __init__(self):

        super().__init__()
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
        self.DB_Button = QtWidgets.QPushButton(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.DB_Button.setFont(font)
        self.DB_Button.setObjectName("DB_Button")
        self.DB_Button.setToolTip("Datenbankeinträge anzeigen & ändern")
        self.verticalLayout.addWidget(self.DB_Button)
        self.startButton = QtWidgets.QPushButton(self.frame_3)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.startButton.setFont(font)
        self.cockpitButton = QtWidgets.QPushButton(self.frame_3)
        self.cockpitButton.setFont(font)
        self.cockpitButton.setObjectName("startButton")
        self.cockpitButton.setToolTip("Auswertung öffnen")
        self.cockpitButton.hide()
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

        # Create a QTimer
        self.timer = QTimer(self)
        # Connect it to f
        self.timer.timeout.connect(self.Auswertung)
        # Call f() every 5 seconds
        self.show()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Agentenbasierte Produktionssteuerung"))
        self.DB_Button.setText(_translate("MainWindow", "Datenbank öffnen"))
        self.startButton.setText(_translate("MainWindow", "Start"))
        self.cockpitButton.setText(_translate("MainWindow", "Auswertung"))
        self.radioButton.setText(_translate("MainWindow", "Simu Modus"))

    def StartSimulation(self):

        Simulation = self.radioButton.isChecked()
        self.startButton.hide()
        self.DB = Objektpool("localhost","AgentenSystem","ProzessDB",3306,"prozessdaten",Simulation)  
        self.timer.start(500)

    def Auswertung(self):
        if self.DB.Programmende == True:
         self.C = CockpitWidget(self.DB)
         self.C.show()  
         self.timer.stop()

    def OpenDBManupulation(self):
        pass


app = QApplication(sys.argv)
w = Fenster()

sys.exit(app.exec_())



