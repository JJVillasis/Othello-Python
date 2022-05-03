#####################################
# Name:             Joshua Villasis #
# Class:            CPSC 481        #
# Final Project:    Othello         #
#####################################

from Othello import Othello

testBoard = [[0, 0, 0, 0, 0, 0, 0, 0],
			 [0, 0, 0, 0, 0, 0, 0, 0], 
			 [0, 0, 2, 2, 2, 2, 0, 0], 
			 [0, 0, 2, 1, 1, 2, 0, 0], 
			 [0, 0, 2, 1, 1, 2, 0, 0], 
			 [0, 0, 2, 1, 2, 2, 0, 0], 
			 [0, 0, 2, 2, 2, 0, 0, 0], 
			 [0, 0, 0, 0, 0, 0, 0, 0]]

game = Othello()
print(game.scoreState(testBoard, game.BLACK_TOKEN))
print(game.scoreState(testBoard, game.WHITE_TOKEN))
#game.play()