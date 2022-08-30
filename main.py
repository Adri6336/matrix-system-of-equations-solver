from sys import exit

def clean_list(target_list, target_content=' '):
    """
    This will clean a list of whatever you don't like
    :param target_list: This is the list that you want to clean
    :param target_content: This is the content that you want to remove
    :return: Cleaned list
    """
    while True:  # Loop forever until broken
        try:
            target_list.remove(target_content)
        except:  # If you can't remove the content anymore, it doesn't exist
            break  # End infinite loop


def reorder_matrix(matrix):
	"""
	This reorders a matrix if theres a zero where we need a nonzero int

	"""
	matrix_copy = matrix[:]
	mod_matrix = matrix[:]
	quit = False	
	size = len(mod_matrix)
	ct = 0

	# 1. Scan matrix to identify if a row needs to be reorganized
	while not quit:
		if ct >= 5000:  # If we've looped 5000 times, this is probably an infinite loop
			print('Error: Infinite Loop')			
			exit(4)
		else:
			ct += 1		

		for x in range(size):
			if mod_matrix[x][x] == 0:  # If there's a zero where we need a non-zero value
				for i in range(size):  # Look through the matrix for a good row
					# Find a row with a non-zero value at col position  
					if mod_matrix[i][x] != 0:
						# Swap rows
						temp = mod_matrix[i]
						mod_matrix[i] = mod_matrix[x][:]
						mod_matrix[x] = temp[:]
						quit = False
						break  # End scan

			else:  # If we go through all rows like this, the loop will end
				quit = True  # This will get set back to false if we encounter a bad value


	return mod_matrix


def get_matrix():
    """
    This will grab a matrix from a user
    :return: matrix
    """

    # Initial Variables
    matrix = []
    quit = False

    # Begin number acquisition
    print('Format your system of equations so that all variables\n' +
          'are contained on the left side of the equation and the\n' +
          'constant value is on the right (ex: x + y = 7).\n' +
          'Once this is done, convert system to matrix and enter here ...\n')

    print('\n(commands: stop [ends collection], reset, and quit)')
    print('Enter matrix values separated by a space (ex: 1 2 3 4)')

    while not quit:
        temp_row_floats = []  # This will hold the floats of the user

        # 1. Grab a row from the user
        temp_row = input('ENTER NUMBERS: ')

        # 2. Interpret order if present
        if temp_row == 'stop':
            return matrix

        elif temp_row == 'reset':
            matrix = []
            continue

        elif temp_row == 'quit':
            print('Exiting program')
            exit(1)

        # 3. Determine if valid row, converting to a list of floats as it goes
        temp_row = temp_row.split(' ')  # Split by space

        try:
            clean_list(temp_row)  # Remove space elements
            clean_list(temp_row, '')  # Remove empty elements

            for item in temp_row:
                temp_row_floats.append(float(item))

        except Exception as e:
            print('Error: Please enter only valid commands or numbers')
            continue

        if len(matrix) >= 1 and len(matrix[0]) != len(temp_row_floats):  # If there's more than one row and input
            print('Number of values must equal first row')               # doesn't equal the first row

        else:
            matrix.append(temp_row_floats)


def solve_sys(matrix):
    """
    This solves a system of equations using matrix math

    :param matrix: A matrix obtained from the get_matrix function
    :return: A solved matrix
    """

    # 1. Create duplicate matrix to manipulate
    mod_matrix = matrix[:]
    total_rows = len(matrix)

    # 2. Go row by row, creating zeros to make an identity matrix
    col = 0  # This represents the column that we want to zero

    for x in range(total_rows):  # for each base row
        for i in range(total_rows):  # for each row that we want to add a zero to

            # 2.1 Skip conditions
            try:
                if x == i:  # If we're at the base row, we can't do anything
                    continue

                elif col > len(mod_matrix[0]):  # If we've gone out of bounds
                    break

                elif mod_matrix[i][col] == 0:  # If this row already has a zero where we want
                    continue

            except Exception as e:  # Something went wrong, get info to troubleshoot
                print(f'ERROR: {str(e)}')
                print(f'DATA: \ni = {i}\nx = {x}\ncol = {col}')
                exit(2)

            # 2.2 Duplicate rows and col_values for later manipulation
            base = mod_matrix[x][:]  # The base row is the row that we don't want to change
            target = mod_matrix[i][:]  # The target row is the row we want to change
            base_col = base[col]  # The value at the column we want to use
            target_col = target[col]

            # 2.3 Determine how rows should be manipulated
            if base_col > 0 and target_col > 0:  # If both values are positive
                base_col *= -1  # Make the base column value negative

            elif base_col < 0 and target_col < 0:  # If both values are negative
                base_col *= -1  # Make the base positive

            elif base_col > 0 and target_col < 0:  # If base is positive and target is negative
                target_col *= -1  # Make target positive

            elif base_col < 0 and target_col > 0:  # If the base is negative and the target is positive
                base_col *= -1  # Make the base positive

            # 2.4 Manipulate rows
            size = len(base)  # Size will be the same for base and target

            for item in range(size):  # Multiply base row by target_col; target row by base_col
                base[item] *= target_col
                target[item] *= base_col

            # 2.5 Create new row and replace mod_matrix[i] with it
            new_row = []

            for item in range(size):
                new_row.append(base[item] + target[item])

            mod_matrix[i] = new_row[:]

        # 2.6 Increment values as needed
        col += 1

    # 3. Finalize identity matrix creation by dividing all elements by the row's id col value
    col = 0
    columns = len(mod_matrix[0])

    try:
        for x in range(total_rows):  # For each base row
            div_by = mod_matrix[x][col]  # Get the value to divide the row by

            for i in range(columns):  # For each target row
                mod_matrix[x][i] = mod_matrix[x][i] / div_by

            col += 1  # Go to the next column for the next row
    except Exception as e:
        print(f'Error: {str(e)}')
        print('System may have been entered in wrong or it may be intractable')
        exit(3)

    return mod_matrix


if __name__ == '__main__':
	matrix = get_matrix()
	print('=== Received ===')
	for row in matrix:
		print(row)

	matrix = reorder_matrix(matrix)  # Ensure that the matrix is properly ordered

	print('\n=== Solution ===')
	new_matrix = solve_sys(matrix)
	variable = 1

	for row in new_matrix:
		print(f'Variable {variable} = {row[-1]}')
		variable += 1

	print('\n=== Solution Matrix ===')
	print('(If this is not a diagonal of 1s surrounded by 0s, the answer is false)')
	for row in new_matrix:
		print(row)

	exit(0)  # Successful completion

