from time import sleep
import operator
import threading
#import PhysicalTransporter
import cozmo
from cozmo.util import degrees, Pose, distance_mm, speed_mmps
import asyncio
from Experimente import CozmoBot

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
        self.my_bot = CozmoBot(cozmo.robot.Robot)
        #def cozmo_program(robot: cozmo.robot.Robot):
        #    self.my_bot = CozmoBot(robot)
        #cozmo.run_program(cozmo_program)
        self.start()

       
        

    def Transportrequest(self,TransportItem):   #Auftrag: [Produkt, Start, Ziel]
        self.print("Product No." + str(TransportItem.productID) + " registered for transport from " + str(TransportItem.location.bezeichnung) + " to " + str(TransportItem.destination.bezeichnung))
        # Das anfragende Produkt in die Transportliste eintragen
        self.Parkingspotselector(TransportItem)
        self.transportlist.append(TransportItem)

    def Parkingspotselector(self,TransportItem):
        puffer = TransportItem.destination.parkingspots
        selectedspot = None

        for i in puffer:
            if i == 0:
                selectedspot = i+1
                break
        if selectedspot == None:
            print("Puffer Voll")
        print(selectedspot)
        code = 0                  

    def Statusupdate(self, Status):
        self.status = Status
        #self.print("Status: " + str(self.status))

    def GetPriority(self):
        #Die Warteliste entsprechend der Prioriaet ordnen. NOCH NICHT FERTIG -----------------------------------------------------------------------
        self.print("sort transfer orders by priority")
        self.transportlist.sort(key=operator.attrgetter("dueDate"),reverse=False)
        
    def Transport(self):
        # Statuswechsel
        self.Statusupdate("busy")
        self.print("transporting product:" + str(self.transportlist[0].productID) + " from " + str(self.transportlist[0].location.bezeichnung) +" to " +str(self.transportlist[0].destination.bezeichnung))
        # Produkt über Abtransport informieren
        self.my_bot.distance=100

        self.transportlist[0].Infoverarbeitung("Abtransport")

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