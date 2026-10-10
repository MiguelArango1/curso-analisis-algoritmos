"""Subarreglo maximo: fuerza bruta y divide y venceras."""


def subarreglo_fuerza_bruta(valores: list[float]) -> tuple[int, int, float]:
    """Encuentra la mejor racha probando todos los pares de dias (i, j).

    Args:
        valores: variacion diaria de caja, una por dia. Tiene al menos
            un elemento.

    Returns:
        Una tupla (inicio, fin, suma) con los indices inclusivos del
        tramo de mayor suma y el valor de esa suma.
    """
    mejor_inicio = 0
    mejor_fin = 0
    mejor_suma = valores[0]
    for i in range(len(valores)):
        suma = 0
        for j in range(i, len(valores)):
            suma += valores[j]
            if suma > mejor_suma:
                mejor_inicio = i
                mejor_fin = j
                mejor_suma = suma
    return mejor_inicio, mejor_fin, mejor_suma


def suma_cruzada(
    valores: list[float], inicio: int, medio: int, fin: int
) -> tuple[int, int, float]:
    """Encuentra el mejor tramo que cruza el punto medio.

    Args:
        valores: variacion diaria de caja.
        inicio: indice inicial del rango considerado (inclusive).
        medio: indice del ultimo elemento de la mitad izquierda.
        fin: indice final del rango considerado (inclusive).

    Returns:
        Una tupla (inicio, fin, suma) del mejor tramo que incluye al
        menos un elemento de cada mitad.
    """
    suma = 0
    mejor_izquierda = valores[medio]
    indice_izquierda = medio
    for i in range(medio, inicio - 1, -1):
        suma += valores[i]
        if suma > mejor_izquierda:
            mejor_izquierda = suma
            indice_izquierda = i

    suma = 0
    mejor_derecha = valores[medio + 1]
    indice_derecha = medio + 1
    for j in range(medio + 1, fin + 1):
        suma += valores[j]
        if suma > mejor_derecha:
            mejor_derecha = suma
            indice_derecha = j

    return indice_izquierda, indice_derecha, mejor_izquierda + mejor_derecha


def subarreglo_maximo(
    valores: list[float], inicio: int, fin: int
) -> tuple[int, int, float]:
    """Encuentra la mejor racha por divide y venceras.

    Args:
        valores: variacion diaria de caja.
        inicio: indice inicial del rango a considerar (inclusive).
        fin: indice final del rango a considerar (inclusive).

    Returns:
        Una tupla (inicio, fin, suma) del mejor tramo dentro de
        valores[inicio..fin].
    """
    if inicio == fin:
        return inicio, fin, valores[inicio]

    medio = (inicio + fin) // 2
    izquierdo = subarreglo_maximo(valores, inicio, medio)
    derecho = subarreglo_maximo(valores, medio + 1, fin)
    cruzado = suma_cruzada(valores, inicio, medio, fin)

    mejor = izquierdo
    if derecho[2] > mejor[2]:
        mejor = derecho
    if cruzado[2] > mejor[2]:
        mejor = cruzado
    return mejor
