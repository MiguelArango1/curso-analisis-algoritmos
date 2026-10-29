"""Mediciones del lab 3: lista enlazada contra tabla hash.

Experimento A: tiempo de busqueda de guias inexistentes frente a n.
Experimento B: tiempo de busqueda frente al factor de carga alfa.
Guarda las graficas en graficas/.
"""

import random
import statistics
import time
from collections.abc import Callable
from pathlib import Path

import matplotlib.pyplot as plt

from estructuras import ListaEnlazada, TablaHash

TAMANOS = [100, 500, 1000, 5000, 20000, 50000, 100000]
BUSQUEDAS_A = 200
N_FIJO = 20000
ALFAS = [0.25, 0.5, 1, 2, 4, 10]
BUSQUEDAS_B = 5000
REPETICIONES = 5
SEMILLA = 42
ESTADOS = ["en bodega", "en reparto", "entregado"]
CARPETA_GRAFICAS = Path(__file__).parent / "graficas"


def generar_guias_inexistentes(
    existentes: set[int], cantidad: int, semilla: int = 7
) -> list[int]:
    """Genera guias de diez digitos que no estan en la coleccion.

    Args:
        existentes: guias almacenadas en las estructuras.
        cantidad: cuantas guias inexistentes generar.
        semilla: semilla del generador, para reproducir la medicion.

    Returns:
        Una lista con `cantidad` guias que no pertenecen a `existentes`.
    """
    azar = random.Random(semilla)
    inexistentes: list[int] = []
    while len(inexistentes) < cantidad:
        guia = azar.randint(10**9, 10**10 - 1)
        if guia not in existentes:
            inexistentes.append(guia)
    return inexistentes


def generar_guias(n: int, semilla: int = SEMILLA) -> list[int]:
    """Genera n guias distintas de diez digitos.

    Args:
        n: cantidad de guias.
        semilla: semilla del generador, para reproducir la medicion.

    Returns:
        Lista de n enteros distintos entre 10**9 y 10**10 - 1.
    """
    azar = random.Random(semilla)
    return azar.sample(range(10**9, 10**10), n)


def es_primo(k: int) -> bool:
    """Dice si un entero es primo.

    Args:
        k: entero a revisar.

    Returns:
        True si k es primo.
    """
    if k < 2:
        return False
    divisor = 2
    while divisor * divisor <= k:
        if k % divisor == 0:
            return False
        divisor += 1
    return True


def primo_desde(objetivo: float) -> int:
    """Busca el primer primo mayor o igual al objetivo.

    Args:
        objetivo: valor desde el que se empieza a buscar.

    Returns:
        El primo mas cercano por encima del objetivo.
    """
    candidato = int(objetivo)
    while not es_primo(candidato):
        candidato += 1
    return candidato


def construir(
    guias: list[int], m: int
) -> tuple[ListaEnlazada, TablaHash, dict[int, str]]:
    """Arma la lista y la tabla con las mismas guias y estados.

    Args:
        guias: guias a almacenar.
        m: numero de casillas de la tabla.

    Returns:
        La lista, la tabla y un diccionario con los estados esperados
        (el diccionario solo se usa para verificar, no es parte de las
        estructuras).
    """
    azar = random.Random(SEMILLA)
    esperados = {guia: azar.choice(ESTADOS) for guia in guias}
    lista = ListaEnlazada()
    tabla = TablaHash(m)
    for guia, estado in esperados.items():
        lista.insertar(guia, estado)
        tabla.insertar(guia, estado)
    return lista, tabla, esperados


def verificar(
    lista: ListaEnlazada, tabla: TablaHash, esperados: dict[int, str]
) -> None:
    """Comprueba que lista y tabla dan el mismo estado en una muestra.

    Args:
        lista: lista enlazada ya cargada.
        tabla: tabla hash ya cargada.
        esperados: estado correcto de cada guia almacenada.
    """
    azar = random.Random(SEMILLA)
    muestra = azar.sample(list(esperados), min(100, len(esperados)))
    for guia in muestra:
        assert lista.buscar(guia) == tabla.buscar(guia) == esperados[guia]


def medir_busquedas(
    buscar: Callable[[int], str | None], guias: list[int]
) -> float:
    """Mide el tiempo medio de una busqueda de guias inexistentes.

    Args:
        buscar: metodo de busqueda de la estructura.
        guias: guias que se buscan (ninguna esta almacenada).

    Returns:
        Mediana, entre las repeticiones, del tiempo medio por busqueda
        en microsegundos.
    """
    tiempos = []
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        for guia in guias:
            buscar(guia)
        fin = time.perf_counter()
        tiempos.append((fin - inicio) / len(guias) * 1e6)
    return statistics.median(tiempos)


def experimento_a() -> tuple[list[int], list[float], list[float]]:
    """Mide lista y tabla para cada n, con alfa cerca de 2.

    Returns:
        Los valores de m usados, los tiempos de la lista y los de la
        tabla (microsegundos por busqueda), en el orden de TAMANOS.
    """
    ms = []
    tiempos_lista = []
    tiempos_tabla = []
    for n in TAMANOS:
        guias = generar_guias(n)
        m = primo_desde(n / 2)
        lista, tabla, esperados = construir(guias, m)
        verificar(lista, tabla, esperados)
        inexistentes = generar_guias_inexistentes(set(guias), BUSQUEDAS_A)

        t_lista = medir_busquedas(lista.buscar, inexistentes)
        t_tabla = medir_busquedas(tabla.buscar, inexistentes)
        ms.append(m)
        tiempos_lista.append(t_lista)
        tiempos_tabla.append(t_tabla)
        print(
            f"n={n:7d}  m={m:6d}  alfa={tabla.factor_carga():.2f}  "
            f"lista={t_lista:10.3f} us  tabla={t_tabla:7.3f} us"
        )
    return ms, tiempos_lista, tiempos_tabla


