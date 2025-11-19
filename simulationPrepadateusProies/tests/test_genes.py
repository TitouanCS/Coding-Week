import sys
import os

# Gérer les caractères spéciaux
parent_folder = os.getcwd().encode('utf-8').decode('utf-8')

# Ajouter ce chemin au sys.path
sys.path.insert(0, parent_folder)

from source.genes import *

# Tests genérés par CHATGPT # 

def test_create_random():
    # Teste si create_random() retourne un dictionnaire avec les bonnes clés
    random_gene = create_random()
    assert Genes.MANGE in random_gene
    assert Genes.ESQUIVE in random_gene
    assert len(random_gene) == 2

    # Teste si les valeurs retournées sont bien dans [0, 1, 2, 3]
    assert random_gene[Genes.MANGE] in [0, 1, 2, 3]
    assert random_gene[Genes.ESQUIVE] in [0, 1, 2, 3]


def test_genes_parent():
    # Teste la fonction genes_parent()
    gene1 = {Genes.MANGE: 1, Genes.ESQUIVE: 0}
    gene2 = {Genes.MANGE: 2, Genes.ESQUIVE: 3}
    
    descendant = genes_parent(gene1, gene2)
    
    # Teste que les gènes descendant sont bien hérités des parents
    assert descendant[Genes.MANGE] in [gene1[Genes.MANGE], gene2[Genes.MANGE]]
    assert descendant[Genes.ESQUIVE] in [gene1[Genes.ESQUIVE], gene2[Genes.ESQUIVE]]


def test_str_representation():
    # Teste la représentation en chaîne de caractères de l'énumération
    assert str(Genes.MANGE) == "MANGE"
    assert str(Genes.ESQUIVE) == "ESQUIVE"