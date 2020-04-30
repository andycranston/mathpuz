#! /usr/bin/python3
#
# @(!--#) @(#) mathpuz2.py, version 009, 30-april-2020
#
# math puzzle generator
#

######################################################################

import sys
import os
import argparse
import random
import html
import cgi
import cgitb; cgitb.enable()   # for troubleshooting

######################################################################

#
# globals
#

CSS_VERSION = '003'

README_URL = 'https://github.com/andycranston/mathpuz'

######################################################################

def advance(row, col, direction):
    if direction == 'south':
        row += 1
    else:
        col += 1

    return row, col

######################################################################

def evalargs(arg1, oper, arg2):
    if oper == '+':
        result = arg1 + arg2
    elif oper == '-':
        result = arg1 - arg2
    elif oper == '*':
        result = arg1 * arg2
    elif oper == '/':
        result = arg1 // arg2
    else:
        result = -99999

    return result

######################################################################

def dosum(puzzle, row, col, direction):
    arg1 = puzzle[row][col]

    row, col = advance(row, col, direction)

    oper = puzzle[row][col]

    row, col = advance(row, col, direction)

    arg2 = puzzle[row][col]

    return evalargs(arg1, oper, arg2)

######################################################################

def dobothsums(puzzle, row, col, direction):
    arg1 = dosum(puzzle, row, col, direction)

    for i in range(0, 3):
        row, col = advance(row, col, direction)

    oper = puzzle[row][col]

    row, col = advance(row, col, direction)

    arg2 = puzzle[row][col]

    return evalargs(arg1, oper, arg2)

######################################################################

def simpleevenlydivides(puzzle, row, col, direction):
    arg1 = puzzle[row][col]

    for i in range(0, 2):
        row, col = advance(row, col, direction)

    arg2 = puzzle[row][col]

    return (arg1 % arg2) == 0
    
######################################################################

def harderevenlydivides(puzzle, row, col, direction):
    arg1 = dosum(puzzle, row, col, direction)

    for i in range(0, 4):
        row, col = advance(row, col, direction)

    arg2 = puzzle[row][col]

    return (arg1 % arg2) == 0

######################################################################

