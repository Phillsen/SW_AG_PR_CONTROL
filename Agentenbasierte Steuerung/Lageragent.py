class Lageragent():

    def __init__(self, Location, Bezeichnung):
        self.location = Location
        self.bezeichnung = Bezeichnung
        self.parkingspots = [0,0,0,0,0,0]

    def Ankunft(self,Product):
        Product.Infoverarbeitung("Fertig")