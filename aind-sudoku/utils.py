from constants import *

# This list holds the board values used in visualization.
assignments = []

def cross(A, B):
    """ Cross product of elements in A and elements in B. """
    return [a + b for a in A for b in B]

# The following structures are used to represent the puzzle, the individual units, and the boxes belonging to the same unit.
boxes = cross(ROWS, COLUMNS)
units_rows = [cross(r, COLUMNS) for r in ROWS]
units_columns = [cross(ROWS, c) for c in COLUMNS]
units_diagonal = [boxes[0::10], boxes[8::8][:-1]]
units_square = [cross(r, c) for r in ROWS_SQUARE for c in COLUMNS_SQUARE]
units_all = units_rows + units_columns + units_diagonal + units_square
units = dict((k, [v for v in units_all if k in v]) for k in boxes)
peers = dict((k, set(sum(units[k], [])) - set([k])) for k in boxes)

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1 + max(len(values[s]) for s in boxes)
    boundary_line = line = '='.join(['=' * (width * 3)] * 3)
    line = '+'.join(['-' * (width * 3)] * 3)
    print(boundary_line)
    for r in ROWS:
        print(''.join(values[r + c].center(width) + ('|' if c in '36' else '') for c in COLUMNS))
        if r in 'CF': print(line)
    print(boundary_line)

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        # Update the assignments when we assign a single value to a box.
        assignments.append(values.copy())
    return values

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    grid_length = len(grid)

    # Sanity check: ensure that we are working with a 9x9 grid.
    assert grid_length == 81, "The grid should be a 9x9 square."

    # Return the grid in dictionary form, replacing the empties with all digits.
    return { boxes[i]:(ALL_DIGITS if (grid[i] is EMPTY) else grid[i]) for i in range(0, grid_length) }