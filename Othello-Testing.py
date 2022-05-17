#####################################
# Name:             Joshua Villasis #
# Class:            CPSC 481        #
# Final Project:    Othello         #
#####################################

#################### Game Libraries ####################
from numpy import zeros
from time import sleep
import random
import math
from sys import exit

#################### Graphics Libraries ####################
import pygame

#################### Global Variables ####################
#AI depth (Minimax)
DEPTH = 4

#Board Dimensions
BOARD_ROWS = 8
BOARD_COLS = 8

#Player turn indicators
BLACK_TURN = 0
WHITE_TURN = 1

#Player token indicators
BLACK_TOKEN = 1
WHITE_TOKEN = 2

#Graphics Dimensions
SQUARESIZE = 100 #pixels
RADIUS = int(SQUARESIZE/2 - 5)
WIDTH = (BOARD_COLS * SQUARESIZE)
HEIGHT = (BOARD_ROWS * SQUARESIZE)
WINDOWSIZE = (WIDTH, HEIGHT)

#Graphics colors
GREEN = (0, 255, 0)     #Game Board
BLACK = (0, 0, 0)       #Black Disc
WHITE = (255, 255, 255) #White Disc

WEIGHTS =   [[16.16, -3.03,  0.99,  0.43,  0.43,  0.99, -3.03, 16.16],
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
        #Create an empty board
        s.board = zeros((BOARD_ROWS, BOARD_COLS))

        #Starting disc positions
        s.W1 = s.strToPos("D4")
        s.W2 = s.strToPos("E5")
        s.B1 = s.strToPos("E4")
        s.B2 = s.strToPos("D5")

        #Place starting discs
        s.board[s.W1[0]][s.W1[1]] = WHITE_TOKEN
        s.board[s.W2[0]][s.W2[1]] = WHITE_TOKEN
        s.board[s.B1[0]][s.B1[1]] = BLACK_TOKEN
        s.board[s.B2[0]][s.B2[1]] = BLACK_TOKEN

        #Determine who's turn to play
        s.turn = BLACK_TURN

    #################### Game Functions ####################

    #Print the board with position indicators
    def printBoard(s, board):
        print("   |A  B  C  D  E  F  G  H |")
        print("   -------------------------")
        for row in range(BOARD_ROWS):
            print(str(row+1) + "| " + str(board[row]))
        print()

    #Check if given position is within bounds
    def isOnBoard(s, pos):
        row = pos[0]
        col = pos[1]

        return 0 <= row <= 7 and 0 <= col <= 7

    #Convert input to position array
    def strToPos(s, str):
        #Get column position
        col = str[0]
        numCol = int(ord(col) % ord('A'))

        #Get row position
        row = int(str[1]) - 1

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
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if s.isVaildMove([row,col], board, token) != False:
                    validMoves.append([row, col])

        return validMoves

    #Place given disc color in position
    def placeToken(s, pos, board, token):
        #Get list of flanked discs
        flanked = s.isVaildMove(pos, board, token)

        #Place disc in position
        board[pos[0]][pos[1]] = token

        #Convert flanked discs
        for row, col in flanked:
            board[row][col] = token

    #Return score of a given token
    def getScore(s, board, token):
        score = 0

        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if board[row][col] == token:
                    score += 1

        return score

    #Return board visualizing score of the game
    def scoreboard(s):
        #Get scores of tokens
        blackScore = s.getScore(s.board, BLACK_TOKEN)
        whiteScore = s.getScore(s.board, WHITE_TOKEN)

        #Create empty board
        scoreboard = zeros((BOARD_ROWS, BOARD_COLS))

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
                return BLACK_TURN, BLACK_TOKEN
            elif playerColor == "W":
                return WHITE_TURN, WHITE_TOKEN
            else:
                print("Unknown command. Please try again.")
                print()

    #################### AI Functions ####################

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
            if (row == 0 or row == BOARD_ROWS) and (col == 0 or col == BOARD_COLS):
                return [row, col]

            #Find move that gives the best score
            tempBoard = board.copy()
            s.placeToken([row, col], tempBoard, token)
            tempScore = s.getScore(tempBoard, token)
            if tempScore > bestScore:
                bestMove = [row, col]
                bestScore = tempScore

        return bestMove

    #Get all positions for the token
    def getTokenPositions(s, board, token):
        tokenPositions = []

        for row in range(s.BOARD_ROWS):
            for col in range(s.BOARD_COLS):
                if board[row][col] == token:
                    tokenPositions.append((row, col))

        return tokenPositions


    #Check if the a given position is a frontier disc
    def isFrontierDisc(s, board, pos):
        frontier = False

        for x, y in [[0,1],[1,1],[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1]]:
            row, col = pos
            row += x
            col += y

            if s.isOnBoard([row, col]) and board[row][col] == 0:
                frontier = True

        return frontier

    #Score the current state of the board
    def scoreState(s, board, token):
        tokenPositions = s.getTokenPositions(board, token)
        score = 0

        #Score player discs
        for row, col in tokenPositions:
            if s.isFrontierDisc(board, (row, col)):
                score += 2 * weightedBoard[row][col]
            else:
                score += 10 * weightedBoard[row][col]

        return score

    #Check if board is end state
    def isTerminalNode(s, board):
        return len(s.getValidMoves(board, BLACK_TOKEN)) == 0 and len(s.getValidMoves(board, WHITE_TOKEN)) == 0


    #Minimax algorithm
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
                return (None, s.getScore(board, token))
        
        #If AI
        if maximizingPlayer:
            val = -math.inf

            #Check if AI skips turn
            if len(possibleMoves) == 0:
                newVal = s.miniMaxMove(board, depth-1, False, token)[1]
                
                if newVal > val:
                    val = newVal
                
                return None, val

            position = random.choice(possibleMoves)
            
            for pos in possibleMoves:
                tempBoard = board.copy()
                s.placeToken(pos, tempBoard, token)
                newVal = s.miniMaxMove(tempBoard, depth-1, False, token)[1]
                
                if newVal > val:
                    val = newVal
                    position = pos
                
            return pos, val

        #Opponent
        else:
            val = math.inf

            #Check if Opponent skips turn
            if len(possibleMoves) == 0:
                newVal = s.miniMaxMove(board, depth-1, True, token)[1]
                
                if newVal < val:
                    val = newVal
                
                return None, val

            position = random.choice(possibleMoves)
            
            for pos in possibleMoves:
                tempBoard = board.copy()
                s.placeToken(pos, tempBoard, token)
                newVal = s.miniMaxMove(tempBoard, depth-1, True, token)[1]

                if newVal < val:
                    val = newVal
                    position = pos
                
            return pos, val

    #################### Graphics Functions ####################

    #Draw the board in the pygame window
    def drawBoard(s, board):
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                pygame.draw.rect(s.screen, GREEN, (col * SQUARESIZE, row*SQUARESIZE, SQUARESIZE, SQUARESIZE))
                #Vertical Hash
                pygame.draw.line(s.screen, BLACK, (col * SQUARESIZE, 0), (col * SQUARESIZE, BOARD_ROWS * SQUARESIZE))
                #Horizontal Hash
                pygame.draw.line(s.screen, BLACK, (0, row*SQUARESIZE), (col * SQUARESIZE+SQUARESIZE, row*SQUARESIZE))

                #Draw black tokens
                if board[row][col] == BLACK_TOKEN:
                    pygame.draw.circle(s.screen, BLACK, (int(col*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
                #Draw white tokens
                elif board[row][col] == WHITE_TOKEN:
                    pygame.draw.circle(s.screen, WHITE, (int(col*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
        pygame.display.update()

    #Draw board visualizing score of the game
    def drawScoreboard(s):
        #Get scores of tokens
        blackScore = s.getScore(s.board, BLACK_TOKEN)
        whiteScore = s.getScore(s.board, WHITE_TOKEN)

        #Draw empty board
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                pygame.draw.rect(s.screen, GREEN, (col * SQUARESIZE, row*SQUARESIZE, SQUARESIZE, SQUARESIZE))
                #Vertical Hash
                pygame.draw.line(s.screen, BLACK, (col * SQUARESIZE, 0), (col * SQUARESIZE, BOARD_ROWS * SQUARESIZE))
                #Horizontal Hash
                pygame.draw.line(s.screen, BLACK, (0, row*SQUARESIZE), (col * SQUARESIZE+SQUARESIZE, row*SQUARESIZE))

        #Draw Tokens
        for row in range(BOARD_ROWS):
            for col in range(BOARD_COLS):
                if blackScore > 0:
                    pygame.draw.circle(s.screen, BLACK, (int(col*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
                    blackScore -= 1
                elif blackScore == 0 and whiteScore > 0:
                    pygame.draw.circle(s.screen, WHITE, (int(col*SQUARESIZE+SQUARESIZE/2), int(row*SQUARESIZE+SQUARESIZE/2)), RADIUS)
                    whiteScore -= 1

                pygame.display.update()
                sleep(.03)

    #################### Play Function ####################

    def play(s):
        #Who goes first
        player = s.playerColor()
        pTurn = player[0]
        pColor = player[1]
        aColor = (pColor % 2) + 1

        #Start pygame
        pygame.init()
        s.screen = pygame.display.set_mode(WINDOWSIZE)

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

                #User input loop
                #Check if token can make a valid move; if not, skip turn
                if len(s.getValidMoves(s.board, pColor)) != 0:
                    input = False
                    while not input:
                        for event in pygame.event.get():

                            #Quit window
                            if event.type == pygame.QUIT:
                                exit(1)
                            #Mosue input
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                #Get Mouse position
                                mousePos = [int(event.pos[1]/SQUARESIZE), int(event.pos[0]/SQUARESIZE)]

                                #User input: disc placement
                                command = s.posToStr(mousePos)

                                print("Player input: " + command)
                                print()

                                pos = s.strToPos(command)
                                #Check if position is a valid move
                                if s.isVaildMove(pos, s.board, pColor) == False:
                                    print("Position (" + command + ") is not a valid move.")
                                    print()
                                    continue

                                else:
                                    s.placeToken(pos, s.board, pColor)
                                    input = True
                                    break

            ##### AI's Turn #####
            else:
                #Add buffer for better UX
                sleep(.5)

                #Check if token can make a valid move; if not, skip turn
                if len(s.getValidMoves(s.board, aColor)) != 0:
                    #AI = find best move to make
                    #pos = s.getBestMove(s.board, aColor)
                    pos = s.miniMaxMove(s.board, DEPTH, True, aColor)[0]

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
