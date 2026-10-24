# Retroalimentación — Laboratorio 2: Dividir y vencer

**Estudiante:** Miguel Angel Arango Puerta · **Laboratorio:** Laboratorio evaluativo 02 — Dividir y vencer
**Fecha límite:** 2026-10-21 23:59 · **Versión revisada:** commit `7f16979`

Excelente trabajo: un laboratorio completo, ordenado y apoyado en sus propias mediciones.

## Nota

| Criterio | Puntos |
|---|---|
| Corrección conceptual | 19 / 20 |
| Calidad de la explicación teórica | 19 / 20 |
| Corrección de la implementación | 25 / 25 |
| Calidad del análisis de las gráficas | 24 / 25 |
| Documentación y organización del informe | 10 / 10 |
| **Total** | **97 / 100** |
| **Nota (0–5)** | **4.85** |

## 1. Corrección conceptual (19 / 20)
**Lo que hizo bien:**
- Identificó con sus datos el cruce: en n = 20 gana la fuerza bruta y desde n = 50 gana divide y vencerás, y explicó por qué (las llamadas recursivas y los dos barridos pesan cuando n es pequeño).
- Comparó con el máximo de un arreglo: combinar cuesta una sola comparación, la recurrencia da `Θ(n)` y dividir no mejora nada.
- Recomendó divide y vencerás, declaró que el tiempo para 1.000.000 de registros es una estimación y la razonó sin regla de tres lineal.

**Lo que puede mejorar:**
- En la pregunta 4 podría decir con más claridad que la fuerza bruta del problema del máximo ya es `Θ(n)`, y por eso no hay nada que ganar dividiendo.

## 2. Calidad de la explicación teórica (19 / 20)
**Lo que hizo bien:**
- Explicó cada término de `T(n) = 2T(n/2) + Θ(n)`: dos mitades, barrido cruzado lineal y comparación de tres sumas.
- Aplicó el método maestro y verificó el caso 2 (`n^(log₂2) = n`).
- Justificó el `Θ(n²)` de la fuerza bruta con la suma `n + (n−1) + … + 1`.

**Lo que puede mejorar:**
- Al verificar el caso 2 hubiera sido bueno escribir explícitamente que `f(n) = Θ(n^(log_b a))`.

## 3. Corrección de la implementación (25 / 25)
**Lo que hizo bien:**
- Las tres funciones dan la suma correcta en todos los casos pedidos y coinciden con una comprobación independiente en cientos de listas aleatorias.
- `subarreglo_maximo` resuelve los tres casos sin llamar a la fuerza bruta y ninguna función cambia la lista recibida.
- Cumple PEP 8, con type hints y docstrings en todas las funciones. `pruebas.py` cubre todo lo pedido y más (25 listas aleatorias, el tramo devuelto suma lo que dice).

## 4. Calidad del análisis de las gráficas (24 / 25)
**Lo que hizo bien:**
- La gráfica tiene las dos curvas en los mismos ejes, título, ejes rotulados y leyenda, en escala lineal y logarítmica, con 12 tamaños (de 5 a 16000).
- Calculó el factor al duplicar n (8000 a 16000): cerca de 4,09 para la fuerza bruta y 2,08 para divide y vencerás, y lo contrastó con lo que predicen `Θ(n²)` y `Θ(n log n)`.
- Los valores que cita (por ejemplo 6,84 s y 25,2 ms en n = 16000) coinciden con la gráfica y con su tabla.

**Lo que puede mejorar:**
- Con un solo par de tamaños el factor puede engañar por el ruido de la medición; mostrar un segundo par (por ejemplo 2000 a 4000) daría más seguridad.

## 5. Documentación y organización del informe (10 / 10)
**Lo que hizo bien:**
- Estructura correcta (`laboratorios/lab2-divide-y-vencer/`), informe en el orden pedido, nombre completo, instrucciones de reproducción, enlaces a los `.py` y gráfica visible.
- Seis commits descriptivos del laboratorio.

## ¿El código funciona?
Sí. Las pruebas pasan, ambos algoritmos dan siempre la misma suma y la medición corre completa y genera la gráfica.

## Para el próximo laboratorio
- Repita el cálculo del factor de crecimiento en más de un par de tamaños y compare.
- Cuando verifique una condición del método maestro, escríbala completa.
- Mantenga el hábito de medir con repeticiones y de apoyar cada afirmación en sus propios datos.
- Siga haciendo commits pequeños con mensajes claros.
