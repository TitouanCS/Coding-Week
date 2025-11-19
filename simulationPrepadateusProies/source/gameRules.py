from source.grille import *
from source.population import *
from source.environnement import *
from random import randint


class GameRules():

    """
    Classe GameRules pour la gestion des règles de jeu d'une simulation d'écosystème.

    Cette classe gère les interactions entre les éléments de l'écosystème (renards, lapins, ours, herbe, etc.),
    ainsi que les règles de déplacement, reproduction, et alimentation. Elle repose sur une grille (`Grille`) 
    et une population (`Population`).

    Attributs de classe :
    ---------------------
    - PARAMETERS : dict
        Dictionnaire contenant les paramètres de la simulation, comme la taille de la grille ou les pourcentages 
        d'apparition d'herbe.

    Attributs d'instance :
    ----------------------
    - __grille : Grille
        Représentation de la grille de jeu.
    - __population : Population
        Gestion de la population animale sur la grille.

    Méthodes principales :
    ----------------------
    - __init__() :
        Initialise une grille, une population et ajoute les éléments initiaux (animaux et herbe) selon `PARAMETERS`.

    - bouge(iden: int) :
        Gère le mouvement et les interactions d'un animal spécifique, y compris la reproduction et l'alimentation.

    - generation() :
        Avance la simulation d'une génération, en déplaçant tous les animaux et en ajoutant de l'herbe si nécessaire.

    - estFiniJeu() -> bool :
        Vérifie si les conditions de fin de jeu (extinction des lapins ou renards) sont remplies.

    - checkInvariant() :
        Effectue des vérifications pour garantir la cohérence entre la grille et la population.

    - addOursAleatoire() :
        Ajoute un ours aléatoirement sur une case vide, selon les paramètres de simulation.

    - __str__() -> str :
        Retourne une représentation textuelle de la grille de jeu.
    """

    PARAMETERS = {}

    # Constructeur

    def __init__(self):

        TAILLE = self.PARAMETERS["Taille"]
        POURCENTAGE_HERBE = self.PARAMETERS["Apparition herbe (%)"]
        self.__grille = Grille(TAILLE)
        self.__population = Population(TAILLE)
        nb_herbe = (POURCENTAGE_HERBE*(TAILLE*TAILLE)) // 100
        tab_coord = [Coordonnee(i, j) for i in range(TAILLE)
                     for j in range(TAILLE)]

        for i in range(GameRules.PARAMETERS["Renards"]):
            aleatoire = randint(0, len(tab_coord)-1)
            c_aleatoire = tab_coord.pop(aleatoire)
            id_ = self.__population.addAnimal(0, c_aleatoire)
            self.set_id(c_aleatoire, id_)
        for i in range(GameRules.PARAMETERS["Lapins"]):
            aleatoire = randint(0, len(tab_coord)-1)
            c_aleatoire = tab_coord.pop(aleatoire)
            id_ = self.__population.addAnimal(1, c_aleatoire)
            self.set_id(c_aleatoire, id_)

        tab_coord = [Coordonnee(i, j) for i in range(TAILLE)
                     for j in range(TAILLE)]
        for i in range(nb_herbe):
            aleatoire = randint(0, len(tab_coord)-1)
            c_aleatoire = tab_coord.pop(aleatoire)
            self.set_envi(c_aleatoire, Environnement.HERBE)

    # Getters
    def get_id(self, c):
        return self.__grille.get_id(c)

    def get_envi(self, c):
        return self.__grille.get_environnement(c)

    def get_grille(self):
        return self.__grille

    def get_population(self):
        return self.__population

    # Setters

    def set_id(self, c, iden):
        self.__grille.set_animalId(c, iden)

    def set_envi(self, c, e):
        self.__grille.set_environnement(c, e)

    def set_population(self, population):
        self.__population = population

    def set_grille(self):
        self.__grille

    def bouge(self, iden):
        coord = self.__population.getAnimal(iden).get_coord()
        TAILLE = self.PARAMETERS["Taille"]
        ajout_herbe = True  # Indique si de l'herbe doit être ajoutée après un mouvement
        x = 1
        couple = None

        if iden != -1:  # Si la case contient un animal
            animal = self.__population.getAnimal(iden)
            sexe_animal = animal.get_sexe()
            cases_voisines = coord.case_voisine(
                TAILLE)  # Indique si l'animal a mangé
            reproduction = False  # Indique si l'animal peut se reproduire
            a_bouge = False

            # Vérification si l'animal doit mourir
            if animal.vaMourir():
                self.__population.deleteAnimal(animal)
                self.set_id(coord, -1)  # Case devient vide
                return

            # Gestion spécifique selon le type d'animal
            if isinstance(animal, Renard):
                x = 0
                perdtour = False
                # Cherche un lapin à manger
                cases_lapin = [
                    c for c in cases_voisines if self.is_prey(c, Lapin)]
                if cases_lapin:
                    cible = self.choisir_au_hasard(cases_lapin)
                    lapin_cible = self.__population.getAnimal(
                        self.get_id(cible))
                    lapin_genes = lapin_cible.get_genes()
                    reprod = np.random.binomial(
                        1, lapin_genes[Genes.ESQUIVE]/Animal.PARAMETERS['CoeffGeneE'])
                    if (reprod == 0):
                        self.manger_animal(coord, cible, iden)
                        a_bouge = True
                    else:
                        perdtour = True

                # Vérifie les possibilités de reproduction
                cases_libres = [
                    c for c in cases_voisines if self.get_id(c) == -1]
                voisins_opposés = [
                    c for c in cases_voisines if self.is_opposite_sex(c, sexe_animal, Renard)
                ]

                # Se déplace si possible (priorité au déplacement après avoir mangé)
                if not a_bouge and len(cases_libres) > 0 and not perdtour:
                    cible = self.choisir_au_hasard(cases_libres)
                    self.deplacer_animal(coord, cible, iden)
                    a_bouge = True

                if a_bouge and len(voisins_opposés) > 0:
                    if (animal.peutSeReproduire()):
                        couple = self.__population.getAnimal(
                            self.get_id(self.choisir_au_hasard(voisins_opposés)))
                        reproduction = True

            elif isinstance(animal, Lapin):
                ajout_herbe = False
                # Cherche de l'herbe à manger
                x = 1
                cases_herbe = [c for c in cases_voisines if (self.get_envi(
                    c) == Environnement.HERBE and self.get_id(c) == -1)]
                if cases_herbe:
                    cible = self.choisir_au_hasard(cases_herbe)
                    self.manger_herbe(coord, cible, iden)
                    a_bouge = True
                    ajout_herbe = True

                # Vérifie les possibilités de reproduction
                cases_libres = [
                    c for c in cases_voisines if self.get_id(c) == -1]
                voisins_opposés = [
                    c for c in cases_voisines if self.is_opposite_sex(c, sexe_animal, Lapin)
                ]
                if voisins_opposés and (len(cases_libres) > 0):
                    if (animal.peutSeReproduire()):
                        reproduction = True
                        couple = self.__population.getAnimal(
                            self.get_id(self.choisir_au_hasard(voisins_opposés)))

                # Se déplace si possible (priorité au déplacement après avoir mangé)
                if not a_bouge and cases_libres:
                    cible = self.choisir_au_hasard(cases_libres)
                    self.deplacer_animal(coord, cible, iden)
                    a_bouge = True
                    ajout_herbe = True

            elif isinstance(animal, Ours):
                perdtour = False
                x = 2
                # Cherche un lapin ou renard à manger
                cases_proix = [c for c in cases_voisines if (
                    self.is_prey(c, Lapin) or self.is_prey(c, Renard))]
                if cases_proix:
                    cible = self.choisir_au_hasard(cases_proix)
                    lapin_cible = self.__population.getAnimal(
                        self.get_id(cible))
                    lapin_genes = lapin_cible.get_genes()
                    reprod = np.random.binomial(
                        1, lapin_genes[Genes.ESQUIVE]/Animal.PARAMETERS['CoeffGeneE'])
                    if ( reprod == 0):
                        self.manger_animal(coord, cible, iden)
                        a_bouge = True
                    else:
                        perdtour = True

                # Vérifie les possibilités de reproduction
                cases_libres = [
                    c for c in cases_voisines if self.get_id(c) == -1]
                voisins_opposés = [
                    c for c in cases_voisines if self.is_opposite_sex(c, sexe_animal, Ours)
                ]

                # Se déplace si possible (priorité au déplacement après avoir mangé)
                if not a_bouge and len(cases_libres) > 0 and not perdtour:
                    cible = self.choisir_au_hasard(cases_libres)
                    self.deplacer_animal(coord, cible, iden)
                    a_bouge = True

                if (a_bouge and len(voisins_opposés) > 0):
                    if (animal.peutSeReproduire()):
                        reproduction = True

            # Si reproduction possible, création d'un nouvel animal
            if reproduction and len(self.get_population().getIdsUtilisables()) > 0:
                if (not isinstance(animal, Ours)):
                    nouveau_gene = genes_parent(
                        animal.get_genes(), couple.get_genes())
                    nouveau_id = self.__population.addAnimal(
                        x, coord, nouveau_gene)
                    self.set_id(coord, nouveau_id)
                else:
                    nouveau_id = self.__population.addAnimal(x, coord)
                    self.set_id(coord, nouveau_id)

                if (type(animal) == Lapin):
                    ajout_herbe = False

            # Vieillissement et réduction de la vie
            animal.vieillit()
            animal.reduireVie()

        # Gestion d'ajout d'herbe
        if ajout_herbe:
            r = randint(0, 100)
            if 0 <= r < self.PARAMETERS["Apparition herbe (%)"]:
                self.set_envi(coord, Environnement.HERBE)
        # Fonctions utilitaires

    def is_prey(self, coord, prey_type):
        """Vérifie si une case contient une proie du type donné."""
        id_voisin = self.get_id(coord)
        if id_voisin != -1:
            animal = self.get_population().getAnimal(id_voisin)
            return isinstance(animal, prey_type)
        return False

    def is_opposite_sex(self, coord, sexe, animal_type):
        """Vérifie si une case contient un animal du sexe opposé et du même type."""
        id_voisin = self.get_id(coord)
        if id_voisin != -1:
            animal = self.get_population().getAnimal(id_voisin)
            return isinstance(animal, animal_type) and animal.get_sexe() != sexe
        return False

    def choisir_au_hasard(self, cases):
        """Retourne une case choisie aléatoirement parmi une liste."""
        return cases[randint(0, len(cases) - 1)]

    def manger_animal(self, origine, cible, iden):
        """Un animal mange une autre proie et occupe sa case."""
        id_proie = self.get_id(cible)
        animal = self.__population.getAnimal(iden)
        proix = self.__population.getAnimal(id_proie)
        self.__population.deleteAnimal(proix)
        self.set_id(cible, iden)
        self.set_id(origine, -1)
        animal.set_coord(cible)
        if (isinstance(animal, Ours)):
            if (isinstance(proix, Lapin)):
                animal.mange('lapin')
            else:
                animal.mange('renard')
        else:
            animal.mange()

    def manger_herbe(self, origine, cible, iden):
        """Un animal mange de l'herbe sur une case."""
        animal = self.__population.getAnimal(iden)
        self.set_envi(cible, Environnement.VIDE)
        self.set_id(cible, iden)
        self.set_id(origine, -1)
        animal.set_coord(cible)
        animal.mange()

    def deplacer_animal(self, origine, cible, iden):
        """Un animal se déplace vers une case libre."""

        animal = self.__population.getAnimal(iden)
        self.set_id(cible, iden)
        self.set_id(origine, -1)
        animal.set_coord(cible)

    def generation(self):
        ours = self.get_population().ours_ids()
        for c in ours:
            self.bouge(c)

        renard_jouer = self.get_population().renard_ids()
        for c in renard_jouer:
            self.bouge(c)
        lapin_jouer = self.get_population().lapin_ids()
        for c in lapin_jouer:
            self.bouge(c)

        case_vide = self.__grille.case_Vide()
        for c in case_vide:
            if self.get_envi(c) == Environnement.VIDE:
                r = randint(0, 100)
                if 0 <= r < self.PARAMETERS["Apparition herbe (%)"]:
                    self.set_envi(c, Environnement.HERBE)

    def estFiniJeu(self):
        if len(self.get_population().renard_coord()) == 0:
            return True
        if len(self.get_population().lapin_coord()) == 0:
            return True

        return False

    def addOursAleatoire(self):
        quantite = self.PARAMETERS['Ours']
        for _ in range(quantite):
            if (len(self.get_population().getIdsUtilisables()) > 0):
                coord_hasard = self.__grille.coord_hasard()
                nv_id = self.__population.addAnimal(2, coord_hasard)
                self.set_id(coord_hasard, nv_id)

    def checkInvariant(self):
        nbAnimauxGrille = 0
        TAILLE = self.get_grille().get_TAILLE()
        for i in range(TAILLE):
            for j in range(TAILLE):
                index = i*TAILLE + j
                id_ = self.get_id(Coordonnee(i, j))
                if id_ != -1:
                    nbAnimauxGrille += 1
                    assert self.get_population().getAnimal(id_).get_coord().get_coord() == (i, j)
                    assert self.get_population().getAnimal(id_).get_id() == id_
                if self.get_population().getAnimal(index) == -1:
                    assert index in self.get_population().getIdsUtilisables()
                else:
                    assert index not in self.get_population().getIdsUtilisables()
        animaux_coord = [coord.get_coord()
                         for coord in self.get_population().animaux_coord()]
        for i, (x, y) in enumerate(animaux_coord):
            nbVu = 0
            if animaux_coord[i] == (x, y):
                nbVu += 1
            assert nbVu == 1
        try:
            assert nbAnimauxGrille == len(self.get_population().animaux_ids())
        except AssertionError as e:
            print(nbAnimauxGrille, len(self.get_population().animaux_ids()))

    def __str__(self):
        return str(self.__grille)
