import time

import pygame, sys, copy, math

ADANCIME_MAX = 3

def elem_identice(lista):
    if (all(elem == lista[0] for elem in lista[1:])):
        return lista[0] if lista[0] != Joc.GOL and lista[0] != Joc.VALID else False
    return False


class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_COLOANE = 10
    JMIN = None  # Jucatorul
    JMAX = None  # Botul
    GOL = '#'
    VALID = '*'

    @classmethod
    def initializeaza(cls, display, NR_COLOANE=10, dim_celula=50):
        cls.display = display
        cls.dim_celula = dim_celula
        cls.x_img = pygame.image.load('ics.png')
        cls.x_img = pygame.transform.scale(cls.x_img, (
        dim_celula, math.floor(dim_celula * cls.x_img.get_height() / cls.x_img.get_width())))
        cls.zero_img = pygame.image.load('zero.png')
        cls.zero_img = pygame.transform.scale(cls.zero_img, (
        dim_celula, math.floor(dim_celula * cls.zero_img.get_height() / cls.zero_img.get_width())))
        cls.celuleGrid = []  # este lista cu patratelele din grid
        for linie in range(NR_COLOANE):
            cls.celuleGrid.append([])
            for coloana in range(NR_COLOANE):
                patr = pygame.Rect(coloana * (dim_celula + 1), linie * (dim_celula + 1), dim_celula, dim_celula)
                cls.celuleGrid[linie].append(patr)

    def deseneaza_grid(self, marcaj=None):  # tabla de exemplu este ["#","x","#","0",......]

        for linie in range(Joc.NR_COLOANE):
            for coloana in range(Joc.NR_COLOANE):
                if marcaj == (linie, coloana):
                    # daca am o patratica selectata, o desenez cu rosu
                    culoare = (255, 0, 0)
                elif self.matr[linie][coloana] == Joc.GOL:
                    # altfel o desenez cu alb
                    culoare = (180, 180, 180)
                else:
                    culoare = (255, 255, 255)
                pygame.draw.rect(self.__class__.display, culoare,
                                 self.__class__.celuleGrid[linie][coloana])  # alb = (255,255,255)
                if self.matr[linie][coloana] == 'x':
                    self.__class__.display.blit(self.__class__.x_img, (coloana * (self.__class__.dim_celula + 1),
                                                                                          linie * (self.__class__.dim_celula + 1)))
                elif self.matr[linie][coloana] == '0':
                    self.__class__.display.blit(self.__class__.zero_img, (coloana * (self.__class__.dim_celula + 1),
                                                                                              linie * (self.__class__.dim_celula + 1)))
        # pygame.display.flip() # !!! obligatoriu pentru a actualiza interfata (desenul)
        pygame.display.update()

    def __init__(self, tabla=None, runde_ramase=20):
        if tabla:
            self.matr = tabla
        else:
            self.matr = []
            for i in range(self.__class__.NR_COLOANE):
                self.matr.append([self.__class__.GOL] * self.__class__.NR_COLOANE)
            self.matr[4][4] = 'x'
            self.matr[5][4] = 'x'
            self.matr[4][5] = '0'
            self.matr[5][5] = '0'
            self.matr[3][4] = '*'
            self.matr[3][5] = '*'
            self.matr[6][4] = '*'
            self.matr[6][5] = '*'
        self.runde_ramase = runde_ramase
        self.scor_min = 0
        self.scor_max = 0
        for i in range(len(self.matr) - 2):
            for j in range(2, len(self.matr)):
                self.scor_min += 1 if elem_identice([self.matr[i][j], self.matr[i + 1][j - 1], self.matr[i + 2][j - 2]]) == self.JMIN else 0
                self.scor_max += 1 if elem_identice([self.matr[i][j], self.matr[i + 1][j - 1], self.matr[i + 2][j - 2]]) == self.JMAX else 0
        for i in range(len(self.matr) - 2):
            for j in range(len(self.matr) - 2):
                self.scor_min += 1 if elem_identice([self.matr[i][j], self.matr[i + 1][j + 1], self.matr[i + 2][j + 2]]) == self.JMIN else 0
                self.scor_max += 1 if elem_identice([self.matr[i][j], self.matr[i + 1][j + 1], self.matr[i + 2][j + 2]]) == self.JMAX else 0

    @classmethod
    def jucator_opus(cls, jucator):
        return cls.JMAX if jucator == cls.JMIN else cls.JMIN

    def final(self):
        if sum([self.VALID in linie for linie in self.matr]) == 0 or self.runde_ramase <= 0:
            return True
        else:
            return False

    MOVE_PER_X = [-1, 0, 1, 0]
    MOVE_PER_Y = [0, -1, 0, 1]

    MOVE_X = [-1, -1, 0, 1, 1, 1, 0, -1]
    MOVE_Y = [0, -1, -1, -1, 0, 1, 1, 1]

    def valid_square(self, matrix, linie, coloana):
        found_x, found_0, has_space = False, False, False
        for i in range(len(self.MOVE_X)):
            if 0 <= linie + self.MOVE_X[i] < len(matrix) and 0 <= coloana + self.MOVE_Y[i] < len(matrix):
                found_0 = True if matrix[linie + self.MOVE_X[i]][coloana + self.MOVE_Y[i]] == '0' else found_0
                found_x = True if matrix[linie + self.MOVE_X[i]][coloana + self.MOVE_Y[i]] == 'x' else found_x
        for i in range(len(self.MOVE_PER_X)):
            if 0 <= linie + Joc.MOVE_PER_X[i] < len(matrix) and 0 <= coloana + Joc.MOVE_PER_Y[i] < len(matrix) and (matrix[linie + Joc.MOVE_PER_X[i]][coloana + Joc.MOVE_PER_Y[i]] == '#' or matrix[linie + Joc.MOVE_PER_X[i]][coloana + Joc.MOVE_PER_Y[i]] == '*'):
                has_space = True
        # print(f"{linie}, {coloana} : {found_0}, {found_x}, {has_space}")
        return found_0 and found_x and has_space

    def mutari(self, jucator):  # jucator = simbolul jucatorului care muta
        l_mutari = []
        for i in range(self.__class__.NR_COLOANE):
            for j in range(self.__class__.NR_COLOANE):
                if self.matr[i][j] == Joc.VALID:
                    for m in range(len(self.MOVE_PER_X)):
                        copie_matr = copy.deepcopy(self .matr)
                        if 0 <= i + self.MOVE_PER_X[m] < len(copie_matr) and 0 <= j + self.MOVE_PER_Y[m] < len(copie_matr) and (copie_matr[i + self.MOVE_PER_X[m]][j + self.MOVE_PER_Y[m]] == '#' or copie_matr[i + self.MOVE_PER_X[m]][j + self.MOVE_PER_Y[m]] == '*'):
                            copie_matr[i][j] = jucator
                            copie_matr[i + self.MOVE_PER_X[m]][j + self.MOVE_PER_Y[m]] = jucator
                            for k in range(len(copie_matr)):
                                for l in range(len(copie_matr)):
                                    if copie_matr[k][l] == Joc.GOL and self.valid_square(copie_matr, k, l):
                                        copie_matr[k][l] = '*'
                                    elif copie_matr[k][l] == Joc.VALID and not self.valid_square(copie_matr, k, l):
                                        copie_matr[k][l] = '#'
                            l_mutari.append(Joc(copie_matr, runde_ramase=self.runde_ramase - 1))
        return l_mutari

    # linie deschisa inseamna linie pe care jucatorul mai poate forma o configuratie castigatoare
    # practic e o linie fara simboluri ale jucatorului opus
    def linie_deschisa(self, lista, jucator):
        jo = self.jucator_opus(jucator)
        # verific daca pe linia data nu am simbolul jucatorului opus
        if not jo in lista:
            return 1
        return 0

    def linii_deschise(self, jucator):
        sum_lines = 0
        for i in range(len(self.matr) - 2):
            for j in range(2, len(self.matr)):
                sum_lines += self.linie_deschisa([self.matr[i][j], self.matr[i + 1][j - 1], self.matr[i + 2][j - 2]], jucator)
        for i in range(len(self.matr) - 2):
            for j in range(len(self.matr) - 2):
                sum_lines += self.linie_deschisa([self.matr[i][j], self.matr[i + 1][j + 1], self.matr[i + 2][j + 2]], jucator)
        return sum_lines

    def estimeaza_scor(self, adancime):
        t_final = self.final()
        if t_final:
            if self.scor_min >= self.scor_max:
                return -999
            else:
                return 999
        else:
            # return (self.linii_deschise(self.__class__.JMAX) - self.linii_deschise(self.__class__.JMIN)) # Bot-ul incearca sa incurce jucatorul cat mai mult
            return (self.scor_max - self.scor_min) # Bot-ul incearca sa obtina o diferenta cat mai mare de scor

    def sirAfisare(self):
        sir = "  |"
        sir += " ".join([str(i) for i in range(self.NR_COLOANE)]) + "\n"
        sir += "-" * (self.NR_COLOANE + 1) * 2 + "\n"
        for i in range(self.NR_COLOANE):  # itereaza prin linii
            sir += str(i) + " |" + " ".join([str(x) for x in self.matr[i]]) + "\n"
        return sir

    def __str__(self):
        return self.sirAfisare()

    def __repr__(self):
        return self.sirAfisare()


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari() care ofera lista cu configuratiile posibile in urma mutarii unui jucator
    """

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, estimare=None):
        self.tabla_joc = tabla_joc
        self.j_curent = j_curent

        # adancimea in arborele de stari
        self.adancime = adancime

        # estimarea favorabilitatii starii (daca e finala) sau al celei mai bune stari-fiice (pentru jucatorul curent)
        self.estimare = estimare

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def mutari(self):
        l_mutari = self.tabla_joc.mutari(self.j_curent)
        juc_opus = Joc.jucator_opus(self.j_curent)
        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]

        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + f"Scor {Joc.JMIN}: {self.tabla_joc.scor_min} - Scor {Joc.JMAX}: {self.tabla_joc.scor_max}\n(Juc curent:" + self.j_curent + f")\nRunde ramase: {self.tabla_joc.runde_ramase}\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        # print(f"\nEstimare: {stare.estimare}\n")
        return stare

    # calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutariCuEstimare = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu estimarea maxima
        stare.stare_aleasa = max(mutariCuEstimare, key=lambda x: x.estimare)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu estimarea minima
        stare.stare_aleasa = min(mutariCuEstimare, key=lambda x: x.estimare)
    stare.estimare = stare.stare_aleasa.estimare
    return stare


def alpha_beta(alpha, beta, stare):
    if stare.adancime == 0 or stare.tabla_joc.final():
        stare.estimare = stare.tabla_joc.estimeaza_scor(stare.adancime)
        # print(f"\nEstimare: {stare.estimare}\n")
        return stare

    if alpha > beta:
        return stare  # este intr-un interval invalid deci nu o mai procesez

    stare.mutari_posibile = stare.mutari()

    if stare.j_curent == Joc.JMAX:
        estimare_curenta = float('-inf')

        for mutare in stare.mutari_posibile:
            # calculeaza estimarea pentru starea noua, realizand subarborele
            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta < stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare
            if (alpha < stare_noua.estimare):
                alpha = stare_noua.estimare
                if alpha >= beta:
                    break

    elif stare.j_curent == Joc.JMIN:
        estimare_curenta = float('inf')

        for mutare in stare.mutari_posibile:

            stare_noua = alpha_beta(alpha, beta, mutare)

            if (estimare_curenta > stare_noua.estimare):
                stare.stare_aleasa = stare_noua
                estimare_curenta = stare_noua.estimare

            if (beta > stare_noua.estimare):
                beta = stare_noua.estimare
                if alpha >= beta:
                    break
    stare.estimare = stare.stare_aleasa.estimare

    return stare


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if (final):
        end_condition = "S-au terminat rundele!" if stare_curenta.tabla_joc.runde_ramase <= 0 else "Nu mai sunt miscari valide!"
        winner_text = Joc.JMIN + " a castigat!" if stare_curenta.tabla_joc.scor_min > stare_curenta.tabla_joc.scor_max else (Joc.JMAX + " a castigat!" if stare_curenta.tabla_joc.scor_min < stare_curenta.tabla_joc.scor_max else "Egalitate!")
        print(f"{end_condition}\n {winner_text}!\nScor {Joc.JMIN}: {stare_curenta.tabla_joc.scor_min} - Scor {Joc.JMAX}: {stare_curenta.tabla_joc.scor_max}")
        return True

    return False


def main():
    # initializare algoritm
    raspuns_valid = False
    mod_joc = '1'
    while not raspuns_valid:
        mod_joc = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Player vs. Player\n 2.Player vs. AI\n 3.Min-Max vs. Alpha-Beta\n 4.Min-Max vs. Min-Max\n 5. Alpha-Beta vs. Alpha-Beta\n")
        if mod_joc in ['1', '2', '3', '4', '5']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")
    if mod_joc != '1':
        if mod_joc == '2':
            raspuns_valid = False
            while not raspuns_valid:
                tip_algoritm = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-beta\n ")
                if tip_algoritm in ['1', '2']:
                    raspuns_valid = True
                else:
                    print("Nu ati ales o varianta corecta.")
            # initializare jucatori
            raspuns_valid = False
            while not raspuns_valid:
                Joc.JMIN = input("Doriti sa jucati cu x sau cu 0? ").lower()
                if (Joc.JMIN in ['x', '0']):
                    raspuns_valid = True
                else:
                    print("Raspunsul trebuie sa fie x sau 0.")
            Joc.JMAX = '0' if Joc.JMIN == 'x' else 'x'

        raspuns_valid = False
        while not raspuns_valid:
            try:
                temp = input("Cu ce adancime sa vada algoritmul/algoritmii? (Default 3) ")
                if temp == "":
                    ADANCIME_MAX = 3
                    raspuns_valid = True
                else:
                    ADANCIME_MAX = int(temp)
                    if ADANCIME_MAX <= 0:
                        float("eroare")
                    else:
                        raspuns_valid = True
            except ValueError as e:
                print("Adancimea trebuie sa fie un intreg mai mare decat 0\n")
                print(e)
    if mod_joc != '2':
        Joc.JMIN = 'x'
        Joc.JMAX = '0'
        if mod_joc != '5':
            tip_algoritm = '1'
        else:
            tip_algoritm = '2'
    runde_de_jucat = 20
    raspuns_valid = False
    while not raspuns_valid:
        try:
            temp = input("Cate runde va avea meciul? (Default 20) ")
            if temp == "":
                runde_de_jucat = 20
                raspuns_valid = True
            else:
                runde_de_jucat = int(temp)
                if runde_de_jucat <= 0:
                    float("eroare")
                else:
                    raspuns_valid = True
        except ValueError as e:
            print("Rundele trebuie sa fie un intreg mai mare decat 0\n")
            print(e)
    # initializare tabla
    tabla_curenta = Joc(runde_ramase=runde_de_jucat)
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala

    stare_curenta = Stare(tabla_curenta, 'x', ADANCIME_MAX if mod_joc != '1' else 0)

    # setari interf grafica
    pygame.init()
    pygame.display.set_caption('x si 0')
    # dimensiunea ferestrei in pixeli
    # dim_celula=..
    ecran = pygame.display.set_mode(
        size=(Joc.NR_COLOANE * 50 + Joc.NR_COLOANE - 1, Joc.NR_COLOANE * 50 + Joc.NR_COLOANE - 1))  # N *100+ (N-1)*dimensiune_linie_despartitoare (dimensiune_linie_despartitoare=1)
    Joc.initializeaza(ecran)

    tabla_curenta.deseneaza_grid()
    player_moves = 0
    while True:

        if (stare_curenta.j_curent == Joc.JMIN or mod_joc == '1') and mod_joc != '3' and mod_joc != '4' and mod_joc != '5':
            # muta jucatorul
            # [MOUSEBUTTONDOWN, MOUSEMOTION,....]
            # l=pygame.event.get()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()  # inchide fereastra
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:  # click

                    pos = pygame.mouse.get_pos()  # coordonatele clickului

                    for linie in range(Joc.NR_COLOANE):
                        for coloana in range(Joc.NR_COLOANE):

                            if Joc.celuleGrid[linie][coloana].collidepoint(
                                    pos):  # verifica daca punctul cu coord pos se afla in dreptunghi(celula)
                                ###############################


                                if stare_curenta.tabla_joc.matr[linie][coloana] == Joc.VALID:
                                    # plasez simbolul pe "tabla de joc"
                                    stare_curenta.tabla_joc.matr[linie][coloana] = stare_curenta.j_curent
                                    for k in range(len(stare_curenta.tabla_joc.matr)):
                                        for l in range(len(stare_curenta.tabla_joc.matr)):
                                            # print(f"{k}, {l}")
                                            if player_moves == 1:
                                                if stare_curenta.tabla_joc.matr[k][l] == Joc.GOL and stare_curenta.tabla_joc.valid_square(stare_curenta.tabla_joc.matr, k, l):
                                                    stare_curenta.tabla_joc.matr[k][l] = '*'
                                                elif stare_curenta.tabla_joc.matr[k][l] == Joc.VALID and not stare_curenta.tabla_joc.valid_square(stare_curenta.tabla_joc.matr, k, l):
                                                    stare_curenta.tabla_joc.matr[k][l] = '#'
                                            else:
                                                if stare_curenta.tabla_joc.matr[k][l] == Joc.VALID:
                                                    stare_curenta.tabla_joc.matr[k][l] = '#'
                                    if player_moves == 0:
                                        for i in range(len(Joc.MOVE_PER_X)):
                                            if 0 <= linie + Joc.MOVE_PER_X[i] < len(stare_curenta.tabla_joc.matr) and 0 <= coloana + Joc.MOVE_PER_Y[i] < len(stare_curenta.tabla_joc.matr) and stare_curenta.tabla_joc.matr[linie + Joc.MOVE_PER_X[i]][coloana + Joc.MOVE_PER_Y[i]] == '#':
                                                stare_curenta.tabla_joc.matr[linie + Joc.MOVE_PER_X[i]][coloana + Joc.MOVE_PER_Y[i]] = '*'
                                    stare_curenta.tabla_joc.deseneaza_grid()
                                    if player_moves == 1:

                                        # afisarea starii jocului in urma mutarii utilizatorului

                                        stare_curenta = Stare(Joc(stare_curenta.tabla_joc.matr, stare_curenta.tabla_joc.runde_ramase - 1), stare_curenta.j_curent, ADANCIME_MAX if mod_joc != '1' else 0)
                                        print("\nTabla dupa mutarea jucatorului")
                                        print(str(stare_curenta))

                                        # testez daca jocul a ajuns intr-o stare finala
                                        # si afisez un mesaj corespunzator in caz ca da
                                        if (afis_daca_final(stare_curenta)):
                                            break

                                        # S-a realizat o mutare. Schimb jucatorul cu cel opus
                                        stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
                                        player_moves = 0
                                    else:
                                        player_moves += 1


        # --------------------------------
        elif stare_curenta.j_curent == Joc.JMAX or mod_joc == '3' or mod_joc == '4' or mod_joc == '5':  # jucatorul e JMAX (calculatorul)
            # Mutare calculator
            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            stare_curenta.tabla_joc.deseneaza_grid()
            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = Joc.jucator_opus(stare_curenta.j_curent)
            if mod_joc == '3':
                if tip_algoritm == '1':
                    tip_algoritm = '2'
                else:
                    tip_algoritm = '1'


if __name__ == "__main__":
    main()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
