import random

from subarreglo import (
    subarreglo_fuerza_bruta,
    subarreglo_maximo,
    suma_cruzada,
)


def ambas(serie):
    return (
        subarreglo_fuerza_bruta(serie),
        subarreglo_maximo(serie, 0, len(serie) - 1),
    )


def suma_del_tramo(serie, resultado):
    inicio, fin, _ = resultado
    return sum(serie[inicio:fin + 1])


# serie de ocho dias de la situacion problema
serie = [-3, 5, -2, 8, -6, 3, 9, -4]
fb, dc = ambas(serie)
assert fb[2] == 17 and dc[2] == 17
assert suma_del_tramo(serie, fb) == 17
assert suma_del_tramo(serie, dc) == 17

# un solo elemento
for unico in ([7], [-7], [0]):
    fb, dc = ambas(unico)
    assert fb == (0, 0, unico[0])
    assert dc == (0, 0, unico[0])

# todos negativos: gana el menos malo
negativos = [-8, -3, -6, -2, -9]
fb, dc = ambas(negativos)
assert fb[2] == -2 and dc[2] == -2
assert fb[0] == fb[1] == 3 and dc[0] == dc[1] == 3

# todos positivos: gana la serie completa
positivos = [4, 1, 7, 3, 9, 2]
fb, dc = ambas(positivos)
assert fb == (0, 5, 26) and dc == (0, 5, 26)

# el mejor tramo cruza el punto medio (medio = 2)
cruzado = [1, -1, 10, 10, -1, 1]
fb, dc = ambas(cruzado)
assert fb[2] == 20 and dc[2] == 20
assert dc[0] <= 2 < dc[1]
inicio, fin, suma = suma_cruzada(cruzado, 0, 2, 5)
assert (inicio, fin, suma) == (2, 3, 20)

# los tramos devueltos suman lo que dicen y las listas no se tocan
original = [-3, 5, -2, 8, -6, 3, 9, -4]
copia = list(original)
ambas(original)
assert original == copia

# 25 listas aleatorias de tamanos distintos, con semilla fija
generador = random.Random(2026)
for _ in range(25):
    n = generador.randint(1, 200)
    lista = [generador.randint(-100, 100) for _ in range(n)]
    copia = list(lista)
    fb, dc = ambas(lista)
    assert fb[2] == dc[2], (lista, fb, dc)
    assert suma_del_tramo(lista, fb) == fb[2]
    assert suma_del_tramo(lista, dc) == dc[2]
    assert lista == copia

print("Todas las pruebas pasaron")
