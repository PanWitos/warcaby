from pionek import Pionek

class Pion(Pionek):   #Klasa Pion dziedziczy po klasie Pionek

    def __repr__(self):
        return "Pion ["+str(self.pozX)+","+str(self.pozY)+"] - "+self.gracz