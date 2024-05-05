import math

matriz = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 1, 1, 0, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 0],
    [0, 0, 0, 1, 1, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]


def encontrar_limites(matrz):
    # Inicializando as variáveis para encontrar os índices mínimos e máximos
    eixo_x = []
    eixo_y = []

    for y in range(len(matrz) - 1):
        for x in range(len(matrz[y]) - 1):
            if matrz[y][x] == 1:
                eixo_x.append(x)
                eixo_y.append(y)

    min_x = min(eixo_x)
    max_x = max(eixo_x)
    min_y = min(eixo_y)
    max_y = max(eixo_y)
    largura = max_x - min_x + 1
    altura = max_y - min_y + 1

    return min(largura, altura)


diamin = encontrar_limites(matriz)
raio = diamin / 2
area = math.pi * (raio ** 2)
print("A área da matriz é: ", area, "pixels.")
