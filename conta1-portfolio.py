import numpy as np
import time

# Gerar matriz 10x10 nula usando numpy
matriz = np.zeros((10, 10), dtype=int)

# Posições dos píxeis da imagem na matriz
posicoes = {
    (1, 2), (1, 3),
    (2, 2), (2, 3), (2, 4),
    (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
    (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8),
    (5, 1), (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8),
    (6, 2), (6, 3), (6, 4), (6, 5), (6, 6), (6, 7), (6, 8),
    (7, 3), (7, 4), (7, 6), (7, 7),
    (8, 4)
}

# Atualizando os valores da matriz nas posições ditas
for (i, j) in posicoes:
    matriz[i, j] = 1

# Medindo esforço computacional
# Contar quantos números 1 a matriz tem
start_time = time.time()
area = np.count_nonzero(matriz == 1)
end_time = time.time()

print(matriz)

print(f"\nÁrea das fibras em pixels: {area}")
print("Tempo de execução: {:.50f} segundos".format(end_time - start_time))