def generatepuzzle(gamenum):
    # random.seed(gamenum)
    random.seed(gamenum)

    # set puzzle array to all zeroes
    puzzle = []
    for i in range(0,6):
        puzzle.append([0] * 6)

    # create numbers in order
    numbers = []
    for i in range(1, 10):
        numbers.append(i)

    # randomise the order of the numbers
    for i in range(0, 9):
        r1 = random.randint(0, 8)
        r2 = random.randint(0, 8)
        if r1 != r2:
            numbers[r1], numbers[r2] = numbers[r2], numbers[r1]

    # put the numbers in the puzzle array
    for i in range(0, 9):
        row = (i % 3) * 2
        col = (i // 3) * 2
        puzzle[row][col] = numbers[i]

    # select the number index to reveal
    puzzle[5][5] = random.randint(0, 8)

    # set random operands
    for col in [1, 3]:
        for row in [0, 2, 4]:
            for flip in [0, 1]:
                operand = '+-*'[random.randint(0, 2)]
                if flip == 0:
                    puzzle[row][col] = operand
                else:
                    puzzle[col][row] = operand

    # set some of the operands to / if evenly divisible
    for rowcol in [0, 2, 4]:
        for direction in ['south', 'east']:
            if direction == 'south':
                row = 0
                col = rowcol
            else:
                row = rowcol
                col = 0

            if random.randint(0, 1) == 0:
                if simpleevenlydivides(puzzle, row, col, direction):
                    temprow, tempcol = row, col
                    temprow, tempcol = advance(temprow, tempcol, direction)
                    puzzle[temprow][tempcol] = '/'
            if random.randint(0, 1) == 0:
                if harderevenlydivides(puzzle, row, col, direction):
                    temprow, tempcol = row, col
                    for i in range(0, 3):
                        temprow, tempcol = advance(temprow, tempcol, direction)
                    puzzle[temprow][tempcol] = '/'
            sum = dobothsums(puzzle, row, col, direction)
            temprow, tempcol = row, col
            for i in range(0, 5):
                temprow, tempcol = advance(temprow, tempcol, direction)
            puzzle[temprow][tempcol] = sum
                
    # set the squares that will be rendered black to -1
    for row in [1, 3]:
        for col in [1, 3]:
            puzzle[row][col] = -1

    return puzzle

######################################################################

def rowcol2index(row, col):
    if row in [0, 2, 4]:
        if col in [0, 2, 4]:
            return ((row // 2) * 3) + (col // 2)

    return -1

######################################################################

def index2rowcol(index):
    index = index % 9

    row = (index // 3) * 2
    col = (index % 3) * 2

    return row, col

######################################################################

def puzzlehtml(puzzle, xval):
    reveal = puzzle[5][5]

    print('<table>')

    for row in range(0, 5):
        print('<tr>')
        for col in range(0 ,5):
            square = puzzle[row][col]
            index = rowcol2index(row, col)
            if type(square) == str:
                print('<td class="white">{}</td>'.format(square))
            elif square == -1:
                print('<td class="black">#</td>')
            elif index == reveal:
                print('<td class="white">')
                print('{}'.format(square))
                print('<input type="hidden" name="x{}" value="{}">'.format(index, square))
                print('</td>')
            else:
                print('<td class="white">')
                print('<input class="guess" type="input" name="x{}" size="1" value="{}">'.format(index, xval[index]))
                print('</td>')
        if row in [0, 2, 4]:
            print('<td class="invis">&nbsp;</td>')
            print('<td class="white">{}</td>'.format(puzzle[row][5]))
        print('</tr>')

    print('<tr>')
    print('<td class="invis">&nbsp;</td>')
    print('</tr>')

    print('<tr>')
    for col in range(0, 5):
        if (col % 2) == 0:
            print('<td class="white">{}</td>'.format(puzzle[5][col]))
        else:
            print('<td class="invis">&nbsp</td>')

    print('</tr>')
        
    print('</table>')

    return

######################################################################

def stripnondigits(s):
    result = ''

    for c in s:
        if c.isdigit():
            result += c

    return result

######################################################################

def checkanswers(puzzle, xval):
    answers = []

    ### print(xval)

    if len(xval) != 9:
        return 'Incorrect number of answers given'

    for x in xval:
        if x == '':
            return 'One or more answers are missing'

        if not x.isdigit():
            return 'One or more answers have invalid characters'

        if (int(x) < 1) or (int(x) > 9):
            return 'Answers must be between 1 and 9 inclusive'

    for i in range(0, 9):
        row, col = index2rowcol(i)

        if int(xval[i]) != puzzle[row][col]:
            return 'One or more answers are incorrect'
        
    return 'Ok'

######################################################################

def removeending(s, e):
    if s.endswith(e):
        s = s[:-(len(e))]

    return s

######################################################################


def main():
    global progname

    basename = removeending(progname, '.py')

    form = cgi.FieldStorage()

    gamenum = stripnondigits(form.getfirst('gamenum', ''))
    generate = form.getfirst('generate', '')
    check = form.getfirst('check', '')

    xval = []

    for x in range(0, 9):
        if generate != '':
            xval.append('')
        else:
            xval.append(form.getfirst('x{}'.format(x), '').strip())

    if False:
        print('<pre>')
        print(xval)
        print('</pre>')

    if False:
        print('<pre>')
        for row in puzzle:
            for item in row:
                print('{:<4} '.format(item), end='')
            print('')
        print('</pre>')

    title = 'Maths Puzzle'

    print("Content-type: text/html")
    print("")
    print('<head>')
    print('<title>{}</title>'.format(title))
    print('<link rel="stylesheet" type="text/css" href="{}.css?version={}">'.format(basename, CSS_VERSION))
    print('</head>')
    print('<body>')
    print('<h1>{} <small class="instructions">(<a href="{}">instructions and source code</a>)</small></h1>'.format(title, README_URL))

    ### print('[{}]'.format(basename))

    print('<form method="post" action="{}">'.format(progname))

    print('Game number: <input type="text" name="gamenum" value="{}" size="4">'.format(gamenum))

    print('&nbsp;')
    print('<input type="submit" name="generate" value="Generate puzzle">')

    print('&nbsp;')
    print('<input type="submit" name="check" value="Check answers">')

    print('<br>')
    print('<br>')

    if (generate != '') or (check != ''):
        if gamenum == '':
            print('No valid game number entered')
        else:
            puzzle = generatepuzzle(gamenum)
            puzzlehtml(puzzle, xval)
            if check != '':
                result = checkanswers(puzzle, xval)
                if result == 'Ok':
                    print('<h2 class="correct">You have solved the puzzle</h2>')
                else:
                    print('<h2 class="incorrect">{}</h2>'.format(result))

    print('</form>')

    print('</body>')

    return 0

######################################################################

#
# Main
#

progname = os.path.basename(sys.argv[0])

sys.exit(main())

# end of file
