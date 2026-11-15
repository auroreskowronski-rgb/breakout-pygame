import pygame


class Paddle(pygame.sprite.Sprite):
    """La raquette contrôlée par le joueur
    avec les flèches gauche et droite."""

    def __init__(self):
        """Charge l'image de la raquette et initialise sa vitesse."""
        super().__init__()
        # Image de la raquette
        self.image = pygame.image.load(
            "BasicBreakoutAssetPack/paddle.png"
        ).convert_alpha()
        # Rectangle de la raquette : sa position
        # et sa taille (sert aux collisions)
        self.rect = self.image.get_rect()
        # Vitesse de déplacement de la raquette (en pixels par image)
        self.speed = 10

    def move_left(self):
        """Déplace la raquette vers la gauche sans sortir de l'écran."""
        self.rect.x -= self.speed
        # Empêche de dépasser le bord gauche
        self.rect.x = max(self.rect.x, 0)

    def move_right(self):
        """Déplace la raquette vers la droite sans sortir de l'écran."""
        self.rect.x += self.speed
        # Empêche de dépasser le bord droit (1280 = largeur de l'écran)
        self.rect.x = min(self.rect.x, 1280 - self.rect.width)
