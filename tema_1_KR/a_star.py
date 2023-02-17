# din nou m-am folosit de modelul de la laborator pentru a* si am folosit clasele mele
def a_star(gr, nrSolutiiCautate, euristica="banala"):
    # in coada vom avea doar noduri de tip Stare
    c = [gr.start]

    while len(c) > 0:
        print("Coada actuala: " + str(c))
        nodCurent = c.pop(0)
        lSuccesori, nrSolutiiCautate = gr.genereazaSuccesori(nodCurent, nrSolutiiCautate, euristica)
        if nrSolutiiCautate == 0:
            return
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # diferenta fata de UCS e ca ordonez dupa valoare, care determina un cost aproximativ pana la o solutie
                if c[i].valoare > s.valoare or (c[i].valoare == s.valoare and c[i].cost < s.cost):
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)
