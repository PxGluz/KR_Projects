# m-am folosit de a_star_optimizat de la laborator si m-am folosit de clasele mele
def a_star(gr, nrSolutiiCautate, euristica="banala"):
    # in coada vom avea doar noduri de tip Stare
    l_open = [gr.start]

    # l_open contine nodurile candidate pentru expandare (este echivalentul lui c din A* varianta neoptimizata)

    # l_closed contine nodurile expandate
    l_closed = []
    while len(l_open) > 0:
        print("Coada actuala: " + str(l_open))
        nodCurent = l_open.pop(0)
        l_closed.append(nodCurent)
        lSuccesori, nrSolutiiCautate = gr.genereazaSuccesori(nodCurent, nrSolutiiCautate, euristica=euristica)
        if nrSolutiiCautate == 0:
            return
        for s in lSuccesori:
            gasitC = False
            for nodC in l_open:
                if s.coloane == nodC.coloane:
                    gasitC = True
                    if s.valoare >= nodC.valoare:
                        lSuccesori.remove(s)
                    else:  # s.valoare<nodC.valoare
                        l_open.remove(nodC)
                    break
            if not gasitC:
                for nodC in l_closed:
                    if s.coloane == nodC.coloane:
                        if s.valoare >= nodC.valoare:
                            lSuccesori.remove(s)
                        else:  # s.valoare<nodC.valoare
                            l_closed.remove(nodC)
                        break
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(l_open)):
                # diferenta fata de UCS e ca ordonez crescator dupa valoare
                # daca valoarile sunt egale ordonez descrescator dupa cost
                if l_open[i].valoare > s.valoare or (l_open[i].valoare == s.valoare and l_open[i].cost <= s.cost):
                    gasit_loc = True
                    break
            if gasit_loc:
                l_open.insert(i, s)
            else:
                l_open.append(s)
