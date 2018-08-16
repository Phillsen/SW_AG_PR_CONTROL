from time import sleep
import _100_Agentenklasse

class Produktagent(_100_Agentenklasse.Agent):
    
    def __init__(self, ID, DueDate, ProcessList, Prozessparameter, RessourcenListe, Transporter, Location, Bezeichnung="Produkt"):
        super().__init__(ID, Location, Bezeichnung)
        self.Transporter = Transporter
        self.processList = ProcessList
        self.processparameter = Prozessparameter
        self.ressourcenliste = RessourcenListe
        self.currentStep = 0
        self.dueDate = DueDate
        self.nextStep = self.currentStep+1
        self.destination = None
        self.lagerLocation = Location
        self.status = "idle"   # idle, wait, busy, transport
        self.done = False
        self.busyTime = 0
        
    def CheckForTasks(self):
        self.StatusUpdate("busy")
        self.print("Überprüfe offene aufgaben...")
        self.Zielwahl()
        self.AnmeldenBeiMaschine()
        self.Transportrequest()
        self.StatusUpdate("wait")
            
    def Infoverarbeitung(self, Info):
        if Info == "Abtransport":
            self.StatusUpdate("transport")
        if Info == "Ankunft":
            self.StatusUpdate("wait")
        if Info == "Prozessstart":
            self.StatusUpdate("processing")
        if Info == "Prozessende":

            if  self.nextStep != len(self.processList)-1:
                self.nextStep+=1
                self.currentStep+=1
                self.StatusUpdate("idle")
            else:
                self.destination = self.lagerLocation
                self.Transportrequest()
        if Info == "Fertig":
            self.StatusUpdate("done")
            self.done = True
     
    def Zielwahl(self):
        self.print("Suche nächstes Ziel")
        
        if self.nextStep > len(self.processList):
            self.destination = self.lagerLocation
        else:
            Zielbezeichnung = self.processList[self.nextStep]
            self.destination = next((x for x in self.ressourcenliste if x.bezeichnung == Zielbezeichnung), None)
            self.print("nächstes Ziel = Ressource" + str(self.destination.ID) + "(" + self.destination.bezeichnung + ")")
        
    def Transportrequest(self):
        self.print("Fordere Transport an.")
        #Einen Weg finden den Transporter anzusprechen
        self.Transporter.Transportrequest(self)

    def AnmeldenBeiMaschine(self):
        self.print("Melde mich bei " +self.destination.bezeichnung +" an.")
        self.destination.Anmeldung(self.ID, self)

    def run(self):
        while True:
            if self.status == "idle":
                self.CheckForTasks()

            if self.done == True:
                break
            else: 
                sleep(0.1)

