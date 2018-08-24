import threading
import datetime
import operator
import serial
import multiprocessing
from time import sleep
import _300_Cozmo

Transportdauer = 1
Speedup = 50
Transportliste = None
Feedback = None

class Agent(threading.Thread):

    def __init__(self, ID, Location, Bezeichnung):
        threading.Thread.__init__(self)
        self.ID = ID
        self.location = Location
        self.bezeichnung = Bezeichnung
        self.printIdent = Bezeichnung + " " + str(self.ID)+ ": "
        self.status = None
        self.lastStatus = None
        self.busyTime = 0
        self.processTime = 0
        self.waitTime = 0
        self.transportTime = 0
        self.idleTime = 0
        self.lastStatusChangeTimestamp = datetime.datetime.now()
        self.startzeit = datetime.datetime.now()
        self.endzeit = None
        self.durchlaufzeit = None
        self.now = None
        

    def print(self, Info):
        print(self.printIdent + Info)

    def StatusUpdate(self,Status):
        self.lastStatus = self.status
        self.status = Status
        self.KPI_Logger()

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


class Maschinenagent(Agent):
    serial_port = serial.Serial()
    serial_port.baudrate
    serial_port.timeout
    serial_port.port

    def __init__(self, ID, Bezeichnung,ComPort,DB, Simulation, Location):
        super().__init__(ID, Location, Bezeichnung)
        self.simulation = Simulation 
        self.DB = DB
        self.serial_port = serial.Serial()
        self.serial_port.baudrate = 9600
        self.serial_port.timeout = 0
        self.serial_port.port = ComPort
        self.waitlist =[]
        self.queue = []
            
        if self.simulation == False:
            if self.serial_port.isOpen(): 
                self.serial_port.close()
            self.serial_port.open()
            print("{0} ist Online".format(self.bezeichnung))
            self.printBluetooth("Statusupdate 2")
        

    def MachineCom(self):
        if self.status == "wait":
            self.printBluetooth(2)
        if self.status == "processing":
            self.printBluetooth(1)
        if self.status == "Sleep Mode":
            self.printBluetooth(3)
                        
    def Anmeldung(self,ID, PA):
        self.print("Product No." + str(ID) + " registered")
        self.waitlist.append(PA.ID)
        self.print("Products on waiting list:" + str(self.waitlist))

    def Ankunft(self,Produkt):
        # Produkt in die Warteschlange eintragen
        self.queue.append(Produkt)
        # Produkt aus der Anmeldeliste austragen
        self.waitlist.remove(Produkt.ID)

    def GetPriority(self):
        self.StatusUpdate("busy")
        self.MachineCom()
        self.print("sort products by priority")
        self.queue.sort(key=operator.attrgetter("dueDate"),reverse=False)

    def Processing(self,Product):
        self.prozesszeit =  int(Product.processparameter[Product.currentStep])/Speedup
        self.StatusUpdate("processing")
        self.MachineCom()
        Product.Infoverarbeitung("Prozessstart")
        sleep(self.prozesszeit)
        Product.Infoverarbeitung("Prozessende")
        del self.queue[0]
        self.StatusUpdate("wait")
        self.MachineCom()

    def printBluetooth(self, Message):
        if self.simulation == False:
            Commstring = "Statusupdate " + str(Message)
            self.serial_port.write(Commstring.encode('utf-8'))

    def run(self):
        while True:
            if len(self.queue) > 0:
                self.GetPriority()
                self.Processing(self.queue[0])
            else:
                sleep(0.1)


class Produktagent(Agent):    
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


class Transportagent(Agent):
    
    def __init__(self, ID, Location, Objektpool):
        super().__init__(ID, Location, Bezeichnung="Transporter")
        global Transportliste
        global Feedback
        
        self.transportlist = []
        self.status = "wait"   # wait, busy
        self.objektpool = Objektpool
        if self.objektpool.simulation == False:
            Transportliste = multiprocessing.Queue()
            Feedback = multiprocessing.Queue()
            CozmoProzess = multiprocessing.Process(target=_300_Cozmo.runCozmo, args=(Transportliste,Feedback))
            CozmoProzess.start()

        self.Auftrag = None
        self.start()

    def Transportrequest(self,TransportItem):   
        self.print("Product No." + str(TransportItem.ID) 
                   + " registered for transport from " 
                   + str(TransportItem.location.bezeichnung) 
                   + " to " 
                   + str(TransportItem.destination.bezeichnung))
        self.transportlist.append(TransportItem)

    def GetPriority(self):
        #Die Warteliste entsprechend der Prioriaet ordnen. NOCH NICHT FERTIG -----------------------------------------------------------------------
        self.print("sort transfer orders by priority")
        self.transportlist.sort(key=operator.attrgetter("dueDate"),reverse=False)
        
    def Transport(self):
        # Statuswechsel
        self.StatusUpdate("busy")
        self.print("transporting product:" + str(self.transportlist[0].ID) 
                   + " from " + str(self.transportlist[0].location.bezeichnung) 
                   +" to " +str(self.transportlist[0].destination.bezeichnung))
               
        # Produkt über Abtransport informieren
        self.transportlist[0].Infoverarbeitung("Abtransport")
        
        # Simulation == Es wird einfach mit der "Dummy"-Transportdauer gerechnet
        if self.objektpool.simulation == True:
            sleep(Transportdauer)
        
        # Demo == Cozmo verursacht die Transportzeit
        elif self.objektpool.simulation == False:
            Transportauftrag = []
            Transportauftrag.append(self.transportlist[0].ID)
            Transportauftrag.append(self.transportlist[0].destination.bezeichnung)
            Transportauftrag.append(self.transportlist[0].destination.ID)

            
            Transportliste.put(Transportauftrag)
            while Feedback.empty() is True:
                sleep(0.5)
                #auf Rückmeldung von Cozmo warten
            x = Feedback.get()
            print("Cozmo meldet: " + x)
             
        #Produktstandort aktualisieren 
        self.transportlist[0].location = self.transportlist[0].destination
        # Produkt über Ankunft informieren
        self.transportlist[0].Infoverarbeitung("Ankunft")
        # Maschine über ankunft informieren
        self.transportlist[0].location.Ankunft(self.transportlist[0])
        # Auftrag aus der Liste Löschen
        del self.transportlist[0]
        # Statuswechsel
        self.StatusUpdate("wait")
 
    def run(self):
        
        while True:
            if len(self.transportlist) > 0:
                # Transportauftrag mit höchster Prio suchen
                self.GetPriority()
                # Den Transportauftrag abarbeiten
                self.Transport()
                sleep(0.5)
            else:
                sleep(0.5)

                
class Lageragent(Agent):

    def __init__(self, ID, Location, Bezeichnung,):
        super().__init__(ID, Location, Bezeichnung)

    def Ankunft(self,Product):
        Product.Infoverarbeitung("Fertig")