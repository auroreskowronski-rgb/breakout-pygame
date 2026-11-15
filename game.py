import csv
import os

import pygame
from ball import Ball
from brick import Brick
from paddle import Paddle


class Game:
    """Gère la fenêtre, les objets du jeu (raquette, balle, briques)
    les sons et la boucle principale."""

    def __init__(self):
        """Crée la fenêtre et prépare tous les éléments
        nécessaires avant le début de la partie."""
        # --- Fenêtre ---
        # Création de la fenêtre de jeu (largeur 1280, hauteur 720)
        self.screen = pygame.display.set_mode((1280, 720))
        # Titre affiché dans la barre de la fenêtre
        pygame.display.set_caption("Dawn Breaker")
        # Horloge utilisée pour limiter le nombre d'images par seconde
        self.clock = pygame.time.Clock()
        # Chargement de l'image de fond
        self.fond = pygame.image.load(
            "BasicBreakoutAssetPack/background.png"
        ).convert_alpha()

        # --- Raquette (le joueur) ---
        self.player = Paddle()
        # Centre la raquette horizontalement
        # (640 = moitié de la largeur de l'écran).
        # round() puis int() évitent une erreur si
        # la largeur de la raquette est impaire.
        self.player.rect.x = int(round(640 - self.player.rect.width / 2, 0))
        # Place la raquette en bas de l'écran, avec une marge de 10 pixels
        self.player.rect.y = 720 - self.player.rect.height - 10

        # --- Balle ---
        self.ball = Ball()
        # Centre la balle horizontalement, comme la raquette
        self.ball.rect.x = int(round(640 - self.ball.rect.width / 2, 0))
        # Place la balle juste au-dessus de la raquette
        self.ball.rect.y = self.player.rect.y - self.ball.rect.height - 5

        # --- Niveaux et briques ---
        # Liste des fichiers CSV des niveaux, dans l'ordre où ils sont joués
        self.level_list = ["level1.csv", "level2.csv", "level3.csv"]
        # Indice du niveau en cours dans level_list (0 = premier niveau)
        self.current_level_index = 0
        # Chargement des briques du premier niveau
        self.bricks = self.load_level(
            os.path.join(
                os.path.dirname(__file__),
                "levels",
                self.level_list[self.current_level_index],
            )
        )

        # --- Sons ---
        # Musique de fond jouée en boucle (-1 = répétition infinie)
        pygame.mixer.music.load("sound/music.ogg")
        pygame.mixer.music.play(-1)
        # Effet sonore joué quand une brique est détruite
        self.brick_sound = pygame.mixer.Sound("sound/brick.ogg")
        # Volume de l'effet (entre 0.0 et 1.0)
        self.brick_sound.set_volume(1)

    def load_level(self, path):
        """Crée les briques d'un niveau à partir d'un fichier CSV.

        Chaque cellule du CSV représente
        une brique : le nombre indique son type
        (couleur), et une cellule vide ou égale à 0 signifie « pas de brique ».
        Retourne un groupe pygame contenant toutes les briques.
        """
        bricks = pygame.sprite.Group()
        with open(path, newline="") as f:
            # i = numéro de la ligne, row = contenu de la ligne
            for i, row in enumerate(csv.reader(f)):
                # j = numéro de la colonne, cell = contenu de la cellule
                for j, cell in enumerate(row):
                    # Ignore les cellules vides ou égales à 0 (pas de brique)
                    if cell.strip() in ("", "0"):
                        continue
                    value = cell.strip()
                    if value in ("", "0"):
                        continue
                    # Crée la brique du type indiqué dans le CSV
                    brick = Brick(int(value))
                    # Position : marge gauche de 82 px + espacement
                    # de 10 px entre les briques
                    brick.rect.x = 82 + j * (brick.rect.width + 10)
                    # Position : marge haute de 50 px + espacement
                    # de 10 px entre les lignes
                    brick.rect.y = 50 + i * (brick.rect.height + 10)
                    bricks.add(brick)
        return bricks

    def reset(self):
        """Replace la raquette et la balle à leur
        position de départ (balle à l'arrêt)."""
        # Replace la raquette au centre en bas de l'écran
        self.player.rect.x = int(round(640 - self.player.rect.width / 2, 0))
        self.player.rect.y = 720 - self.player.rect.height - 10

        # Replace la balle juste au-dessus de la raquette
        self.ball.rect.x = int(round(640 - self.ball.rect.width / 2, 0))
        self.ball.rect.y = self.player.rect.y - self.ball.rect.height - 5

        # Réinitialise la vitesse de la balle à son état
        # initial (vers le haut, sans déviation)
        self.ball.speed_x = 0
        self.ball.speed_y = -10
        # La balle attend que le joueur appuie sur Espace
        self.ball.is_moving = False

    def run(self):
        """Boucle principale : événements, affichage
        déplacements et collisions à chaque image."""
        # Tant que running vaut True, le jeu continue
        running = True
        while running:
            # --- Événements (fermeture de la fenêtre, touche Espace) ---
            for event in pygame.event.get():
                # Clic sur la croix de la fenêtre : on arrête le jeu
                if event.type == pygame.QUIT:
                    running = False

                # Appui sur Espace : lance la balle
                if (event.type == pygame.KEYDOWN
                        and event.key == pygame.K_SPACE):
                    self.ball.is_moving = True

            # --- Affichage ---
            # Le fond est dessiné en premier, puis les
            # autres éléments par-dessus
            self.screen.blit(self.fond, (0, 0))
            self.screen.blit(self.player.image, self.player.rect)
            self.screen.blit(self.ball.image, self.ball.rect)
            for brick in self.bricks:
                self.screen.blit(brick.image, brick.rect)

            # --- Gestion des touches de déplacement ---
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                self.player.move_left()
            if keys[pygame.K_RIGHT]:
                self.player.move_right()

            # --- Déplacement de la balle et collisions ---
            self.ball.move(self.player)
            self.ball.check_collision_paddle(self.player)
            self.ball.check_collision_bricks(self.bricks, self.brick_sound)

            # --- Passage au niveau suivant ---
            # Quand le joueur a détruit toutes les briques du niveau
            if len(self.bricks) == 0:
                self.current_level_index += 1
                # S'il reste un niveau, on le charge ; sinon, le jeu se termine
                if self.current_level_index < len(self.level_list):
                    self.bricks = self.load_level(
                        os.path.join(
                            os.path.dirname(__file__),
                            "levels",
                            self.level_list[self.current_level_index],
                        )
                    )
                    self.reset()
                else:
                    running = False

            # Met à jour l'écran avec tout ce qui vient d'être dessiné
            pygame.display.flip()
            # Limite le jeu à 60 images par seconde
            self.clock.tick(60)

            # Si la balle sort par le bas de l'écran
            # on replace la raquette et la balle
            if self.ball.rect.y > 720:
                self.reset()

        # Fin de la boucle : ferme proprement pygame
        pygame.quit()
