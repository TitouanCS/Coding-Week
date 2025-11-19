from abc import ABC, abstractmethod
import numpy as np
from random import randint
from source.genes import *


class Animal(ABC):

    """
    Module simulant une population animale dans un écosystème avec des caractéristiques génétiques.

    Classes :
    ---------
    - Animal : Classe abstraite représentant un animal générique avec des méthodes communes.
    - Renard : Classe représentant un renard, héritant d'Animal.
    - Lapin : Classe représentant un lapin, héritant d'Animal.
    - Ours : Classe représentant un ours, héritant d'Animal.

    Attributs de classe communs (dans Animal) :
    ------------------------------------------
    - PARAMETERS : Dictionnaire contenant des paramètres globaux pour tous les animaux 

    Classes détaillées :
    -------------------
    1. **Animal (classe abstraite)** :
    - Constructeur :
        - Initialise les coordonnées, l'identifiant, l'âge, le sexe, et les gènes (aléatoires ou fournis).
    - Méthodes abstraites : 
        - `vaMourir` : Détermine si l'animal doit mourir.
        - `reduireVie` : Réduit les ressources nécessaires pour la survie.
        - `peutSeReproduire` : Vérifie si l'animal peut se reproduire.
        - `mange` : Simule l'action de manger.
        - `__str__` : Retourne une représentation textuelle de l'animal.
    - Méthodes générales :
        - `set_coord` et `get_coord` : Accès et modification des coordonnées.
        - `get_id` : Retourne l'identifiant unique de l'animal.
        - `get_sexe` : Retourne le sexe de l'animal.
        - `get_age` : Retourne l'âge de l'animal.
        - `vieillit` : Augmente l'âge en fonction des gènes.
        - `get_genes` : Retourne les gènes de l'animal.

    2. **Renard** :
    - Ajoute un attribut spécifique : `__food` (nourriture actuelle).
    - Intègre l'influence des gènes dans :
        - `mange` : Augmente la nourriture en tenant compte des gènes liés à l'appétit.
        - `reduireVie` : Réduit la nourriture en tenant compte des gènes d'esquive.
    - Méthodes spécifiques :
        - `peutSeReproduire` : Vérifie si le renard peut se reproduire en fonction de sa nourriture et d'une probabilité.
        - `vaMourir` : Vérifie si le renard doit mourir (famine ou vieillesse).
        - `__str__` : Retourne une représentation sous la forme `"R<id>"`.

    3. **Lapin** :
    - Ajoute un attribut spécifique : `__food` (nourriture actuelle).
    - Intègre l'influence des gènes dans :
        - `mange` : Augmente la nourriture en tenant compte des gènes liés à l'appétit.
        - `reduireVie` : Réduit la nourriture en tenant compte des gènes d'esquive.
    - Méthodes spécifiques :
        - `peutSeReproduire` : Vérifie si le lapin peut se reproduire.
        - `vaMourir` : Vérifie si le lapin doit mourir (famine ou vieillesse).
        - `__str__` : Retourne une représentation sous la forme `"L<id>"`.

    4. **Ours** :
    - Ajoute un attribut spécifique : `__food` (nourriture actuelle).
    - Méthodes spécifiques :
        - `mange(type_proie)` : L'ours mange un lapin ou un renard pour augmenter sa nourriture.
        - `peutSeReproduire` : Vérifie si l'ours peut se reproduire en fonction de sa nourriture et d'une probabilité.
        - `vaMourir` : Vérifie si l'ours doit mourir (famine ou vieillesse).
        - `reduireVie` : Réduit la nourriture de l'ours à chaque cycle.
        - `__str__` : Retourne une représentation sous la forme `"O<id>"`.

"""

    PARAMETERS = {
        "foodInitRenard": 5,
        "foodInitLapin": 10,
        "foodInitOurs": 5,  # Nourriture initiale pour l'ours
        "foodLapin": 5,
        'foodHerbe': 10,
        "foodRenard": 10,   # Nourriture gagnée en mangeant un renard
        "foodReprodRenard": 8,
        "foodReprodLapin": 2,
        "foodReprodOurs": 2,  # Seuil de nourriture pour reproduction
        "maxFoodRenard": 10,
        "maxFoodLapin": 10,
        "maxFoodOurs": 30,  # Capacité maximale de nourriture pour l'ours
        "maxAge": 100,
        "maxAgeOurs": 150,  # Espérance de vie maximale pour l'ours
        "ProbaBirthR": 0.15,
        "ProbaBirthOurs": 0.1,# Probabilité de reproduction pour les ours
        'CoeffGeneE' : 5,
        'CoeffGeneM' :5
    }

    def __init__(self, Coord, id, genes=None):
        if (genes is None):
            self._genes = create_random()
        else:
            self._genes = genes
        self.__coord = Coord
        self.__id = id
        self.__age = 0
        self.__sexe = randint(0, 1)

    def set_coord(self, coord):
        self.__coord = coord

    def get_coord(self):
        return self.__coord

    def get_id(self):
        return self.__id

    def get_sexe(self):
        return self.__sexe

    def get_age(self):
        return self.__age

    def get_genes(self):
        return self._genes

    def vieillit(self):
        self.__age += 1 + (self._genes[Genes.MANGE] *(self.PARAMETERS['CoeffGeneM']/10))

    def get_genes(self):
        return self._genes

    @abstractmethod
    def vaMourir(self):
        pass

    @abstractmethod
    def reduireVie(self):
        pass

    @abstractmethod
    def peutSeReproduire(self):
        pass

    @abstractmethod
    def mange(self):
        pass

    @abstractmethod
    def __str__(self):
        pass


