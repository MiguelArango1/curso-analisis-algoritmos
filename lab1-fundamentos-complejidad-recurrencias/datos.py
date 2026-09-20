"""Generadores de lotes de registros para los escenarios de Tamiza.

Los tres generadores producen n indices de riesgo enteros distintos
(los valores 0..n-1), lo que garantiza que sean comparables entre
escenarios de un mismo tamano. El orden objetivo de Tamiza es de
mayor a menor indice de riesgo.
"""

import random


def generar_aleatorio(n: int, semilla: int = 42) -> list[int]:
    """Genera un lote de n registros en orden aleatorio (escenario A).

    Args:
        n: cantidad de registros del lote.
        semilla: semilla del generador aleatorio, para que el
            experimento sea reproducible.

    Returns:
        Lista de n indices de riesgo enteros distintos, desordenada.
    """
    datos = list(range(n))
    generador = random.Random(semilla)
    generador.shuffle(datos)
    return datos


def generar_casi_ordenado(n: int, semilla: int = 42) -> list[int]:
    """Genera un lote casi ordenado: 98% ordenado y 2% al final (escenario B).

    Args:
        n: cantidad de registros del lote.
        semilla: semilla del generador aleatorio.

    Returns:
        Lista de n indices de riesgo enteros distintos, con el primer
        98% en el orden que el algoritmo produce (mayor a menor) y el
        2% restante desordenado al final.
    """
    generador = random.Random(semilla)
    corte = round(n * 0.98)
    ordenados = list(range(n - 1, n - corte - 1, -1))
    nuevos = list(range(n - corte))
    generador.shuffle(nuevos)
    return ordenados + nuevos


def generar_inverso(n: int) -> list[int]:
    """Genera un lote en el orden exactamente contrario (escenario C).

    Args:
        n: cantidad de registros del lote.

    Returns:
        Lista de n indices de riesgo enteros distintos, en el orden
        inverso al que el algoritmo debe producir (es decir, de menor
        a mayor, cuando el objetivo es de mayor a menor).
    """
    return list(range(n))
