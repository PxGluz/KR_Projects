import time
from BF_DF_DFI import breadth_first, depth_first, depth_first_iterativ
from ucs import uniform_cost
from a_star import a_star
from a_star_optimizat import a_star as a_star_op
from ida_star import ida_star


class Bloc:
    def __init__(self, nume, g, r):
        self.nume = nume  # memoram numele blocului
        self.g = g  # greutatea blocului
        self.r = r  # rezistenta blocului

    def __repr__(self):
        return f"({self.nume}, {self.g}, {self.r})"


class Stare:
    def __init__(self, coloane, parinte=None, cost=0, euristica="banala"):
        self.coloane = coloane  # list de coloane
        self.parinte = parinte  # parintele din arborele de parcurgere
        self.valoare = self.valoare_stare(euristica)  # aproximare a costului pentru a ajunge la o solutie
        self.cost = cost  # costul total al blocurilor mutate pana la starea actuala

    def valoare_stare(self, euristica):
        """
        Functia care este folosita la initializare pentru determinarea valorii unei stari

        :param euristica: tipul de euristica care poate fi ales (banala, admisibila1, admisibila2, neadmisibila::default)
        :return: returneaza valoarea starii in functie de euristica aleasa
        """
        len_list = [len(x) for x in self.coloane]
        goal = int(sum(len_list) / len(self.coloane))
        plus_one_columns = sum(len_list) % len(self.coloane)
        value = 0
        if euristica == "banala":  # la euristica banala doar determinam daca starea este starea finala prin 0 daca este solutie sau 1 daca nu este solutie
            for col in len_list:
                if col > goal:
                    if plus_one_columns and col == goal + 1:
                        plus_one_columns -= 1
                    else:
                        value = 1
        elif euristica == "admisibila1":  # la euristica admisibila1 determinam cate blocuri ar trebui mutate pentru a se ajunge la o solutie
            for col in len_list:
                if col > goal:
                    if plus_one_columns:
                        value += col - goal - 1
                        plus_one_columns -= 1
                    else:
                        value += col - goal
        elif euristica == "admisibila2":  # la euristica admisibila2 determinam suma costurilor blocurilor care trebuie mutate
            for i in range(len(len_list)):
                if len_list[i] > goal:
                    if plus_one_columns:
                        value += sum([x.g for x in self.coloane[i][-(len_list[i] - goal - 1):]])
                        plus_one_columns -= 1
                    else:
                        value += sum([x.g for x in self.coloane[i][-(len_list[i] - goal):]])
        else:  # la euristica neadmisibila inmultim valoarea de la euristica admisibila1 cu 1000
            for col in len_list:
                if col > goal:
                    if plus_one_columns:
                        value += (col - goal - 1) * 1000
                        plus_one_columns -= 1
                    else:
                        value += (col - goal) * 1000
        return value

    def obtineDrum(self):
        """
        Functie pentru obtinerea unei liste de coloane ale starilor care au fost parcurse pentru a fi atinsa starea curenta

        :return: returneaza listle de coloane ale starilor parcurse pentru a ajunge la starea curenta
        """
        l = [self.coloane]
        stare = self
        while stare.parinte is not None:
            l.insert(0, stare.parinte.coloane)
            stare = stare.parinte
        return l

    def afisDrum(self):  # returneaza si lungimea drumului
        """
        Functie apelata pentru afisarea drumului in consola sub forma unei solutii

        :return: returneaza lungimea drumului
        """
        l = self.obtineDrum()
        for stare in l:
            print_list = []
            len_list = [len(x) for x in stare]
            i = 0
            while i < max(len_list):
                print_list.insert(0, "")
                for col in stare:
                    if len(col) <= i:
                        print_list[0] += ("          " if i != 0 else "_______   ")
                    else:
                        print_list[0] += f"[{col[i].nume}/{col[i].g}/{col[i].r}]   "
                i += 1
            for row in print_list:
                print(row)
            equal_amount = max([len(x) for x in print_list])
            while equal_amount:
                print('=', end='')
                equal_amount -= 1
            print()
        return len(l)

    def contineInDrum(self, infoNodNou):
        """
        Functie folosita pentru determinarea daca o stare a fost deja atinsa pe drumul unei alte stari

        :param infoNodNou: lista de coloane a starii care trebuie verificate
        :return: returneaza un True daca starea apare in drum si False daca starea nu apare in drum
        """
        # return infoNodNou in self.obtineDrum()
        nodDrum = self
        while nodDrum is not None:
            if (infoNodNou == nodDrum.coloane):
                return True
            nodDrum = nodDrum.parinte

        return False

    def stare_valida(self):
        """
        Functie apelata pentru validarea unei stari (daca exista blocuri a caror rezistenta este depasita)

        :return: returneaza False in cazul in care starea este invalida si True daca starea este valida
        """
        for col in self.coloane:
            for i in range(len(col)):
                s = sum([x.g for x in col[i+1:]])
                if s > col[i].r:
                    return False
        return True

    def __repr__(self):
        representation = ""
        for col in self.coloane:
            representation += col.__str__() + "\n"
        representation += f"Valoare: {self.valoare}\n---------------------------------\n"
        return representation


