import random
import copy
import math
import cProfile

# Piece Values
# 0 = Empty
# 1 = Red
# 2 = Black
# 3 = KingRed
# 4 = KingBlack

# Player Values
# 0 = Red
# 1 = Black
Player = {"RED":0, "BLACK": 1}

# Direction Values
# 0 = Backward
# 1 = Forward
Direction = {"BACK":0, "FORWARD": 1}

# Diagonal Values
# 0 = Left to Right
# 1 = Right to Left

TurnsPlayed = 0
MAX_TURNS = 40
Board = [[0 for x in xrange(8)] for x in xrange(8)]
Move = []
BoardList = []
MoveList = []
jumped = False
jumpStack = []
jumpBoard = []

def isKingPiece(a, b, player):
    if Board[b][a] == 3+player:
        return True
    return False    

def isPlayerPiece(a, b, player):
    if Board[b][a] == 1+player or Board[b][a] == 3+player:
        return True
    return False

def isOpponentPlayerPiece(a, b, player):
    if Board[b][a] == 2-player or Board[b][a] == 4-player:
        return True
    return False

def isOutOfBounds(a, b):
    squareLen = len(Board)
    if a > squareLen-1 or b > squareLen-1 or a < 0 or b < 0:
        return True
    return False


def printMatrix(matrix):
    print ' ',
    for i in range(len(matrix[1])): 
        print i+1, " ",
    print
    for i, a in enumerate(matrix):
        print "\n", i+1,
        for j, b in enumerate(a):
            print ' '.join(str(b)+" "),
        print

def InitCheckerLayout():

    for a in xrange(0,8):
        for b in xrange(0, 8):
            if (a+b)%2 != 0:
                if b < 3:
                    Board[b][a] = 1
                elif b > 4:
                    Board[b][a] = 2

                    
def InitializeGame():
    global Board

    # Scenario 1    
    # Board[2][1]=1
    # Board[2][5]=1
    # Board[6][3]=1
    # Board[3][2]=2
    # Board[5][2]=2
    # Board[7][0]=2

    # Scenario 2
    # Board[3][2]=1
    # Board[2][5]=1
    # Board[4][3]=2
    # Board[6][3]=2

    #Scenario 3
    # Board[3][2] = 1
    # Board[2][5] = 1
    # Board[3][6] = 1
    # Board[4][3] = 2
    # Board[6][3] = 2
    # Board[4][7] = 2

    # Scenario 4
    # Board[7][2]=3
    # Board[1][4]=1
    # Board[1][6]=1
    # Board[6][1]=2
    # Board[4][3]=2
    # Board[0][7]=4

def SimulateGame():
   
    InitializeGame()
    Turns = 0

    printMatrix(Board)

    while Turns <=  MAX_TURNS:
       print "\nTurn #", Turns+1

       if not PlayTurn(Player["RED"]) or not PlayTurn(Player["BLACK"]):
           print "[Game Over]"
           break
           
       Turns += 1

       if Turns == 2:
           break

def PlayTurn(player):
    global BoardList, MoveList, Board, Move

    BoardList = []
    MoveList = []
    #FindSuccessors(player)
    canPlay = True

    Move = FindBestMove(player)
    if not Move
        canPlay = False
    # if not len(MoveList):
    #     canPlay = False
    # else:
    #     i = int(math.ceil((len(BoardList)-1)*random.random()))
    #     Board = BoardList[i]
    #     Move = MoveList [i]

    if player == Player["RED"]:
        print "\nRED's Turn: "
    else:
        print "\nBLACK's Turn: "
    
    if canPlay:
        printMatrix(Board)
        print "MOVE: ", Move
    else:
        print "[Can't Move]"
        if player == Player["RED"]:
            print "\nBLACK Wins!"
        else:
            print "\nRED Wins!"

    return canPlay

def FindSuccessors(player):
    global jumped

    jumped = False
    for a in xrange(8):
        for b in xrange(8):
            if(a+b)%2 != 0 and isPlayerPiece(a, b, player):
                    moves = FindMoves(Board, a, b, a, b, 0, player)
                    #print "MOVE SEQUENCE: ", moves

def JumpNode(a, b, aa, bb):
    aDiff = (aa-a)/abs(aa-a)
    bDiff = (bb-b)/abs(bb-b)

    return [aa+aDiff, bb+bDiff]

def CheckPromotion(B, a, b, player):
    if b == 7*(1-player) and B[b][a] == 1+player:
        B[b][a] = 3+player

