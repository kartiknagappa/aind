from random import randrange, shuffle
from operator import add

board_squares_per_side = 7
board_size = board_squares_per_side**2
token = 'O'
square_unused = ' '
square_used = 'X'
display_count = 0
invalid_index = -1
first_move = True
game_step = 0

# relative L positions
relative_positions = [
  -13, # [-2, 1]
   -5, # [-1, 2]
    9, # [ 1, 2]
   15, # [ 2, 1]
   13, # [ 2,-1]
    5, # [ 1,-2]
   -9, # [-1,-2]
  -15  # [-2,-1]
]

number_of_relative_positions = len(relative_positions)
position_order = list(range(number_of_relative_positions))

def indexToRowColumn(index):
  if index == invalid_index:
    return [invalid_index, invalid_index]

  row = index // board_squares_per_side
  column = index % board_squares_per_side

  return [row, column]

def rowColumnToIndex(row, column):
  return row * board_squares_per_side + column

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

  print("\n({0:d}) ({1}->{2}): {3} -> {4}\n".format(game_step, previous_position, current_position, previous, current), end='')
  print("\n   0 1 2 3 4 5 6", end='')
  print("\n  ---------------", end='')
  for r in range(board_squares_per_side):
    print("\n{:d} |".format(r), end='')
    for c in range(board_squares_per_side):
      square = board[r * board_squares_per_side + c]
      print("{:s}|".format(square), end='')
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