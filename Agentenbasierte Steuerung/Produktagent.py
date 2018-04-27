import threading
from time import sleep
import datetime

class Produktagent(threading.Thread):
    
    def __init__(self, ProductID, DueDate, ProcessList, Prozessparameter, RessourcenListe, Transporter, Location):
        threading.Thread.__init__(self)
        self.Transporter = Transporter
        self.productID = ProductID
        self.processList = ProcessList
        self.processparameter = Prozessparameter
        self.ressourcenliste = RessourcenListe
        self.currentStep = 0
        self.dueDate = DueDate
        self.nextStep = self.currentStep+1
        self.destination = None
        self.lagerLocation = Location
        self.location = Location
        self.status = "idle"   # idle, wait, busy, transport
        self.lastStatus = None
        self.printIdent = "PA" + str(self.productID)+ ": "
        self.done = False
        self.startzeit = datetime.datetime.now()
        self.endzeit = None
        self.durchlaufzeit = None
        self.busyTime = 0
        self.processTime = 0
        self.transportTime = 0
        self.waitTime = 0
        self.idleTime = 0
        self.lastStatusChangeTimestamp = datetime.datetime.now()
        self.now = None
                                
    def Statusupdate(self, Status):
        self.lastStatus = self.status
        self.status = Status
        self.KPI_Logger()
        
    def CheckForTasks(self):
        self.Statusupdate("busy")
        self.print("Überprüfe offene aufgaben...")
        self.Zielwahl()
        self.AnmeldenBeiMaschine()
        self.Transportrequest()
        self.Statusupdate("wait")
            
    def Infoverarbeitung(self, Info):
        if Info == "Abtransport":
            self.Statusupdate("transport")
        if Info == "Ankunft":
            self.Statusupdate("wait")
        if Info == "Prozessstart":
            self.Statusupdate("processing")
        if Info == "Prozessende":

            if  self.nextStep != len(self.processList)-1:
                self.nextStep+=1
                self.currentStep+=1
                self.Statusupdate("idle")
            else:
                self.destination = self.lagerLocation
                self.Transportrequest()
        if Info == "Fertig":
            self.Statusupdate("done")
            self.done = True
           
    
    def KPI_Logger(self,):
        self.now = datetime.datetime.now()
        TimeSpanSinceLastStatus = float((self.now-self.lastStatusChangeTimestamp).total_seconds())

        if self.lastStatus == "busy":
            if self.busyTime == None:
                self.busyTime = TimeSpanSinceLastStatus
            else:
                self.busyTime = self.busyTime + TimeSpanSinceLastStatus

        elif self.lastStatus == "wait":
            if self.waitTime == None:
                self.waitTime = TimeSpanSinceLastStatus
            else:
                self.waitTime = self.waitTime + TimeSpanSinceLastStatus
            
        elif self.lastStatus == "transport":
            if self.transportTime == None:
                self.transportTime = TimeSpanSinceLastStatus
            else:
                self.transportTime = self.transportTime + TimeSpanSinceLastStatus

        elif self.lastStatus == "processing":
            if self.processTime == None:
                self.processTime = TimeSpanSinceLastStatus
            else:
                self.processTime = self.processTime + TimeSpanSinceLastStatus
        
        self.lastStatusChangeTimestamp = datetime.datetime.now()



     
    def Zielwahl(self):
        self.print("Suche nächstes Ziel")
        
        if self.nextStep > len(self.processList):
            self.destination = self.lagerLocation
        else:
            Zielbezeichnung = self.processList[self.nextStep]
            self.destination = next((x for x in self.ressourcenliste if x.bezeichnung == Zielbezeichnung), None)
            self.print("nächstes Ziel = Ressource" + str(self.destination.processID) + "(" + self.destination.bezeichnung + ")")
        
    def Transportrequest(self):
        self.print("Fordere Transport an.")
        #Einen Weg finden den Transporter anzusprechen
        self.Transporter.Transportrequest(self)

    def AnmeldenBeiMaschine(self):
        self.print("Melde mich bei " +self.destination.bezeichnung +" an.")
        self.destination.Anmeldung(self.productID, self)

    def run(self):
        while True:
            if self.status == "idle":
                self.CheckForTasks()

            if self.done == True:
                break
            else: 
                sleep(0.1)

    def print(self, Info):
        pass
        print(self.printIdent + Info)