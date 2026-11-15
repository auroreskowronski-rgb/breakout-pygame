import pygame
import utilities


class Ball(pygame.sprite.Sprite):
    """La balle : gère son déplacement et ses rebonds
    sur les murs, la raquette et les briques."""

    def __init__(self):
        """Charge l'image de la balle et initialise sa vitesse."""
        super().__init__()
        # Image de la balle
        self.image = pygame.image.load(
            "BasicBreakoutAssetPack/ball.png"
        ).convert_alpha()
        # Rectangle de la balle : sa positio
        #  et sa taille (sert aux collisions)
        self.rect = self.image.get_rect()
        # Vitesse de déplacement de la balle (en pixels par image)
        self.speed_x = 0
        # Valeur négative = la balle monte
        self.speed_y = -10
        # False tant que le joueur n'a pas lancé la balle
        self.is_moving = False

    def move(self, player):
        """Déplace la balle et gère les rebonds
        sur les murs gauche, droit et haut."""
        if not self.is_moving:
            # Tant qu'elle ne bouge pas, elle reste positionnée
            # au-dessus de la raquette
            self.rect.x = int(
                round(
                    player.rect.x + (player.rect.width / 2) -
                    (self.rect.width / 2), 0
                )
            )
            self.rect.y = player.rect.y - self.rect.height + 10
        # Sauvegarde la position précédente de la balle avant de la déplacer
        # (sert à savoir de quel côté une brique est touchée)
        self.previous_rect = self.rect.copy()
        # Déplacement de la balle selon sa vitesse
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Rebond sur le mur gauche
        if self.rect.x <= 0:
            self.rect.x = 0
            self.speed_x = -self.speed_x

        # Rebond sur le mur droit (1280 est la largeur de l'écran)
        if self.rect.x >= 1280 - self.rect.width:
            self.rect.x = 1280 - self.rect.width
            self.speed_x = -self.speed_x

        # Rebond sur le haut de l'écran
        if self.rect.y <= 0:
            self.rect.y = 0
            self.speed_y = -self.speed_y

    def check_collision_paddle(self, paddle):
        """Fait rebondir la balle sur la raquette
        l'angle dépend de l'endroit de l'impact."""
        # Si la balle ne touche pas la raquette, il n'y a rien à faire
        if not self.rect.colliderect(paddle.rect):
            return
        # Vitesse totale de la balle (longueur du vecteur vitesse)
        # conservée après le rebond
        amp_vect_1 = utilities.amplitude_vector(self.speed_x, self.speed_y)
        # Replace la balle juste au-dessus de la
        # raquette (évite qu'elle reste coincée dedans)
        self.rect.bottom = paddle.rect.top
        # Calcule le décalage entre le centre de
        # la balle et le centre de la raquette
        ball_center = self.rect.centerx
        paddle_center = paddle.rect.centerx
        offset = ball_center - paddle_center
        # Plus l'impact est loin du centre, plus la vitesse
        # horizontale est grande (limitée à 9)
        self.speed_x = min(abs(offset) ** 2 * 0.01, 9)
        # Calcule la vitesse verticale pour garder
        # la même vitesse totale (théorème de Pythagore)
        self.speed_y = (amp_vect_1**2 - self.speed_x**2) ** 0.5
        # La balle repart vers le haut
        self.speed_y = -self.speed_y

        # Impact à gauche du centre : la balle part vers la gauche
        if offset < 0:
            self.speed_x = -self.speed_x

    def check_collision_bricks(self, bricks, sound):
        """Gère la collision avec les briques : rebond
        suppression de la brique et effet sonore.

        bricks : groupe de briques du niveau.
        sound : effet sonore joué quand une brique est détruite.
        """
        for brick in bricks:
            if self.rect.colliderect(brick.rect):
                # Avant son déplacement, la balle était
                #  à gauche ou à droite de la brique :
                # c'est un impact sur le côté
                # on inverse la vitesse horizontale
                if (
                    self.previous_rect.right <= brick.rect.left
                    or self.previous_rect.left >= brick.rect.right
                ):
                    self.speed_x = -self.speed_x
                # Sinon, l'impact est sur le dessus
                # ou le dessous : on inverse la vitesse verticale
                else:
                    self.speed_y = -self.speed_y

                # Détruit la brique touchée et joue le son
                bricks.remove(brick)
                sound.play()
                # Une seule brique détruite par image
                break
