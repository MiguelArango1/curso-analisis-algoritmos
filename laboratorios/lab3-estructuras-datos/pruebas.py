import random

from estructuras import ListaEnlazada, TablaHash

ESTADOS = ["en bodega", "en reparto", "entregado"]


def largo_de(lista):
    contador = 0
    actual = lista.cabeza
    while actual is not None:
        contador += 1
        actual = actual.siguiente
    return contador


# serie de ejemplo de la situacion problema
ejemplo = [
    (1000000010, "en bodega"),
    (1000000024, "en reparto"),
    (1000000017, "en bodega"),
    (1000000005, "entregado"),
]
lista = ListaEnlazada()
tabla = TablaHash(7)
for guia, estado in ejemplo:
    lista.insertar(guia, estado)
    tabla.insertar(guia, estado)

# busqueda exitosa e infructuosa en las dos estructuras
for guia, estado in ejemplo:
    assert lista.buscar(guia) == estado
    assert tabla.buscar(guia) == estado
assert lista.buscar(1000000999) is None
assert tabla.buscar(1000000999) is None

# estructuras vacias
assert ListaEnlazada().buscar(5) is None
assert TablaHash(7).buscar(5) is None

# la lista inserta al inicio y cuenta su tamano
assert lista.cabeza.guia == 1000000005
assert lista.tamano == 4 and largo_de(lista) == 4
assert tabla.tamano == 4

# colision forzada: con m = 7 las guias 10, 24 y 17 caen en la casilla 3
tabla = TablaHash(7)
for guia in (10, 24, 17):
    assert tabla.hash(guia) == 3
    tabla.insertar(guia, "en bodega")
assert tabla.buscar(10) == "en bodega"
assert tabla.buscar(24) == "en bodega"
assert tabla.buscar(17) == "en bodega"
assert tabla.buscar(99) is None
assert tabla.casillas[3].tamano == 3
assert largo_de(tabla.casillas[3]) == 3
assert all(c.tamano == 0 for i, c in enumerate(tabla.casillas) if i != 3)

# factor de carga
assert tabla.factor_carga() == 3 / 7

# con m = 1 toda guia cae en la misma casilla (la tabla es una lista)
una_casilla = TablaHash(1)
for guia in range(50):
    una_casilla.insertar(guia, "en bodega")
assert una_casilla.casillas[0].tamano == 50
assert una_casilla.factor_carga() == 50

# 25 colecciones aleatorias: lista y tabla tienen que decir lo mismo
generador = random.Random(2026)
for _ in range(25):
    n = generador.randint(0, 300)
    m = generador.randint(1, 60)
    guias = generador.sample(range(10**9, 10**10), n)
    referencia = {g: generador.choice(ESTADOS) for g in guias}

    lista = ListaEnlazada()
    tabla = TablaHash(m)
    for guia, estado in referencia.items():
        lista.insertar(guia, estado)
        tabla.insertar(guia, estado)

    assert lista.tamano == n and tabla.tamano == n
    assert tabla.factor_carga() == n / m
    for guia, estado in referencia.items():
        assert lista.buscar(guia) == estado
        assert tabla.buscar(guia) == estado

    inexistentes = 0
    while inexistentes < 30:
        guia = generador.randint(10**9, 10**10 - 1)
        if guia in referencia:
            continue
        assert lista.buscar(guia) is None
        assert tabla.buscar(guia) is None
        inexistentes += 1

print("Todas las pruebas pasaron")
