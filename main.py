# Using this library for now: https://pypi.org/project/imparaai-checkers/

from checkers.game import Game
import alphabeta

game = Game()

print(alphabeta.alphabeta(game))
