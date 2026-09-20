"""Experimento de la Parte 4: validacion experimental de la complejidad.

Mide cuanto se demoran insertion_sort y merge_sort con el escenario A
(aleatorio), usando los mismos tamanos de la Parte 3, y guarda la grafica
parte4_tiempo.png en graficas/.
"""

import statistics
import time
from collections.abc import Callable
from pathlib import Path

import matplotlib.pyplot as plt

from algoritmos import insertion_sort, merge_sort
from datos import generar_aleatorio

TAMANOS = [100, 200, 400, 800, 1600, 3200, 6400]
REPETICIONES = 3
CARPETA_GRAFICAS = Path(__file__).parent / "graficas"

ALGORITMOS = {
    "Insertion sort": insertion_sort,
    "Merge sort": merge_sort,
}


def medir_algoritmo(
    algoritmo: Callable[[list[int]], tuple[list[int], int]], n: int
) -> float:
    """Mide el tiempo mediano de un algoritmo sobre el escenario A.

    Args:
        algoritmo: funcion de ordenamiento instrumentada a medir.
        n: tamano del lote a generar y ordenar.

    Returns:
        Tiempo mediano de ejecucion, en segundos, sobre REPETICIONES corridas.
    """
    tiempos = []
    for _ in range(REPETICIONES):
        datos = generar_aleatorio(n)
        inicio = time.perf_counter()
        algoritmo(datos)
        fin = time.perf_counter()
        tiempos.append(fin - inicio)
    return statistics.median(tiempos)


def ejecutar_experimento() -> dict:
    """Corre el experimento comparativo sobre el escenario A.

    Returns:
        Diccionario {nombre_algoritmo: [tiempos_por_tamano]}.
    """
    resultados = {nombre: [] for nombre in ALGORITMOS}
    for nombre, algoritmo in ALGORITMOS.items():
        for n in TAMANOS:
            tiempo = medir_algoritmo(algoritmo, n)
            resultados[nombre].append(tiempo)
            print(f"{nombre:16s} n={n:6d}  t={tiempo:.6f}s")
    return resultados


def graficar_tiempo(resultados: dict) -> None:
    """Genera parte4_tiempo.png: tiempo vs. tamano, una curva por algoritmo."""
    plt.figure(figsize=(8, 5))
    for nombre, tiempos in resultados.items():
        plt.plot(TAMANOS, tiempos, marker="o", label=nombre)
    plt.title(
        "Insertion sort vs. merge sort: tiempo de ejecucion (escenario A)"
    )
    plt.xlabel("Tamano de entrada (n, numero de registros)")
    plt.ylabel("Tiempo de ejecucion (segundos, mediana de 3 corridas)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(CARPETA_GRAFICAS / "parte4_tiempo.png", dpi=150)
    plt.close()


def main() -> None:
    """Corre la comparacion y guarda la grafica de la Parte 4."""
    CARPETA_GRAFICAS.mkdir(exist_ok=True)
    resultados = ejecutar_experimento()
    graficar_tiempo(resultados)
    print("\nGrafica guardada en graficas/parte4_tiempo.png")


if __name__ == "__main__":
    main()
