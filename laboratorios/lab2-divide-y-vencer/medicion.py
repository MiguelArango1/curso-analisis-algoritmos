"""Medicion del subarreglo maximo: fuerza bruta contra divide y venceras.

Genera listas con semilla fija, mide cuanto se demora cada algoritmo con
la misma lista y guarda la grafica graficas/tiempo_vs_n.png.
"""

import random
import statistics
import time
from collections.abc import Callable
from pathlib import Path

import matplotlib.pyplot as plt

from subarreglo import subarreglo_fuerza_bruta, subarreglo_maximo

TAMANOS = [5, 10, 20, 50, 100, 200, 500, 1000, 2000, 4000, 8000, 16000]
REPETICIONES = 3
SEMILLA = 42
CARPETA_GRAFICAS = Path(__file__).parent / "graficas"


def generar_serie(n: int, semilla: int = SEMILLA) -> list[int]:
    """Genera una serie de n variaciones enteras entre -100 y 100.

    Args:
        n: cantidad de dias de la serie.
        semilla: semilla del generador, para poder repetir la medicion.

    Returns:
        Lista de n enteros.
    """
    generador = random.Random(semilla)
    return [generador.randint(-100, 100) for _ in range(n)]


def llamadas_por_medicion(n: int) -> int:
    """Cuantas veces se llama el algoritmo dentro de una medicion.

    Con listas muy chicas una sola llamada dura microsegundos y el reloj
    casi no la distingue, asi que se repite y se divide el tiempo.

    Args:
        n: tamano de la serie.

    Returns:
        Numero de llamadas seguidas que se cronometran juntas.
    """
    if n <= 100:
        return 500
    if n <= 1000:
        return 20
    return 1


def medir(algoritmo: Callable[[], tuple[int, int, float]], n: int) -> float:
    """Mide el tiempo mediano de una sola llamada al algoritmo.

    Args:
        algoritmo: funcion sin argumentos que ejecuta el algoritmo.
        n: tamano de la serie, para decidir cuantas llamadas agrupar.

    Returns:
        Mediana, en segundos, del tiempo de una llamada.
    """
    llamadas = llamadas_por_medicion(n)
    tiempos = []
    for _ in range(REPETICIONES):
        inicio = time.perf_counter()
        for _ in range(llamadas):
            algoritmo()
        fin = time.perf_counter()
        tiempos.append((fin - inicio) / llamadas)
    return statistics.median(tiempos)


def ejecutar_experimento() -> tuple[list[float], list[float]]:
    """Mide los dos algoritmos en todos los tamanos.

    Returns:
        Dos listas con los tiempos (s) de fuerza bruta y de divide y
        venceras, en el orden de TAMANOS.
    """
    tiempos_fb = []
    tiempos_dc = []
    for n in TAMANOS:
        serie = generar_serie(n)
        suma_fb = subarreglo_fuerza_bruta(serie)[2]
        suma_dc = subarreglo_maximo(serie, 0, n - 1)[2]
        assert suma_fb == suma_dc, f"las sumas no coinciden en n={n}"

        t_fb = medir(lambda: subarreglo_fuerza_bruta(serie), n)
        t_dc = medir(lambda: subarreglo_maximo(serie, 0, n - 1), n)
        tiempos_fb.append(t_fb)
        tiempos_dc.append(t_dc)
        print(
            f"n={n:6d}  fuerza bruta={t_fb:.8f}s  "
            f"divide y venceras={t_dc:.8f}s  suma={suma_fb}"
        )
    return tiempos_fb, tiempos_dc


def mostrar_duplicaciones(
    tiempos_fb: list[float], tiempos_dc: list[float]
) -> None:
    """Imprime cuanto se multiplica el tiempo cuando n se duplica.

    Args:
        tiempos_fb: tiempos de fuerza bruta.
        tiempos_dc: tiempos de divide y venceras.
    """
    print("\nCuando n se duplica, el tiempo se multiplica por:")
    for i in range(1, len(TAMANOS)):
        if TAMANOS[i] == 2 * TAMANOS[i - 1]:
            print(
                f"  {TAMANOS[i - 1]:6d} -> {TAMANOS[i]:6d}  "
                f"fuerza bruta x{tiempos_fb[i] / tiempos_fb[i - 1]:.2f}  "
                f"divide y venceras x{tiempos_dc[i] / tiempos_dc[i - 1]:.2f}"
            )


def graficar(tiempos_fb: list[float], tiempos_dc: list[float]) -> None:
    """Guarda graficas/tiempo_vs_n.png con escala lineal y logaritmica.

    Args:
        tiempos_fb: tiempos de fuerza bruta.
        tiempos_dc: tiempos de divide y venceras.
    """
    figura, ejes = plt.subplots(1, 2, figsize=(12, 5))
    escalas = [("linear", "Escala lineal"), ("log", "Escala logarítmica")]
    for eje, (escala, titulo) in zip(ejes, escalas):
        eje.plot(TAMANOS, tiempos_fb, marker="o", label="Fuerza bruta")
        eje.plot(TAMANOS, tiempos_dc, marker="s", label="Divide y vencerás")
        eje.set_xscale(escala)
        eje.set_yscale(escala)
        eje.set_title(f"Subarreglo máximo: tiempo vs. n ({titulo})")
        eje.set_xlabel("Tamaño de entrada n (número de días)")
        eje.set_ylabel("Tiempo de ejecución (segundos)")
        eje.legend()
        eje.grid(True, linestyle="--", alpha=0.5)
    figura.tight_layout()
    figura.savefig(CARPETA_GRAFICAS / "tiempo_vs_n.png", dpi=150)
    plt.close(figura)


def main() -> None:
    """Corre el experimento, imprime los resultados y guarda la grafica."""
    CARPETA_GRAFICAS.mkdir(exist_ok=True)
    tiempos_fb, tiempos_dc = ejecutar_experimento()
    mostrar_duplicaciones(tiempos_fb, tiempos_dc)
    graficar(tiempos_fb, tiempos_dc)
    print("\nGrafica guardada en graficas/tiempo_vs_n.png")


if __name__ == "__main__":
    main()
