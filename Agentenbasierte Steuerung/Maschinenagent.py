import operator
from time import sleep
import serial
import Agentenklasse


Speedup = 50         # Zum Debuggen die Prozesszeit um diesen Faktor verkürzen

class Maschinenagent(Agentenklasse.Agent):
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