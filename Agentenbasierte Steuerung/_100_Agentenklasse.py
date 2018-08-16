import threading
import datetime


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

