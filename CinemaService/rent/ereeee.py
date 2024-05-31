def iterate_rectangles(matrix):
    n, m = len(matrix), len(matrix[0])
    for top in range(n):
        for bottom in range(top, n):
            for left in range(m):
                for right in range(left, m):
                    yield (top, bottom, left, right)


def calculate_rectangle_sum(matrix, top, bottom, left, right):
    sum = 0
    for i in range(top, bottom + 1):
      for j in range(left, right + 1):
        sum += matrix[i][j]
    return sum


n, m = 5, 5
"""matrix = [
    [1, 0, 7, -8, 2],
    [2, 7, -5, 3, 1],
    [6, -8, 4, 2, 1],
    [-7, 3, 1, -2, 1],
    [2, 7, 4, 0, -50]

]"""
matrix = [
    [10, -1, -1, 7, -3],
    [-6, -6, 5, 7, -6],
    [8, -2, 1, 5, 6],
    [-1, -2, -3, -8, 1],
    [-9, -9, 5, 6, -1]
]
max_summ = -100000


for top, bottom, left, right in iterate_rectangles(matrix):
    a = calculate_rectangle_sum(matrix, top, bottom, left, right)
    if a >= max_summ:
        max_summ = a

    print(f"Прямоугольник: (top={top}, bottom={bottom}, left={left}, right={right})")
    print(max_summ)

