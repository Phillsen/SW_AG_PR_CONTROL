from time import sleep
import operator
import cozmo
import _100_Agentenklasse
import multiprocessing
import _900_Experimente
#import Transporter


# Transportdauer(s)für die Simulation. Kann beliebeig eingestellt werden. 
Transportdauer = 1


class Transportagent(_100_Agentenklasse.Agent):
    
    def __init__(self, ID, Location, Objektpool):
        super().__init__(ID, Location, Bezeichnung="Transporter")
        self.status = "wait"   # wait, busy
        self.transportlist = []
        self.start()
        self.objektpool = Objektpool
        

    def Transportrequest(self,TransportItem):   
        self.print("Product No." + str(TransportItem.ID) + " registered for transport from " + str(TransportItem.location.bezeichnung) + " to " + str(TransportItem.destination.bezeichnung))
        # Das anfragende Produkt in die Transportliste eintragen
        self.transportlist.append(TransportItem)

    def GetPriority(self):
        #Die Warteliste entsprechend der Prioriaet ordnen. NOCH NICHT FERTIG -----------------------------------------------------------------------
        self.print("sort transfer orders by priority")
        self.transportlist.sort(key=operator.attrgetter("dueDate"),reverse=False) 
        
    def Transport(self):
        
        # Statuswechsel
        self.StatusUpdate("busy")
        self.print("transporting product:" + str(self.transportlist[0].ID) + " from " + str(self.transportlist[0].location.bezeichnung) +" to " +str(self.transportlist[0].destination.bezeichnung))
        x = "product:" + str(self.transportlist[0].ID)
        # Produkt über Abtransport informieren
        self.transportlist[0].Infoverarbeitung("Abtransport")
        MainWindow.q.put(x)


        # Simulation == Es wird einfach mit der "Dummy"-Transportdauer gerechnet
        if self.objektpool.simulation == True:
            sleep(Transportdauer)
        
        # Demo == Cozmo verursacht die Transportzeit
        elif self.objektpool.simulation == False:
            pass
            #Cozmokram
        
        
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