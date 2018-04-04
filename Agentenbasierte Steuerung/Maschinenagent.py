import threading
import operator
from time import sleep
import serial

Simulation = True       # Wenn True wird der Physische Komunikationsteil abgeschaltet
Speedup = 10            # Zum Debuggen die Prozesszeit um diesen Faktor verkürzen

class Maschinenagent(threading.Thread):
    serial_port = serial.Serial()
    serial_port.baudrate
    serial_port.timeout
    serial_port.port

    def __init__(self, ProcessID, Bezeichnung,ComPort,DB):
        threading.Thread.__init__(self)
        self.DB = DB
        self.serial_port = serial.Serial()
        self.serial_port.baudrate = 9600
        self.serial_port.timeout = 0
        self.serial_port.port = ComPort
        self.processID = ProcessID
        self.bezeichnung = Bezeichnung
        self.status = "idle"
        self.waitlist =[]
        self.queue = []
        self.prozesszeit = 0
        self.printIdent = "MA" + str(self.processID)+ ": "
        
        if Simulation == False:
            if self.serial_port.isOpen(): 
                self.serial_port.close()
            self.serial_port.open()
        self.printBluetooth("Statusupdate 2")

    def Statusupdate(self, Status):
        self.status = Status
        self.print("Status: " +str(self.status))
        if self.status == "idle":
            self.printBluetooth(2)
        if self.status == "processing":
            self.printBluetooth(1)
        if self.status == "Sleep Mode":
            self.printBluetooth(3)
                    
    def Anmeldung(self,ProductID, PA):
        self.print("Product No." + str(ProductID) + " registered")
        self.waitlist.append(PA.productID)
        self.print("Products on waiting list:" + str(self.waitlist))

    def Ankunft(self,Produkt):
        # Produkt in die Warteschlange eintragen
        self.queue.append(Produkt)
        # Produkt aus der Anmeldeliste austragen
        self.waitlist.remove(Produkt.productID)

    def GetPriority(self):
        pass
        self.print("sort products by priority")
        self.queue.sort(key=operator.attrgetter("dueDate"),reverse=False)

    def Processing(self,Product):
        self.Statusupdate("Updating process parameters")
        self.prozesszeit =  int(Product.processparameter[Product.currentStep])/Speedup
        self.Statusupdate("processing")
        Product.Infoverarbeitung("Prozessstart")
        sleep(self.prozesszeit)
        Product.Infoverarbeitung("Prozessende")
        del self.queue[0]
        self.Statusupdate("idle")

    def print(self, Info):
        print(self.printIdent + Info)

    def printBluetooth(self, Message):
        if Simulation == False:
            Commstring = "Statusupdate " + str(Message)
            self.serial_port.write(Commstring.encode('utf-8'))

    def run(self):
        while True:
            if len(self.queue) > 0:
                self.GetPriority()
                self.Processing(self.queue[0])
            else:
                sleep(0.1)