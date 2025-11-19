from enum import Enum


class Environnement(Enum):
    """
    Classes:
        Environnement: Énumération permettant de modéliser différents types d'environnements dans une grille.

    Attributs de classe:
        - VIDE (int): Représente une case vide (valeur 1).
        - HERBE (int): Représente une case avec de l'herbe (valeur 2).
        - MONTAGNE (int): Représente une case montagneuse (valeur 3).

    Méthodes:
        - __str__(): Retourne une représentation textuelle de l'environnement sous forme de caractères ("V" pour VIDE, "H" pour HERBE, "M" pour MONTAGNE).
"""

    VIDE = 1
    HERBE = 2
    MONTAGNE = 3

    def __str__(self):
        if self.value == 1:
            return "V"
        elif self.value == 2:
            return "H"
        elif self.value == 3:
            return "M"
        else:
            raise ValueError("Impossible")
