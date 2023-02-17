# la algoritmul ucs m-am folosit de modelul de la laborator si l-am adaptat la clasele mele
def uniform_cost(gr, nrSolutiiCautate=1):
    # in coada vom avea doar noduri de tip Stare
    c = [gr.start]

    while len(c) > 0:
        print("Coada actuala: " + str(c))
        nodCurent = c.pop(0)

        lSuccesori, nrSolutiiCautate = gr.genereazaSuccesori(nodCurent, nrSolutiiCautate)
        if nrSolutiiCautate == 0:
            return
        for s in lSuccesori:
            i = 0
            gasit_loc = False
            for i in range(len(c)):
                # ordonez dupa cost, care este costul intregului drum pana la momentul actual
                if c[i].cost > s.cost:
                    gasit_loc = True
                    break
            if gasit_loc:
                c.insert(i, s)
            else:
                c.append(s)
