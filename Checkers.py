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
tBoardList = []
MoveList = []
tMoveList = []
jumped = False
jumpStack = []
jumpBoard = []

def isKingPiece(B, a, b, player):
    if B[b][a] == 3+player:
        return True
    return False    

def isPlayerPiece(B, a, b, player):
    if B[b][a] == 1+player or B[b][a] == 3+player:
        return True
    return False

def isOpponentPlayerPiece(B, a, b, player):
    if B[b][a] == 2-player or B[b][a] == 4-player:
        return True
    return False

def isOutOfBounds(B, a, b):
    squareLen = len(B)
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
    global Board

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
    Board[7][2]=3
    Board[1][4]=1
    Board[1][6]=1
    Board[6][1]=2
    Board[4][3]=2
    Board[0][7]=4

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
    if not Move:
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

def FindSuccessors(B, player):
    global jumped

    tBoardList[:] = []
    tMoveList[:] = []
    printMatrix(B)
    jumped = False
    for a in xrange(8):
        for b in xrange(8):
            if(a+b)%2 != 0 and isPlayerPiece(B, a, b, player):
                    moves = FindMoves(B, a, b, a, b, 0, player)
                    print "MOVE SEQUENCE: ", moves

def JumpNode(a, b, aa, bb):
    aDiff = (aa-a)/abs(aa-a)
    bDiff = (bb-b)/abs(bb-b)

    return [aa+aDiff, bb+bDiff]

def CheckPromotion(B, a, b, player):
    if b == 7*(1-player) and B[b][a] == 1+player:
        B[b][a] = 3+player

def FindBestMove(player):
    global Board
    #FindSuccessors(player)

    print "Finding best Move for player:", player
    raw_input()
    [maxValue, maxIndex] = MaxValue(Board, player, 0)
    print "MaxValue: ", maxValue
    print "MaxIndex: ", maxIndex

    Board = BoardList[maxIndex]
    return MoveList[maxIndex]


    
def MaxValue(B, player, depth):
    print "Finding Max Value at Depth", depth, " for Player: ", player
    FindSuccessors(B, player)
    print "Found ", len(tBoardList), " Moves: ", tMoveList
    if depth == 0:
        BoardList[:] = tBoardList
        MoveList[:] = tMoveList
        
    dBoardList = copy.deepcopy(tBoardList)
    dMoveList  = copy.deepcopy(tMoveList)

    maxValue = -9999
    maxIndex = -1

    if ReachedTerminalState(B, player, depth) or (len(dMoveList) == 0):
        maxValue = EvalState(B, player)
        print "Terminal at Max Node at Depth", depth, " for player ", player, " Value: ", maxValue
    else:
        
        for i in xrange(len(dMoveList)):
            [value, t] = MinValue(dBoardList[i], (player+1)%2,  depth+1)
            if value > maxValue:
                maxValue = value
                maxIndex = i

    return [maxValue, maxIndex]



def MinValue(B, player, depth):
    print "Finding Min Value at Depth", depth, " for Player: ", player
    FindSuccessors(B, player)
    print "Found ", len(tBoardList), " Moves"

    dBoardList = copy.deepcopy(tBoardList)
    dMoveList  = copy.deepcopy(tMoveList)

    minValue = 9999
    minIndex = -1

    if ReachedTerminalState(B, player, depth) or (len(dMoveList) == 0):
        #print "Reached Terminal at Min Node"
        minValue = EvalState(B, player)
        print "Terminal at Max Node at Depth", depth, " for player ", player, " Value: ", minValue
    else:
        for i in xrange(len(dBoardList)):
            [value, t] = MaxValue(dBoardList[i], (player+1)%2, depth+1)
            if value < minValue:
                minValue = value
                minIndex = i

    return [minValue, minIndex]


def ReachedTerminalState(B, player, depth):
    max_depth = 3

    if(depth > max_depth and depth%2 == 0):
        return True
    return False

def EvalState(B, player):
    printMatrix(B)
    value = 0
    for a in xrange(8):
        for b in xrange(8):
            if (a+b)%2 != 0:
                if B[b][a] == 1+player or B[b][a] == 3+player:
                    value += 1
                elif B[b][a] == 2-player or B[b][a] == 4-player:
                    value -= 1

    #print "Returned Value ", value
    return value
    
def FindMoves(B, a, b, aa, bb, moves, player):

    global BoardList, MoveList
    global jumped, jumpStack, jumpBoard

    # Terminal Conditions

    if isOutOfBounds(B,aa,bb):
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
                tMoveList.append([aa,bb])
                tBoardList.append(BT)
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
                tBoardList[:] = []
                tMoveList[:] = []
                jumped = True

            #print "Board[",aa,"][",bb,"]: ", jumpBoard[bb][aa]
            #print "[",a,",",b,"]->[",aa,",",bb,"] : ", "Jump Move Complete"
            FindMoves(jumpBoard, aa, bb, aa, bb, moves, player)

            if moves == 2:
                tBoardList.append(jumpBoard)
                tMoveList.append(jumpStack)
            return jumpStack
        else:
            #printMatrix(B)
            #print "[",a,",",b,"]->[",aa,",",bb,"] : ", "Invalid Empty"
            return #Cant move any further
        
    elif (a != aa and b != bb) and isPlayerPiece(B, aa, bb, player):
        #print "[",a,",",b,"]->[",aa,",",bb,"] : ", "Invalid: Same Player Piece"
        return #Cant move any further
    
    elif isOpponentPlayerPiece(B, aa, bb, player) and moves%2 != 0:
        #Try to Jump
        #print "[",a,",",b,"]->[",aa,",",bb,"] : ", "Trying to Jump"
        jn = JumpNode(a, b, aa, bb)
        return FindMoves(B, aa, bb, jn[0], jn[1], moves+1, player)
        

    if isKingPiece(B, aa, bb, player):
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
