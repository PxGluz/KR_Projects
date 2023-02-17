#### algoritm BF
# presupunem ca vrem mai multe solutii (un numar fix) prin urmare vom folosi o variabilă numită nrSolutiiCautate
# daca vrem doar o solutie, renuntam la variabila nrSolutiiCautate
# si doar oprim algoritmul la afisarea primei solutii

# ne folosim de codul de bf de la laborator, cu mici schimbari pentru adaptarea la clasele create pentru problema
def breadth_first(gr, nrSolutiiCautate=1):
    # in coada vom avea doar noduri de tip Stare, in care se vor memora coloanele de blocuri
    c = [gr.start]

    while len(c) > 0:
        print("Coada actuala:\n" + str(c))
        nodCurent = c.pop(0)
        # solutiile vor fi determinate in momentul in care acestea intra in lista de succesori si vor fi afisate daca sunt gasite
        lSuccesori, nrSolutiiCautate = gr.genereazaSuccesori(nodCurent, nrSolutiiCautate)
        if nrSolutiiCautate == 0:
            return
        c.extend(lSuccesori)


# ne vom folosi din nou de modelul de la laborator pentru df cu micile modificari aplicate si la bf pentru adaptarea la clasele proprii
def depth_first(gr, nrSolutiiCautate=1):
    # vom simula o stiva prin relatia de parinte a nodului curent
    df(gr, gr.start, nrSolutiiCautate)


def df(gr, nodCurent, nrSolutiiCautate):
    if nrSolutiiCautate <= 0:  # testul acesta s-ar valida doar daca in apelul initial avem df(start,if nrSolutiiCautate=0)
        return nrSolutiiCautate
    print("\nStiva actuala: " + "->\n".join([x.__str__() for x in nodCurent.obtineDrum()]) + f"\nvalue: {nodCurent.valoare}")

    lSuccesori, nrSolutiiCautate = gr.genereazaSuccesori(nodCurent, nrSolutiiCautate)
    if nrSolutiiCautate == 0:
        return nrSolutiiCautate
    for sc in lSuccesori:
        if nrSolutiiCautate != 0:
            nrSolutiiCautate = df(gr, sc, nrSolutiiCautate)

    return nrSolutiiCautate


#############################################

# din nou ne vom folosi de codul de la laborator pentru dfi si ii vom aduce modificari pentru adaptarea la clasele specifice problemei
def dfi(gr, nodCurent, adancime, nrSolutiiCautate):
    print("\nStiva actuala: " + "->\n".join([x.__str__() for x in nodCurent.obtineDrum()]))
    if adancime > 1:
        lSuccesori, nrSolutiiCautate = gr.genereazaSuccesori(nodCurent, nrSolutiiCautate)
        if nrSolutiiCautate == 0:
            return nrSolutiiCautate
        for sc in lSuccesori:
            if nrSolutiiCautate != 0:
                nrSolutiiCautate = dfi(gr, sc, adancime - 1, nrSolutiiCautate)
    return nrSolutiiCautate


def depth_first_iterativ(gr, nrSolutiiCautate=1):
    # aici ne vom folosi de o adancime destul de generoasa care permite trecerea celei mai mari coloane pe o alta coloana
    for i in range(1, max([len(x) for x in gr.start.coloane]) + 1):
        if nrSolutiiCautate == 0:
            return
        print("**************\nAdancime maxima: ", i)
        nrSolutiiCautate = dfi(gr, gr.start, i, nrSolutiiCautate)
