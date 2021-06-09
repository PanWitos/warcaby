from pionek import Pionek

class Pion(Pionek):

    def __repr__(self):
        return "Pion ["+str(self.pozX)+","+str(self.pozY)+"] - "+self.gracz