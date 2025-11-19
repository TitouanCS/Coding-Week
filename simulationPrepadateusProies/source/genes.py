from enum import Enum
import numpy as np


class Genes(Enum):
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

    MANGE = 1
    ESQUIVE = 2

    def __str__(self):
        if self.value == 1:
            return "MANGE"
        elif self.value == 2:
            return "ESQUIVE"
        else:
            raise ValueError("Impossible")


def create_random():
    # Définir les valeurs possibles et leurs probabilités
    dic = {}
    valeurs = [0, 1, 2, 3]
    probabilites = [0.25, 0.25, 0.25, 0.25]
    # Tirer une valeur
    dic[Genes.MANGE] = float(np.random.choice(valeurs, p=probabilites))
    dic[Genes.ESQUIVE] = float(np.random.choice(valeurs, p=probabilites))
    return dic


def genes_parent(gene1, gene2):
    dic = {}
    prem_gene = np.random.randint(0, 1)
    dic[Genes.MANGE] = gene1[Genes.MANGE] if prem_gene == 0 else gene2[Genes.MANGE]
    deuxieme_gene = np.random.randint(0, 1)
    dic[Genes.ESQUIVE] = gene1[Genes.ESQUIVE] if deuxieme_gene == 0 else gene2[Genes.ESQUIVE]
    return dic
