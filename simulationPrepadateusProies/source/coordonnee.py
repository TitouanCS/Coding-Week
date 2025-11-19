class Coordonnee():

    """
    Classe Coordonnee pour représenter des coordonnées sur une grille.

    Cette classe permet de gérer les coordonnées d'une case dans une grille carrée 
    et de déterminer les cases voisines.

    Attributs :
    -----------
    - x : int
        Coordonnée x de la case.
    - y : int
        Coordonnée y de la case.

    Méthodes :
    ----------
    - get_coord() -> tuple :
        Retourne les coordonnées (x, y) sous forme de tuple.

    - case_voisine(taille: int) -> list[Coordonnee] :
        Retourne une liste des coordonnées des cases voisines valides dans une grille 
        de taille donnée. Les déplacements incluent les directions cardinales 
        (haut, bas, gauche, droite) et les diagonales. Vérifie que les coordonnées 
        des voisins restent dans les limites de la grille.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get_coord(self):
        return (self.x, self.y)

    def case_voisine(self, taille):
        # Liste des déplacements possibles (haut, bas, gauche, droite et diagonales)
        mouvements = [(i+self.x, j+self.y) for i in [-1, 0, 1]
                      for j in [-1, 1]] + [(-1+self.x, self.y)] + [(1+self.x, self.y)]
        voisins = []
        for dx, dy in mouvements:
            if 0 <= dx < taille and 0 <= dy < taille:  # Vérifie que la nouvelle case est valide
                voisins.append(Coordonnee(dx, dy))
        return voisins