def FindBestMove(player):
    global Board
    FindSuccessors(player)

    if len(MoveList) == 0:
        return False

    value = MaxValue(Board, player, 0)

    for i in xrange(len(MoveList)):
        if value == MinValue(BoardList[i], (player+1)%2, 1)
            Board = BoardList[i]
            Move = MoveList[i]
    
def MaxValue(B, player, depth):
    FindSuccessors(player)

    if ReachedTerminalState(B, player, depth):
        value = EvalState(B, player)
    else:
        value = -9999
        for i in xrange(len(MoveList)):
            value = max(value, MinValue(BoardList[i], (player+1)%2,  depth+1)


def FindMoves(B, a, b, aa, bb, moves, player):

    global BoardList, MoveList
    global jumped, jumpStack, jumpBoard

    # Terminal Conditions

    if isOutOfBounds(aa,bb):
        #print "[",a,",",b,"]->[",aa,",",bb,"] : ", "Out of Bounds"
        return
    
    elif (B[bb][aa] == 0): # Empty
        if moves == 1:
            #print "[",a,",",b,"]->[",aa,",",bb,"] : ", "Simple Move Complete"
            BT = copy.deepcopy(B)
            BT[bb][aa] = B[b][a]
            BT[b][a] = 0
            CheckPromotion(BT, aa, bb, player)
            if not jumped:
                MoveList.append([aa,bb])
                BoardList.append(BT)
                return [aa, bb] #Simple Move Complete
            else: 
                return
        
        elif moves%2 == 0 and (a != aa and b != bb):
            jn = JumpNode(aa, bb, a, b);
            if moves == 2:
                jumpBoard = copy.deepcopy(B)
                jumpStack = []
            jumpBoard[b][a] = 0
            jumpBoard[bb][aa] = B[jn[1]][jn[0]]
            jumpBoard[jn[1]][jn[0]] = 0
            CheckPromotion(jumpBoard, aa, bb, player)
            jumpStack.append([aa,bb])

            if not jumped:
                BoardList[:] = []
                MoveList[:] = []
                jumped = True

            #print "Board[",aa,"][",bb,"]: ", jumpBoard[bb][aa]
            #print "[",a,",",b,"]->[",aa,",",bb,"] : ", "Jump Move Complete"
            FindMoves(jumpBoard, aa, bb, aa, bb, moves, player)

            if moves == 2:
                BoardList.append(jumpBoard)
                MoveList.append(jumpStack)
            return jumpStack
        else:
            #print "[",a,",",b,"]->[",aa,",",bb,"] : ", "Invalid Empty"
            return #Cant move any further
        
    elif (a != aa and b != bb) and isPlayerPiece(aa, bb, player):
        #print "[",a,",",b,"]->[",aa,",",bb,"] : ", "Invalid: Same Player Piece"
        return #Cant move any further
    
    elif isOpponentPlayerPiece(aa, bb, player) and moves%2 != 0:
        #Try to Jump
        #print "[",a,",",b,"]->[",aa,",",bb,"] : ", "Trying to Jump"
        jn = JumpNode(a, b, aa, bb)
        return FindMoves(B, aa, bb, jn[0], jn[1], moves+1, player)
        

    if isKingPiece(aa, bb, player):
        #print "King Piece ===> "
        return [ FindMoves(B, aa, bb, aa-1, b-1, moves+1, player) ] + \
               [ FindMoves(B, aa, bb, aa+1, b-1, moves+1, player) ] + \
               [ FindMoves(B, aa, bb, aa-1, b+1, moves+1, player) ] + \
               [ FindMoves(B, aa, bb, aa+1, b+1, moves+1, player) ] 
        
    elif player == Player["RED"]:
        #print "Red Piece ===> "
        return [ FindMoves(B, aa, bb, aa-1, b+1, moves+1, player) ] + \
               [ FindMoves(B, aa, bb, aa+1, b+1, moves+1, player) ] 
        
    else:
        #print "Black Piece ===> "
        return [ FindMoves(B, aa, bb, aa-1, b-1, moves+1, player) ] + \
               [ FindMoves(B, aa, bb, aa+1, b-1, moves+1, player) ]


#cProfile.run('SimulateGame()')

##printMatrix(Board)
##
##print "\n"
##
##for i in xrange(len(BoardList)):
##    print "State [",i+1,"] => "
##    printMatrix(BoardList[i])
##    print "MOVES: ",MoveList[i]
##    print "\n"
#InitializeGame()
#printMatrix(Board)
#FindSuccessors(Player["RED"])
SimulateGame()