class Renard(Animal):

    def __init__(self, Coord, id, genes=None):
        super().__init__(Coord, id, genes)
        self.__food = self.PARAMETERS["foodInitRenard"]

    def get_food(self):
        return self.__food

    def set_food(self, food):
        self.__food = food

    def mange(self):
        ajoute = 5*self._genes[Genes.MANGE] / (self.PARAMETERS['CoeffGeneM'])
        self.__food = min(
            self.__food+self.PARAMETERS["foodLapin"]+ajoute, self.PARAMETERS["maxFoodRenard"]+2 * ajoute)

    def peutSeReproduire(self):
        return self.__food >= self.PARAMETERS["foodReprodRenard"] and np.random.binomial(1, self.PARAMETERS['ProbaBirthR'])

    def vaMourir(self):
        
        return self.get_age() >= self.PARAMETERS["maxAge"] or self.__food <= 0

    def reduireVie(self):
        self.__food = self.__food - 1 - (self._genes[Genes.ESQUIVE] * (self.PARAMETERS["CoeffGeneE"]/10))

    def __str__(self):
        return f"R{self.get_id()}"


class Lapin(Animal):

    def __init__(self, Coord, id, genes=None):
        super().__init__(Coord, id, genes)
        self.__food = self.PARAMETERS["foodInitLapin"]

    def get_food(self):
        return self.__food

    def set_food(self, food):
        self.__food = food

    def mange(self):
        ajoute = 5*self._genes[Genes.MANGE] / (self.PARAMETERS['CoeffGeneM'])
        self.__food = min(
            self.__food + self.PARAMETERS["foodHerbe"]+ajoute, self.PARAMETERS["maxFoodLapin"] + 2*ajoute)

    def peutSeReproduire(self):
        return self.__food >= self.PARAMETERS["foodReprodLapin"]

    def __str__(self):
        return f"L{self.get_id()}"

    def vaMourir(self):
        return self.get_age() >= self.PARAMETERS["maxAge"] or self.__food <= 0

    def reduireVie(self):
        self.__food = self.__food - 1 - (self._genes[Genes.ESQUIVE] * (self.PARAMETERS["CoeffGeneE"]/10))


class Ours(Animal):

    def __init__(self, Coord, id):
        super().__init__(Coord, id)
        self.__food = self.PARAMETERS["foodInitOurs"]

    def get_food(self):
        return self.__food

    def set_food(self, food):
        self.__food = food

    def mange(self, type_proie):
        """L'ours mange soit un lapin, soit un renard."""
        if type_proie == "lapin":
            self.__food = min(
                self.__food +
                self.PARAMETERS["foodLapin"], self.PARAMETERS["maxFoodOurs"]
            )
        elif type_proie == "renard":
            self.__food = min(
                self.__food +
                self.PARAMETERS["foodRenard"], self.PARAMETERS["maxFoodOurs"]
            )

    def peutSeReproduire(self):
        """L'ours peut se reproduire s'il a suffisamment de nourriture et selon une probabilité."""
        return self.__food >= self.PARAMETERS["foodReprodOurs"] and np.random.binomial(1, self.PARAMETERS["ProbaBirthOurs"])

    def vaMourir(self):
        """Un ours meurt soit par vieillesse, soit par famine."""
        return self.get_age() >= self.PARAMETERS["maxAgeOurs"] or self.__food <= 0

    def reduireVie(self):
        """Réduction de la nourriture à chaque cycle."""
        self.__food -= 1

    def __str__(self):
        return f"O{self.get_id()}"
