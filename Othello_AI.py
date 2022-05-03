#####################################
# Name:             Joshua Villasis #
# Class:            CPSC 481        #
# Final Project:    Othello         #
#####################################

##### Game Libraries #####
from numpy import zeros
from time import sleep
import random
import math

##### Graphics Libraries #####
import pygame
from sys import exit

##### Global Variables #####
GREEN = (0, 255, 0)     #Game Board
BLACK = (0, 0, 0)       #Black Disc
WHITE = (255, 255, 255) #White Disc

weightedBoard = [[16.16, -3.03,  0.99,  0.43,  0.43,  0.99, -3.03, 16.16],
                 [-4.12, -1.81, -0.08, -0.27, -0.27, -0.08, -1.81, -4.12], 
                 [ 1.33, -0.04,  0.51,  0.07,  0.07,  0.51, -0.04,  1.33],
                 [ 0.63, -0.18, -0.04, -0.01, -0.01, -0.04, -0.18,  0.63],
                 [ 0.63, -0.18, -0.04, -0.01, -0.01, -0.04, -0.18,  0.63],
                 [ 1.33, -0.04,  0.51,  0.07,  0.07,  0.51, -0.04,  1.33],
                 [-4.12, -1.81, -0.08, -0.27, -0.27, -0.08, -1.81, -4.12],
                 [16.16, -3.03,  0.99,  0.43,  0.43,  0.99, -3.03, 16.16]]