def experimento_b() -> tuple[list[int], list[float], list[float]]:
    """Mide la tabla con n fijo y distintos factores de carga.

    Returns:
        Los valores de m usados, los alfa reales y los tiempos
        (microsegundos por busqueda).
    """
    guias = generar_guias(N_FIJO)
    inexistentes = generar_guias_inexistentes(set(guias), BUSQUEDAS_B)
    ms = []
    alfas = []
    tiempos = []
    for alfa_objetivo in ALFAS:
        m = primo_desde(N_FIJO / alfa_objetivo)
        lista, tabla, esperados = construir(guias, m)
        verificar(lista, tabla, esperados)
        tiempo = medir_busquedas(tabla.buscar, inexistentes)
        ms.append(m)
        alfas.append(tabla.factor_carga())
        tiempos.append(tiempo)
        print(
            f"m={m:6d}  alfa={tabla.factor_carga():6.3f}  "
            f"tabla={tiempo:7.3f} us"
        )
    return ms, alfas, tiempos


def mostrar_factores(
    tiempos_lista: list[float], tiempos_tabla: list[float]
) -> None:
    """Imprime cuanto se multiplica el tiempo entre n consecutivos.

    Args:
        tiempos_lista: tiempos de la lista, por cada n.
        tiempos_tabla: tiempos de la tabla, por cada n.
    """
    print("\nDe un n al siguiente, cuanto se multiplica el tiempo:")
    for i in range(1, len(TAMANOS)):
        print(
            f"  {TAMANOS[i - 1]:7d} -> {TAMANOS[i]:7d}  "
            f"n x{TAMANOS[i] / TAMANOS[i - 1]:5.2f}  "
            f"lista x{tiempos_lista[i] / tiempos_lista[i - 1]:6.2f}  "
            f"tabla x{tiempos_tabla[i] / tiempos_tabla[i - 1]:5.2f}"
        )


def graficar_a(
    tiempos_lista: list[float], tiempos_tabla: list[float]
) -> None:
    """Guarda graficas/lista_vs_tabla.png (escala lineal y logaritmica).

    Args:
        tiempos_lista: tiempos de la lista, por cada n.
        tiempos_tabla: tiempos de la tabla, por cada n.
    """
    figura, ejes = plt.subplots(1, 2, figsize=(12, 5))
    escalas = [("linear", "escala lineal"), ("log", "escala logarítmica")]
    for eje, (escala, nombre) in zip(ejes, escalas):
        eje.plot(TAMANOS, tiempos_lista, marker="o", label="Lista enlazada")
        eje.plot(TAMANOS, tiempos_tabla, marker="s", label="Tabla hash")
        eje.set_xscale(escala)
        eje.set_yscale(escala)
        eje.set_title(f"Guía inexistente: tiempo vs. n ({nombre})")
        eje.set_xlabel("Número de guías n (envíos almacenados)")
        eje.set_ylabel("Tiempo medio por búsqueda (µs)")
        eje.legend()
        eje.grid(True, linestyle="--", alpha=0.5)
    figura.tight_layout()
    figura.savefig(CARPETA_GRAFICAS / "lista_vs_tabla.png", dpi=150)
    plt.close(figura)


def graficar_b(alfas: list[float], tiempos: list[float]) -> None:
    """Guarda graficas/tiempo_vs_alfa.png.

    Args:
        alfas: factores de carga reales de cada tabla.
        tiempos: tiempo medio por busqueda de cada tabla (microsegundos).
    """
    figura, eje = plt.subplots(figsize=(7, 5))
    eje.plot(alfas, tiempos, marker="o", label=f"Tabla hash (n = {N_FIJO})")
    eje.set_title("Guía inexistente: tiempo de búsqueda vs. factor de carga")
    eje.set_xlabel("Factor de carga α = n / m (adimensional)")
    eje.set_ylabel("Tiempo medio por búsqueda (µs)")
    eje.legend()
    eje.grid(True, linestyle="--", alpha=0.5)
    figura.tight_layout()
    figura.savefig(CARPETA_GRAFICAS / "tiempo_vs_alfa.png", dpi=150)
    plt.close(figura)


def main() -> None:
    """Corre los dos experimentos, imprime los datos y guarda las graficas."""
    CARPETA_GRAFICAS.mkdir(exist_ok=True)
    print("Experimento A: lista contra tabla")
    _, tiempos_lista, tiempos_tabla = experimento_a()
    mostrar_factores(tiempos_lista, tiempos_tabla)
    graficar_a(tiempos_lista, tiempos_tabla)

    print(f"\nExperimento B: efecto de alfa con n = {N_FIJO}")
    _, alfas, tiempos = experimento_b()
    graficar_b(alfas, tiempos)
    print("\nGraficas guardadas en graficas/")


if __name__ == "__main__":
    main()
