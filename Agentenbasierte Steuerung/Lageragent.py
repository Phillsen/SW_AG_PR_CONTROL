import Agentenklasse


class Lageragent(Agentenklasse.Agent):

    def __init__(self, ID, Location, Bezeichnung,):
        super().__init__(ID, Location, Bezeichnung)
                     

    def Ankunft(self,Product):
        Product.Infoverarbeitung("Fertig")

