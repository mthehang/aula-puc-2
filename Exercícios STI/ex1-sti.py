import numpy as np

matriz = np.random.randint(2, size=(4, 4))

print('Faça uma ista de 4 números com 0 e 1!')
lista = []
i = 0
while i < 4:
    lista.append(int(input(f'Digite o {i + 1}° número: ')))
    i += 1

print(f"\n{matriz}\n")

for linha in range(len(matriz)):
    print(linha)
    if np.array_equal(matriz[linha], lista):
        print("Jogador venceu!")
        exit()
    else:
        pass

print("Jogador perdeu!")




