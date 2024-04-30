import numpy as np
import time
import math

# Gerando matriz 10x10 nula usando numpy
matriz = np.zeros((10, 10), dtype=int)

# Posições dos píxeis da imagem na matriz
posicoes = {
    (1, 2), (1, 3),
    (2, 2), (2, 3), (2, 4),
    (3, 1), (3, 2), (3, 3), (3, 4), (3, 5),
    (4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (4, 6), (4, 7), (4, 8),
    (5, 2), (5, 3), (5, 4), (5, 5), (5, 6), (5, 7), (5, 8),
    (6, 3), (6, 4), (6, 6), (6, 7),
    (7, 4)
}

# Atualizando os valores da matriz nas posições ditas
for (i, j) in posicoes:
    matriz[i, j] = 1

# Medindo esforço computacional
start_time = time.time()

# Encontrando os limites da "imagem" de números 1
x_coords = [i for (i, j) in posicoes]
y_coords = [j for (i, j) in posicoes]

min_x, max_x = min(x_coords), max(x_coords)
min_y, max_y = min(y_coords), max(y_coords)

# Calculando a largura e a altura do retângulo
largura = max_x - min_x + 1
altura = max_y - min_y + 1

menor_diametro = min(largura, altura)

# Conta do Diâmetro mínimo de Feret
area = (menor_diametro/2)**2 * math.pi

end_time = time.time()

print(f"\nÁrea das fibras por Diâmetro Mínimo de Feret: {round(area, 2)}")
print("Tempo de execução: {:6f} segundos".format(end_time - start_time))

