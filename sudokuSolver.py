# Sudoku solver
import time

myBoard = [
    [7,8,0,4,0,0,1,2,0],
    [6,0,0,0,7,5,0,0,9],
    [0,0,0,6,0,1,0,7,8],
    [0,0,7,0,4,0,2,6,0],
    [0,0,1,0,5,0,9,3,0],
    [9,0,4,0,6,0,0,0,5],
    [0,7,0,3,0,0,0,1,2],
    [1,2,0,0,0,7,4,0,0],
    [0,4,9,2,0,6,0,0,7]
]

def printBoard(board):
    for i in range(9):
        if i%3==0:
            print("___________________")
        for j in range(9):
            if j%3==0:
                print("|",end="")#,
            else:
                print(' ',end="")#,
            if j==8:
                print(board[i][j])
            else:
                print(board[i][j],end="")#,
    print("___________________")


def solve(board):
    nextPos = nextEmpty(board)
    if nextPos==0: #finished
        print("Finished:")
        printBoard(board)
        return(1)
    for number in range(1,10): # try values
        # check if valid with number
        valid = isValid(board,number,nextPos)
        if valid:
            board[nextPos[0]][nextPos[1]] = number
            if solve(board):
                return(1)
        board[nextPos[0]][nextPos[1]] = 0
    return(0)

def nextEmpty(bo):
    for i in range(9):
        for j in range(9):
            if bo[i][j] == 0:
                return([i,j])
    return(0)

def isValid(bo,num,pos):
    """"Checks validity of board with new number num in position pos"""
    # check row:
    for c in range(9):
        if bo[pos[0]][c]==num and c!=pos[1]: # invalid
            return(0)
    #check column:
    for r in range(9):
        if bo[r][pos[1]]==num and r!=pos[0]: # invalid
            return(0)
    # check box:
    iBox = pos[0]//3  #integer division
    jBox = pos[1]//3
    for i in range(iBox*3,iBox*3+3):
        for j in range(jBox*3,jBox*3+3):
            if bo[i][j]==num and [i,j]!=pos:
                return(0)
    return(1)


print(printBoard(myBoard))
solve(myBoard)
print("--------------------------")
