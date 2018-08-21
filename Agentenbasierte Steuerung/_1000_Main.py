# Modulimporte
import sys
from PyQt5.QtWidgets import *
import threading
import multiprocessing
import pymysql
from _100_Agents import Lageragent, Maschinenagent, Produktagent, Transportagent
from _200_Windows import Fenster, CockpitWidget
import _300_Cozmo
import random
import time


class main(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.simulation = None 
        self.host = "localhost"
        self.user = "AgentenSystem"
        self.pwd = "ProzessDB"
        self.port = 3306
        self.db = "prozessdaten"
        self.ressourcen = []
        self.produkte = []
        self.Lagerlocation = None
        self.Transporter = None
        self.Lager = None
        self.FensterAnlegen()
        self.start()

    def FensterAnlegen(self):
        self.App = QApplication(sys.argv)
        self.Hauptfenster = Fenster(self)
        sys.exit(self.App.exec_())

    def LagerAnlegen(self):
        # Lagerposition lorrekt anlegen <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<< To Do
        self.Lager = Lageragent(0,(0,0),"Lager")
        self.Lagerlocation = self.Lager.location

    def TransportAgentAnlegen(self):
        self.Transporter = Transportagent(1,self.Lagerlocation,self)
        
    def RessourcenInstanzAnlegen(self,ID,Bezeichnung,ComPort):
        Agentenvariable = "M"+str(ID)
        Agentenvariable = Maschinenagent(ID,Bezeichnung,ComPort,self, self.simulation, (0,0))
        Agentenvariable.start()
        self.ressourcen.append(Agentenvariable)
     
    def ProduktInstanzAnlegen(self, ID, Datum, Prozessliste, Parameterliste):
        Agentenvariable = "P"+str(ID)
        Prozesse = Prozessliste.split(",")
        Parameter = Parameterliste.split(",")
        Prozesse.insert(0,"Start")
        Agentenvariable = Produktagent(ID, Datum, Prozesse, Parameter, self.ressourcen, self.Transporter, self.Lager)
        Agentenvariable.start()
        self.produkte.append(Agentenvariable)
     
    def RessourcenAusDBLesen(self):
        conn = pymysql.connect(host=self.host, user=self.user, passwd=self.pwd, port=self.port, db=self.db)
        cursor = conn.cursor()
        sql = ('SELECT * FROM ressourcen')
        cursor.execute(sql)
        data = cursor.fetchall()
        for n in data:
            self.RessourcenInstanzAnlegen(n[0],n[1],n[2])
            print("{0} ist Online".format(n))
        conn.close()

    def ProdukteAusDBLesen(self):
        conn = pymysql.connect(host=self.host, user=self.user, passwd=self.pwd, port=self.port, db=self.db)
        cursor = conn.cursor()
        sql = ('SELECT * FROM produkte')
        cursor.execute(sql)
        data = cursor.fetchall()

        for n in data:
            self.ProduktInstanzAnlegen(n[0],n[1],n[2],n[3])
        conn.close()

    def RessourcenListe(self, Process):
        for n in self.produkte:
            if n.bezeichnung == Process:
                return n
    
    def UseCozmo(self, Simubutton):
        self.simulation = Simubutton
            
    def SimuStart(self):
        self.LagerAnlegen()
        self.RessourcenAusDBLesen()
        self.TransportAgentAnlegen()
        time.sleep(1)
        
        self.ProdukteAusDBLesen()
     
    def Auswertung(self):
        self.Auswertefenster = CockpitWidget(self)
        self.Auswertefenster.show() 
        
    def run(self):
        while True:
            pass


if __name__ == '__main__':
    
    main()
