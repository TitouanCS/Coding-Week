import sys
import os

# Gérer les caractères spéciaux
parent_folder = os.getcwd().encode('utf-8').decode('utf-8')

# Ajouter ce chemin au sys.path
sys.path.insert(0, parent_folder)

from source.coordonnee import *

c1=Coordonnee(4,5)
c2=Coordonnee(5,6)
TAILLE = 7

v1 = [Coordonnee(3,4),Coordonnee(3,6),Coordonnee(4,4),Coordonnee(4,6),Coordonnee(5,4),Coordonnee(5,6),Coordonnee(3,5),Coordonnee(5,5)]
v2 = [Coordonnee(4,5),Coordonnee(5,5),Coordonnee(6,5),Coordonnee(4,6),Coordonnee(6,6)]
    
def test_init():
    assert c1.get_coord() == (4,5)
    assert c2.get_coord() == (5,6)
       
def test_case_voisine():
    voisins=c1.case_voisine(TAILLE)
    for i in range(0,len(voisins)):
        assert voisins[i].get_coord()==v1[i].get_coord()
    voisins=c2.case_voisine(TAILLE)
    for i in range(0,len(voisins)):
        assert voisins[i].get_coord()==v2[i].get_coord()