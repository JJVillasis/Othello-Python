import numpy
import sys

class Othello:

    #Class Constructor
    def __init__(s):
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
        s.board = numpy.zeros((s.BOARD_ROWS, s.BOARD_COLS))

        #Place starting discs
        s.board[s.WHITE_START1[0]][s.WHITE_START1[1]] = s.WHITE_TOKEN
        s.board[s.WHITE_START2[0]][s.WHITE_START2[1]] = s.WHITE_TOKEN
        s.board[s.BLACK_START1[0]][s.BLACK_START1[1]] = s.BLACK_TOKEN
        s.board[s.BLACK_START2[0]][s.BLACK_START2[1]] = s.BLACK_TOKEN

        #Int turn - determine who's turn to play
        s.turn = s.BLACK_TURN

    #Print the board with position indicators
    def printBoard(s):
        print("   |A  B  C  D  E  F  G  H |")
        print("   -------------------------")
        for row in range(s.BOARD_ROWS):
            print(str(row+1) + "| " + str(s.board[row]))
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

    #Place given disc color in position
    def placeToken(s, pos, board, token):
        #Get list of flanked discs
        flanked = s.isVaildMove(pos, board, token)

        #Place disc in position
        board[pos[0]][pos[1]] = token

        #Convert flanked discs
        for row, col in flanked:
            board[row][col] = token

    #Retrun list of scores of the tokens
    def getScores(s, board):
        blackScore = 0
        whiteScore = 0

        for row in range(s.BOARD_ROWS):
            for col in range(s.BOARD_COLS):
                if board[row][col] == s.BLACK_TOKEN:
                    blackScore += 1
                elif board[row][col] == s.WHITE_TOKEN:
                    whiteScore += 1

        return blackScore, whiteScore

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

    def play(s):
        #Who goes first
        player = s.playerColor()
        pTurn = player[0]
        pColor = player[1]
        aColor = (pColor % 2) + 1

        #Game loop
        while True:

            s.printBoard()

            #Player's turn
            if s.turn == pTurn:
                #User input loop
                while True:
                    #User input: disc placement
                    command = input("Player's Turn (A-F|1-8): ").upper()
                    print()

                    #Check if command is valid
                    if not s.isVaildCommand(command):
                        print("Unknown command. Please try again.")
                        print()
                        continue

                    pos = s.strToPos(command)

                    #Check if position is a valid move
                    if s.isVaildMove(pos, s.board, pColor) == False:
                        print("Position (" + command + ") is not a valid move.")
                        print()
                        continue
                    else:
                        break

                s.placeToken(pos, s.board, pColor)

            #AI's Turn
            else:
                while True:
                    #User input: disc placement
                    command = input("AI's Turn (A-F|1-8): ").upper()
                    print()

                    #Check if command is valid
                    if not s.isVaildCommand(command):
                        print("Unknown command. Please try again.")
                        print()
                        continue

                    pos = s.strToPos(command)

                    #Check if position is a valid move
                    if s.isVaildMove(pos, s.board, aColor) == False:
                        print("Position (" + command + ") is not a valid move.")
                        print()
                        continue
                    else:
                        break

                s.placeToken(pos, s.board, aColor)

            #No more valid moves => Game Over
            if len(s.getValidMoves(s.board, pColor)) == 0 and len(s.getValidMoves(s.board, aColor)) == 0:
                break
            #Next Turn
            else:
                s.turn += 1
                s.turn %= 2




game = Othello()
game.play()