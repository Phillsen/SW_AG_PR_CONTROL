from time import sleep
import operator
import threading


# Transportdauer(s)für die Simulation. Kann beliebeig eingestellt werden. 
Transportdauer = 1



class Transportagent(threading.Thread):
    
    def __init__(self, TransporterID, Location): 
        threading.Thread.__init__(self)
        self.transporterID = TransporterID
        self.location = Location
        self.status = "idle"   # idle, busy
        self.transportlist = []
        self.printIdent = "TA" + str(self.transporterID)+ ": "
        self.start()
                

    def Transportrequest(self,TransportItem):   #Auftrag: [Produkt, Start, Ziel]
        self.print("Product No." + str(TransportItem.productID) + " registered for transport from " + str(TransportItem.location.bezeichnung) + " to " + str(TransportItem.destination.bezeichnung))
        # Das anfragende Produkt in die Transportliste eintragen
        self.transportlist.append(TransportItem)

    def Statusupdate(self, Status):
        self.status = Status
        #self.print("Status: " + str(self.status))

    def GetPriority(self):
        #Die Warteliste entsprechend der Prioriaet ordnen. NOCH NICHT FERTIG
        self.print("sort transfer orders by priority")
        self.transportlist.sort(key=operator.attrgetter("dueDate"),reverse=False)
        
    def Transport(self):
        # Statuswechsel
        self.Statusupdate("busy")
        self.print("transporting product:" + str(self.transportlist[0].productID) + " from " + str(self.transportlist[0].location.bezeichnung) +" to " +str(self.transportlist[0].destination.bezeichnung) )
        # Produkt über Abtransport informeieren
        self.transportlist[0].Infoverarbeitung("Abtransport")
        # Transport simulieren
        sleep(Transportdauer)
        # Produktstandort aktualisieren 
        self.transportlist[0].location = self.transportlist[0].destination
        # Produkt über Ankunft informieren
        self.transportlist[0].Infoverarbeitung("Ankunft")
        # Maschine über ankunft informieren
        self.transportlist[0].location.Ankunft(self.transportlist[0])
        # Auftrag aus der Liste Löschen
        del self.transportlist[0]
        # Statuswechsel
        self.Statusupdate("idle")

    def print(self, Info):
        print(self.printIdent + Info)

    def run(self):
        while True:
            if len(self.transportlist) > 0:
                # Transportauftrag mit höchster Prio suchen
                self.GetPriority()
                # Den Transportauftrag abarbeiten
                self.Transport()
            else:
                sleep(0.1)