class Graph:  # graful problemei

    def __init__(self, start):
        self.start = start  # informatia nodului de start
        self.start_time = time.time()  # timpul de la inceperea programului

    # va genera succesorii sub forma de noduri in arborele de parcurgere
    def genereazaSuccesori(self, stare_curenta, nr_solutii_cautate, euristica="banala"):
        """
        Functie folosita pentru generarea tuturor succesorilor valizi ai unei stari, si filtrarea solutiilor valide

        :param stare_curenta: starea in care se afla programul la apelarea functiei
        :param nr_solutii_cautate: numarul ramas de solutii care trebuie cautate
        :param euristica: euristica aleasa pentru determinarea valorii unei stari
        :return: returneaza 2 parametrii: o lista de succesori si numarul de solutii ramase de cautat
        """
        listaSuccesori = []
        for i in range(len(stare_curenta.coloane)):
            if len(stare_curenta.coloane[i]) > 0:
                for j in range(len(stare_curenta.coloane)):  # se parcurg toate coloanele pe care poate fi mutat blocul de pe coloana i
                    if j == i:
                        continue
                    coloane_temp = [[Bloc(y.nume, y.g, y.r) for y in x] for x in stare_curenta.coloane]
                    coloane_temp[j].append(coloane_temp[i].pop())
                    if not stare_curenta.contineInDrum(coloane_temp):  # se verifica daca starea obtinuta a mai fost atinsa pe drumul starii curente
                        stare_noua = Stare(coloane_temp, stare_curenta, stare_curenta.cost + coloane_temp[j][-1].g, euristica=euristica)
                        if stare_noua.stare_valida():
                            if self.testeaza_scop(stare_curenta=stare_noua) and nr_solutii_cautate > 0:  # se filtreaza solutiile ca acestea sa nu fie adaugate in lista de succesori
                                print("Solutie:")
                                stare_noua.afisDrum()
                                print(f"Cost: {stare_noua.cost}\nTimp cautare: {time.time() - self.start_time} s\n##################################\n")
                                nr_solutii_cautate -= 1
                            else:
                                listaSuccesori.append(stare_noua)
        return listaSuccesori, nr_solutii_cautate

    def testeaza_scop(self, stare_curenta):
        """
        Functie care determina daca starea in care ne aflam este o solutie

        :param stare_curenta: starea in care se afla coloanele
        :return: returneaza True daca starea este solutie si False daca starea nu este solutie
        """
        return stare_curenta.valoare == 0


def citire_din_fisier(nume_fisier="blocheaza.txt", euristica="banala"):
    """
    Functie care citeste datele dupa cum a fost specificat formatul din enunt, cu o euristica aleasa si din fisierul specificat

    :param nume_fisier: numele fisierului din care vor fi citite datele
    :param euristica: euristica aleasa pentru determinarea valorii
    :return: returneaza un obiect de tip Graph care contine starea initiala specificata in fisierul de intrare
    """
    coloane = []
    with open(nume_fisier) as f:
        lines = f.readlines()
    for line in lines:
        line = line[:-1] if line[-1] == '\n' else line
        blocks = line.split('|')
        col = []
        if line != "_":
            for block in blocks:
                properties = block.split(',')
                new_bloc = Bloc(properties[0], int(properties[1]), int(properties[2]))
                col.append(new_bloc)
        coloane.append(col)
    new_stare = Stare(coloane, euristica=euristica)
    if new_stare.stare_valida():
        grafic = Graph(new_stare)
        if grafic.testeaza_scop(grafic.start):
            print("Starea initiala este solutie!\n")
            grafic.start.afisDrum()
        else:
            return Graph(new_stare)
    else:
        print("Stare de start invalida!")
        return None


if __name__ == "__main__":
    fisier_ales = "nu_blocheaza.txt"
    euristica_aleasa = "admisibila1"
    nrSolutiiCautate = 4

    gr = citire_din_fisier(fisier_ales, euristica_aleasa)

    if gr is not None:
        breadth_first(gr, nrSolutiiCautate=nrSolutiiCautate)
        # depth_first(gr, nrSolutiiCautate=nrSolutiiCautate)
        # depth_first_iterativ(gr, nrSolutiiCautate=nrSolutiiCautate)
        # uniform_cost(gr, nrSolutiiCautate=nrSolutiiCautate)
        # a_star(gr, nrSolutiiCautate=nrSolutiiCautate, euristica=euristica_aleasa)
        # a_star_op(gr, nrSolutiiCautate=nrSolutiiCautate, euristica=euristica_aleasa)
        # ida_star(gr, nrSolutiiCautate=nrSolutiiCautate, euristica=euristica_aleasa)
