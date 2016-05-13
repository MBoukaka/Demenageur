#!/usr/bin/env python

import tkinter as tk
from tkinter.filedialog import askopenfilenames
import pydoc
import os


_ROOT = os.path.abspath(os.path.dirname(__file__))


def enum(**enums):
    return type('Enum', (), enums)
Objectif = enum(plein=True, vide=False)


class Menu(object):
    def __init__(self, app):
        self.app = app

    def Ouvrirlvl(self):
        self.app.grid_forget()
        niveau_files = self.app.tk.splitlist(askopenfilenames(initialdir=os.path.join(_ROOT, 'niveaux')))
        self.app.niveau_files = list(niveau_files)
        self.app.start_next_niveau()

    def About(self):
        AboutDialog()


class Direction(object):
    left = 'Left'
    right = 'Right'
    up = 'Up'
    down = 'Down'


class AboutDialog(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self = tk.Toplevel()
        self.title("A Propos")

        info = tk.Label(self, text=("Sokoban sous Python 3.5 par Lucas Nadal & Yann Floris"))
        info.grid(row=0)

        self.ok_button = tk.Button(self, text="OK", command=self.destroy)
        self.ok_button.grid(row=1)


class CompleteDialog(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self = tk.Toplevel()
        self.title("Félicitations !")

        info = tk.Label(self, text=("Vous avez fini ce niveau !"))
        info.grid(row=0)

        self.ok_button = tk.Button(self, text="OK", command=self.destroy)
        self.ok_button.grid(row=1)


class Niveau(object):
    mur = '*'
    objectif = 'o'
    caisse_sur_objectif = '@'
    caisse = '#'
    joueur = 'P'
    sol = ' '


class Image(object):
    mur = os.path.join(_ROOT, 'images/mur.gif')
    objectif = os.path.join(_ROOT, 'images/objectif.gif')
    caisse_sur_objectif = os.path.join(_ROOT, 'images/caisse-sur-objectif.gif')
    caisse = os.path.join(_ROOT, 'images/caisse.gif')
    joueur = os.path.join(_ROOT, 'images/joueur.gif')
    joueur_sur_objectif = os.path.join(_ROOT, 'images/joueur-sur-objectif.gif')


class Application(tk.Frame):
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid()
        self.configure(background="black")
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
        directions = {Direction.left, Direction.right, Direction.up, Direction.down}
        if event.keysym in directions:
            self.move_joueur(event.keysym)

    def creer_menu(self):
        root = self.master
        menu = tk.Menu(root)
        user_menu = Menu(self)
        root.config(menu=menu)

        file_menu = tk.Menu(menu)
        menu.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Redémarrer", command=self.restart_niveau)
        file_menu.add_command(label="Ouvrir...", command=user_menu.Ouvrirlvl)
        file_menu.add_command(label="Quitter", command=menu.quit)

        help_menu = tk.Menu(menu)
        menu.add_cascade(label="Aide", menu=help_menu)
        help_menu.add_command(label="A Propos", command=user_menu.About)

    def default_frame(self):
        start_width = 30
        start_label = tk.Label(self.frame, text="Bienvenue !\n", width=start_width)
        start_label.grid(row=0, column=0)

        start_label2 = tk.Label(self.frame, text="Pour jouer, choissisez un\nniveau dans Fichier -> Ouvrir...\n", width=start_width)
        start_label2.grid(row=1, column=0)

    def clear_niveau(self):
        self.frame.destroy()
        self.frame = tk.Frame(self)
        self.frame.grid()
        self.niveau = []

    def start_next_niveau(self):
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

    def restart_niveau(self):
        if self.current_niveau:
            self.niveau_files.append(self.current_niveau)
            self.start_next_niveau()

    def load_niveau(self, niveau):
        self.clear_niveau()

        for row, line in enumerate(niveau):
            niveau_row = list(line)
            for column,x in enumerate(niveau_row):
                if x == Niveau.joueur:
                    niveau_row[column] = Niveau.sol

                elif x == Niveau.objectif:
                    self.objectifs[(row, column)] = Objectif.vide

                elif x == Niveau.caisse_sur_objectif:
                    self.objectifs[(row, column)] = Objectif.plein

            self.niveau.append(niveau_row)

            for column, char in enumerate(line):
                if char == Niveau.mur:
                    mur = tk.PhotoImage(file=Image.mur)
                    w = tk.Label(self.frame, image=mur)
                    w.mur = mur
                    w.grid(row=row, column=column)

                elif char == Niveau.objectif:
                    objectif = tk.PhotoImage(file=Image.objectif)
                    w = tk.Label(self.frame, image=objectif)
                    w.objectif = objectif
                    w.grid(row=row, column=column)

                elif char == Niveau.caisse_sur_objectif:
                    caisse_sur_objectif = tk.PhotoImage(file=Image.caisse_sur_objectif)
                    w = tk.Label(self.frame, image=caisse_sur_objectif)
                    w.caisse_sur_objectif = caisse_sur_objectif
                    w.grid(row=row, column=column)
                    self.caisses[(row, column)] = w

                elif char == Niveau.caisse:
                    caisse = tk.PhotoImage(file=Image.caisse)
                    w = tk.Label(self.frame, image=caisse)
                    w.caisse = caisse
                    w.grid(row=row, column=column)
                    self.caisses[(row, column)] = w

                elif char == Niveau.joueur:
                    joueur_image = tk.PhotoImage(file=Image.joueur)
                    self.joueur = tk.Label(self.frame, image=joueur_image)
                    self.joueur.joueur_image = joueur_image
                    self.joueur.grid(row=row, column=column)
                    self.joueur_position = (row, column)

    def move_joueur(self, direction):
        row, column = self.joueur_position
        prev_row, prev_column = row, column

        blocked = True
        if direction == Direction.left and self.niveau[row][column - 1] is not Niveau.mur and column > 0:
            blocked = self.move_caisse((row, column - 1), (row, column - 2))
            if not blocked:
                self.joueur_position = (row, column - 1)

        elif direction == Direction.right and self.niveau[row][column + 1] is not Niveau.mur:
            blocked = self.move_caisse((row, column + 1), (row, column + 2))
            if not blocked:
                self.joueur_position = (row, column + 1)

        elif direction == Direction.down and self.niveau[row + 1][column] is not Niveau.mur:
            blocked = self.move_caisse((row + 1, column), (row + 2, column))
            if not blocked:
                self.joueur_position = (row + 1, column)

        elif direction == Direction.up and self.niveau[row - 1][column] is not Niveau.mur and row > 0:
            blocked = self.move_caisse((row - 1, column), (row - 2, column))
            if not blocked:
                self.joueur_position = (row - 1, column)

        all_objectifs_plein = True
        for objectif in self.objectifs.values():
            if objectif is not Objectif.plein:
                all_objectifs_plein = False

        if all_objectifs_plein:
            self.start_next_niveau()
            return

        row, column = self.joueur_position
        if self.niveau[prev_row][prev_column] is Niveau.objectif and not blocked:
            objectif = tk.PhotoImage(file=Image.objectif)
            w = tk.Label(self.frame, image=objectif)
            w.objectif = objectif
            w.grid(row=prev_row, column=prev_column)

        if not blocked:
            self.joueur.grid_forget()

            if self.niveau[row][column] is Niveau.objectif:
                joueur_image = tk.PhotoImage(file=Image.joueur_sur_objectif)
            else:
                joueur_image = tk.PhotoImage(file=Image.joueur)

            self.joueur = tk.Label(self.frame, image=joueur_image)
            self.joueur.joueur_image = joueur_image
            self.joueur.grid(row=row, column=column)

    def move_caisse(self, location, next_location):
        row, column = location
        next_row, next_column = next_location

        if self.niveau[row][column] is Niveau.caisse and self.niveau[next_row][next_column] is Niveau.sol:
            self.caisses[(row, column)].grid_forget()
            caisse = tk.PhotoImage(file=Image.caisse)
            w = tk.Label(self.frame, image=caisse)
            w.caisse = caisse
            w.grid(row=next_row, column=next_column)

            self.caisses[(next_row, next_column)] = w
            self.niveau[row][column] = Niveau.sol
            self.niveau[next_row][next_column] = Niveau.caisse

        elif self.niveau[row][column] is Niveau.caisse and self.niveau[next_row][next_column] is Niveau.objectif:
            self.caisses[(row, column)].grid_forget()
            caisse_sur_objectif = tk.PhotoImage(file=Image.caisse_sur_objectif)
            w = tk.Label(self.frame, image=caisse_sur_objectif)
            w.caisse = caisse_sur_objectif
            w.grid(row=next_row, column=next_column)

            self.caisses[(next_row, next_column)] = w
            self.niveau[row][column] = Niveau.sol
            self.niveau[next_row][next_column] = Niveau.caisse_sur_objectif
            self.objectifs[(next_row, next_column)] = Objectif.plein

        elif self.niveau[row][column] is Niveau.caisse_sur_objectif and self.niveau[next_row][next_column] is Niveau.sol:
            self.caisses[(row, column)].grid_forget()
            caisse = tk.PhotoImage(file=Image.caisse)
            w = tk.Label(self.frame, image=caisse)
            w.caisse = caisse
            w.grid(row=next_row, column=next_column)

            self.caisses[(next_row, next_column)] = w
            self.niveau[row][column] = Niveau.objectif
            self.niveau[next_row][next_column] = Niveau.caisse
            self.objectifs[(row, column)] = Objectif.vide

        elif self.niveau[row][column] is Niveau.caisse_sur_objectif and self.niveau[next_row][next_column] is Niveau.objectif:
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

    def bloque(self, location, next_location):
        row, column = location
        next_row, next_column = next_location

        if self.niveau[row][column] is Niveau.caisse and self.niveau[next_row][next_column] is Niveau.mur:
            return True
        elif self.niveau[row][column] is Niveau.caisse_sur_objectif and self.niveau[next_row][next_column] is Niveau.mur:
            return True
        elif (self.niveau[row][column] is Niveau.caisse_sur_objectif and
                  (self.niveau[next_row][next_column] is Niveau.caisse or
                           self.niveau[next_row][next_column] is Niveau.caisse_sur_objectif)):
            return True
        elif (self.niveau[row][column] is Niveau.caisse and
                  (self.niveau[next_row][next_column] is Niveau.caisse or
                           self.niveau[next_row][next_column] is Niveau.caisse_sur_objectif)):
            return True


app = Application()
app.bind_all("<Key>", app.key)
app.mainloop()
