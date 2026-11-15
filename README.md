# 🧱 Breakout (casse-briques) en Python

Jeu de casse-briques développé avec **Python** et **pygame** : une balle, une raquette, des briques à détruire, 3 niveaux, de la musique et des effets sonores.

## Fonctionnalités
- 3 niveaux chargés depuis des fichiers CSV (`levels/`), faciles à modifier ou à étendre
- Code organisé en classes : `Game`, `Ball`, `Paddle`, `Brick`
- Musique et son de destruction des briques

## Installation et lancement
```bash
pip install pygame
python3 main.py
```

## Commandes
| Touche | Action |
|---|---|
| ← / → | Déplacer la raquette |
| Espace | Lancer / relancer la balle |

## Structure
```
main.py        point d'entrée
game.py        boucle principale et niveaux
ball.py        balle
paddle.py      raquette
brick.py       briques
levels/        niveaux (CSV)
sound/         musique et effets
```

## Crédits
Sprites : *Basic Breakout Asset Pack*.
