import pygame
import matplotlib.pyplot as plt
from source.gameRules import GameRules
from source.coordonnee import Coordonnee
from source.animal import Animal
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import sys


class InterfaceGraphique:

    """
    InterfaceGraphique est responsable de la gestion de l'interface graphique (GUI) du jeu de simulation.
    Elle gère l'affichage des menus, des crédits, des paramètres et de la simulation.
    
    Attributs :
    MARRON (tuple) : Couleur pour les lapins.
    RED (tuple) : Couleur pour les renards.
    ORANGE (tuple) : Couleur pour les renards.
    VERT (tuple) : Couleur pour l'herbe.
    NOIR (tuple) : Couleur pour le fond.
    BLANC (tuple) : Couleur pour le texte.
    BLEU (tuple) : Couleur pour l'effet de survol des boutons.
    COULEUR_RENARDS (tuple) : Couleur pour les renards.
    COULEUR_LAPIN (tuple) : Couleur pour les lapins.
    COULEUR_FOND (tuple) : Couleur de fond.
    COULEUR_TEXTE (tuple) : Couleur du texte.
    COULEUR_HERBE (tuple) : Couleur de l'herbe.
    COULEUR_SURVOL (tuple) : Couleur pour l'effet de survol des boutons.
    TAILLE_FONT_TITRE (int) : Taille de la police pour le titre.
    TAILLE_FONT_STITRE (int) : Taille de la police pour les sous-titres.
    TAILLE_FONT_SSTITRE (int) : Taille de la police pour les petits sous-titres.
    TAILLE_FONT_BOUTTON (int) : Taille de la police pour les boutons.
    TAILLE_FONT_TXT (int) : Taille de la police pour le texte.
    
    Méthodes :
    __init__(self, largeur, hauteur, nom_fenetre="Simulation Écosystème", FPS=5):
        Initialise l'interface graphique avec les dimensions spécifiées de la fenêtre, le titre de la fenêtre, et les FPS.
    
    ecranInitial(self):
        Affiche le menu initial avec le titre du jeu et les boutons pour entrer dans le jeu ou voir les crédits.
    
    ecranCredits(self):
        Affiche un écran de crédits avec des informations sur les développeurs et contributeurs, et permet de revenir au menu principal.
    
    ecranParametres(self):
        Affiche un écran pour configurer les paramètres de la simulation, comme le nombre de lapins, de renards, et l'apparence de l'herbe.
    
    ecranParametresAvances(self):
        Affiche un écran pour configurer les paramètres avancés de la simulation, comme la fréquence d'images (FPS) et d'autres paramètres avancés.

    plotSurface(self, populationLapinsOverTime, populationRenardsOverTime):
        Crée une surface représentant un graphique montrant l'évolution des populations de lapins et de renards.
        
    alleleHistogramSurface(self, alleleFrequenciesByGeneByAnimal):
        Crée une surface représentant un histogramme des fréquences des allèles pour chaque animal.
    
    grilleSurface(self, grille, population):
        Crée une surface représentant la grille de simulation avec les animaux (lapins, renards, ours) et l'herbe.
        
    parametresSurface(self):
        Crée une surface affichant les paramètres de la simulation.
        
    run(self):
        Lance la simulation du jeu, en gérant l'affichage des éléments graphiques, les événements et la mise à jour des populations.

    """


    # Couleurs utilisées dans l'interface
    MARRON = (139, 69, 19)  # Lapins
    RED = (255, 0, 0)
    ORANGE = (255, 165, 0)  # Renards
    VERT = (34, 139, 34)    # Herbe
    NOIR = (0, 0, 0)        # Fond noir
    BLANC = (255, 255, 255)  # Texte
    BLEU = (30, 144, 255)  # Effet de survol des boutons

    COULEUR_RENARDS = ORANGE
    COULEUR_LAPIN = MARRON
    COULEUR_FOND = NOIR
    COULEUR_TEXTE = BLANC
    COULEUR_HERBE = VERT
    COULEUR_SURVOL = BLEU

    TAILLE_FONT_TITRE = 120
    TAILLE_FONT_STITRE = 90
    TAILLE_FONT_SSTITRE = 40
    TAILLE_FONT_BOUTTON = 60
    TAILLE_FONT_TXT = 28

    def __init__(self, largeur, hauteur, nom_fenetre="Simulation Écosystème", FPS=5):
        """Initialise l'interface graphique."""
        self.HAUTEUR = hauteur
        self.LARGEUR = largeur
        self.ratioHauteurGrille = 1
        self.ratioLargeurGrille = 0.67
        self.ecran = pygame.display.set_mode((self.LARGEUR, self.HAUTEUR))
        pygame.display.set_caption(nom_fenetre)
        # Vitesse de la simulation en images par seconde
        self.FPS = 2

    def ecranInitial(self):
        """Affiche le menu initial. Ce dernier contient :
                - un titre, 
                - deux boutons (credits et entrer)
        """
        pygame.mixer.music.load("assets/music/musique_menu.mp3")
        pygame.mixer.music.play(-1)  # Lecture en boucle

        # Fonts
        fontTitre = pygame.font.Font(
            None, InterfaceGraphique.TAILLE_FONT_TITRE)
        fontBoutons = pygame.font.Font(
            None, InterfaceGraphique.TAILLE_FONT_BOUTTON)
        fontBoutonsSurvol = pygame.font.Font(
            None, InterfaceGraphique.TAILLE_FONT_BOUTTON + 10)  # Pour l'effet de survol

        # Texte
        titre = fontTitre.render(
            "WHAT DOES THE FOX SAY ?", True, InterfaceGraphique.COULEUR_TEXTE)

        # Marges
        margeX, margeY = 60, 30  # Marges pour agrandir les boutons

        # Image
        imageBiome = pygame.transform.scale(pygame.image.load(
            # Importe & ajuste la taille
            "assets/images/herbe.png"), (self.LARGEUR, self.HAUTEUR // 4))

        # Rectangles des boutons
        boutonJeu = pygame.Rect(0, 0, 0, 0)
        boutonCredits = pygame.Rect(0, 0, 0, 0)

        en_cours = True

        while en_cours:

            # Dessiner le fond
            self.ecran.fill(self.COULEUR_FOND)
            self.ecran.blit(titre, (self.LARGEUR // 2 -
                            titre.get_width() // 2, self.HAUTEUR // 8))
            self.ecran.blit(imageBiome, (0, 3*self.HAUTEUR // 4))

            # Vérifier si la souris est au-dessus des boutons
            mouseX, mouseY = pygame.mouse.get_pos()

            # Bouton "Entrer dans le jeu"
            if boutonJeu.collidepoint(mouseX, mouseY):
                texteJeu = fontBoutonsSurvol.render(
                    "Entrer dans le jeu", True, InterfaceGraphique.COULEUR_SURVOL)
            else:
                texteJeu = fontBoutons.render(
                    "Entrer dans le jeu", True, InterfaceGraphique.COULEUR_FOND)

            boutonJeu.width = texteJeu.get_width() + margeX
            boutonJeu.height = texteJeu.get_height() + margeY
            boutonJeu.center = (self.LARGEUR // 2, self.HAUTEUR // 2 - 70)

            # Bouton "Crédits"
            if boutonCredits.collidepoint(mouseX, mouseY):
                texteCredits = fontBoutonsSurvol.render(
                    "Crédits", True, InterfaceGraphique.COULEUR_SURVOL)
            else:
                texteCredits = fontBoutons.render(
                    "Crédits", True, InterfaceGraphique.COULEUR_FOND)

            boutonCredits.width = texteCredits.get_width() + margeX
            boutonCredits.height = texteCredits.get_height() + margeY
            boutonCredits.center = (self.LARGEUR // 2, self.HAUTEUR // 2 + 70)

            # Dessiner les rectangles des boutons
            pygame.draw.rect(self.ecran, self.COULEUR_TEXTE,
                             boutonJeu, border_radius=10)  # Bouton jeu
            pygame.draw.rect(self.ecran, self.COULEUR_TEXTE,
                             boutonCredits, border_radius=10)  # Bouton crédits

            # Afficher les textes centrés dans les rectangles
            self.ecran.blit(texteJeu, texteJeu.get_rect(
                center=boutonJeu.center))
            self.ecran.blit(texteCredits, texteCredits.get_rect(
                center=boutonCredits.center))

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if boutonJeu.collidepoint(event.pos):
                        en_cours = False  # Passe au menu suivant
                    elif boutonCredits.collidepoint(event.pos):
                        self.ecranCredits()  # Appeler l'écran des crédits

    def ecranCredits(self):
        """Affiche l'écran des crédits"""

        fontSTitre = pygame.font.Font(
            None, InterfaceGraphique.TAILLE_FONT_STITRE)
        fontTxt = pygame.font.Font(None, InterfaceGraphique.TAILLE_FONT_TXT)

        sTitre = fontSTitre.render(
            "Crédits", True, InterfaceGraphique.COULEUR_TEXTE)
        textRetour = fontTxt.render(
            "Appuyez sur R pour revenir au menu principal", True, InterfaceGraphique.COULEUR_TEXTE)

        phrases = [
            "ABOU HAMAD Christian",
            "DILET Quentin",
            "GAY-CORTIJO Titouan",
            "LÉGER Joseph",
            "LUKSCH Guglielmo",
            "YUAN Juefei Lorenzo",
            "--- Remerciements --",
            "KEBAILI Thomas",
            "--------------------",
            "Examiné par KEBAILI Thomas le vendredi 22 novembre 2024"
        ]

        en_cours = True

        while en_cours:
            self.ecran.fill(InterfaceGraphique.COULEUR_FOND)
            self.ecran.blit(sTitre, (self.LARGEUR // 2 -
                            sTitre.get_width() // 2, self.HAUTEUR // 16))

            for i, phrase in enumerate(phrases):
                texte = fontTxt.render(
                    phrase, True, InterfaceGraphique.COULEUR_TEXTE)
                self.ecran.blit(texte, (self.LARGEUR // 2 - texte.get_width() // 2, self.HAUTEUR //
                                4 - texte.get_height() // 2 + i*self.HAUTEUR/(2*len(phrases))))
            self.ecran.blit(textRetour, (self.LARGEUR // 2 -
                            textRetour.get_width() // 2, self.HAUTEUR - self.HAUTEUR // 8))

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:  # Retour au menu principal
                        en_cours = False

    def ecranParametres(self):
        """Affiche un écran pour configurer les paramètres de simulation."""

        OPT_PARAMETERS = None

        fontSSTitre = pygame.font.Font(
            None, InterfaceGraphique.TAILLE_FONT_SSTITRE)
        fontTxt = pygame.font.Font(None, InterfaceGraphique.TAILLE_FONT_TXT)

        # Paramètres par défaut
        PARAMETERS = {"Lapins": 2000, "Renards": 700,
                      "Ours": 100, "Taille": 100, "Apparition herbe (%)": 10}
        champs = list(PARAMETERS.keys())
        valeurs = [str(PARAMETERS[c]) for c in champs]
        index = 0

        # Charger l'icône d'engrenage
        ImageEngrenage = pygame.transform.scale(pygame.image.load(
            # Redimensionner à 50x50 pixels
            "assets/images/gear_icon.png"), (self.LARGEUR // 24, self.HAUTEUR // 16))
        IconeEngrenage = ImageEngrenage.get_rect(
            topright=(self.LARGEUR - self.LARGEUR // 60, self.HAUTEUR // 40))

        # Charger les images pour l'animation
        imageChasse = pygame.transform.scale(pygame.image.load(
            "assets/images/chasse.png"), (self.HAUTEUR // 4, self.HAUTEUR // 4))
        imageBiome = pygame.transform.scale(pygame.image.load(
            # Importe & ajuste la taille
            "assets/images/herbe.png"), (self.LARGEUR, self.HAUTEUR // 4))

        # Positions initiales pour l'animation
        chasseX = 0

        # Créer les zones cliquables pour chaque champ
        rects = list()
        saisie = ""
        for i, champ in enumerate(champs):
            rect = pygame.Rect(self.LARGEUR // 2 - self.LARGEUR // 16, 4*self.HAUTEUR // 16 + i * 3*self.HAUTEUR // (
                # Rectangle pour chaque champ
                16*len(champs)) - self.HAUTEUR // 40, self.LARGEUR // 8, self.HAUTEUR // 20)
            rects.append(rect)

        def afficher():
            """Affiche l'écran de configuration."""
            self.ecran.fill(InterfaceGraphique.COULEUR_FOND)

            # Titre
            titre = fontSSTitre.render("Configuration de la Simulation",
                                       True, InterfaceGraphique.COULEUR_TEXTE)
            self.ecran.blit(titre, (self.LARGEUR // 2 -
                            titre.get_width() // 2, self.HAUTEUR//16))

            # Affichage des champs et des valeurs
            for i, champ in enumerate(champs):
                couleur = InterfaceGraphique.COULEUR_TEXTE if i == index else (
                    150, 150, 150)
                texte = fontTxt.render(
                    f"{champ} : {valeurs[i]}", True, couleur)
                self.ecran.blit(texte, (self.LARGEUR // 2 -
                                texte.get_width() // 2, 4*self.HAUTEUR // 16 + i * (3*self.HAUTEUR // (16*len(champs)))))

        # Afficher la saisie en cours si elle est active
            if saisie:
                saisie_texte = fontTxt.render(f"Saisissez la valeur puis cliquez sur MAJ : {
                                              saisie}", True, InterfaceGraphique.COULEUR_TEXTE)
                self.ecran.blit(saisie_texte, (self.LARGEUR // 2 -
                                saisie_texte.get_width() // 2, self.HAUTEUR // 2))

            # Instructions
            instructions = fontTxt.render(
                "Utilisez ^v pour naviguer, <> pour ajuster, Entrée pour valider", True, (
                    150, 150, 150)
            )

            self.ecran.blit(instructions, (self.LARGEUR // 2 -
                            instructions.get_width() // 2, 9*self.HAUTEUR/16))

            self.ecran.blit(ImageEngrenage, IconeEngrenage.topleft)

            # Afficher le lapin et le renard animés
            nonlocal chasseX  # Accéder aux variables externes
            self.ecran.blit(imageBiome, (0, 3*self.HAUTEUR // 4))
            self.ecran.blit(
                imageChasse, (chasseX, 3*self.HAUTEUR // 4 - 3*self.HAUTEUR // 32))

            chasseX += 0.5

            # Réinitialiser les positions si les deux sortent de l'écran

            if chasseX > self.LARGEUR:
                chasseX = -200

            pygame.display.flip()

        en_cours = True
        while en_cours:
            afficher()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        for i, rect in enumerate(rects):
                            if rect.collidepoint(event.pos):
                                index = i  # Sélectionner le champ cliqué
                                saisie = ""  # Réinitialiser la saisie
                                break
                        # Si le clic est sur l'icône
                        if IconeEngrenage.collidepoint(event.pos):
                            OPT_PARAMETERS = self.ecranParametresAvances()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        index = (index - 1) % len(champs)
                    elif event.key == pygame.K_DOWN:
                        index = (index + 1) % len(champs)
                    elif event.key == pygame.K_LEFT:
                        valeurs[index] = str(max(1, int(valeurs[index]) - 1))
                    elif event.key == pygame.K_RIGHT:
                        if index == 4 :
                            valeurs[index] = str(min(100,int(valeurs[index]) + 1))
                        else : valeurs[index] = str(min(int(int(valeurs[3]))**2//2,int(valeurs[index]) + 1))
                    elif event.key == pygame.K_RETURN:
                        en_cours = False
                        pygame.mixer.music.stop()
                if event.type == pygame.KEYDOWN:
                    if index != -1:  # Un champ est sélectionné
                        if event.key == pygame.K_BACKSPACE:
                            # Supprimer le dernier caractère
                            saisie = saisie[:-1]
                        elif event.key == pygame.K_RSHIFT:  # Valider la saisie
                            if saisie.isdigit():  # Vérifier si la saisie est un nombre
                                tmpSaisie = str(max(1, int(saisie)))
                                if index == 4 :
                                    valeurs[index] = str(min(100,int(tmpSaisie)))
                                else :
                                    valeurs[index] = str(min(int(int(valeurs[3]))**2//2,int(tmpSaisie)))
                                if index == 3 :
                                    for indexToCheck in [0,1,2] :
                                        valeurs[indexToCheck] = int(valeurs[3])**2//2
                                saisie = ""  # Réinitialiser la saisie
                                index = -1  # Désélectionner le champ
                        elif event.unicode.isdigit():  # Ajouter les chiffres tapés
                            saisie += event.unicode

        # Mise à jour des paramètres avec les nouvelles valeurs
        for i, champ in enumerate(champs):
            PARAMETERS[champ] = int(valeurs[i])

        return PARAMETERS, OPT_PARAMETERS

    def ecranParametresAvances(self):
        """Affiche l'écran des paramètres avancés."""

        fontSSTitre = pygame.font.Font(
            None, InterfaceGraphique.TAILLE_FONT_SSTITRE)
        fontTxt = pygame.font.Font(None, InterfaceGraphique.TAILLE_FONT_TXT)

        # Charger les images pour l'animation
        imageChasse = pygame.transform.scale(pygame.image.load(
            "assets/images/chasse.png"), (self.HAUTEUR//4, self.HAUTEUR//4))
        imageBiome = pygame.transform.scale(pygame.image.load(
            "assets/images/herbe.png"), (self.LARGEUR, self.HAUTEUR//4))

        # Positions initiales pour l'animation
        chasseX = 0

        OPT_PARAMETERS = {"fps": 5} | Animal.PARAMETERS
        champs = list(OPT_PARAMETERS.keys())
        valeurs = [str(OPT_PARAMETERS[c]) for c in champs]
        index = 0
        # Créer les zones cliquables pour chaque champ
        saisie = ""
        rects = list()
        for i, champ in enumerate(champs):
            rect = pygame.Rect(
                self.LARGEUR // 2 - self.LARGEUR // 12,
                4 * self.HAUTEUR // 20 + i * 7 *
                self.HAUTEUR // (16 * len(champs)) - self.HAUTEUR // 18,
                self.LARGEUR // 6,
                self.HAUTEUR // 40
            )
            rects.append(rect)

        def afficher():
            self.ecran.fill(InterfaceGraphique.COULEUR_FOND)
            titre = fontSSTitre.render(
                "Paramètres Avancés", True, InterfaceGraphique.COULEUR_TEXTE)
            self.ecran.blit(titre, (self.LARGEUR // 2 -
                            titre.get_width() // 2, self.HAUTEUR // 16))

            for i, champ in enumerate(champs):
                couleur = InterfaceGraphique.COULEUR_TEXTE if i == index else (
                    150, 150, 150)
                texte = fontTxt.render(f"{champ.capitalize()} : {
                                       valeurs[i]}", True, couleur)
                self.ecran.blit(texte, (self.LARGEUR // 2 - texte.get_width() // 2, 5*self.HAUTEUR //
                                32 - texte.get_height() // 2 + i*7*self.HAUTEUR/(16*len(OPT_PARAMETERS))))

            # Afficher la saisie en cours si elle est active
            if saisie:
                saisie_texte = fontTxt.render(f"Saisissez la valeur puis cliquez sur MAJ : {
                                              saisie}", True, InterfaceGraphique.COULEUR_TEXTE)
                self.ecran.blit(saisie_texte, (self.LARGEUR // 2 -
                                saisie_texte.get_width() // 2, self.HAUTEUR // 1.5))

            instructions = fontTxt.render(
                "Utilisez ^v pour naviguer, <> pour ajuster, Entrée pour valider", True, (150, 150, 150))
            self.ecran.blit(instructions, (self.LARGEUR // 2 -
                            instructions.get_width() // 2, 10*self.HAUTEUR // 16))

            # Afficher le lapin et le renard animés
            nonlocal chasseX  # Accéder aux variables externes
            self.ecran.blit(imageBiome, (0, 3*self.HAUTEUR // 4))
            self.ecran.blit(
                imageChasse, (chasseX, 3*self.HAUTEUR // 4 - 3*self.HAUTEUR // 32))

            chasseX += 0.5

            # Réinitialiser les positions si les deux sortent de l'écran

            if chasseX > self.LARGEUR:
                chasseX = -200

            pygame.display.flip()

        en_cours = True
        while en_cours:
            afficher()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        for i, rect in enumerate(rects):
                            if rect.collidepoint(event.pos):
                                index = i  # Sélectionner le champ cliqué
                                saisie = ""  # Réinitialiser la saisie
                                break
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        index = (index - 1) % len(champs)
                    elif event.key == pygame.K_DOWN:
                        index = (index + 1) % len(champs)
                    elif event.key == pygame.K_LEFT:
                        if index == 17 :
                            valeurs[index] = str(max(3, float(valeurs[index]) - 1))
                        else : valeurs[index] = str(
                            max(0, float(valeurs[index]) - 1))  # FPS min 1
                    elif event.key == pygame.K_RIGHT:
                        valeurs[index] = str(
                            min(1000, float(valeurs[index]) + 1))  # FPS max 60
                    elif event.key == pygame.K_RETURN:
                        en_cours = False
                if event.type == pygame.KEYDOWN:
                    if index != -1:  # Un champ est sélectionné
                        if event.key == pygame.K_BACKSPACE:
                            # Supprimer le dernier caractère
                            saisie = saisie[:-1]
                        elif event.key == pygame.K_RSHIFT:  # Valider la saisie
                            try:
                                # Vérifier si la saisie est un float valide
                                float(saisie)
                                valeurs[index] = saisie
                                if index == 17 :
                                     valeurs[index] = str(max(3, int(saisie)))
                                saisie = ""  # Réinitialiser la saisie
                                index = -1  # Désélectionner le champ
                            except ValueError:
                                print("Veuillez entrer un nombre valide.")
                        elif event.unicode.isdigit() or event.unicode == ".":  # Ajouter les chiffres ou un point
                            if event.unicode == "." and "." in saisie:
                                continue  # Empêcher plusieurs points
                            saisie += event.unicode

        for i, champ in enumerate(champs):
            OPT_PARAMETERS[champ] = float(valeurs[i])

        return OPT_PARAMETERS

    def plotSurface(self, populationLapinsOverTime, populationRenardsOverTime):
        """Crée une surface représentant un graphique."""

        def normaliseCouleur(couleur):
            return (couleur[0] / 255, couleur[1] / 255, couleur[2] / 255)

        LARGEUR = int(self.LARGEUR * (1 - self.ratioLargeurGrille))
        HAUTEUR = int(self.HAUTEUR * self.ratioHauteurGrille // 2)

        # Calcul du facteur d'échelle pour les renards
        maxLapins = max(populationLapinsOverTime)
        maxRenards = max(populationRenardsOverTime)

        scaleFactor = maxLapins / maxRenards

        scaledRenards = [
            value * scaleFactor for value in populationRenardsOverTime]

        fig, ax_lapins = plt.subplots(
            figsize=(LARGEUR / 100, HAUTEUR / 100), dpi=100)

        # Tracé des lapins
        ax_lapins.plot(populationLapinsOverTime, label="Lapins",
                       color=normaliseCouleur(InterfaceGraphique.COULEUR_LAPIN))
        ax_lapins.set_ylabel("Population Lapins", fontsize=10, labelpad=10)
        ax_lapins.set_xlabel("Temps", fontsize=10, labelpad=10)
        ax_lapins.legend(loc="upper left")
        ax_lapins.grid(True)

        # Tracé des renards scalés
        ax_lapins.plot(scaledRenards, label="Renards (scalés)",
                       color=normaliseCouleur(InterfaceGraphique.COULEUR_RENARDS))
        ax_lapins.legend(loc="upper left")

        # Création d'un axe secondaire pour les valeurs réelles des renards
        ax_renards = ax_lapins.twinx()
        ax_renards.set_ylabel("Population Renards (réelle)",
                              fontsize=10, labelpad=10)
        ax_renards.set_ylim(0, max(populationRenardsOverTime) * 1.1)

        # Titre du graphique
        ax_lapins.set_title("Évolution des Populations", fontsize=12, pad=15)

        # Ajustement automatique des espaces
        fig.tight_layout()

        # Dessin du canvas
        canvas = FigureCanvas(fig)
        canvas.draw()
        raw_data = canvas.tostring_rgb()
        size = canvas.get_width_height()
        surface = pygame.image.fromstring(raw_data, size, "RGB")
        plt.close(fig)
        return surface

    def alleleHistogramSurface(self, alleleFrequenciesByGeneByAnimal):

        (nbHistos, animalPresentHisto) = (0, [])

        for animal, alleleFrequenciesByGene in alleleFrequenciesByGeneByAnimal.items():
            if alleleFrequenciesByGene != {}:
                if animal == 'Ours' : continue
                nbHistos += 1
                animalPresentHisto.append(animal)
            # Si aucun histogramme à afficher, retourner une surface vide
            if nbHistos == 0:
                print("Aucun histogramme à afficher.")
                return pygame.Surface((0, 0))  # Surface vide
        fig, ax = plt.subplots(nbHistos, 1, figsize=(int(
            self.LARGEUR * (1-self.ratioLargeurGrille)) / 100, self.HAUTEUR // 200), dpi=100)

        def alleleHistogramUnitAxes(ax, alleleFrequenciesByGene, nomAnimal):

            i = 0
            colors = ['skyblue', 'green']
            bar_width = 0.2
            x_offset = 0

            # Pour chaque gène et ses allèles, créer un histogramme
            for gene, alleleFrequency in (alleleFrequenciesByGene.items()):
                sorted_dic = {}
                tab_s = sorted(alleleFrequency)
                for j in range(4) :
                    if j in tab_s :
                        sorted_dic[j] = alleleFrequency[j]
                    else :
                        sorted_dic[j] = 0
                alleleFrequency = sorted_dic
                proportions = list(sorted_dic.values())
                x_positions = [x + x_offset for x in range(4)]
                ax.bar(x_positions, proportions, width=bar_width, color=colors[i % len(
                    colors)], alpha=0.7, label=f"Gène: {gene}")
                x_offset += bar_width
    
                # Configuration des labels et du titre
                ax.set_title(f"Gènes des {animal}")
                ax.set_ylabel("Proportion")
                ax.set_xlabel("Allèles")
                ax.legend()

                i += 1

        if nbHistos > 1:
            for i, animal in enumerate(animalPresentHisto):
                alleleHistogramUnitAxes(
                    ax[i], alleleFrequenciesByGeneByAnimal[animal], animal)
        else:
            alleleHistogramUnitAxes(
                ax[i],alleleFrequenciesByGeneByAnimal[animal], animal)

        # Convertir en image et renvoyer pour l'affichage dans la simulation
        canvas = FigureCanvas(fig)
        canvas.draw()
        raw_data = canvas.tostring_rgb()
        size = canvas.get_width_height()
        surface = pygame.image.fromstring(raw_data, size, "RGB")
        plt.close(fig)

        return surface

    def grilleSurface(self, grille, population):
        """Crée une surface représentant la grille."""
        LARGEUR = int(self.LARGEUR * self.ratioLargeurGrille)
        HAUTEUR = int(self.HAUTEUR * self.ratioHauteurGrille)
        TAILLE = grille.get_TAILLE()

        # Création de la surface
        surface = pygame.Surface((LARGEUR, HAUTEUR))

        # Calcul des tailles des cases
        taille_case_x = LARGEUR // TAILLE
        taille_case_y = HAUTEUR // TAILLE

        # Dessin des éléments
        for i in range(TAILLE):
            for j in range(TAILLE):
                x, y = j * taille_case_x, i * taille_case_y
                rect = pygame.Rect(x, y, taille_case_x, taille_case_y)
                if grille.get_environnement(Coordonnee(j, i)).value == 2:
                    pygame.draw.rect(
                        surface, InterfaceGraphique.COULEUR_HERBE, rect)

        # Dessiner les lapins
        for coordonneeLapin in population.lapin_coord():
            x, y = coordonneeLapin.get_coord()
            x = x * taille_case_x + taille_case_x // 2
            y = y * taille_case_y + taille_case_y // 2
            pygame.draw.circle(surface, InterfaceGraphique.COULEUR_LAPIN, (x, y), min(
                taille_case_x, taille_case_y) // 3)  # Marron pour les lapins

        # Dessiner les renards
        for coordonneeRenard in population.renard_coord():
            x, y = coordonneeRenard.get_coord()
            x = x * taille_case_x + taille_case_x // 2
            y = y * taille_case_y + taille_case_y // 2
            pygame.draw.circle(surface, InterfaceGraphique.COULEUR_RENARDS, (x, y), min(
                taille_case_x, taille_case_y) // 3)  # Orange pour les renards

        for coordonneeRenard in population.ours_coord():
            x, y = coordonneeRenard.get_coord()
            x = x * taille_case_x + taille_case_x // 2
            y = y * taille_case_y + taille_case_y // 2
            pygame.draw.circle(surface, InterfaceGraphique.BLANC, (x, y), min(
                taille_case_x, taille_case_y) // 3)  # Orange pour les renards

        return surface

    def parametresSurface(self):
        """Affiche les paramètres de jeu en bas de la fenêtre."""
        font = pygame.font.Font(None, 24)

        HAUTEUR = int((1 - self.ratioHauteurGrille) * self.HAUTEUR)
        LARGEUR = self.LARGEUR

        # Création de la surface
        surface = pygame.Surface((LARGEUR, HAUTEUR))
        surface.fill(InterfaceGraphique.COULEUR_FOND)

        # Paramètres de simulation
        PARAMETERS = Animal.PARAMETERS

        # Position initiale pour l'affichage des paramètres
        x_offset = 10  # Début à gauche
        y_offset = 10  # Premier paramètre en haut de la surface

        # Affichage des paramètres ligne par ligne
        for i, (cle, valeur) in enumerate(PARAMETERS.items()):
            texte = font.render(f"{cle}: {valeur}", True,
                                InterfaceGraphique.COULEUR_TEXTE)
            surface.blit(texte, (x_offset, y_offset))
            y_offset += 20  # Espacement entre les lignes

        return surface

    def run(self):
        """Lance la simulation."""
        pygame.init()
        self.ecranInitial()
        PARAMETERS, OPT_PARAMETERS = self.ecranParametres()
        GameRules.PARAMETERS = PARAMETERS
        if OPT_PARAMETERS != None:
            del OPT_PARAMETERS["fps"]
            Animal.PARAMETERS = OPT_PARAMETERS

        gameRules = GameRules()
        gameRules.checkInvariant()
        pygame.mixer.music.load("assets/music/son_ours.mp3")

        # Historique des populations
        populationLapinsOverTime = []
        populationRenardsOverTime = []

        clock = pygame.time.Clock()
        pause = False
        en_cours = True

        # Charger l'image d'ours
        # Remplacez par le chemin correct
        image_ours = pygame.image.load("assets/images/ours.png")
        # Ajustez la taille selon vos besoins
        image_ours = pygame.transform.scale(image_ours, (60, 60))
        bouton_ours_rect = image_ours.get_rect(
            bottomright=(self.LARGEUR//1.02, self.HAUTEUR//1.02))

        while en_cours :
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    en_cours = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        pause = not pause
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Clic gauche
                        if bouton_ours_rect.collidepoint(event.pos):
                            gameRules.addOursAleatoire()  # Action à exécuter
                            pygame.mixer.music.play()
            if not pause:
                # Mise à jour des données de simulation
                gameRules.generation()
                gameRules.checkInvariant()
                populationLapinsOverTime.append(
                    len(gameRules.get_population().lapin_ids()))
                populationRenardsOverTime.append(
                    len(gameRules.get_population().renard_ids()))

            # Affichage
            self.ecran.fill(InterfaceGraphique.COULEUR_FOND)

            # Dessiner la grille
            grilleSurface = self.grilleSurface(

                gameRules.get_grille(), gameRules.get_population())
            plotSurface = self.plotSurface(
                populationLapinsOverTime, populationRenardsOverTime)

            # Calcul des fréquences des allèles
            alleleFrequenciesByGeneByAnimal = gameRules.get_population(
            ).alleleFrequenciesByGeneByAnimal()
            # Tracer l'histogramme des allèles
            try :
                alleleHistogramSurface = self.alleleHistogramSurface(
                    alleleFrequenciesByGeneByAnimal)
            except ValueError as e :
                pass

            self.ecran.blit(grilleSurface, (0, 0))
            self.ecran.blit(
                plotSurface, (int(self.LARGEUR * self.ratioLargeurGrille), 0))
            
            self.ecran.blit(alleleHistogramSurface, (int(
                self.LARGEUR * (self.ratioLargeurGrille)), self.HAUTEUR // 2))


            # Afficher le bouton d'ours
            self.ecran.blit(image_ours, bouton_ours_rect.topleft)

            pygame.display.flip()
            clock.tick(self.FPS)

        pygame.quit()
        sys.exit()
