from scipy.sparse import csr_matrix

class SparseMatrix:
    def __init__(self, matrix_path=None, num_rows=None, num_cols=None):
        
        if matrix_path:
            # Load the matrix from a file
            self.rows, self.cols, self.elements = self._load_from_file(matrix_path)
        else:
            # Create an empty matrix with the specified dimensions
            self.rows = num_rows
            self.cols = num_cols
            self.elements = {}  # Store only non-zero elements in a dictionary

    def _load_from_file(self, file_path):
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Remove whitespace and empty lines
        lines = [line.strip() for line in lines if line.strip()]

        # Read number of rows and columns
        try:
            rows = int(lines[0].split('=')[1])  # First line contains rows
            cols = int(lines[1].split('=')[1])  # Second line contains cols
        except (ValueError, IndexError):
            raise ValueError("Input file has wrong format")

        # Initialize a dictionary
        elements = {}
        
        # Parse the non-zero elements from the file
        for line in lines[2:]:
            try:
                # Remove parentheses and split by comma
                row, col, val = line.replace('(', '').replace(')', '').split(',')
                row, col, val = int(row), int(col), int(val)
                if row >= rows or col >= cols:
                    raise ValueError("Matrix element out of bounds")
                # Store the non-zero value in the dictionary
                elements[(row, col)] = val
            except (ValueError, IndexError):
                raise ValueError("Input file has wrong format")

        return rows, cols, elements

    def get_element(self, current_row, current_col):

        return self.elements.get((current_row, current_col), 0)

    def set_element(self, current_row, current_col, value):
        
        if current_row >= self.rows or current_col >= self.cols:
            raise IndexError("Element position out of bounds")
        if value != 0:
            # Set a non-zero element
            self.elements[(current_row, current_col)] = value
        elif (current_row, current_col) in self.elements:
            # Remove the element if it's set to zero
            del self.elements[(current_row, current_col)]

    def __add__(self, other):
        
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must be the same for addition")
        
        # Create a new matrix to store the result
        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)
        
        # Add elements from the first matrix
        for key, value in self.elements.items():
            result.set_element(key[0], key[1], value + other.get_element(key[0], key[1]))
        
        # Add elements from the second matrix (if they don't exist in the first matrix)
        for key, value in other.elements.items():
            if key not in self.elements:
                result.set_element(key[0], key[1], value)
        
        return result

    def __sub__(self, other):
        
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matrix dimensions must be the same for subtraction")
        
        # Create a new matrix to store the result
        result = SparseMatrix(num_rows=self.rows, num_cols=self.cols)
        
        # Subtract elements from the first matrix
        for key, value in self.elements.items():
            result.set_element(key[0], key[1], value - other.get_element(key[0], key[1]))
        
        # Subtract elements from the second matrix (if they don't exist in the first matrix)
        for key, value in other.elements.items():
            if key not in self.elements:
                result.set_element(key[0], key[1], -value)
        
        return result

    def __mul__(self, other):
        
        if self.cols != other.rows:
            raise ValueError("Number of columns of first matrix must equal number of rows of second matrix for multiplication")
        
        # Create a new matrix to store the result
        result = SparseMatrix(num_rows=self.rows, num_cols=other.cols)
        
        # Perform matrix multiplication
        for (i, j), val1 in self.elements.items():
            for k in range(other.cols):
                val2 = other.get_element(j, k)
                if val2 != 0:
                    result.set_element(i, k, result.get_element(i, k) + val1 * val2)
        
        return result

    def to_dense(self):
        
        dense_matrix = [[0] * self.cols for _ in range(self.rows)]
        for (i, j), value in self.elements.items():
            dense_matrix[i][j] = value
        return dense_matrix


def load_matrix(file_path):
    try:
        matrix = SparseMatrix(matrix_path=file_path)
        return matrix
    except ValueError as e:
        print(f"Error loading matrix from {file_path}: {e}")
        return None


def main():
    # Get file paths and operation choice from the user
    matrix1_file = input("Enter the file path for Matrix 1: ")
    matrix2_file = input("Enter the file path for Matrix 2: ")
    operation = input("Choose operation - Enter + for adding/Enter - for subtracting/Enter x for multiplying: ").lower()

    # Load matrices
    matrix1 = load_matrix(matrix1_file)
    matrix2 = load_matrix(matrix2_file)

    if matrix1 is None or matrix2 is None:
        return  # Stop the program if there was an error while loading the matrices

    # Perform the operation
    try:
        if operation == "+":
            result = matrix1 + matrix2
        elif operation == "-":
            result = matrix1 - matrix2
        elif operation == "x":
            result = matrix1 * matrix2
        else:
            print("Invalid operation")
            return
    except ValueError as e:
        print(f"Error performing operation: {e}")
        return

    # Output the result as a dense matrix for demonstration
    dense_result = result.to_dense()
    for row in dense_result:
        print(row)


if __name__ == "__main__":
    main()
