#!/usr/bin/env python3

import pygame
from game import Game

"""jeu_python.main"""

__author__ = "skowro_j"

# Initialisation de tous les modules de Pygame (affichage, son, etc.)
pygame.init()


# Le jeu ne démarre que si ce fichier est lancé directement
if __name__ == "__main__":
    # Création du jeu puis lancement de la boucle principale
    game = Game()
    game.run()
