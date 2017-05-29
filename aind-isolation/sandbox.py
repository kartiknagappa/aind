from math import floor, log
from operator import add
from random import randrange, shuffle

# board properties
board_rows = 7
board_columns = 7
board_size = board_rows * board_columns

# game properties
invalid_index = -1
first_move = True
game_step = 0

# relative L positions
relative_positions = [
  -2*board_columns + 1, # [-2, 1]
  -1*board_columns + 2, # [-1, 2]
   1*board_columns + 2, # [ 1, 2]
   2*board_columns + 1, # [ 2, 1]
   2*board_columns - 1, # [ 2,-1]
   1*board_columns - 2, # [ 1,-2]
  -1*board_columns - 2, # [-1,-2]
  -2*board_columns - 1  # [-2,-1]
]

# display format
box_row_width=int(floor(log(board_rows-1,10)))+1
box_column_width=int(floor(log(board_columns-1,10)))+1
token = 'O'
square_unused = ' '
square_used = 'X'

# display lines: these lines contain the column numbers and the separator
line_0 = " "*box_row_width + " " + "".join("{:{width}}".format(i, width=box_column_width+1) for i in range(board_columns))
line_1 = " "*(box_row_width+1) + "-" + "-"*(box_column_width+1)*board_columns

number_of_relative_positions = len(relative_positions)
position_order = list(range(number_of_relative_positions))

def indexToRowColumn(index):
  if index == invalid_index:
    return [invalid_index, invalid_index]

  row = index // board_columns
  column = index % board_columns

  return [row, column]

def rowColumnToIndex(row, column):
  return row * board_columns + column

def isValidIndex(index):
  return 0 <= index < board_size

def isLegalMove(target_square_state, current_position, new_position):
  if target_square_state is square_unused:
    if first_move:
      return True

    if isValidIndex(current_position) and \
      isValidIndex(new_position):
      currentRowColumn = indexToRowColumn(current_position)
      newRowColumn = indexToRowColumn(new_position)
      distance_between_rows = abs(currentRowColumn[0] - newRowColumn[0])
      distance_between_columns = abs(currentRowColumn[1] - newRowColumn[1])
      return (distance_between_rows == 1 and distance_between_columns == 2) or (distance_between_rows == 2 and distance_between_columns == 1)

  return False

def getStartingPosition(start=invalid_index):
  if start == invalid_index:
    return randrange(board_size)
  else:
    return start

def formatPosition(position):
  row, column = indexToRowColumn(position)
  return "[{0:2},{1:2}]".format(row, column)

def displayBoard(board, previous_position=invalid_index, current_position=invalid_index):
  previous = formatPosition(previous_position)
  current = formatPosition(current_position)

  print("\n({0}) ({1}->{2}): {3} -> {4}\n".format(game_step, previous_position, current_position, previous, current), end='')
  print(line_0)
  print(line_1)
  for r in range(board_rows):
    line_r = "{:{width}}".format(r, width=box_row_width) + " |" + "".join("{:{width}}|".format(board[r * board_columns + c], width=box_column_width) for c in range(board_columns))
    print(line_r)
  print("")

def move(board, current_position, new_position):
  global first_move
  global game_step

  game_step += 1
  if first_move:
    first_move = False
  else:
    board[current_position] = square_used
  board[new_position] = token

  return new_position, board

def shuffle_position_order():
  global position_order
  shuffle(position_order)

def get_next_move(board, current_position):
  available_move = True
  new_board = board[:]

  i = 0
  shuffle_position_order()
  while available_move is True:
    if i >= number_of_relative_positions:
      available_move = False
    else:
      # find the available move
      next_position = current_position + relative_positions[position_order[i]]
      i += 1
      if isValidIndex(next_position) and \
         isLegalMove(new_board[next_position], current_position, next_position):
        available_move = next_position

  return available_move

def game():
  # initialize the board and pick a starting point
  board = [' ' for i in range(board_size)]
  current_position = invalid_index
  next_position = getStartingPosition()

  while next_position is not False:
    previous_position = current_position
    current_position, board = move(board, current_position, next_position)
    displayBoard(board, previous_position, current_position)
    next_position = get_next_move(board, current_position)

game()
print("\n*** end ***\n")