import math


def apply_gamma(matrix, gamma):
    height = len(matrix)
    width = len(matrix[0])

    new_matrix = [[0 for _ in range(width)] for _ in range(height)]

    for i in range(height):
        for j in range(width):
            r = matrix[i][j]

            normalized = r / 255.0

            s = (normalized ** gamma) * 255

            new_matrix[i][j] = int(s)

    return new_matrix

def apply_negative(matrix):
    height = len(matrix)
    width = len(matrix[0])

    new_matrix = [[0 for _ in range(width)] for _ in range(height)]

    for i in range(height):
        for j in range(width):
            r = matrix[i][j]
            s = 255 - r

            new_matrix[i][j] = int(s)

    return new_matrix


def apply_log(matrix):
    height = len(matrix)
    width = len(matrix[0])

    new_matrix = [[0 for _ in range(width)] for _ in range(height)]

    c = 255/math.log(1+255)
    for i in range(height):
        for j in range(width):
            r = matrix[i][j]

            s = c * math.log(1 + r)

            new_matrix[i][j] = int(s)

    return new_matrix



def apply_smoothing(matrix):
    height = len(matrix)
    width = len(matrix[0])

    new_matrix = [row[:] for row in matrix]

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            
            total_sum = 0
            for ki in [-1, 0, 1]:  
                for kj in [-1, 0, 1]: 
                    total_sum += matrix[i + ki][j + kj]
            
            new_matrix[i][j] = int(total_sum / 9)
            
    return new_matrix



def apply_median(matrix):
    height = len(matrix)
    width = len(matrix[0])
    
    new_matrix = [row[:] for row in matrix]

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            
            neighborhood = []
            for ki in [-1, 0, 1]:
                for kj in [-1, 0, 1]:
                    neighborhood.append(matrix[i + ki][j + kj])
            
            neighborhood.sort()
            
            median_value = neighborhood[4]
            
            new_matrix[i][j] = median_value
            
    return new_matrix
def apply_edge_detection(matrix):
    height = len(matrix)
    width = len(matrix[0])
    
    new_matrix = [row[:] for row in matrix]

    kernel = [
        [-1, -1, -1],
        [-1,  8, -1],
        [-1, -1, -1]
    ]

    for i in range(1, height - 1):
        for j in range(1, width - 1):
            
            total_sum = 0
            for ki in [-1, 0, 1]:
                for kj in [-1, 0, 1]:
                    pixel_value = matrix[i + ki][j + kj]
                    kernel_value = kernel[ki + 1][kj + 1] 
                    total_sum += pixel_value * kernel_value
            
            if total_sum < 0:
                total_sum = 0
            elif total_sum > 255:
                total_sum = 255
                
            new_matrix[i][j] = int(total_sum)
            
    return new_matrix    