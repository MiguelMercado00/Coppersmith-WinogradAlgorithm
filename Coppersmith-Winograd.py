#Integrantes:
#- Miguel Mercado
#- Nicol Franchesca Garcia
#- Camilo Melo
#- Sebastian Nacy
#- Juan José Barón

import numpy as np

def generate_random_matrix(rows, cols):
    # Generar una matriz aleatoria con dimensiones pares para que funcione el algoritmo de Coppersmith-Winograd
    return np.random.randint(1, 10, size=(rows + rows % 2, cols + cols % 2))

def coppersmith_winograd(A, B):
    n1, m1 = A.shape
    n2, m2 = B.shape

    if m1 != n2:
        raise ValueError("Las matrices no son compatibles para la multiplicación")

    # Algoritmo de Coppersmith-Winograd
    # Ajustar las dimensiones de las matrices para que sean pares si es necesario (agregando filas y columnas de ceros)
    if n1 % 2 != 0:
        A = np.vstack((A, np.zeros((1, m1))))
        n1 += 1
    if m1 % 2 != 0:
        A = np.hstack((A, np.zeros((n1, 1))))
        m1 += 1
    if n2 % 2 != 0:
        B = np.vstack((B, np.zeros((1, m2))))
        n2 += 1
    if m2 % 2 != 0:
        B = np.hstack((B, np.zeros((n2, 1))))
        m2 += 1

    # Dividir las matrices en bloques
    A11, A12 = A[:n1//2, :], A[n1//2:, :]
    A21, A22 = A[:n1//2, :], A[n1//2:, :]
    B11, B12 = B[:, :m2//2], B[:, m2//2:]
    B21, B22 = B[:, :m2//2], B[:, m2//2:]

    # Calcular los términos intermedios
    S1 = B12 - B22
    S2 = A11 + A12
    S3 = A21 + A22
    S4 = B21 - B11
    S5 = A11 + A22
    S6 = B11 + B22
    S7 = A12 - A22
    S8 = B21 + B22
    S9 = A11 - A21
    S10 = B11 + B12

    # Calcular los productos intermedios
    P1 = np.dot(A11, S1)
    P2 = np.dot(S2, B22)
    P3 = np.dot(S3, B11)
    P4 = np.dot(A22, S4)
    P5 = np.dot(S5, S6)
    P6 = np.dot(S7, S8)
    P7 = np.dot(S9, S10)

    # Calcular los bloques de la matriz resultante
    C11 = P5 + P4 - P2 + P6
    C12 = P1 + P2
    C21 = P3 + P4
    C22 = P5 + P1 - P3 - P7

    # Obtener la matriz resultante eliminando filas y columnas adicionales (si se agregaron)
    C = C11[:n1//2, :m2//2]

    return C

# Generar matrices aleatorias con dimensiones NxM y MxP, asegurando que sean pares
N, M, P = 3, 4, 5
A = generate_random_matrix(N, M)
B = generate_random_matrix(M, P)

# Realizar la multiplicación de matrices utilizando el algoritmo de Coppersmith-Winograd
resultado = coppersmith_winograd(A, B)
print("Matriz A:")
print(A)
print("\nMatriz B:")
print(B)
print("\nResultado de la multiplicación:")
print(resultado)
