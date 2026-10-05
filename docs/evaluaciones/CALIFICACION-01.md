# Retroalimentación — Laboratorio 1: Fundamentos, complejidad y recurrencias

**Estudiante:** Miguel Arango · **Laboratorio:** Laboratorio evaluativo 01 — Fundamentos, complejidad y recurrencias (Plataforma Tamiza)
**Fecha límite:** 2026-10-04 23:59 · **Versión revisada:** commit `b8b87ff`

Muy buen trabajo: un informe ordenado, con código correcto y conclusiones apoyadas en sus propias mediciones.

## Nota

| Criterio | Puntos |
|---|---|
| Corrección conceptual | 22 / 25 |
| Calidad de la explicación teórica | 23 / 25 |
| Corrección de la implementación | 19 / 20 |
| Calidad del análisis de las gráficas | 18 / 20 |
| Documentación y organización del informe | 8 / 10 |
| **Total** | **90 / 100** |
| **Nota (0–5)** | **4.50** |

## 1. Corrección conceptual (22 / 25)
**Lo que hizo bien:**
- Separa con claridad "correcto" de "viable" y nombra la restricción que Tamiza incumple: la ventana de cuatro horas.
- Explica con números (60 veces más registros, unas 3.600 veces más trabajo) por qué un servidor el doble de rápido no basta.
- El ejemplo propio (conciliación de inventarios en SAP) tiene volumen y restricción de tiempo.
- En la ética identifica dos perjuicios (el paciente y el operador del centro de contacto) y dice quién asume el costo de cada uno. También discute que el orden de la lista decide a quién se llama primero.

**Lo que puede mejorar:**
- En la parte ambiental falta un cálculo aunque sea aproximado (horas de servidor por noche y por año) para que el consumo no quede solo en palabras.
- En el ejemplo de Nutresa diga más o menos cuántos registros y cuánto dura la ventana de cierre.

## 2. Calidad de la explicación teórica (23 /25)
**Lo que hizo bien:**
- Define peor, mejor y caso promedio indicando sobre qué entradas se toma cada uno, justifica que usaría el peor caso y deja escrita la predicción antes de medir.
- Plantea `T(n) = 2T(n/2) + Θ(n)` explicando cada término y la resuelve con el árbol de recursión, con costo por nivel, número de niveles y costo total.
- El cálculo línea a línea de insertion sort y la tabla de complejidades están completos.

**Lo que puede mejorar:**
- En el caso promedio de insertion sort afirma que cada elemento se devuelve "más o menos la mitad" sin mostrar la suma; un paso más lo dejaría demostrado.
- Falta comentar si merge sort también tiene un mejor caso distinto en el conteo de comparaciones.

## 3. Corrección de la implementación (19 / 20)
**Lo que hizo bien:**
- `insertion_sort` y `merge_sort` ordenan bien (de mayor a menor, y lo declara), no cambian la lista recibida, cuentan solo comparaciones entre elementos y no usan `sorted()` ni `sort()`.
- `merge_sort` tiene su propia mezcla recursiva. Los generadores dan listas del tamaño pedido, sin repetidos y con semilla.
- El código cumple PEP 8, con type hints y docstrings en todas las funciones.

**Lo que puede mejorar:**
- En el escenario B, los registros nuevos que se anexan son todos más pequeños que los ya ordenados. En la realidad llegarían con valores mezclados, y eso haría el caso un poco más exigente.

## 4. Calidad del análisis de las gráficas (18 / 20)
**Lo que hizo bien:**
- Las tres gráficas tienen título, ejes rotulados, leyenda y las curvas pedidas en los mismos ejes.
- Identifica con datos el peor caso (C), el mejor (B) y el parecido al promedio (A), y verifica que `n(n-1)/2` coincide con lo medido.
- Describe lo que hace cada curva en la Parte 4 y lo contrasta con las complejidades calculadas.
- El concepto técnico recomienda merge sort, extrapola a 1.200.000 registros declarándolo como estimación, responde sobre el servidor con un dato medido y añade memoria y estabilidad.

**Lo que puede mejorar:**
- Su explicación de por qué merge sort gana desde n = 100 es una suposición ("creo que..."). Podría comprobarla con tamaños aún más pequeños.
- Las gráficas de tiempo se ven muy pegadas al eje para los tamaños pequeños; una escala logarítmica mostraría mejor la forma de las curvas.

## 5. Documentación y organización del informe (8 / 10)
**Lo que hizo bien:**
- Carpeta y archivos en el lugar acordado, README por partes, gráficas visibles y enlaces al código en las Partes 3 y 4.

**Lo que puede mejorar:**
- Las instrucciones de reproducción solo sirven para Windows; agregue el comando de activación para Mac/Linux.
- Los commits del laboratorio son descriptivos, pero fueron hechos todos en el mismo minuto; no muestran el avance real del trabajo. Haga commits a medida que avanza.

## ¿El código funciona?
Sí. Ambos scripts corren sin errores y generan las gráficas. Los dos algoritmos ordenaron bien en todas mis pruebas, incluidas listas vacías y de un elemento.

## Para el próximo laboratorio
- Haga commits pequeños mientras trabaja, no todos al final.
- Agregue un cálculo aproximado de consumo o de costo cuando hable de impacto ambiental.
- Muestre las sumas completas cuando afirme una complejidad promedio.
- Pruebe escalas logarítmicas en las gráficas cuando las curvas tengan tamaños muy distintos.
- Incluya instrucciones de reproducción para varios sistemas operativos.
