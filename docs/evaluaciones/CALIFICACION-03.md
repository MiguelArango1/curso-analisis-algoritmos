# Retroalimentación — Laboratorio 03: Estructuras de datos

**Estudiante:** Miguel Angel Arango Puerta · **Laboratorio:** Laboratorio evaluativo 03 — Estructuras de datos
**Fecha límite:** 2026-11-01 23:59 · **Versión revisada:** commit `e86214e`

Excelente trabajo: un laboratorio completo, ordenado y bien sustentado con sus propias mediciones.

## Nota

| Criterio | Puntos |
|---|---|
| Corrección conceptual | 20 / 20 |
| Calidad de la explicación teórica | 20 / 20 |
| Corrección de la implementación | 25 / 25 |
| Calidad del análisis de las gráficas | 25 / 25 |
| Documentación y organización del informe | 10 / 10 |
| **Total** | **100 / 100** |
| **Nota (0–5)** | **5.00** |

## 1. Corrección conceptual (20 / 20)
**Lo que hizo bien:**
- Explica bien la colisión y por qué ocurre aunque haya más casillas que guías, usando el ejemplo de 10, 24 y 17 con m = 7.
- Compara encadenamiento y direccionamiento abierto con ventajas y costos claros para cada uno.
- Justifica por qué la tabla no sirve para rangos y estima la altura (unos 400.000 niveles) y las comparaciones del árbol degenerado frente a unas 19 del equilibrado.
- Recomienda una combinación (tabla hash más árbol equilibrado) y declara que la cifra de 5.000.000 de envíos es una estimación, con su razonamiento.

## 2. Calidad de la explicación teórica (20 / 20)
**Lo que hizo bien:**
- Justifica el Θ(n) de la lista y el Θ(1 + α) de la tabla paso a paso.
- Nombra el supuesto de hash uniforme simple y explica que, si todas las guías caen en una casilla, la tabla se vuelve una lista de n nodos con búsqueda Θ(n).

## 3. Corrección de la implementación (25 / 25)
**Lo que hizo bien:**
- `ListaEnlazada` y `TablaHash` funcionan: búsquedas exitosas e infructuosas correctas, `buscar` iterativo y la tabla reutiliza la lista sin `dict`, `set` ni `hash()`.
- Las pruebas cubren la colisión con m = 7 (casilla 3 con longitud 3), el factor de carga 3/7 y 25 colecciones aleatorias; todas pasan.
- Docstrings con `Args` y `Returns`, type hints y dos líneas en blanco entre funciones en el código de las estructuras y de las mediciones.

## 4. Calidad del análisis de las gráficas (25 / 25)
**Lo que hizo bien:**
- Ambas gráficas tienen título, ejes rotulados con unidades y leyenda; la primera tiene siete valores de n con las dos curvas en los mismos ejes y la segunda seis valores de α.
- Calcula factores de crecimiento con cifras que coinciden con lo publicado y los contrasta con Θ(n), Θ(1) y Θ(1 + α).
- Reconoce con honestidad que la lista crece algo más rápido de lo esperado y que α = 1 sale más bajo que α = 0,25, y lo atribuye a ruido sin inventar causas.

## 5. Documentación y organización del informe (10 / 10)
**Lo que hizo bien:**
- Siguió la estructura acordada (`laboratorios/lab3-estructuras-datos/`) con todos los archivos del entregable.
- El informe sigue el orden pedido, tiene instrucciones de reproducción, enlaces a los `.py` y gráficas visibles con ruta relativa.
- Varios commits con mensajes descriptivos.

## ¿El código funciona?
Sí. Las pruebas pasan y la medición corre en menos de un minuto y vuelve a generar las dos gráficas.
