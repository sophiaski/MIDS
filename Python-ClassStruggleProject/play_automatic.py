import sys
from class_struggle_automatic import Game, Board, Player

try:
    Game(int(sys.argv[1]))
#    example = Game(sys.argv[1])
except:
    print("Something happened inside the function.")
