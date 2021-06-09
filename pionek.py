

class Pionek:
    def __init__(self, pozX, pozY, gracz):
        self.pozX = pozX
        self.pozY = pozY
        self.gracz = gracz

    def ruch(self, nowaPozX, nowaPozY):
        self.pozX = nowaPozX
        self.pozY = nowaPozY

    def __repr__(self):
        return "Pionek ["+str(self.pozX)+","+str(self.pozY)+"] - "+self.gracz
