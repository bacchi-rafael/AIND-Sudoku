assignments = []

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [s+t for s in A for t in B]



def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    for unit in unitlist:
        vals = [values[box] for box in unit if len(values[box]) == 2]
        if len(vals):
            dupes = [x for n, x in enumerate(vals) if x in vals[:n]]
            if len(dupes):
                for box in unit:
                    if (len(values[box]) > 1) and (values[box] not in dupes):
                        for dp in dupes:
                            for d in dp:
                                assign_value(values, box, values[box].replace(d, ''))
    return values

    # Find all instances of naked twins
    # Eliminate the naked twins as possibilities for their peers

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
    g = ["123456789" if l == '.' else l for l in grid]
    return dict(l for l in zip(boxes, g))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    """
    Go through all the boxes, and whenever there is a box with a value, eliminate this value from the values of all its peers.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for box in values:
        if len(values[box]) == 1:
            for peer in peers[box]:
                val = values[peer].replace(values[box], '')
                assign_value(values, peer, val)
    return values

def only_choice(values):
    """
    Go through all the units, and whenever there is a unit with a value that only fits in one box, assign the value to this box.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    for unit in unitlist:
        for digit in '123456789':
            dplaces = [box for box in unit if digit in values[box]]
            if len(dplaces) == 1:
                assign_value(values, dplaces[0], digit)
    return values

def reduce_puzzle(values):
    """
    Iterate eliminate(), only_choice() and naked_twins(). If at some point,
    there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.
    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Run the 3 methods defined to reduce the possibilities using constraints
        values = eliminate(values)
        values = only_choice(values)
        values = naked_twins(values)

        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def is_solved(values):
    """
      Check if all the boxes in the sudoku have only 1 character
      Input: A sudoku in dictionary form.
      Output: True if all boxes have just 1 character, False otherwise
    """
    # Return True if all values in the grid are 1 char long
    return len([box for box in values.keys() if len(values[box]) == 1]) == len(values)

def search(values):
    """
      Implements AI Search functionality that will try to solve the sudoku by
      reducing it using constraint propagation but if it's not enough it will attempt
      to use different values in boxes recursively to find a solution
      Input: A sudoku in dictionary form.
      Output: The resulting sudoku in dictionary form, or False in case the current attempt does not solve the sudoku.
    """
    grid = reduce_puzzle(values)
    if !grid:
        return False
    elif is_solved(grid):
        return grid
    else:
        guesses = 10
        for idx in grid.keys():
            box_opts = len(grid[idx])
            if (box_opts > 1) and (box_opts < guesses):
                guesses, box = len(grid[idx]), idx

        for val in grid[box]:
            new_grid = dict(grid)
            assign_value(new_grid, box, val)
            res = search(new_grid)
            if res:
                return res

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    return search(grid_values(grid))

rows = 'ABCDEFGHI'
cols = '123456789'

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]

# Diagonal sudoku
# Created 2 diagonal units as additional constraints
diagonal_units = [[a+b for a,b in zip(rows, cols)], [a+b for a,b in zip(rows, cols[::-1])]]

# Added diagonal_units as a new constraint
# Tso it can be used by all methods (eliminate, only_choice and naked_twins)
# to reduce the possibilities
unitlist = row_units + column_units + square_units + diagonal_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
