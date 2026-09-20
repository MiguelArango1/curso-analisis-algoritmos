"""Experimento de la Parte 3: peor caso, mejor caso y caso promedio.

Corre insertion_sort con los tres escenarios de Tamiza (A, B y C) para
varios tamanos de entrada y mide tiempo y comparaciones. Al final guarda
parte3_comparaciones.png y parte3_tiempo.png en graficas/.
"""

import statistics
import time
from collections.abc import Callable
from pathlib import Path

import matplotlib.pyplot as plt

from algoritmos import insertion_sort
from datos import generar_aleatorio, generar_casi_ordenado, generar_inverso

TAMANOS = [100, 200, 400, 800, 1600, 3200, 6400]
REPETICIONES = 3
CARPETA_GRAFICAS = Path(__file__).parent / "graficas"

ESCENARIOS = {
    "A - Aleatorio": generar_aleatorio,
    "B - Casi ordenado": generar_casi_ordenado,
    "C - Orden inverso": generar_inverso,
}


def medir_escenario(
    generador: Callable[[int], list[int]], n: int
) -> tuple[float, int]:
    """Mide el tiempo mediano y las comparaciones de insertion_sort.

    Args:
        generador: funcion que produce el lote de datos para el tamano n.
        n: tamano del lote a generar y ordenar.

    Returns:
        Una tupla (tiempo_mediano_segundos, comparaciones).
    """
    tiempos = []
    comparaciones = 0
    for _ in range(REPETICIONES):
        datos = generador(n)
        inicio = time.perf_counter()
        _, comparaciones = insertion_sort(datos)
        fin = time.perf_counter()
        tiempos.append(fin - inicio)
    return statistics.median(tiempos), comparaciones


def ejecutar_experimento() -> dict:
    """Corre el experimento completo sobre los tres escenarios.

    Returns:
        Diccionario {nombre_escenario: {"tiempos": [...],
        "comparaciones": [...]}}.
    """
    resultados = {
        nombre: {"tiempos": [], "comparaciones": []} for nombre in ESCENARIOS
    }
    for nombre, generador in ESCENARIOS.items():
        for n in TAMANOS:
            tiempo, comparaciones = medir_escenario(generador, n)
            resultados[nombre]["tiempos"].append(tiempo)
            resultados[nombre]["comparaciones"].append(comparaciones)
            print(
                f"{nombre:20s} n={n:6d}  t={tiempo:.6f}s  "
                f"comparaciones={comparaciones}"
            )
    return resultados


def graficar_comparaciones(resultados: dict) -> None:
    """Genera parte3_comparaciones.png: comparaciones vs. tamano de entrada."""
    plt.figure(figsize=(8, 5))
    for nombre, datos in resultados.items():
        plt.plot(TAMANOS, datos["comparaciones"], marker="o", label=nombre)
    plt.title("Insertion sort: comparaciones vs. tamano de entrada")
    plt.xlabel("Tamano de entrada (n, numero de registros)")
    plt.ylabel("Numero de comparaciones")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(CARPETA_GRAFICAS / "parte3_comparaciones.png", dpi=150)
    plt.close()


def graficar_tiempo(resultados: dict) -> None:
    """Genera parte3_tiempo.png: tiempo de ejecucion vs. tamano de entrada."""
    plt.figure(figsize=(8, 5))
    for nombre, datos in resultados.items():
        plt.plot(TAMANOS, datos["tiempos"], marker="o", label=nombre)
    plt.title("Insertion sort: tiempo de ejecucion vs. tamano de entrada")
    plt.xlabel("Tamano de entrada (n, numero de registros)")
    plt.ylabel("Tiempo de ejecucion (segundos, mediana de 3 corridas)")
    plt.legend()
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(CARPETA_GRAFICAS / "parte3_tiempo.png", dpi=150)
    plt.close()


def main() -> None:
    """Corre el experimento y guarda las dos graficas de la Parte 3."""
    CARPETA_GRAFICAS.mkdir(exist_ok=True)
    resultados = ejecutar_experimento()
    graficar_comparaciones(resultados)
    graficar_tiempo(resultados)
    print(
        "\nGraficas guardadas en graficas/parte3_comparaciones.png "
        "y graficas/parte3_tiempo.png"
    )


if __name__ == "__main__":
    main()
