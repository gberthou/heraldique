from analyse import Symbole, Mot, Analyse

class Regle:
    def __init__(self, symbole, taille):
        self.symbole = symbole
        self.taille = taille

class Transition:
    def __init__(self, symbole, decalage, num):
        # decalage: True -> decalage, False -> reduction
        # num: numero de l'etat a atteindre si decalage,
        #      numero de la regle si reduction

        self.symbole = symbole
        self.decalage = decalage
        self.num = num

class Etat:
    def __init__(self, transitions):
        self.transitions = transitions

    def verifierTransition(self, mot):
        print(mot.symbole)
        candidats = [t for t in self.transitions if t.symbole == mot.symbole]
        taille = len(candidats)
        if taille == 0:
            raise Exception("L'etat courant n'a pas de transition pour le symbole donne")
        elif taille > 1:
            raise Exception("L'automate est ambigu")
        return candidats[0]

ETATS = [
    #0
    Etat([Transition(Symbole.d, True, 6),
          Transition(Symbole.e, True, 8),
          Transition(Symbole.P, True, 1),
          Transition(Symbole.C, True, 2),
          Transition(Symbole.E, True, 5)]),
    #1
    Etat([Transition(Symbole.att, False, 0),
          Transition(Symbole.et, False, 0),
          Transition(Symbole.fin, True, -1)]),
    #2
    Etat([Transition(Symbole.a, True, 3),
          Transition(Symbole.att, False, 12),
          Transition(Symbole.et, False, 12),
          Transition(Symbole.fin, False, 12)]),
    #3
    Etat([Transition(Symbole.n, True, 13),
          Transition(Symbole.F, True, 4),
          Transition(Symbole.N, True, 14)]),
    #4
    Etat([Transition(Symbole.fin, False, 11)]),
    #5
    Etat([Transition(Symbole.fin, False, 13)]),
    #6
    Etat([Transition(Symbole.c, True, 7),
          Transition(Symbole.fin, False, 3)]),
    #7
    Etat([Transition(Symbole.att, False, 5),
          Transition(Symbole.et, False, 5),
          Transition(Symbole.fin, False, 5)]),
    #8
    Etat([Transition(Symbole.d, True, 6),
          Transition(Symbole.et, False, 8),
          Transition(Symbole.fin, False, 8),
          Transition(Symbole.C, True, 12),
          Transition(Symbole.LC, True, 9)]),
    #9
    Etat([Transition(Symbole.et, True, 10),
          Transition(Symbole.fin, False, 9)]),
    #10
    Etat([Transition(Symbole.d, True, 6),
          Transition(Symbole.C, True, 11)]),
    #11
    Etat([Transition(Symbole.att, False, 7),
          Transition(Symbole.et, False, 7),
          Transition(Symbole.fin, False, 7)]),
    #12
    Etat([Transition(Symbole.att, False, 6),
          Transition(Symbole.et, False, 6)]),
    #13
    Etat([Transition(Symbole.f, False, 3)]),
    #14
    Etat([Transition(Symbole.f, True, 15)]),
    #15
    Etat([Transition(Symbole.d, True, 6),
          Transition(Symbole.C, True, 16)]),
    #16
    Etat([Transition(Symbole.att, True, 18),
          Transition(Symbole.fin, False, 2),
          Transition(Symbole.A, True, 17)]),
    #17
    Etat([Transition(Symbole.fin, False, 10)]),
    #18
    Etat([Transition(Symbole.fin, False, 1)])
]

REGLES = [
    Regle(Symbole.P2, 1),
    Regle(Symbole.A, 1),
    Regle(Symbole.A, 0),
    Regle(Symbole.N, 1),
    Regle(Symbole.N, 0),
    Regle(Symbole.C, 2),
    Regle(Symbole.LC, 1),
    Regle(Symbole.LC, 3),
    Regle(Symbole.LC, 0),
    Regle(Symbole.E, 2),
    Regle(Symbole.F, 4),
    Regle(Symbole.P, 3),
    Regle(Symbole.P, 1),
    Regle(Symbole.P, 1)
]

class Automate:
    def __init__(self):
        self.mots = []  # Pile
        self.etats = [] # Pile

    def appliquerTransition(self, an, mot):
        etat = self.etats[-1]
        for i,e in enumerate(ETATS):
            if e == etat:
                print("ETAT %d"%i)
        
        transition = etat.verifierTransition(mot)
        if transition.decalage:
            if transition.num == -1: # Chaine acceptee
                return True
            else:
                self.etats.append(ETATS[transition.num])
                if transition.symbole.value <= Symbole.fin.value:
                    self.mots.append(mot)
                    print("a")
                    an.lireMot()
        else: # Reduction
            regle = REGLES[transition.num]
            contenu = []
            for i in range(regle.taille):
                contenu.append(self.mots.pop())
                self.etats.pop()
            contenu.reverse()
            mot = Mot(regle.symbole.value, contenu)
            self.mots.append(mot)
            self.appliquerTransition(an, mot)
        return False

    def parse(self, chaine):
        self.etats.append(ETATS[0])

        an = Analyse(chaine)
        mot = an.lireMot()
        n=0
        while mot != None:
            print("-------%d"%n)
            print(self.mots)
            print(self.etats)
            n+=1

            if self.appliquerTransition(an, mot):
                break

            mot = an.getMotCourant()

        if len(self.mots) != 1 or self.mots[0].symbole != Symbole.P:
            raise Exception("Erreur de syntaxe")

        return self.mots[0]


auto = Automate()
mot = auto.parse("parti de sinople et de sable")
mot.afficher()

