from source.coordonnee import *
from source.environnement import *
from random import randint


class Grille():

    """
    Classe GameRules pour la gestion des règles de jeu d'une simulation d'écosystème.

    Cette classe gère les interactions entre les éléments de l'écosystème (renards, lapins, ours, herbe, etc.),
    ainsi que les règles de déplacement, reproduction, et alimentation. Elle repose sur une grille (`Grille`) 
    et une population (`Population`), qui sont des dépendances essentielles.

    Attributs de classe :
    ---------------------
    - PARAMETERS : dict
        Dictionnaire contenant les paramètres de simulation. Exemples de clés :
        - "Taille" : int, taille de la grille (NxN).
        - "APPARITION HERBE (%)" : int, pourcentage de chance qu'une case vide produise de l'herbe après une génération.
        - "Renards" : int, nombre initial de renards.
        - "Lapins" : int, nombre initial de lapins.
        - "Ours" : int, nombre initial d'ours.

    Attributs d'instance :
    ----------------------
    - __grille : Grille
        Objet représentant la grille de jeu, contenant des informations sur les animaux et l'environnement.
    - __population : Population
        Objet contenant la liste des animaux, leurs positions et leurs propriétés (vie, âge, sexe, etc.).
      __grilleEnvironnement : 
        Objet contenant la liste des  environnements

    Méthodes principales :
    ----------------------
    - __init__() :
        Initialise une grille, une population et ajoute les éléments initiaux (animaux et herbe) selon les paramètres 
        définis dans `PARAMETERS`.

    - bouge(iden: int) :
        Gère les interactions pour un animal donné, notamment :
        - Le mouvement vers une case voisine.
        - L'alimentation (herbe ou proies selon le type d'animal).
        - La reproduction si un partenaire compatible est disponible.
        - La gestion de la mort si les conditions sont remplies (e.g., vieillesse ou faim).

    - generation() :
        Simule une génération complète :
        - Déplacement et action de tous les animaux dans l'ordre (ours, renards, puis lapins).
        - Apparition possible d'herbe sur des cases vides.

    - estFiniJeu() -> bool :
        Retourne `True` si les conditions de fin de jeu sont remplies :
        - Extinction des renards ou des lapins.
        - (Optionnel) Peut être étendu pour inclure d'autres critères de fin.

    - checkInvariant() :
        Vérifie la cohérence entre la grille et la population :
        - Les positions des animaux sur la grille doivent correspondre à celles dans la population.
        - Les identifiants d'animaux doivent être correctement attribués.

    - addOursAleatoire() :
        Ajoute un ours sur une case vide aléatoire, si des cases sont disponibles.

    - __str__() -> str :
        Retourne une représentation textuelle de la grille de jeu, utile pour afficher l'état actuel du jeu.
    """

    def __init__(self, TAILLE):
        self.__TAILLE = TAILLE
        self.__grilleId = [[-1 for _ in range(TAILLE)] for _ in range(TAILLE)]
        self.__grilleEnvironnement = [
            [Environnement(1) for _ in range(TAILLE)] for _ in range(TAILLE)]

    # Getters

    def get_TAILLE(self):
        return self.__TAILLE

    def get_id(self, coord):
        x, y = coord.get_coord()
        return self.__grilleId[x][y]

    def get_environnement(self, coord):
        x, y = coord.get_coord()
        return self.__grilleEnvironnement[x][y]

    # Setters

    def set_animalId(self, coord, id):
        if not isinstance(coord, Coordonnee):
            raise TypeError("Argument [coord] doit être de type Coordonnée")
        x, y = coord.get_coord()
        if not (0 <= x < self.get_TAILLE() and 0 <= y < self.get_TAILLE()):
            raise ValueError("Coordonnée(s) invalide(s)")
        self.__grilleId[x][y] = id

    def set_environnement(self, coord, environnement):
        if not isinstance(environnement, Environnement):
            raise TypeError(
                "Argument [environnement] doit être de type Environnement")
        if not isinstance(coord, Coordonnee):
            raise TypeError("Argument [coord] doit être de type Coordonnée")
        x, y = coord.get_coord()
        if not (0 <= x < self.get_TAILLE() and 0 <= y < self.get_TAILLE()):
            raise ValueError("Coordonnée(s) invalide(s)")
        self.__grilleEnvironnement[x][y] = environnement

    # Méthodes de classe

    def removeId(self, coord):
        x, y = coord.get_coord()
        if not (0 <= x < self.get_TAILLE() and 0 <= y < self.get_TAILLE()):
            raise ValueError("Coordonnée(s) invalide(s)")
        self.__grilleId[x][y] = -1

    def coord_hasard(self):
        available = []
        for i in range(self.__TAILLE):
            for j in range(self.__TAILLE):
                if self.__grilleId[i][j] == -1:
                    available.append((i, j))
        if (len(available) == 0):
            raise ValueError("Erreur logique ")
        hasard = randint(0, len(available)-1)
        x, y = available[hasard]
        return Coordonnee(x, y)

    def case_Vide(self):
        available = []
        for i in range(self.__TAILLE):
            for j in range(self.__TAILLE):
                if self.__grilleId[i][j] == -1:
                    available.append(Coordonnee(i, j))
        return available

    def __str__(self):
        res = f""
        for x in range(self.get_TAILLE()):
            res += "|"
            for y in range(self.get_TAILLE()):
                res += f" {self.get_id(Coordonnee(x, y))
                           } {self.get_environnement(Coordonnee(x, y)).__str__()} |"
            res += "\n"
        return res
