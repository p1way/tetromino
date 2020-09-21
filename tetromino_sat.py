from satispy import Variable, Cnf
from satispy.solver import Minisat
from functools import reduce
from itertools import combinations
import sys, time

def usage():
    print("""Usage: python tetromino_sat.py nrow ncol types
    Hint: nrow and ncol should be the number of row and column of the table to fill with tetromino and types should be the list of the types identifiers of the tetromino pieces of the problem, separated by a comma.
    Types identifier :
OOOO --> 1
---
OO   --> 2
OO
---
O
O    --> 3
OO
---
 O
 O   --> 4
OO
---
 OO  --> 5
OO
---
OO   --> 6
 OO
---
 O   --> 7
OOO

    Example 1 : python tetromino_sat.py 4 4 1,2,3,4
    Solution :
1111
3224
3224
3344

    Example 2 (waken the 2nd messenger in the Talos Principle game) : tetromino_sat.py 6 8 1,7,7,2,2,5,6,6,6,4,4,4
11114455
22224556
22224666
44646667
46646777
46447777
""")
    exit(1)

def exactly_one(literals):
    clauses = reduce(lambda x, y: x | y, literals) # at least one
    for comb in combinations(literals, 2): # no more than one
        clauses &= - comb[0] | - comb[1]
    return clauses
    
    
def orientation(lits,i1,j1,i2,j2,i3,j3,k):
    for index in [i1,j1,i2,j2,i3,j3]:
        if index < 0 :
            return Cnf()
    try :
        return (lits[i1][j1][k][1] & lits[i2][j2][k][2] & lits[i3][j3][k][3])
    except IndexError:
        return Cnf()

def solve(nrow, ncol, pieces):
    t0 = time.time()
    npieces = len(pieces)
    formula = Cnf()

    # create literals
    lits = []
    for i in range(nrow):
        row = []
        for j in range(ncol):
            col = []
            for k in range(npieces):
                piece = []
                for l in range(4):
                    piece.append(Variable("x_{0}_{1}_{2}_{3}".format(i,j,k,l)))
                col.append(piece)
            row.append(col)
        lits.append(row)
    t1 = time.time()
    print("Time spent to create the literals:",t1-t0)

    # construct formula

    # constraints set 1 : exactly one square by case
    for i in range(nrow):
        for j in range(ncol):
            squares = []
            for piece in lits[i][j] :
                for square in piece :
                    squares.append(square)
            formula &= exactly_one(squares)
    t2 = time.time()
    print("Time spent to build the first constraint set",t2-t1)

    # constraints set 2 : exactly one case by square
    for k in range(len(pieces)):
        for l in range(4):
            cases = []
            for row in lits :
                for col in row :
                    cases.append(col[k][l])
            formula &= exactly_one(cases)
    t3 = time.time()
    print("Time spent to build the second constraint set",t3-t2)
            
    # constraints set 3 : pieces shapes
    for i in range(nrow):
        for j in range(ncol):
            for k in range(npieces) :
                if pieces[k] == 1 : # bar
                    orientation1 = orientation(lits,i,j+1,i,j+2,i,j+3,k)
                    orientation2 = orientation(lits,i+1,j,i+2,j,i+3,j,k)
                    clause = lits[i][j][k][0] >> (orientation1 | orientation2)
                elif pieces[k] == 2 : # 2*2 square
                    orientation1 = orientation(lits,i,j+1,i+1,j,i+1,j+1,k)
                    clause = lits[i][j][k][0] >> orientation1
                elif pieces[k] == 3 : # L
                    orientation1 = orientation(lits,i+1,j,i+2,j,i+2,j+1,k)
                    orientation2 = orientation(lits,i,j+1,i,j+2,i-1,j+2,k)
                    orientation3 = orientation(lits,i-1,j,i-2,j,i-2,j-1,k)
                    orientation4 = orientation(lits,i,j-1,i,j-2,i+1,j-2,k)
                    clause = lits[i][j][k][0] >> (orientation1 | orientation2 | orientation3 | orientation4)
                elif pieces[k] == 4 : # reversed L
                    orientation1 = orientation(lits,i+1,j,i+2,j,i+2,j-1,k)
                    orientation2 = orientation(lits,i,j+1,i,j+2,i+1,j+2,k)
                    orientation3 = orientation(lits,i-1,j,i-2,j,i-2,j+1,k)
                    orientation4 = orientation(lits,i,j-1,i,j-2,i-1,j-2,k)
                    clause = lits[i][j][k][0] >> (orientation1 | orientation2 | orientation3 | orientation4)
                elif pieces[k] == 5 : # snake
                    orientation1 = orientation(lits,i,j+1,i-1,j+1,i-1,j+2,k)
                    orientation2 = orientation(lits,i+1,j,i+1,j+1,i+2,j+1,k)
                    clause = lits[i][j][k][0] >> (orientation1 | orientation2)
                elif pieces[k] == 6 : # reversed snake
                    orientation1 = orientation(lits,i,j+1,i+1,j+1,i+1,j+2,k)
                    orientation2 = orientation(lits,i+1,j,i+1,j-1,i+2,j-1,k)
                    clause = lits[i][j][k][0] >> (orientation1 | orientation2)
                elif pieces[k] == 7 : # castle
                    orientation1 = orientation(lits, i+1, j-1, i+1, j,   i+1, j+1, k)
                    orientation2 = orientation(lits, i-1, j-1, i,   j-1, i+1, j-1, k)
                    orientation3 = orientation(lits, i-1, j-1, i-1, j,   i-1, j+1, k)
                    orientation4 = orientation(lits, i-1, j+1, i,   j+1, i+1, j+1, k)
                    clause = lits[i][j][k][0] >> (orientation1 | orientation2 | orientation3 | orientation4)
                formula &= clause
    t2 = time.time()
    print("Time spent to build the third constraint set",t2-t1)

    # solve using minisat
    solver = Minisat()
    t3 = time.time()
    print("Time spent to solve the SAT problem",t3-t2)
    print("Total time", t3-t0)
    return solver.solve(formula), lits

def print_solution(sol, lits, nrow, ncol, pieces):
    for i in range(nrow):
        row = []
        for j in range(ncol):
            for k in range(len(pieces)) :
                for l in range(4):
                    if sol[lits[i][j][k][l]] :
                        row.append(pieces[k])
        print(''.join(list(map(str,row))))
    
if __name__ == '__main__':
    # sanity checks
    if len(sys.argv) != 4:
        usage()
    nrow = int(sys.argv[1])
    ncol = int(sys.argv[2])
    pieces = list(map(int,sys.argv[3].split(',')))
    if nrow*ncol != 4*len(pieces) or reduce(lambda x, y : x and (y < 1 or (y > 7)), pieces):
        print("the problem is not well-formed !")
        usage()

    # solving using minisat
    solution, lits = solve(nrow, ncol, pieces)
    if solution.success:
        print("Found a solution!")
        # print the solution
        print_solution(solution, lits, nrow, ncol, pieces)
    else :
        print("The expression cannot be satisfied.")

# tile encoding of pieces
#
# 1234 --> bar
# ---
# 12   --> 2*2 square
# 34
# ---
# 1
# 2    --> L
# 34
# ---
#  1
#  2   --> reversed L
# 43
# ---
#  34  --> snake (looking at the right)
# 12
# ---
# 12   --> reversed snake  (looking at the left)
#  34
# ---
#  1   --> castle
# 234
