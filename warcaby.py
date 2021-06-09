from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from damka import Damka
from pion import Pion

X,Y = 8, 8

class Warcaby:
    def __init__(self):
        self.window = Tk()
        self.window.title("Warcaby")
        self.mainframe = ttk.Frame(self.window)
        self.mainframe.grid(column=0, row=0, sticky=(N,W,E,S), padx=35, pady=30)

        self.rozstawienie()
        self.window.mainloop()

    def rozstawienie(self):
        self.tura = 'C'
        self.wybranyPionek = None
        self.liczbaPionkowCzarne = 12
        self.liczbaPionkowBiale = 12
        self.plansza = []
        self.przyciski = []
        self.dostepneRuchy = {}

        self.mainframe.grid_columnconfigure(7, weight =1)
        ttk.Button(self.mainframe, text="RESET", command=lambda :self.rozstawienie()).grid(row = 5, column = 9, padx = 15)
        self.info = Label(self.mainframe, text="Tura gracza 1").grid(row=2, column=9, padx=15)

        self.stworzPlansze()

    def stworzPlansze(self):
        for x in range(X):
            self.przyciski.append([])
            self.plansza.append([])
            for y in range(Y):
                if (x%2 == y%2):
                    self.przyciski[x].append(ttk.Button(self.mainframe, text="", command=lambda pozX=x,pozY=y:self.wybor(pozX,pozY,"")).grid(row = x, column= y))
                    self.plansza[x].append(0)
                else:
                    if(x < 3):
                        self.przyciski[x].append(ttk.Button(self.mainframe, text="C", command=lambda pozX=x, pozY=y:self.wybor(pozX,pozY,"C")).grid(row = x, column = y))
                        self.plansza[x].append(Pion(x,y,'C'))
                    elif(x > 4):
                        self.przyciski[x].append(ttk.Button(self.mainframe, text="B", command=lambda pozX=x, pozY=y:self.wybor(pozX,pozY,"B")).grid(row = x, column = y))
                        self.plansza[x].append(Pion(x,y,'B'))
                    else:
                        self.przyciski[x].append(ttk.Button(self.mainframe, text="", command=lambda pozX=x, pozY=y:self.wybor(pozX,pozY,"")).grid(row = x, column = y))
                        self.plansza[x].append(0)

    def wybor(self, pozX, pozY, oznaczenie):

        if isinstance(self.plansza[pozX][pozY], Damka):
            oznaczenie = self.plansza[pozX][pozY].gracz + "d"
        print(oznaczenie, "-[",pozX,pozY,"]")

        if(self.wybranyPionek):
            wynik = self.ruch(pozX, pozY)
            if not wynik:
                if isinstance(self.wybranyPionek, Damka):
                    temp = self.wybranyPionek.gracz + "d"
                else:
                    temp = self.wybranyPionek.gracz
                
                self.przyciski[self.wybranyPionek.pozX][self.wybranyPionek.pozY] = ttk.Button(self.mainframe, text=temp, command=lambda x=self.wybranyPionek.pozX, y=self.wybranyPionek.pozY, text=self.wybranyPionek.gracz:self.wybor(x,y,text)).grid(row = self.wybranyPionek.pozX, column = self.wybranyPionek.pozY)
                self.wybranyPionek = None
                self.wybor(pozX, pozY, oznaczenie)
                messagebox.showinfo("Blad","ruch niedozwolony")
            else:
                self.wybranyPionek = None
        
        
        pionek = self.plansza[pozX][pozY]
        if pionek != 0 and pionek.gracz == self.tura:
            self.wybranyPionek = pionek
            temp = "["+oznaczenie+"]"
            self.przyciski[pozX][pozY] = ttk.Button(self.mainframe, text= temp, command=lambda x=pozX, y=pozY, text=oznaczenie:self.wybor(x,y,text)).grid(row = pozX, column= pozY)
            self.dostepneRuchy = self.znajdzRuchy(pionek)
            return True
        return False

    def znajdzRuchy(self, pionek):
        ruchy = {}
        ruchLewo = pionek.pozY -1
        ruchPrawo = pionek.pozY +1
        pozX = pionek.pozX
        

        if isinstance(pionek, Pion):
            if pionek.gracz == "B":
                ruchy.update(self.ruchWLewo(pozX - 1, max(pozX - 3, -1), -1, pionek.gracz, ruchLewo))
                ruchy.update(self.ruchWPrawo(pozX - 1, max(pozX - 3, -1), -1, pionek.gracz, ruchPrawo))
            else:
                ruchy.update(self.ruchWLewo(pozX + 1, min(pozX + 3, X), 1, pionek.gracz, ruchLewo))
                ruchy.update(self.ruchWPrawo(pozX + 1, min(pozX + 3, X), 1, pionek.gracz, ruchPrawo))
        elif isinstance(pionek, Damka):
                ruchy.update(self.ruchWLewo(pozX - 1, max(pozX - 3, -1), -1, pionek.gracz, ruchLewo))
                ruchy.update(self.ruchWPrawo(pozX - 1, max(pozX - 3, -1), -1, pionek.gracz, ruchPrawo))
                ruchy.update(self.ruchWLewo(pozX + 1, min(pozX + 3, X), 1, pionek.gracz, ruchLewo))
                ruchy.update(self.ruchWPrawo(pozX + 1, min(pozX + 3, X), 1, pionek.gracz, ruchPrawo))
        
        print(ruchy)
        for i in ruchy:
            if ruchy[i] != []:
                noweruchy = {}
                for i in ruchy:
                    if ruchy[i] != []:
                        noweruchy[i] = (ruchy[i])
                return noweruchy
        return ruchy

    def ruchWLewo(self, start, koniec, krok, gracz, zakres, zbitePionki=[]):
        ruchy = {}
        ostatniPionek = []

        for x in range(start, koniec, krok):
            if zakres < 0:
                break

            aktualnyPionek = self.plansza[x][zakres]
            if aktualnyPionek == 0:
                if zbitePionki and not ostatniPionek:
                    break
                elif zbitePionki:
                    ruchy[(x,zakres)] = ostatniPionek + zbitePionki
                else:
                    ruchy[(x,zakres)] = ostatniPionek

                if ostatniPionek:
                    if krok == -1:
                        pozX = max(x-3,-1)
                    else:
                        pozX = min(x+3,X)
                    ruchy.update(self.ruchWLewo(x+krok, pozX, krok, gracz, zakres-1, zbitePionki=zbitePionki+ostatniPionek))
                    ruchy.update(self.ruchWPrawo(x+krok, pozX, krok, gracz, zakres+1, zbitePionki=zbitePionki+ostatniPionek))
                break
            elif aktualnyPionek.gracz == gracz:
                break
            else:
                ostatniPionek = [aktualnyPionek]

            zakres -= 1
        
        return ruchy

    def ruchWPrawo(self, start, koniec, krok, gracz, zakres, zbitePionki=[]):
        ruchy = {}
        ostatniPionek = []
        for x in range(start, koniec, krok):
            if zakres >= Y:
                break

            aktualnyPionek = self.plansza[x][zakres]
            if aktualnyPionek == 0:
                if zbitePionki and not ostatniPionek:
                    break
                elif zbitePionki:
                    ruchy[(x,zakres)] = ostatniPionek + zbitePionki
                else:
                    ruchy[(x,zakres)] = ostatniPionek

                if ostatniPionek:
                    if krok == -1:
                        pozX = max(x-3,-1)
                    else:
                        pozX = min(x+3,X)
                    ruchy.update(self.ruchWLewo(x+krok, pozX, krok, gracz, zakres-1, zbitePionki=zbitePionki+ostatniPionek))
                    ruchy.update(self.ruchWPrawo(x+krok, pozX, krok, gracz, zakres+1, zbitePionki=zbitePionki+ostatniPionek))
                break
            elif aktualnyPionek.gracz == gracz:
                break
            else:
                ostatniPionek = [aktualnyPionek]

            zakres += 1
        
        return ruchy


    def ruch(self,x,y):
        wolneMiejsce = self.plansza[x][y]
        if self.wybranyPionek and wolneMiejsce == 0 and (x,y) in self.dostepneRuchy:
            self.plansza[self.wybranyPionek.pozX][self.wybranyPionek.pozY], self.plansza[x][y] = self.plansza[x][y], self.plansza[self.wybranyPionek.pozX][self.wybranyPionek.pozY]
            self.przyciski[self.wybranyPionek.pozX][self.wybranyPionek.pozY] = ttk.Button(self.mainframe, text="", command=lambda pozX=self.wybranyPionek.pozX, pozY=self.wybranyPionek.pozY:self.wybor(pozX,pozY,"")).grid(row = self.wybranyPionek.pozX, column=self.wybranyPionek.pozY)

            if isinstance(self.wybranyPionek, Damka):
                temp = self.wybranyPionek.gracz + "d"
            else: 
                temp = self.plansza[x][y].gracz
            
            self.przyciski[x][y] = ttk.Button(self.mainframe, text=temp, command=lambda pozX=x, pozY=y, text=temp:self.wybor(pozX,pozY,text)).grid(row = x, column = y)
            self.wybranyPionek.ruch(x,y)

            if (x == X-1) and self.plansza[x][y].gracz == 'C' and not isinstance(self.plansza[x][y], Damka):
                self.plansza[x][y] = Damka(x,y,"C")
                self.przyciski[x][y] = ttk.Button(self.mainframe, text='Cd', command=lambda pozX=x, pozY=y:self.wybor(pozX,pozY,"C")).grid(row = x, column = y)
                print("Damka C")
            elif (x == 0) and self.plansza[x][y].gracz == 'B' and not isinstance(self.plansza[x][y], Damka):
                self.plansza[x][y] = Damka(x,y,"B")
                self.przyciski[x][y] = ttk.Button(self.mainframe, text='Bd', command=lambda pozX=x, pozY=y:self.wybor(pozX,pozY,"B")).grid(row = x, column = y)
                print("Damka B")
            
            zbitePionki = self.dostepneRuchy[(x,y)]
            if zbitePionki:
                self.usunPionek(zbitePionki)
            self.nastepnaTura()
        
        else:
            return False
        
        return True

    def nastepnaTura(self):
        self.dostepneRuchy = {}
        if self.tura == "C":
            self.tura = "B"
            self.info = Label(self.mainframe, text="Tura gracza 2").grid(row=2, column=9, padx=15)
            print("Tura gracza 2")
        else:
            self.tura = "C"
            self.info = Label(self.mainframe, text="Tura gracza 1").grid(row=2, column=9, padx=15)
            print("Tura gracza 1")

    def usunPionek(self, pionki):
        for pionek in pionki:
            self.plansza[pionek.pozX][pionek.pozY] = 0
            self.przyciski[pionek.pozX][pionek.pozY] = (ttk.Button(self.mainframe, text="", command=lambda x=pionek.pozX, y=pionek.pozY :self.wybor(x,y,"")).grid(row = pionek.pozX, column = pionek.pozY))
            if pionek !=0:
                if pionek.gracz == "C":
                    self.liczbaPionkowCzarne -= 1
                else:
                    self.liczbaPionkowBiale -= 1
        
        if self.liczbaPionkowCzarne <= 0:
            self.wygrana("B")
        elif self.liczbaPionkowBiale <= 0:
            self.wygrana("C")
    
    def wygrana(self, wygrany):
        if wygrany == "C":
            messagebox.showinfo("Wygral gracz 1")
        elif wygrany == "B":
            messagebox.showinfo("Wygral gracz 2")



#warcaby = Warcaby()

        