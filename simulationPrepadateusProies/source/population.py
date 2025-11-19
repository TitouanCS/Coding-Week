from random import randint
from source.animal import *
from source.genes import *


class Population():

    """
    Classe Population

    Cette classe gère une population d'animaux (renards, lapins et ours) dans une grille, avec la gestion des coordonnées, des identifiants, et des caractéristiques génétiques.

    Attributs :
        - __TAILLE (int) : Taille de la grille (côté de la grille carrée).
        - __AnimauxPopulation (list) : Liste contenant les animaux indexés par leurs identifiants. Les emplacements vides sont représentés par -1.
        - __idsUtilisables (list) : Liste des identifiants disponibles pour ajouter de nouveaux animaux.

    Méthodes :
        - __init__(TAILLE) : Initialise une population vide dans une grille de taille TAILLE x TAILLE.
        - getAnimauxPopulation() -> list : Retourne la liste des animaux dans la population.
        - getIdsUtilisables() -> list : Retourne la liste des identifiants disponibles.
        - getAnimal(id) -> object : Retourne l'animal correspondant à l'identifiant donné.
        - getTAILLE() -> int : Retourne la taille de la grille.
        - deleteAnimal(animal) : Supprime un animal de la population et libère son identifiant.
        - selectId() -> int : Sélectionne un identifiant libre. Lève une ValueError s'il n'y en a plus.
        - addAnimal(sexe, coord, genes=None) -> int : Ajoute un animal dans la grille en fonction du sexe (0=Renard, 1=Lapin, 2=Ours) et des coordonnées. Retourne l'identifiant de l'animal ajouté.
        - geneFrequency(gene) -> dict : Retourne les fréquences relatives d'un gène spécifique dans la population.
        - alleleFrequenciesByGeneByAnimal() -> dict : Retourne les fréquences d'allèles par gène et par espèce dans la population.
        - animaux_ids() -> list : Retourne une liste des identifiants de tous les animaux présents.
        - renard_ids() -> list : Retourne une liste des identifiants des renards.
        - lapin_ids() -> list : Retourne une liste des identifiants des lapins.
        - ours_ids() -> list : Retourne une liste des identifiants des ours.
        - animaux_coord() -> list : Retourne une liste des coordonnées de tous les animaux présents.
        - renard_coord() -> list : Retourne une liste des coordonnées des renards.
        - lapin_coord() -> list : Retourne une liste des coordonnées des lapins.
        - ours_coord() -> list : Retourne une liste des coordonnées des ours.

    Exceptions :
        - ValueError : Levée dans `selectId()` si aucun identifiant n'est disponible ou dans `addAnimal()` si les coordonnées ou l'espèce sont invalides.
"""

    def __init__(self, TAILLE):
        self.__TAILLE = TAILLE
        self.__AnimauxPopulation = [
            -1 for _ in range(self.__TAILLE*self.__TAILLE)]
        self.__idsUtilisables = list(range(self.__TAILLE*self.__TAILLE))

    # Getters

    def getAnimauxPopulation(self):
        return self.__AnimauxPopulation

    def getIdsUtilisables(self):
        return self.__idsUtilisables

    def getAnimal(self, id):
        return self.__AnimauxPopulation[id]

    def getTAILLE(self):
        return self.__TAILLE

    # Méthodes de classe

    def deleteAnimal(self, animal):
        id_ = animal.get_id()
        self.__AnimauxPopulation[id_] = -1
        self.__idsUtilisables.append(id_)

    def selectId(self):
        if len(self.__idsUtilisables) == 0:
            raise ValueError("Plus de place")
        res = self.getIdsUtilisables()[0]
        self.__idsUtilisables = self.__idsUtilisables[1::]
        return res

    def addAnimal(self, sexe, coord, genes=None):
        x, y = coord.get_coord()
        if not (0 <= x < self.getTAILLE() and 0 <= y < self.getTAILLE()):
            raise ValueError("Coordonnée(s) invalide(s)")
        id_ = self.selectId()
        if (sexe == 0):
            self.__AnimauxPopulation[id_] = Renard(coord, id_, genes)
        elif sexe == 1:
            self.__AnimauxPopulation[id_] = Lapin(coord, id_, genes)
        elif sexe == 2:
            self.__AnimauxPopulation[id_] = Ours(coord, id_)
        else:
            raise ValueError(
                """L'argument [espece] est un entier entre 0 et 2""")
        return id_

    def alleleFrequenciesByGeneByAnimal(self):

        def alleleFrequenciesByGene(espece):

            allelesByGene = dict()

            for id_ in self.animaux_ids():
                animal = self.getAnimal(id_)
                if isinstance(animal, espece):
                    # Pour chaque gène de l'animal, on met à jour les fréquences des allèles
                    for gene, allele in animal.get_genes().items():
                        if gene not in allelesByGene:
                            allelesByGene[gene] = {}
                        if allele not in allelesByGene[gene]:
                            allelesByGene[gene][allele] = 1
                        else : allelesByGene[gene][allele] += 1
            # Calcul des proportions des allèles
            alleleProportionsByGene = {}
            for gene, countByAllele in allelesByGene.items():
                alleleProportionsByGene[gene] = {}
                if espece == Lapin:
                    for allele, alleleCount in countByAllele.items():
                        alleleProportionsByGene[gene][allele] = alleleCount / \
                            len(self.lapin_ids())

                elif espece == Renard:
                    for allele, alleleCount in countByAllele.items():
                        alleleProportionsByGene[gene][allele] = alleleCount / \
                            len(self.renard_ids())
                else:
                    # espèce = Ours
                    for allele, alleleCount in countByAllele.items():
                        alleleProportionsByGene[gene][allele] = alleleCount / \
                            len(self.ours_ids())
            return alleleProportionsByGene

        return {
            "Renard": alleleFrequenciesByGene(Renard),
            "Lapin": alleleFrequenciesByGene(Lapin)
        }

    def animaux_ids(self):
        """Retourne une liste des ids des animaux"""
        return [animal.get_id() for animal in self.__AnimauxPopulation if animal != -1]

    def renard_ids(self):
        """Retourne une liste des ids des renards."""
        return [animal.get_id() for animal in self.__AnimauxPopulation if animal != -1 and isinstance(animal, Renard)]

    def lapin_ids(self):
        """Retourne une liste des ids des lapins."""
        return [animal.get_id() for animal in self.__AnimauxPopulation if animal != -1 and isinstance(animal, Lapin)]

    def ours_ids(self):
        """Retourne une liste des ids des lapins."""
        return [animal.get_id() for animal in self.__AnimauxPopulation if animal != -1 and isinstance(animal, Ours)]

    def animaux_coord(self):
        """Retourne une liste des ids des animaux"""
        return [animal.get_coord() for animal in self.__AnimauxPopulation if animal != -1]

    def renard_coord(self):
        """Retourne une liste des corrdonnées des renards."""
        return [animal.get_coord() for animal in self.__AnimauxPopulation if animal != -1 and isinstance(animal, Renard)]

    def lapin_coord(self):
        """Retourne une liste des coordonnéés des lapins."""
        return [animal.get_coord() for animal in self.__AnimauxPopulation if animal != -1 and isinstance(animal, Lapin)]

    def ours_coord(self):
        return [animal.get_coord() for animal in self.__AnimauxPopulation if animal != -1 and isinstance(animal, Ours)]
