''' Créé par Lucas Nadal et Yann Floris pour un projet de fin d'année en ISN, année 2016 '''

import tkinter as tk
from tkinter.filedialog import askopenfilenames
import pydoc
import os


def enum(**enums):
    return type('Enum', (), enums)
Objectif = enum(plein=True, vide=False)


class Menu(object): #Création objets menu
    def __init__(self, app): #Initialisation du menu
        self.app = app

    def Ouvrirlvl(self): #Bouton ouvrir...
        app.grid_forget()
        niveau_files = askopenfilenames(initialdir = "niveaux")
        self.app.niveau_files = list(niveau_files)
        self.app.start_next_niveau()

    def About(self): #Bouton A Propos
        AboutDialog()


class Direction(object): #Directions pour touches clavier
    left = 'Left'
    right = 'Right'
    up = 'Up'
    down = 'Down'


class AboutDialog(tk.Frame): #Fenêtre bouton A Propos
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self = tk.Toplevel()
        self.title("A Propos")

        info = tk.Label(self, text=("Sokoban sous Python 3.5 par Lucas Nadal & Yann Floris"))
        info.grid(row=0)

        self.ok_button = tk.Button(self, text="OK", command=self.destroy)
        self.ok_button.grid(row=1)


class CompleteDialog(tk.Frame): #Fenêtre niveau gagné
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self = tk.Toplevel()
        self.title("Félicitations !")

        info = tk.Label(self, text=("Vous avez fini ce niveau !"))
        info.grid(row=0)

        self.ok_button = tk.Button(self, text="OK", command=self.destroy)
        self.ok_button.grid(row=1)


class Niveau(object): #Lecture fichiers niveau, association objets/caractères
    mur = '*'
    objectif = 'o'
    caisse_sur_objectif = '@'
    caisse = '#'
    joueur = 'P'
    sol = ' '


class Image(object): #Associations objets/images
    mur = os.path.join('images/mur.gif')
    objectif = os.path.join('images/objectif.gif')
    caisse_sur_objectif = os.path.join('images/caisse-sur-objectif.gif')
    caisse = os.path.join('images/caisse.gif')
    joueur = os.path.join('images/joueur.gif')
    joueur_sur_objectif = os.path.join('images/joueur-sur-objectif.gif')


