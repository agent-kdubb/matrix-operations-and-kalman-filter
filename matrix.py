import math
from math import sqrt
import numbers

def zeroes(height, width):
        """
        Creates a matrix of zeroes.
        """
        g = [[0.0 for _ in range(width)] for __ in range(height)]
        return Matrix(g)

def identity(n):
        """
        Creates a n x n identity matrix.
        """
        I = zeroes(n, n)
        for i in range(n):
            I.g[i][i] = 1.0
        return I

class Matrix(object):

    # Constructor
    def __init__(self, grid):
        self.g = grid
        self.h = len(grid)
        self.w = len(grid[0])

    #
    # Primary matrix math methods
    #############################
 
    def determinant(self):
        """
        Calculates the determinant of a 1x1 or 2x2 matrix.
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate determinant of non-square matrix.")
        if self.h > 2:
            raise(NotImplementedError, "Calculating determinant not implemented for matrices largerer than 2x2.")
        a = self.g[0][0]
        b = self.g[0][1]
        c = self.g[1][0]
        d = self.g[1][1]
        if self.h == 2:
            if self.w == 2:
                det_A = 1 / ((a*d) - (b*c))
        elif self.w == 1:
            if self.w == 1:
                det_A == a
        return det_A
    
    def trace(self):
        """
        Calculates the trace of a matrix (sum of diagonal entries).
        """
        if not self.is_square():
            raise(ValueError, "Cannot calculate the trace of a non-square matrix.")
           
        tr_A = 0
        
        for i in range(self.h):
            for j in range(self.w):
                if i == j:
                    tr_A += self.g[i][j] 
        return tr_A
        

    def inverse(self):
        """
        Calculates the inverse of a 1x1 or 2x2 Matrix.
        """
        if not self.is_square():
            raise(ValueError, "Non-square Matrix does not have an inverse.")
        if self.h > 2:
            raise(NotImplementedError, "inversion not implemented for matrices larger than 2x2.")

        if self.h == 2:
            if self.w == 2:
                if self.g[0][0]*self.g[1][1] == self.g[0][1]*self.g[1][0]:
                    raise ValueError('A non-invertible matrix has been entered. ad = bc')
                else:    
                    det_A = 1/(self.g[0][0]*self.g[1][1]-self.g[0][1]*self.g[1][0])
                    inverse = [[det_A*self.g[1][1],det_A*-self.g[0][1]],[det_A*-self.g[1][0],det_A*self.g[0][0]]]
          
        elif self.h == 1:
            inverse = [[1 / self.g[0][0]]]
    
        return Matrix(inverse)

    def T(self):
        """
        Returns a transposed copy of this Matrix.
        """
        def get_column(matrix, column_number):
            column = []
            for i in range(matrix.h):
                num = matrix[i][column_number]
                column.append(num)
            return column
        
        matrix_transpose = []
    
        for i in range(self.w):
            new_row = get_column(self, i)
            matrix_transpose.append(new_row)
            
        return Matrix(matrix_transpose)

    def is_square(self):
        return self.h == self.w

    #
    # Begin Operator Overloading
    ############################
    def __getitem__(self,idx):
        """
        Defines the behavior of using square brackets [] on instances
        of this class.

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > my_matrix[0]
          [1, 2]

        > my_matrix[0][0]
          1
        """
        return self.g[idx]

    def __repr__(self):
        """
        Defines the behavior of calling print on an instance of this class.
        """
        s = ""
        for row in self.g:
            s += " ".join(["{} ".format(x) for x in row])
            s += "\n"
        return s

    def __add__(self,other):
        """
        Defines the behavior of the + operator
        """
        if self.h != other.h or self.w != other.w:
            raise(ValueError, "Matrices can only be added if the dimensions are the same") 
          
        matrixSum = []
    
        for i in range(self.h):
            row = []
            for j in range(self.w):
                el_sum =  self[i][j] + other[i][j]
                row.append(el_sum)
            matrixSum.append(row)
     
        return Matrix(matrixSum)
        

    def __neg__(self):
        """
        Defines the behavior of - operator (NOT subtraction)

        Example:

        > my_matrix = Matrix([ [1, 2], [3, 4] ])
        > negative  = -my_matrix
        > print(negative)
          -1.0  -2.0
          -3.0  -4.0
        """
     
        neg_matrix = []
        for i in range(len(self.g)):
            row = []
            for j in range(len(self[i])):
                neg = -self[i][j]
                row.append(neg)
            neg_matrix.append(row)
        return Matrix(neg_matrix)
        


    def __sub__(self, other):
        """
        Defines the behavior of - operator (as subtraction)
        """
          
        matrixSubtract = []
    
        for i in range(self.h):
            row = []
            for j in range(self.w):
                el_subtract =  self[i][j] - other[i][j]
                row.append(el_subtract)
            matrixSubtract.append(row)
            
        return Matrix(matrixSubtract)
        


    def __mul__(self, other):
        """
        Defines the behavior of * operator (matrix multiplication)
        """
        def get_column(matrix, column_number):
            column = []
            for i in range(matrix.h):
                num = matrix[i][column_number]
                column.append(num)
            return column 
        
        def transpose(matrix):
    
            matrix_transpose = []
    
            for i in range(len(matrix[0])):
                new_row = get_column(matrix, i)
                matrix_transpose.append(new_row)
            
            return matrix_transpose
        
        def dot_product(vector_one, vector_two):
            
            product = 0
            
            for i in range(len(vector_one)):
                product += (vector_one[i] * vector_two[i]) 
                
            return product
        
        otherT = transpose(other)
        product = []
   
        for i in range(self.h):
            new_row = []  
            for j in range(len(otherT)):
                new_num = dot_product(self[i], otherT[j])
                new_row.append(new_num)
            product.append(new_row)
        return Matrix(product)
        
        
    def __rmul__(self, other):
        """
        Called when the thing on the left of the * is not a matrix.

        Example:

        > identity = Matrix([ [1,0], [0,1] ])
        > doubled  = 2 * identity
        > print(doubled)
          2.0  0.0
          0.0  2.0
        """
        if isinstance(other, numbers.Number):
            pass
              
        r = []

        for i in range(self.h):
            row = []
            for j in range(self.w):
                scalar = other * self[i][j]
                row.append(scalar)
            r.append(row)
        return Matrix(r)
        
    
   