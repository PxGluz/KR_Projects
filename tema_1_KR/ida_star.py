# acesta este codul de la laborator pe care l-am adaptat la clasele mele
def ida_star(gr, nrSolutiiCautate, euristica="banala"):
    nodStart = gr.start
    limita = nodStart.valoare  # Stabilim limita ca fiind valoarea primei stari
    while True:
        print("Limita de pornire: ", limita)
        nrSolutiiCautate, rez = construieste_drum(gr, nodStart, limita, nrSolutiiCautate, euristica)
        if rez == "gata":  # in cazul in care a gasit numarul de solutii cautat
            break
        if rez == float('inf'):  # in cazul in care s-au gasit toate starile
            print("Nu mai exista solutii!")
            break
        limita = rez
        print(">>> Limita noua: ", limita)  # se schimba limita pana se atinge una din conditiile de mai sus


def construieste_drum(gr, nodCurent, limita, nrSolutiiCautate, euristica):
    print(f"A ajuns la: \n{nodCurent.coloane.__str__()}\n")
    if nodCurent.valoare > limita:  # gasim o stare mai proasta decat cea pe care am ales-o ca limita
        return nrSolutiiCautate, nodCurent.valoare
    lSuccesori, nrSolutiiCautate = gr.genereazaSuccesori(nodCurent, nrSolutiiCautate, euristica=euristica)
    if nrSolutiiCautate == 0:
        return 0, "gata"
    minim = float('inf')
    for s in lSuccesori:
        nrSolutiiCautate, rez = construieste_drum(gr, s, limita, nrSolutiiCautate, euristica)
        if rez == "gata":
            return 0, "gata"
        print("Compara ", rez, " cu ", minim)
        if rez < minim:
            minim = rez
            print("Noul minim: ", minim)
    return nrSolutiiCautate, minim
