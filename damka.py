from pionek import Pionek

class Damka(Pionek):        #Klasa Damka dziedziczy po klasie Pionek
    
    def __repr__(self):
        return "Damka ["+str(self.pozX)+","+str(self.pozY)+"] - "+self.gracz