class Application(tk.Frame):
    def __init__(self, master=None): #Définition de l'état du programme, de la grille et des chaînes par défaut
        tk.Frame.__init__(self, master)
        self.grid()
        self.master.title("Sokoban sous Python 3.5")
        self.master.resizable(0,0)
        icon = tk.PhotoImage(file=Image.caisse)
        self.master.tk.call('wm', 'iconphoto', self.master._w, icon)
        self.creer_menu()

        self.DEFAULT_SIZE = 200
        self.frame = tk.Frame(self, height=self.DEFAULT_SIZE, width=self.DEFAULT_SIZE)
        self.frame.grid()
        self.default_frame()

        self.joueur_position = ()
        self.joueur = None

        self.current_niveau = None
        self.niveau_files = []
        self.niveau = []
        self.caisses = {}
        self.objectifs = {}
        
    def key(self, event):
        directions = {Direction.left, Direction.right, Direction.up, Direction.down} #Rassembler les touches dans une chaîne
        if event.keysym in directions: #Si la touche enclenchée par l'utilisateur appartient à la chaîne, alors bouger le joueur
            self.move_joueur(event.keysym)

    def creer_menu(self): #Création menu fenêtre accueil
        menu = tk.Menu(self.master)
        user_menu = Menu(self)
        self.master.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Redémarrer", command=self.restart_niveau)
        file_menu.add_command(label="Ouvrir...", command=user_menu.Ouvrirlvl)
        file_menu.add_command(label="Quitter", command=menu.quit)

        help_menu = tk.Menu(menu)
        menu.add_cascade(label="Aide", menu=help_menu)
        help_menu.add_command(label="A Propos", command=user_menu.About)

    def default_frame(self): #Création fenêtre d'Accueil
        start_width = 30
        start_label = tk.Label(self.frame, text="Bienvenue !\n", width=start_width)
        start_label.grid(row=0, column=0)

        start_label2 = tk.Label(self.frame, text="Pour jouer, choissisez un\nniveau dans Fichier -> Ouvrir...\n", width=start_width)
        start_label2.grid(row=1, column=0)

    def clear_niveau(self): #Fermer fenêtre de jeu
        self.frame.destroy()
        self.frame = tk.Frame(self)
        self.frame.grid()
        self.niveau = []

    def start_next_niveau(self): #Passage niveau suivant (mauvais fonctionnement, arret du niveau)
        self.clear_niveau()
        if len(self.niveau_files) > 0:
            self.current_niveau = self.niveau_files.pop()
            niveau = open(self.current_niveau, "r")
            self.grid()
            self.load_niveau(niveau)
            self.master.title("Sokoban sous Python 3.5 par Lucas Nadal & Yann Floris")
        else:
            self.current_niveau = None
            self.master.title("Sokoban sous Python 3.5")
            self.default_frame()
            CompleteDialog()

    def restart_niveau(self): #Fonction redémarrer du menu
        if self.current_niveau:
            self.niveau_files.append(self.current_niveau)
            self.start_next_niveau()

    def load_niveau(self, niveau): #Génération du niveau basé sur le texte
        self.clear_niveau()

        for row, line in enumerate(niveau): #Pour chaque ligne du fichier choisi
            niveau_row = list(line)
            for column,x in enumerate(niveau_row): #Pour chaque caractère de chaque ligne
                if x == Niveau.joueur: #Si caractère est joueur, considérer sur le sol
                    niveau_row[column] = Niveau.sol

                elif x == Niveau.objectif: #Si caractère est objectif, considérer objectif vide
                    self.objectifs[(row, column)] = Objectif.vide

                elif x == Niveau.caisse_sur_objectif: #Si caractère caisse sur objectif, considérer objectif rempli
                    self.objectifs[(row, column)] = Objectif.plein

            self.niveau.append(niveau_row) #Ajouter l'élément à la liste self.niveau

            for column, car in enumerate(line): #Pour chaque caractère du fichier choisi
                if car == Niveau.mur: #Si caractère est mur, créer mur dans la grille
                    mur = tk.PhotoImage(file=Image.mur)
                    w = tk.Label(self.frame, image=mur)
                    w.mur = mur
                    w.grid(row=row, column=column)

                elif car == Niveau.objectif: #Si caractère est objectif, créer objectif dans la grille
                    objectif = tk.PhotoImage(file=Image.objectif)
                    w = tk.Label(self.frame, image=objectif)
                    w.objectif = objectif
                    w.grid(row=row, column=column)

                elif car == Niveau.caisse_sur_objectif:
                    caisse_sur_objectif = tk.PhotoImage(file=Image.caisse_sur_objectif)
                    w = tk.Label(self.frame, image=caisse_sur_objectif)
                    w.caisse_sur_objectif = caisse_sur_objectif
                    w.grid(row=row, column=column)
                    self.caisses[(row, column)] = w

                elif car == Niveau.caisse:
                    caisse = tk.PhotoImage(file=Image.caisse)
                    w = tk.Label(self.frame, image=caisse)
                    w.caisse = caisse
                    w.grid(row=row, column=column)
                    self.caisses[(row, column)] = w

                elif car == Niveau.joueur:
                    joueur_image = tk.PhotoImage(file=Image.joueur)
                    self.joueur = tk.Label(self.frame, image=joueur_image)
                    self.joueur.joueur_image = joueur_image
                    self.joueur.grid(row=row, column=column)
                    self.joueur_position = (row, column)

    def move_joueur(self, direction): #Délpacement joueur
        row, column = self.joueur_position
        prev_row, prev_column = row, column

        blocked = True
        if direction == Direction.left and self.niveau[row][column - 1] is not Niveau.mur and column > 0: #Si joueur va à gauche et block suivant n'est pas mur
            blocked = self.move_caisse((row, column - 1), (row, column - 2)) #Vérifier si caisse poussée est bloquée
            if not blocked: #Si non bloquée déplacer à gauche
                self.joueur_position = (row, column - 1)

        elif direction == Direction.right and self.niveau[row][column + 1] is not Niveau.mur: #Si joueur va à droite et block suivant n'est pas mur
            blocked = self.move_caisse((row, column + 1), (row, column + 2)) #Vérifier si caisse poussée est bloquée
            if not blocked: #Si non bloquée déplacer à droite
                self.joueur_position = (row, column + 1)

        elif direction == Direction.down and self.niveau[row + 1][column] is not Niveau.mur:
            blocked = self.move_caisse((row + 1, column), (row + 2, column))
            if not blocked:
                self.joueur_position = (row + 1, column)

        elif direction == Direction.up and self.niveau[row - 1][column] is not Niveau.mur and row > 0:
            blocked = self.move_caisse((row - 1, column), (row - 2, column))
            if not blocked:
                self.joueur_position = (row - 1, column)

        all_objectifs_plein = True #Tous objectifs remplis
        for objectif in self.objectifs.values(): #Pour chaque objectif
            if objectif is not Objectif.plein: #Si au moins 1 objectif pas plein
                all_objectifs_plein = False #Alors tous objectifs pas pleins

        if all_objectifs_plein: #Si tous objectifs remplis
            self.start_next_niveau() #Mettre fin au niveau
            return

        row, column = self.joueur_position

        if not blocked:
            self.joueur.grid_forget() #Effacer de la mémoire la position précédente du joueur

            if self.niveau[row][column] is Niveau.objectif: #Si joueur est sur case objectif
                joueur_image = tk.PhotoImage(file=Image.joueur_sur_objectif) #Afficher image joueur sur objectif
            else:
                joueur_image = tk.PhotoImage(file=Image.joueur) #Sinon afficher image joueur

            self.joueur = tk.Label(self.frame, image=joueur_image)
            self.joueur.joueur_image = joueur_image
            self.joueur.grid(row=row, column=column)

    def move_caisse(self, location, next_location): #Pousser les caisses
        row, column = location
        next_row, next_column = next_location

        if self.niveau[row][column] is Niveau.caisse and self.niveau[next_row][next_column] is Niveau.sol: #Si block suivant caisse est vide
            self.caisses[(row, column)].grid_forget()
            caisse = tk.PhotoImage(file=Image.caisse)
            w = tk.Label(self.frame, image=caisse)
            w.caisse = caisse
            w.grid(row=next_row, column=next_column)

            self.caisses[(next_row, next_column)] = w
            self.niveau[row][column] = Niveau.sol
            self.niveau[next_row][next_column] = Niveau.caisse

        elif self.niveau[row][column] is Niveau.caisse and self.niveau[next_row][next_column] is Niveau.objectif: #Si block suivant caisse est objectif
            self.caisses[(row, column)].grid_forget()
            caisse_sur_objectif = tk.PhotoImage(file=Image.caisse_sur_objectif)
            w = tk.Label(self.frame, image=caisse_sur_objectif)
            w.caisse = caisse_sur_objectif
            w.grid(row=next_row, column=next_column)

            self.caisses[(next_row, next_column)] = w
            self.niveau[row][column] = Niveau.sol
            self.niveau[next_row][next_column] = Niveau.caisse_sur_objectif
            self.objectifs[(next_row, next_column)] = Objectif.plein

        elif self.niveau[row][column] is Niveau.caisse_sur_objectif and self.niveau[next_row][next_column] is Niveau.sol: #Si block suivant caisse sur objectif est vide
            self.caisses[(row, column)].grid_forget()
            caisse = tk.PhotoImage(file=Image.caisse)
            w = tk.Label(self.frame, image=caisse)
            w.caisse = caisse
            w.grid(row=next_row, column=next_column)

            self.caisses[(next_row, next_column)] = w
            self.niveau[row][column] = Niveau.objectif
            self.niveau[next_row][next_column] = Niveau.caisse
            self.objectifs[(row, column)] = Objectif.vide

        elif self.niveau[row][column] is Niveau.caisse_sur_objectif and self.niveau[next_row][next_column] is Niveau.objectif: #Si block suivant caisse sur objectif est objectif
            self.caisses[(row, column)].grid_forget()
            caisse_sur_objectif = tk.PhotoImage(file=Image.caisse_sur_objectif)
            w = tk.Label(self.frame, image=caisse_sur_objectif)
            w.caisse_sur_objectif = caisse_sur_objectif
            w.grid(row=next_row, column=next_column)

            self.caisses[(next_row, next_column)] = w
            self.niveau[row][column] = Niveau.objectif
            self.niveau[next_row][next_column] = Niveau.caisse_sur_objectif
            self.objectifs[(row, column)] = Objectif.vide
            self.objectifs[(next_row, next_column)] = Objectif.plein

        if self.bloque(location, next_location):
            return True
        return False

    def bloque(self, location, next_location): #Bloquage caisse
        row, column = location
        next_row, next_column = next_location

        if self.niveau[row][column] is Niveau.caisse and self.niveau[next_row][next_column] is Niveau.mur: #Si block suivant caisse est mur
            return True
        elif self.niveau[row][column] is Niveau.caisse_sur_objectif and self.niveau[next_row][next_column] is Niveau.mur: #Si block suivant caisse sur objectif est mur
            return True
        elif (self.niveau[row][column] is Niveau.caisse_sur_objectif and #Si block suivant caisse sur objectof est caisse ou caisse sur objectif
                  (self.niveau[next_row][next_column] is Niveau.caisse or
                           self.niveau[next_row][next_column] is Niveau.caisse_sur_objectif)):
            return True
        elif (self.niveau[row][column] is Niveau.caisse and#Si block suivant caisse est caisse ou caisse sur objectif
                  (self.niveau[next_row][next_column] is Niveau.caisse or
                           self.niveau[next_row][next_column] is Niveau.caisse_sur_objectif)):
            return True


app = Application()
app.bind_all("<Key>", app.key)
app.mainloop()