class Othello:

    #Class Constructor
    def __init__(s):
        #AI depth
        s.depth = 4

        #Board Dimensions
        s.BOARD_ROWS = 8
        s.BOARD_COLS = 8

        #Input positions
        s.ROW_POS = 1
        s.COL_POS = 0

        #Player turn indicators
        s.BLACK_TURN = 0
        s.WHITE_TURN = 1

        #Player token indicators
        s.BLACK_TOKEN = 1
        s.WHITE_TOKEN = 2

        #Starting disc positions
        s.WHITE_START1 = s.strToPos("D4")
        s.WHITE_START2 = s.strToPos("E5")
        s.BLACK_START1 = s.strToPos("E4")
        s.BLACK_START2 = s.strToPos("D5")

        #Create an empty board
        s.board = zeros((s.BOARD_ROWS, s.BOARD_COLS))

        #Place starting discs
        s.board[s.WHITE_START1[0]][s.WHITE_START1[1]] = s.WHITE_TOKEN
        s.board[s.WHITE_START2[0]][s.WHITE_START2[1]] = s.WHITE_TOKEN
        s.board[s.BLACK_START1[0]][s.BLACK_START1[1]] = s.BLACK_TOKEN
        s.board[s.BLACK_START2[0]][s.BLACK_START2[1]] = s.BLACK_TOKEN

        #Int turn - determine who's turn to play
        s.turn = s.BLACK_TURN

    ##### Game Functions #####

    #Print the board with position indicators
    def printBoard(s, board):
        print("   |A  B  C  D  E  F  G  H |")
        print("   -------------------------")
        for row in range(s.BOARD_ROWS):
            print(str(row+1) + "| " + str(board[row]))
        print()

    #Check if given position is within bounds
    def isOnBoard(s, pos):
        row = pos[0]
        col = pos[1]

        return 0 <= row <= 7 and 0 <= col <= 7

    #Check if player input is a valid position command
    def isVaildCommand(s, command):
        cols = ["A", "B", "C", "D", "E", "F", "G", "H"]

        for row in range(1, 9):
            rowStr = str(row)
            for col in cols:
                compStr = col + rowStr

                if command == compStr:
                    return True

        return False

    #Convert input to position array
    def strToPos(s, str):
        #Get column position
        col = str[s.COL_POS]
        numCol = int(ord(col) % ord('A'))

        #Get row position
        row = int(str[s.ROW_POS]) - 1

        #return position
        return row, numCol

    #Convert position to Readable string
    def posToStr(s, pos):
        #Readable Columns
        cols = ["A", "B", "C", "D", "E", "F", "G", "H"]
        output = ""
        output += cols[pos[1]]
        output += str(pos[0]+1)
        return output

    #Check if position on board is open and can flank enemy disc
    #If valid move, return list of flanked discs
    def isVaildMove(s, pos, board, token):
        moveRow = pos[0]
        moveCol = pos[1]

        #Check if space is open
        if board[moveRow][moveCol] != 0:
            return False

        #Temporarily place disc on copy board
        tempBoard = board.copy()
        tempBoard[moveRow][moveCol] = token

        #Get enemy token
        oppToken = (token % 2) + 1

        #List of flippable tiles if move is made
        flippedTiles = []

        #x,y = search direction reletive to move
        for x,y in [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]:
            #Get first step in given direction
            row,col  = moveRow, moveCol
            row += x
            col += y

            #If token next to move is enemy disc,
            if s.isOnBoard([row,col]) and tempBoard[row][col] == oppToken:
                #Advance a step
                row += x
                col += y

                #If out of bounds, increment x,y
                if not s.isOnBoard([row,col]):
                    continue

                #While found token is enemy's, advance a step
                while tempBoard[row][col] == oppToken:
                    row += x
                    col += y

                    #If out of bounds, increment x,y
                    if not s.isOnBoard([row, col]):
                        break
                if not s.isOnBoard([row,col]):
                    continue

                #If found token is own, flanked line is found
                if tempBoard[row][col] == token:

                    #Go in reverse direction to get flanked discs
                    while True:
                        row -= x
                        col -= y

                        #At made move
                        if tempBoard[row][col] == token:
                            break

                        flippedTiles.append([row, col])

        #If no enemy disc is flanked, not a valid move
        if(len(flippedTiles) == 0):
            return False

        return flippedTiles

    #Get the valids moves of a given token
    def getValidMoves(s, board, token):
        validMoves = []

        #Traverse board, finding valid moves
        for row in range(s.BOARD_ROWS):
            for col in range(s.BOARD_COLS):
                if s.isVaildMove([row,col], board, token) != False:
                    validMoves.append([row, col])

        return validMoves

    ###### AI Functions #####

    #Get best move of current state of the board for token
    def getBestMove(s, board, token):
        #Get list of valid moves for token
        posibleMoves = s.getValidMoves(board, token)

        #Randomize possible moves list
        random.shuffle(posibleMoves)

        bestScore = -1
        bestMove = [0,0]

        #Traverse list of valid moves
        for row, col in posibleMoves:

            #Prioritize going for corners
            if (row == 0 or row == s.BOARD_ROWS) and (col == 0 or col == s.BOARD_COLS):
                return [row, col]

            #Find move that gives the best score
            tempBoard = board.copy()
            s.placeToken([row, col], tempBoard, token)
            tempScore = s.getScore(tempBoard, token)
            if tempScore > bestScore:
                bestMove = [row, col]
                bestScore = tempScore

        return bestMove

    def getTokenPositions(s, board, token):
        tokenPositions = []

        for row in range(s.BOARD_ROWS):
            for col in range(s.BOARD_COLS):
                if board[row][col] == token:
                    tokenPositions.append((row, col))

        return tokenPositions

    def scoreState(s, board, token):
        tokenPositions = s.getTokenPositions(board, token)
        score = 0

        #Score frontier discs
        for row, col in tokenPositions:
            if s.isFrontierDisc(board, (row, col)):
                score += 2 * weightedBoard[row][col]
            else:
                score += 10 * weightedBoard[row][col]

        return score

    def isFrontierDisc(s, board, pos):
        frontier = False

        for x, y in [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]:
            row, col = pos
            row += x
            col += y

            if s.isOnBoard([row, col]) and board[row][col] == 0:
                frontier = True

        return frontier


    def isTerminalNode(s, board):
        return len(s.getValidMoves(board, s.BLACK_TOKEN)) == 0 and len(s.getValidMoves(board, s.WHITE_TOKEN)) == 0


    def miniMaxMove(s, board, depth, maximizingPlayer, token):
         #Get list of valid moves
        possibleMoves = s.getValidMoves(board, token)

        oppToken = (token % 2) + 1

        #If at beginning or terminal node
        if depth == 0 or s.isTerminalNode(board):
            #End of game
            if s.isTerminalNode(board):
                #AI wins
                if s.getScore(board, token) > s.getScore(board, oppToken):
                    return (None, 10000000000)
                #Opponent wins
                elif s.getScore(board, oppToken) > s.getScore(board, token):
                    return (None, -10000000000)
                #Tie
                else:
                    return (None, 0)
            #Depth is 0
            else:
                if maximizingPlayer:
                    return (None, s.scoreState(board, token))
                else:
                    return (None, s.scoreState(board, oppToken))
        
        #If AI
        if maximizingPlayer:
            val = -math.inf

            #Check if AI skips turn
            if len(possibleMoves) == 0:
                newVal = s.miniMaxMove(board, depth-1, False, oppToken)[1]
                
                if newVal > val:
                    val = newVal
                
                return None, val

            position = random.choice(possibleMoves)
            
            for pos in possibleMoves:
                tempBoard = board.copy()
                s.placeToken(pos, tempBoard, token)
                newVal = s.miniMaxMove(tempBoard, depth-1, False, oppToken)[1]
                
                if newVal > val:
                    val = newVal
                    position = pos
                
            return pos, val

        #Opponent
        else:
            val = math.inf

            #Check if opponent skips turn
            if len(possibleMoves) == 0:
                newVal = s.miniMaxMove(board, depth-1, True, oppToken)[1]
                
                if newVal < val:
                    val = newVal
                
                return None, val

            position = random.choice(possibleMoves)
            
            for pos in possibleMoves:
                tempBoard = board.copy()
                s.placeToken(pos, tempBoard, token)
                newVal = s.miniMaxMove(tempBoard, depth-1, True, oppToken)[1]

                if newVal < val:
                    val = newVal
                    position = pos
                
            return pos, val

    #Place given disc color in position
    def placeToken(s, pos, board, token):
        #Get list of flanked discs
        flanked = s.isVaildMove(pos, board, token)

        #Place disc in position
        board[pos[0]][pos[1]] = token

        #Convert flanked discs
        for row, col in flanked:
            board[row][col] = token

    #Return list of scores of the token
    def getScore(s, board, token):
        score = 0

        for row in range(s.BOARD_ROWS):
            for col in range(s.BOARD_COLS):
                if board[row][col] == token:
                    score += 1

        return score

    #Return board visualizing score of the game
    def scoreboard(s):
        #Get scores of tokens
        blackScore = s.getScore(s.board, s.BLACK_TOKEN)
        whiteScore = s.getScore(s.board, s.WHITE_TOKEN)

        #Create empty board
        scoreboard = zeros((s.BOARD_ROWS, s.BOARD_COLS))

        #Array iterators
        row = 0
        col = 0

        #Black score
        for s in range (blackScore):
            scoreboard[row][col] = 1

            #Increment iterator
            col += 1
            if col == 8:
                col = 0
                row += 1

        #White Score
        for s in range (whiteScore):
            scoreboard[row][col] = 2

            #Increment iterator
            col += 1
            if col == 8:
                col = 0
                row += 1

        return scoreboard

    #Find if player goes first or second
    def playerColor(s):
        while True:
            #Ask player which color to play as
            playerColor = input("Pick color token to play (W-White/B-Black): ").upper()
            print()

            if playerColor == "B":
                return s.BLACK_TURN, s.BLACK_TOKEN
            elif playerColor == "W":
                return s.WHITE_TURN, s.WHITE_TOKEN
            else:
                print("Unknown command. Please try again.")
                print()

    ##### Graphics Functions #####

    #Draw the board in the pygame window
    def drawBoard(s, board):
        for row in range(s.BOARD_ROWS):
            for col in range(s.BOARD_COLS):
                pygame.draw.rect(s.screen, GREEN, (col * s.SQUARESIZE, row*s.SQUARESIZE, s.SQUARESIZE, s.SQUARESIZE))
                #Vertical Hash
                pygame.draw.line(s.screen, BLACK, (col * s.SQUARESIZE, 0), (col * s.SQUARESIZE, s.BOARD_ROWS * s.SQUARESIZE))
                #Horizontal Hash
                pygame.draw.line(s.screen, BLACK, (0, row*s.SQUARESIZE), (col * s.SQUARESIZE+s.SQUARESIZE, row*s.SQUARESIZE))

                #Draw black tokens
                if board[row][col] == s.BLACK_TOKEN:
                    pygame.draw.circle(s.screen, BLACK, (int(col*s.SQUARESIZE+s.SQUARESIZE/2), int(row*s.SQUARESIZE+s.SQUARESIZE/2)), s.RADIUS)
                #Draw white tokens
                elif board[row][col] == s.WHITE_TOKEN:
                    pygame.draw.circle(s.screen, WHITE, (int(col*s.SQUARESIZE+s.SQUARESIZE/2), int(row*s.SQUARESIZE+s.SQUARESIZE/2)), s.RADIUS)
        pygame.display.update()

    #Draw board visualizing score of the game
    def drawScoreboard(self):
        #Get scores of tokens
        blackScore = self.getScore(self.board, self.BLACK_TOKEN)
        whiteScore = self.getScore(self.board, self.WHITE_TOKEN)

        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                pygame.draw.rect(self.screen, GREEN, (col * self.SQUARESIZE, row*self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                #Vertical Hash
                pygame.draw.line(self.screen, BLACK, (col * self.SQUARESIZE, 0), (col * self.SQUARESIZE, self.BOARD_ROWS * self.SQUARESIZE))
                #Horizontal Hash
                pygame.draw.line(self.screen, BLACK, (0, row*self.SQUARESIZE), (col * self.SQUARESIZE+self.SQUARESIZE, row*self.SQUARESIZE))

        for row in range(self.BOARD_ROWS):
            for col in range(self.BOARD_COLS):
                if blackScore > 0:
                    pygame.draw.circle(self.screen, BLACK, (int(col*self.SQUARESIZE+self.SQUARESIZE/2), int(row*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
                    blackScore -= 1
                elif blackScore == 0 and whiteScore > 0:
                    pygame.draw.circle(self.screen, WHITE, (int(col*self.SQUARESIZE+self.SQUARESIZE/2), int(row*self.SQUARESIZE+self.SQUARESIZE/2)), self.RADIUS)
                    whiteScore -= 1

                pygame.display.update()
                sleep(.03)

        #pygame.display.update()

    ##### Play Function #####

    def play(s):
        #Who goes first
        player = s.playerColor()
        pTurn = player[0]
        pColor = player[1]
        aColor = (pColor % 2) + 1

        #Start pygame
        pygame.init()

        #Graphics Dimensions
        s.SQUARESIZE = 100 #pixels
        s.RADIUS = int(s.SQUARESIZE/2 - 5)
        windowWidth = (s.BOARD_COLS * s.SQUARESIZE)
        windowHeight = (s.BOARD_ROWS * s.SQUARESIZE)
        s.windowSize = (windowWidth, windowHeight)

        s.screen = pygame.display.set_mode(s.windowSize)

        s.drawBoard(s.board)
        pygame.display.update()

        ##### Game loop #####
        while True:

            print("==================================================")
            print()

            s.printBoard(s.board)
            s.drawBoard(s.board)

            ##### Player's turn #####
            if s.turn == pTurn:

                sleep(.5)

                #User input loop
                #Check if token can make a valid move; if not, skip turn
                if len(s.getValidMoves(s.board, pColor)) != 0:
                    pos = s.getBestMove(s.board, pColor)

                    #Signal AI output
                    output = s.posToStr(pos)
                    print("Best Move Input: " + output)

                    #Place disc
                    s.placeToken(pos, s.board, pColor)

            ##### AI's Turn #####
            else:
                #Add buffer for better UX
                sleep(.5)

                #Check if token can make a valid move; if not, skip turn
                if len(s.getValidMoves(s.board, aColor)) != 0:
                    #AI = find best move to make
                    #pos = s.getBestMove(s.board, aColor)
                    pos = s.miniMaxMove(s.board, s.depth, True, aColor)[0]

                    #Signal AI output
                    output = s.posToStr(pos)
                    print("AI Input: " + output)

                    #Place disc
                    s.placeToken(pos, s.board, aColor)

            print("==================================================")
            print()

            #No more valid moves => Game Over
            if len(s.getValidMoves(s.board, pColor)) == 0 and len(s.getValidMoves(s.board, aColor)) == 0:
                break
            #Next Turn
            else:
                s.turn = (s.turn + 1) % 2


        #Game Over
        print("Game Over!")
        print()

        s.printBoard(s.board)
        s.drawBoard(s.board)
        sleep(2)

        #Get scores
        playerScore = s.getScore(s.board, pColor)
        aiScore = s.getScore(s.board, aColor)

        #Print scoreboard
        s.drawScoreboard()
        s.printBoard(s.scoreboard())

        print("Player = " + str(playerScore))
        print("AI = " + str(aiScore))
        print()

        #Who Won
        if playerScore > aiScore:
            print("Player Wins!")
        elif aiScore > playerScore:
            print("AI Wins!")
        else:
            print("Draw...")

        print()

        while True:
            for event in pygame.event.get():
                #Quit window
                if event.type == pygame.QUIT:
                    exit(1)

game = Othello()
game.play()
