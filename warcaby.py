from tkinter import *
from tkinter import ttk
from tkinter import messagebox

from damka import Damka
from pion import Pion

X,Y = 8, 8

class Warcaby:
    def __init__(self):                             #Przy tworzeniu obiektu Warcaby okno i wywołujemy metodę która rozstawi nam nową partję warcab
        self.window = Tk()
        self.window.title("Warcaby")
        self.mainframe = ttk.Frame(self.window)
        self.mainframe.grid(column=0, row=0, sticky=(N,W,E,S), padx=35, pady=30)

        self.rozstawienie()
        self.window.mainloop()

    def rozstawienie(self):                         #W metodzie rozstawienie ustawiamy nową partię warcab
        self.tura = 'C'                             #Ustawianie tury gracza 1, pionki C (według dokumentu)
        self.wybranyPionek = None                   #Aktualnie nie ma wybranego pionka
        self.liczbaPionkowCzarne = 12               #Liczba pionków obu graczy na początku gry
        self.liczbaPionkowBiale = 12
        self.plansza = []                           #Pierwsza inicjalizacja tablicy do przechowywania obiektów pionków
        self.przyciski = []                         #Pierwsza inicjalizacja tablicy do przechowywania przycisków
        self.dostepneRuchy = {}                     #Słownik z dostępnymi dla aktualnie wybranego pionka ruchami, na początku pusty

        self.mainframe.grid_columnconfigure(7, weight = 1)              
        ttk.Button(self.mainframe, text="RESET", command=lambda :self.rozstawienie()).grid(row = 8, column = 5, pady=10) #Przcisk REST uruchamia rozstawienie ponownie, zaczynamy nową gre
        self.info = Label(self.mainframe, text="Tura gracza 1").grid(row=8, column=2, pady=10)                           #Informacja o turze aktualnego gracza

        self.stworzPlansze()                        #Wywołanie stworzenia nowej planszy

    def stworzPlansze(self):
        for x in range(X):                          #Stworzenie siatki do przechowywania pionkow i przyciskow
            self.przyciski.append([])
            self.plansza.append([])
            for y in range(Y):
                if (x%2 == y%2):
                    self.przyciski[x].append(ttk.Button(self.mainframe, text="", command=lambda pozX=x,pozY=y:self.wybor(pozX,pozY,"")).grid(row = x, column= y)) #Zaczynając od indeksu 0,0 co drugie pole będzie zawierało int 0, na tych polach pionki nie będą mogł się poruszać (według zasad gry)
                    self.plansza[x].append(0)
                else:
                    if(x < 3):
                        self.przyciski[x].append(ttk.Button(self.mainframe, text="C", command=lambda pozX=x, pozY=y:self.wybor(pozX,pozY,"C")).grid(row = x, column = y)) #Wypełnienie górnej części planszy pionkami gracza czarnego
                        self.plansza[x].append(Pion(x,y,'C'))
                    elif(x > 4):
                        self.przyciski[x].append(ttk.Button(self.mainframe, text="B", command=lambda pozX=x, pozY=y:self.wybor(pozX,pozY,"B")).grid(row = x, column = y)) #Wypełnienie dolnej części planszy pionkami gracza białego
                        self.plansza[x].append(Pion(x,y,'B'))
                    else:
                        self.przyciski[x].append(ttk.Button(self.mainframe, text="", command=lambda pozX=x, pozY=y:self.wybor(pozX,pozY,"")).grid(row = x, column = y)) #Wypełnienie reszty pustych pól 0, po tych polach pionki będą mogł się poruszać
                        self.plansza[x].append(0)

    def wybor(self, pozX, pozY, oznaczenie):        #Metoda służaca do wyboru pola na planszy

        if isinstance(self.plansza[pozX][pozY], Damka):         #Jeśli obiekt jest damką, mam mieć dodatkowo "d" przy swojej nazwie
            oznaczenie = self.plansza[pozX][pozY].gracz + "d"
        print(oznaczenie, "- [",pozX,pozY,"]")                   

        if(self.wybranyPionek):                     #Sprawdzenie czy gracz ma już wybranego pionka
            wynik = self.ruch(pozX, pozY)           #Gracz z wybranym pionkiem proboje wykonać ruch na wybrane pole
            if not wynik:                           #Jeśli ruch się nie powiódł
                if isinstance(self.wybranyPionek, Damka):   #Jeśli obiekt jest damką, mam mieć dodatkowo "d" przy swojej nazwie
                    temp = self.wybranyPionek.gracz + "d"
                else:
                    temp = self.wybranyPionek.gracz
                
                self.przyciski[self.wybranyPionek.pozX][self.wybranyPionek.pozY] = ttk.Button(self.mainframe, text=temp, command=lambda x=self.wybranyPionek.pozX, y=self.wybranyPionek.pozY, text=self.wybranyPionek.gracz:self.wybor(x,y,text)).grid(row = self.wybranyPionek.pozX, column = self.wybranyPionek.pozY)
                self.wybranyPionek = None
                self.wybor(pozX, pozY, oznaczenie)
                messagebox.showinfo("Blad","ruch niedozwolony")     #W wypadku nieudanego ruchu resetuje się oznaczenie, usuwamy aktualnego pionka z wybranych, wyświetlamy błąd. Wykonujemy także kolejny wybór na tym polu, jeśli jest tam nasz pionek, to teraz on będzie wybrany
            else:
                self.wybranyPionek = None   #Jeśli ruch się udał usuwamy pionka z wybranych
        
        
        pionek = self.plansza[pozX][pozY]   #Wrzucenie zawartości z wybranego pola do zmiennej tymczasowej
        if pionek != 0 and pionek.gracz == self.tura: #Sprawdzanie czy zawartością jest pionek i jest to pionek aktualnego gracza
            self.wybranyPionek = pionek     #Pionek z pola zostaje wybrany
            temp = "["+oznaczenie+"]"       #Otrzymuje dodatkowe oznaczenie w formie nawiasów
            self.przyciski[pozX][pozY] = ttk.Button(self.mainframe, text= temp, command=lambda x=pozX, y=pozY, text=oznaczenie:self.wybor(x,y,text)).grid(row = pozX, column= pozY)
            self.dostepneRuchy = self.znajdzRuchy(pionek)   #Sprawdzenie dostępnych róchów dla wybranego pionka
            return True
        return False

    def znajdzRuchy(self, pionek):          #Szukanie dostepnych ruchów dla pionka
        ruchy = {}                          #Inicjalizacja słownika z ruchami
        ruchLewo = pionek.pozY -1           #Potencjalne dwa ruchy na lewo i prawo, pionek porusza się tylko po skosie
        ruchPrawo = pionek.pozY +1
        pozX = pionek.pozX
        

        if isinstance(pionek, Pion):        #Jeśli pionek jest zwykłym pionkiem
            if pionek.gracz == "B":         #Jeśli jest graczem białych, to porusza się tylko do góry
                ruchy.update(self.ruchWLewo(pozX - 1, max(pozX - 3, -1), -1, pionek.gracz, ruchLewo))       #Metody na potencjalne ruchy w lewo i prawo, z uwzględnieniem ruchu do góry (krok -1)
                ruchy.update(self.ruchWPrawo(pozX - 1, max(pozX - 3, -1), -1, pionek.gracz, ruchPrawo))
            else:                           #Jeśli jest graczem czarnych to porusza się tylko na dół
                ruchy.update(self.ruchWLewo(pozX + 1, min(pozX + 3, X), 1, pionek.gracz, ruchLewo))         #Metody na potencjalne ruchy w lewo i prawo, z uwzględnieniem ruchu do dołu (krok 1)
                ruchy.update(self.ruchWPrawo(pozX + 1, min(pozX + 3, X), 1, pionek.gracz, ruchPrawo))
        elif isinstance(pionek, Damka):     #Jeśli pionek jest damką
                ruchy.update(self.ruchWLewo(pozX - 1, max(pozX - 3, -1), -1, pionek.gracz, ruchLewo))       #Meetody na wszystkie potencjalne ruchy w lewo i prawo, w górę i w dół
                ruchy.update(self.ruchWPrawo(pozX - 1, max(pozX - 3, -1), -1, pionek.gracz, ruchPrawo))
                ruchy.update(self.ruchWLewo(pozX + 1, min(pozX + 3, X), 1, pionek.gracz, ruchLewo))
                ruchy.update(self.ruchWPrawo(pozX + 1, min(pozX + 3, X), 1, pionek.gracz, ruchPrawo))
        
        print(ruchy)    #Wypisanie dostępnych ruchów
        for i in ruchy: #Jeśli w potencjalnych ruchach znajdują się ruchy wraz ze zbiciem, zwracamy listę tylko takich ruchów (obowiązek bicia)
            if ruchy[i] != []:
                noweruchy = {}
                for i in ruchy:
                    if ruchy[i] != []:
                        noweruchy[i] = (ruchy[i])
                return noweruchy
        return ruchy    #zwrócenie listy dostępnych róchów

    def ruchWLewo(self, start, koniec, krok, gracz, zakres, zbitePionki=[]):    #Znajdywanie ruchów na lewo
        ruchy = {}                      #Inicjalizacja słownika z ruchami
        ostatniPionek = []              #Przechowywanie pionka z ostatnio sprawdzanego pola

        for x in range(start, koniec, krok):    #sprawdzanie czy nie wychodzimy poza obszar naszej siatki
            if zakres < 0:
                break

            aktualnyPionek = self.plansza[x][zakres]    #Przechowujemy zawartość planszy
            if aktualnyPionek == 0:                     #Jeśli ta zawartość wynosi 0, to znaczy że pole jest puste
                if zbitePionki and not ostatniPionek:   #Jeśli zbiliśmy już jakiegoś przeciwnika, ale nie ma więcej opcji zbicia dalej
                    break
                elif zbitePionki:                       #Jeśli zbiliśmy juz jakiegoś przeciwnika i możemy przeskoczyć nad kolejnym
                    ruchy[(x,zakres)] = ostatniPionek + zbitePionki
                else:                                   
                    ruchy[(x,zakres)] = ostatniPionek

                if ostatniPionek:                       #Jeśli na poprzednim polu był pionek przeciwnika
                    if krok == -1:                      #Zależnie od kroku przygotowujemy zmienne na kolejne wywołanie szukania ruchów, możemy za jednym zamachem zbić więcej niz 1 pionka
                        pozX = max(x-3,-1)
                    else:
                        pozX = min(x+3,X)
                    ruchy.update(self.ruchWLewo(x+krok, pozX, krok, gracz, zakres-1, zbitePionki=zbitePionki+ostatniPionek))    #Szukanie nowych ruchów na lewo i prawo, tym razem jedynymi możliwościami będą tylko kolejne zbicia, tablica zbite pinki ma już w sobie zawartość
                    ruchy.update(self.ruchWPrawo(x+krok, pozX, krok, gracz, zakres+1, zbitePionki=zbitePionki+ostatniPionek))
                break
            elif aktualnyPionek.gracz == gracz:         #Jeśli zawartością pola jest pionek, sprawdzamy do którego gracza należy. Jeśli do atkualnego, to kończymy szukanie, nad własnym pionkeim nie można przeskoczyć
                break
            else:
                ostatniPionek = [aktualnyPionek]        #Jeśli zawartością pola jest pionek przeciwnika, moze być możliwość przeskoczenia go. Idziemy więc po skosie na kolejne pole

            zakres -= 1
        
        return ruchy    #Zwracanie dostępnych ruchów

    def ruchWPrawo(self, start, koniec, krok, gracz, zakres, zbitePionki=[]):   #Analogicznie jak w ruchu w lewo, tym razem w drugą stronę
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


    def ruch(self,x,y):                     #Wykonanie ruchu
        wolneMiejsce = self.plansza[x][y]   #Miejsce na które chcemy wykonać ruch
        if self.wybranyPionek and wolneMiejsce == 0 and (x,y) in self.dostepneRuchy:    #Jeśłi mamy wybrany pionek, miejsce nie jest zajęte (0) i dane miejsce jest na liście dostępnych ruchów, mozemy się tu poruszyć
            self.plansza[self.wybranyPionek.pozX][self.wybranyPionek.pozY], self.plansza[x][y] = self.plansza[x][y], self.plansza[self.wybranyPionek.pozX][self.wybranyPionek.pozY]     #Jednoczesna zamiana przycisków i obiektów, stare miejsce zostaje zwolnione, nowe ma na sobie teraz pionka
            self.przyciski[self.wybranyPionek.pozX][self.wybranyPionek.pozY] = ttk.Button(self.mainframe, text="", command=lambda pozX=self.wybranyPionek.pozX, pozY=self.wybranyPionek.pozY:self.wybor(pozX,pozY,"")).grid(row = self.wybranyPionek.pozX, column=self.wybranyPionek.pozY)

            if isinstance(self.wybranyPionek, Damka):   #Jeśli obiekt jest damką, mam mieć dodatkowo "d" przy swojej nazwie
                temp = self.wybranyPionek.gracz + "d"
            else: 
                temp = self.plansza[x][y].gracz
            
            self.przyciski[x][y] = ttk.Button(self.mainframe, text=temp, command=lambda pozX=x, pozY=y, text=temp:self.wybor(pozX,pozY,text)).grid(row = x, column = y)     #Aktualizowanie przycisku
            self.wybranyPionek.ruch(x,y)

            if (x == X-1) and self.plansza[x][y].gracz == 'C' and not isinstance(self.plansza[x][y], Damka):        #Sprawdzanie czy pionek nie zamieni się w damke
                self.plansza[x][y] = Damka(x,y,"C")
                self.przyciski[x][y] = ttk.Button(self.mainframe, text='Cd', command=lambda pozX=x, pozY=y:self.wybor(pozX,pozY,"C")).grid(row = x, column = y)
                print("Damka C")
            elif (x == 0) and self.plansza[x][y].gracz == 'B' and not isinstance(self.plansza[x][y], Damka):
                self.plansza[x][y] = Damka(x,y,"B")
                self.przyciski[x][y] = ttk.Button(self.mainframe, text='Bd', command=lambda pozX=x, pozY=y:self.wybor(pozX,pozY,"B")).grid(row = x, column = y)
                print("Damka B")
            
            zbitePionki = self.dostepneRuchy[(x,y)]     #Usuwanie zbitych pionków z planszy
            if zbitePionki:
                self.usunPionek(zbitePionki)
            self.nastepnaTura()                         #Zmiana tury
        
        else:
            return False                                #W razie niepowodznie ruchu zwracamy False
        
        return True

    def nastepnaTura(self):                             #Zmiana tury
        self.dostepneRuchy = {}                         #Czyścimy dostepne ruchy
        if self.tura == "C":                            #Jeśli turę miał gracz czarny, teraz turę ma gracz biały, i na odwrót. Aktualizowanie informacji.
            self.tura = "B"
            self.info = Label(self.mainframe, text="Tura gracza 2").grid(row=2, column=9, padx=15)
            print("Tura gracza 2")
        else:
            self.tura = "C"
            self.info = Label(self.mainframe, text="Tura gracza 1").grid(row=2, column=9, padx=15)
            print("Tura gracza 1")

    def usunPionek(self, pionki):                       #Usuwanie wszystkich zbitych pionków, wstawanie w ich miejsca pustych pól (0), aktualizowanie siatki przycisków
        for pionek in pionki:
            self.plansza[pionek.pozX][pionek.pozY] = 0
            self.przyciski[pionek.pozX][pionek.pozY] = (ttk.Button(self.mainframe, text="", command=lambda x=pionek.pozX, y=pionek.pozY :self.wybor(x,y,"")).grid(row = pionek.pozX, column = pionek.pozY))
            if pionek !=0:
                if pionek.gracz == "C":
                    self.liczbaPionkowCzarne -= 1
                else:
                    self.liczbaPionkowBiale -= 1
        
        if self.liczbaPionkowCzarne <= 0:               #Jeśli którykolwiek z graczy stracił swoje pionki wywołujemy wygraną
            self.wygrana("B")
        elif self.liczbaPionkowBiale <= 0:
            self.wygrana("C")
    
    def wygrana(self, wygrany):
        if wygrany == "C":
            messagebox.showinfo("Wygral gracz 1")
        elif wygrany == "B":
            messagebox.showinfo("Wygral gracz 2")



warcaby = Warcaby()

        