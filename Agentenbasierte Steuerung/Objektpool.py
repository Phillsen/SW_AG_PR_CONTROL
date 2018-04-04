import pymysql
import threading
from Produktagent import Produktagent
from Transportagent import Transportagent
from Maschinenagent import Maschinenagent
from Lageragent import Lageragent
import sys
from time import sleep




class Objektpool(threading.Thread):

    def __init__(self, Host,User,PWD,Port,DB):
        threading.Thread.__init__(self)
        self.host = Host
        self.user = User
        self.pwd = PWD
        self.port = Port
        self.db = DB
        self.ressourcen = []
        self.produkte = []
        self.LagerAnlegen()
        self.TransportAgentAnlegen()
        self.RessourcenAusDBLesen()
        self.ProdukteAusDBLesen()
        self.Lagerlocation = None
        self.Transporter = None
        self.Lager = None
        self.start()

    def LagerAnlegen(self):
        self.Lager = Lageragent(0,"Lager")
        self.Lagerlocation = self.Lager
        
    def TransportAgentAnlegen(self):
        self.Transporter = Transportagent(1,self.Lagerlocation)

    def RessourcenInstanzAnlegen(self,ID,Bezeichnung,ComPort):
        Agentenvariable = "M"+str(ID)
        Agentenvariable = Maschinenagent(ID,Bezeichnung,ComPort,self)
        Agentenvariable.start()
        self.ressourcen.append(Agentenvariable)
     
    def ProduktInstanzAnlegen(self, ID, Datum, Prozessliste, Parameterliste):
        Agentenvariable = "P"+str(ID)
        Prozesse = Prozessliste.split(",")
        Parameter = Parameterliste.split(",")
        Prozesse.insert(0,"Start")
        Agentenvariable = Produktagent(ID, Datum, Prozesse, Parameter, self.ressourcen, self.Transporter, self.Lager )
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

    def run(self):
        Prgrammende = False
        while True:
           
            for n in self.produkte:
                if n.status == "done":
                    Programmende = True
                else:
                    Programmende = False
                sleep(2)
            if Programmende == True:
                for n in self.ressourcen:
                    n.Statusupdate("Sleep Mode")
                sleep(5)
                break
            else:
                sleep(0.5)
                

                