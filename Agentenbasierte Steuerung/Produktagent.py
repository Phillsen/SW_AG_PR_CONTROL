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
        self.printIdent = "PA" + str(self.productID)+ ": "
        self.done = False
        self.StatusspeicherRuntime = []
        self.StatusspeicherAuswertung = [[],[],[],[],[]]
        self.startzeit = datetime.datetime.now()
        self.endzeit = None
        self.durchlaufzeit = None
                        
    def Statusupdate(self, Status):
        self.status = Status
        self.print("Status: " +str(self.status))
        self.StatusspeicherRuntime.append([Status,datetime.datetime.now()])
        
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
            self.Statusupdate("In Bearbeitung")
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
            self.endzeit = datetime.datetime.now()
            self.KPI_Auswertung()
    
    def KPI_Auswertung(self):
        self.durchlaufzeit = self.endzeit - self.startzeit
        self.print(str(self.startzeit))
        self.print(str(self.endzeit))
        self.print("Durchlaufzeit: "+ str(self.durchlaufzeit))

        for n in range(0,(len(self.StatusspeicherRuntime)-1)):
            
            Stempel = self.StatusspeicherRuntime[n]
            Stempel_2 = self.StatusspeicherRuntime[n+1]
            Beginn = Stempel[1]
            Ende = Stempel_2[1]
            Status = Stempel[0]
            Dauer = Ende-Beginn

            if Status == "idle":
                self.StatusspeicherAuswertung[0].append(Dauer)
            if Status == "busy":
                self.StatusspeicherAuswertung[1].append(Dauer)
            if Status == "transport":
                self.StatusspeicherAuswertung[2].append(Dauer)
            if Status == "wait":
                self.StatusspeicherAuswertung[3].append(Dauer)
            if Status == "In Bearbeitung":
                self.StatusspeicherAuswertung[4].append(Dauer)

     
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
                test = None
                break
            else: 
                sleep(0.1)

    def print(self, Info):
        print(self.printIdent + Info)