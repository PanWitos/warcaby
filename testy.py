from damka import Damka
from pion import Pion
from warcaby import Warcaby

X,Y = 8, 8

class Test(Warcaby):
    def __init__(self):
        
        self.rozstawienie(1)

    def rozstawienie(self, typ):
        print("Nowa gra")
        self.tura = 'C'
        self.wybranyPionek = None
        self.liczbaPionkowCzarne = 12
        self.liczbaPionkowBiale = 12
        self.plansza = []
        self.dostepneRuchy = {}

        if(typ == 1):
            self.stworzPlansze()
        elif(typ == 2):
            self.liczbaPionkowCzarne = 1
            self.liczbaPionkowBiale = 2
            self.stworzPlansze2()
        elif(typ == 3):
            self.liczbaPionkowCzarne = 1
            self.liczbaPionkowBiale = 1
            self.stworzPlansze3()
        elif(typ == 4):
            self.liczbaPionkowCzarne = 1
            self.liczbaPionkowBiale = 1
            self.stworzPlansze4()
        elif(typ == 5):
            self.liczbaPionkowCzarne = 1
            self.liczbaPionkowBiale = 1
            self.stworzPlansze5()

    def stworzPlansze(self):
        for x in range(X):
            self.plansza.append([])
            for y in range(Y):
                if (x%2 == y%2):
                    self.plansza[x].append(0)
                else:
                    if(x < 3):
                        self.plansza[x].append(Pion(x,y,'C'))
                    elif(x > 4):
                        self.plansza[x].append(Pion(x,y,'B'))
                    else:
                        self.plansza[x].append(0)

    def stworzPlansze2(self):
        for x in range(X):
            self.plansza.append([])
            for y in range(Y):
                if (y % 2 == x % 2):
                    self.plansza[x].append(0)
                else:
                    if (x == 1 and y == 2):
                        self.plansza[x].append(Pion(x,y,'C'))
                    elif (x == 2 and y == 1):
                        self.plansza[x].append(Pion(x,y,'B'))
                    elif (x == 4 and y == 1):
                        self.plansza[x].append(Pion(x,y,'B'))
                    else:
                        self.plansza[x].append(0)
    
    def stworzPlansze3(self):
        for x in range(X):
            self.plansza.append([])
            for y in range(Y):
                if (y % 2 == x % 2):
                    self.plansza[x].append(0)
                else:
                    if (x == 6 and y == 1):
                        self.plansza[x].append(Pion(x,y,'C'))
                    else:
                        self.plansza[x].append(0)
    
    def stworzPlansze4(self):
        for x in range(X):
            self.plansza.append([])
            for y in range(Y):
                if (y % 2 == x % 2):
                    self.plansza[x].append(0)
                else:
                    if (x == 7 and y == 0):
                        self.plansza[x].append(Damka(x,y,'C'))
                    elif (x == 6 and y == 1):
                        self.plansza[x].append(Pion(x,y,'B'))
                    else:
                        self.plansza[x].append(0)
    
    def stworzPlansze5(self):
        for x in range(X):
            self.plansza.append([])
            for y in range(Y):
                if (y % 2 == x % 2):
                    self.plansza[x].append(0)
                else:
                    if (x == 2 and y == 1):
                        self.plansza[x].append(Pion(x,y,'C'))
                    elif (x == 3 and y == 2):
                        self.plansza[x].append(Pion(x,y,'B'))
                    else:
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
                
                self.wybranyPionek = None
                self.wybor(pozX, pozY, oznaczenie)
                print("Blad","ruch niedozwolony")
            else:
                self.wybranyPionek = None
        
        
        pionek = self.plansza[pozX][pozY]
        if pionek != 0 and pionek.gracz == self.tura:
            self.wybranyPionek = pionek
            temp = "["+oznaczenie+"]"
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

            if isinstance(self.wybranyPionek, Damka):
                temp = self.wybranyPionek.gracz + "d"
            else: 
                temp = self.plansza[x][y].gracz
            
            self.wybranyPionek.ruch(x,y)

            if (x == X-1) and self.plansza[x][y].gracz == 'C' and not isinstance(self.plansza[x][y], Damka):
                self.plansza[x][y] = Damka(x,y,"C")
                print("Damka C")
            elif (x == 0) and self.plansza[x][y].gracz == 'B' and not isinstance(self.plansza[x][y], Damka):
                self.plansza[x][y] = Damka(x,y,"B")
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
            print("Tura gracza 2")
        else:
            self.tura = "C"
            print("Tura gracza 1")

    def usunPionek(self, pionki):
        for pionek in pionki:
            print("Zbito pionka")
            self.plansza[pionek.pozX][pionek.pozY] = 0
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
            print("Wygral gracz 1")
        elif wygrany == "B":
            print("Wygral gracz 2")

    def test1(self):
        print("TEST 1")
        self.rozstawienie(1)
        self.wybor(2,1,"C")
        self.wybor(3,0,"")
        self.wybor(5,0,"B")
        self.wybor(4,1,"")
        self.wybor(2,5,"C")
        self.wybor(3,6,"")
        self.wybor(4,1,"B")
        self.wybor(3,2,"")
    
    def test2(self):
        print("TEST 2")
        self.rozstawienie(1)
        self.wybor(2,5,"C")
        self.wybor(1,2,"")

    def test3(self):
        print("TEST 3")
        self.rozstawienie(1)
        self.wybor(2,5,"C")
        self.wybor(3,4,"")
        self.wybor(5,4,"B")
        self.wybor(4,5,"")
        self.wybor(2,3,"C")
        self.wybor(3,2,"")
        self.wybor(4,5,"B")
        self.wybor(2,3,"")
    
    def test4(self):
        print("TEST 4")
        self.rozstawienie(2)
        self.wybor(1,2,"C")
        self.wybor(5,2,"")

    def test5(self):
        print("TEST 5")
        self.rozstawienie(3)
        self.wybor(6,1,"C")
        self.wybor(7,0,"")

    def test6(self):
        print("TEST 6")
        self.rozstawienie(4)
        self.wybor(7,0,"C")
        self.wybor(5,2,"")

    def test7(self):
        print("TEST 7")
        self.rozstawienie(5)
        self.wybor(2,1,"C")
        self.wybor(4,3,"")

    def test8(self):
        print("TEST 8")
        self.rozstawienie(5)
        self.wybor(2,1,"C")
        self.wybor(4,3,"")
        self.rozstawienie(1)
        self.wybor(2,3,"C")
        self.wybor(3,4,"")

test = Test()
test.test1()
test.test2()
test.test3()
test.test4()
test.test5()
test.test6()
test.test7()
test.test8()




        