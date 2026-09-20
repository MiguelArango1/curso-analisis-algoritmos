"""Algoritmos de ordenamiento instrumentados para el Laboratorio 1.

Los dos ordenan de MAYOR a MENOR, que es lo que necesita Tamiza para su
lista de llamadas (primero los pacientes con mas riesgo).
"""


def insertion_sort(datos: list[int]) -> tuple[list[int], int]:
    """Ordena una lista de indices de riesgo con el metodo de insercion.

    No modifica la lista recibida: trabaja sobre una copia. Ordena de
    mayor a menor.

    Args:
        datos: lista de indices de riesgo a ordenar.

    Returns:
        Una tupla con la lista ordenada y el numero total de
        comparaciones entre elementos realizadas durante el proceso.
    """
    resultado = list(datos)
    comparaciones = 0
    for i in range(1, len(resultado)):
        clave = resultado[i]
        j = i - 1
        while j >= 0:
            comparaciones += 1
            if resultado[j] < clave:
                resultado[j + 1] = resultado[j]
                j -= 1
            else:
                break
        resultado[j + 1] = clave
    return resultado, comparaciones


def merge_sort(datos: list[int]) -> tuple[list[int], int]:
    """Ordena una lista de indices de riesgo con el metodo de mezcla.

    No modifica la lista recibida: trabaja sobre una copia. Ordena de
    mayor a menor.

    Args:
        datos: lista de indices de riesgo a ordenar.

    Returns:
        Una tupla con la lista ordenada y el numero total de
        comparaciones entre elementos realizadas durante el proceso.
    """
    comparaciones = 0

    def _dividir(sublista: list[int]) -> list[int]:
        nonlocal comparaciones
        if len(sublista) <= 1:
            return list(sublista)
        medio = len(sublista) // 2
        izquierda = _dividir(sublista[:medio])
        derecha = _dividir(sublista[medio:])
        return _mezclar(izquierda, derecha)

    def _mezclar(izquierda: list[int], derecha: list[int]) -> list[int]:
        nonlocal comparaciones
        mezclada = []
        i = j = 0
        while i < len(izquierda) and j < len(derecha):
            comparaciones += 1
            if izquierda[i] >= derecha[j]:
                mezclada.append(izquierda[i])
                i += 1
            else:
                mezclada.append(derecha[j])
                j += 1
        mezclada.extend(izquierda[i:])
        mezclada.extend(derecha[j:])
        return mezclada

    return _dividir(datos), comparaciones
