"""
Constants used by the project are listed here.
"""

# Empty boxes are represented using this symbol.
EMPTY = '.'

# This represents all digits used in the puzzle.
ALL_DIGITS = '123456789'

# Row representation and row grouping by square units.
ROWS = 'ABCDEFGHI'
ROWS_SQUARE = ['ABC', 'DEF', 'GHI']

# Column representation and column grouping by square units.
COLUMNS = '123456789'
COLUMNS_SQUARE = ['123', '456', '789']

# This list holds the board values used in visualization.
assignments = []

# This holds the naked twin pairs that have been processed.
processed_naked_twins = []

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

def eliminate(values):
    """Eliminate values using the elimination strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the solved boxes/values eliminated from peers.
    """

    # Iterate through the list of all solved boxes, i.e., boxes that have a single digit.
    for unit in units_all:
        for solved_box in [solved_box for solved_box in unit if len(values[solved_box]) == 1]:
            # Eliminate the solved value from the other boxes in the same unit.
            for unsolved_box in [box for box in unit if box is not solved_box and values[solved_box] in values[box]]:
                values = assign_value(values, unsolved_box, values[unsolved_box].replace(values[solved_box], ''))
    return values

def only_choice(values):
    """Eliminate values using the only choice strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the only digit choice set for specific boxes.
    """

    for unit in units_all:
        for digit in ALL_DIGITS:
            # Find the list of boxes in a unit that can take on a specific value.
            box_choices = [box for box in unit if digit in values[box]]
            # If there is only one box that can take on this specific value,
            if len(box_choices) == 1:
                # then, assign this specific value to that box.
                values = assign_value(values, box_choices[0], digit)
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    global processed_naked_twins

    for unit in units_all:
        # Find all boxes with two-digit possibilities in a unit.
        for value in set([values[box] for box in unit if len(values[box]) == 2]):
            # If there are exactly two boxes that have the same two-digit possibilities (naked twins),
            naked_twins_candidate = set([box for box in unit if values[box] == value])
            if len(naked_twins_candidate) == 2 and naked_twins_candidate not in processed_naked_twins:
                # then, we have found a pair of naked twins in a unit.
                processed_naked_twins.append(naked_twins_candidate)
                # Eliminate the naked twins as possibilities for their common peers.
                digits_to_eliminate = set(value)
                for affected_peer in set.intersection(*[peers[naked_twin] for naked_twin in naked_twins_candidate]):
                    # Eliminate the naked twin digit pair from the possible values for each common peer.
                    if len(values[affected_peer]) > 1:
                        affected_peer_new_value = ''.join(sorted([digit for digit in set(values[affected_peer]) - digits_to_eliminate]))
                        values = assign_value(values, affected_peer, affected_peer_new_value)
    return values

def single_possibility(values):
    """Eliminate values using the single possibility strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the single possible value set for units with eight solved boxes.
    """

    # Iterate through the list of all units, checking to see if there is only one unsolved box in that unit.
    for unit in units_all:
        unsolved_boxes = [box for box in unit if len(values[box]) > 1]
        if len(unsolved_boxes) == 1:
            # There is only one unsolved box in this unit.
            # Set the value of this box to the only remaining value.
            value = set(ALL_DIGITS) - set([values[box] for box in unit if box is not unsolved_boxes[0]])
            values = assign_value(values, unsolved_boxes[0], list(value)[0])
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Initial state - check how many boxes have a determined value.
        solved_values_before = len([box for box in boxes if len(values[box]) == 1])

        # Run predefined strategies to reduce the puzzle.
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)
        values = single_possibility(values)

        # Check how many boxes have a determined value, to compare with the initial state.
        solved_values_after = len([box for box in boxes if len(values[box]) == 1])

        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after

        # Sanity check: return False if there is a box with zero available values:
        if len([box for box in boxes if len(values[box]) == 0]):
            return False

    return values

def search(values):
    """Using depth-first search and propagation, create a search tree and solve the sudoku."""

    # First, reduce the puzzle using the previous function.
    values = reduce_puzzle(values)

    if values == False:
        # We have box with zero possible values.
        return False

    if all(len(values[box]) == 1 for box in boxes):
        # The puzzle has been completely solved.
        return values

    # Choose one of the unfilled squares with the fewest possibilities.
    n, chosen_box = min((len(values[chosen_box]), chosen_box) for chosen_box in boxes if len(values[chosen_box]) > 1)

    # Iterate through the possibilities to find a viable solution.
    for digit in values[chosen_box]:
        # Check that no other peer has been assigned this value

        # Make a copy of the puzzle, set the value of the chosen box to one of the possible values, and search for a solution.
        candidate_solution = values.copy()
        candidate_solution = assign_value(candidate_solution, chosen_box, digit)
        candidate_solution = search(candidate_solution)
        if candidate_solution:
            return candidate_solution

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    # Convert the grid to a dictionary and search for a solution.
    return search(grid_values(grid))

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

    global assignments

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

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    solution = solve(diag_sudoku_grid)
    display(solution)

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
