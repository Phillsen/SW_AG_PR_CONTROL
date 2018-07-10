import sys
import Window
import Objektpool

#Datenbank abfragen
      
#Entsprechend viele Agenteninstanzen anlegen

#GUI-Instanz parametrisieren, anlegen und starten




def StartSimuRun():
    # Die Agenten Starten
    print("Test------------------------------------Test-----------------------------------Test---------------------------------Test")
    pass     

def StartGUI():
    Mainwindow = Window.Fenster(StartSimuRun)
    

def main():

    # Hauptfenster Anlegen und öffnen
    StartGUI()
    app = QApplication(sys.argv)
    sys.exit(app.exec_())
    






main()