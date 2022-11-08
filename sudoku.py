#!/usr/bin/env python
#coding:utf-8
"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import heapq

ROW = "ABCDEFGHI"
COL = "123456789"


def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def backtracking(board):
    """Takes a board and returns solved board."""
    backtrackRecursion(board)
    return board

def backtrackRecursion(board):
    # Create Priority Queue of next spots
    pq = []
    for row in range (0,9):
        for col in range(0,9):
            val = board[ROW[row] + COL[col]]
            if(val == 0):
                # Add this node to the PQ
                # Find number of invalid zones
                heapq.heappush(pq, (possibilities(board,row,col),row,col) )

    # If pq is empty, we are done!
    if len(pq) == 0:
        return True

    # Get smallest value
    tup = heapq.heappop(pq)
    row = tup[1]
    col = tup[2]


    for i in range(1, 10): # numbers 1 thru 9
        # See if this number is valid to place
        if not isValid(board,row,col,i):
            continue

        # If we are here, number is valid! Try it out!
        board[ROW[row] + COL[col]] = i

        if backtrackRecursion(board):
            return True

        # Not valid, get rid of the value we just inserted
        board[ROW[row] + COL[col]] = 0

    # Nothing worked, return false
    return False

def isValid(board,r,c,nextVal):
    for i in range(0, 9): # indices 0 thru 8
        # Check if row is valid
        if board[ROW[r] + COL[i]] == nextVal:
            return False

        # Check if col is valid
        if board[ROW[i] + COL[c]] == nextVal:
            return False

        # Check if box is valid
        if board[ROW[i // 3 + 3 * (r // 3)] + COL[i % 3 + 3 * (c // 3)]] == nextVal:
            return False

    # All is valid
    return True

def possibilities(board,r,c):
    s = set()
    for i in range(0, 9): # indices 0 thru 8
        # Check if row is valid
        rowVal = board[ROW[r] + COL[i]]
        if rowVal != 0:
            s.add(rowVal)

        # Check if col is valid
        colVal = board[ROW[i] + COL[c]]
        if colVal != 0:
            s.add(colVal)

        # Check if box is valid
        boxVal = board[ROW[i // 3 + 3 * (r // 3)] + COL[i % 3 + 3 * (c // 3)]]
        if boxVal != 0:
            s.add(boxVal)

    # All is valid
    return 9-len(s)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        
        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                  for r in range(9) for c in range(9)}       
        
        solved_board = backtracking(board)
        
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(board_to_string(solved_board))
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        #numSolved = 0
        #numNotSolved = 0
        #times = []

        # Solve each board using backtracking
        for line in sudoku_list.split("\n"):

            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                      for r in range(9) for c in range(9)}

            # Print starting board. TODO: Comment this out when timing runs.
            print_board(board)

            # startTime = time.time()
            # Solve with backtracking

            solved_board = backtracking(board)

            # endTime = time.time() - startTime
            # times.append(endTime)
            # if '0' not in board_to_string(board):
            #     numSolved+=1
            # else:
            #     numNotSolved+=1

            # Print solved board. TODO: Comment this out when timing runs.
            print_board(solved_board)

            # Write board to file
            outfile.write(board_to_string(solved_board))
            outfile.write('\n')

        print("Finishing all boards in file.")
