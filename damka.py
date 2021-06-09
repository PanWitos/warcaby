from pionek import Pionek

class Damka(Pionek):

    def wezTyp(self):
        return self.typ
    

    def __repr__(self):
        return "Damka ["+str(self.pozX)+","+str(self.pozY)+"] - "+self.gracz