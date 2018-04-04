class Lageragent():

    def __init__(self, Location, Bezeichnung):
        self.location = Location
        self.bezeichnung = Bezeichnung

    def Ankunft(self,Product):
        Product.Infoverarbeitung("Fertig")