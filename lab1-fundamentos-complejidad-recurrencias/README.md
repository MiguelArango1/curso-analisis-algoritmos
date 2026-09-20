# Laboratorio evaluativo 01: Fundamentos, complejidad y recurrencias

**Autor:** Miguel Arango (miguelarangop36@gmail.com)

## Cómo reproducir el experimento

Desde la raíz del repositorio (`curso-analisis-algoritmos/`):

```bash
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
cd lab1-fundamentos-complejidad-recurrencias
```

Y para correr cada parte:

```bash
python parte3_casos.py        # Parte 3: peor caso, mejor caso, caso promedio
python parte4_complejidad.py  # Parte 4: insertion sort vs merge sort
```

Cada script imprime en consola el tiempo y las comparaciones por tamaño de entrada, y guarda las gráficas en `graficas/`.

En todo el laboratorio ordeno de mayor a menor índice de riesgo, que es lo que necesita Tamiza. Por eso el escenario C (orden inverso) es una lista de menor a mayor.

---

## Parte 1. Analizar el algoritmo antes de comprar hardware

Que Tamiza lleve ocho años sacando la lista bien no quiere decir que el algoritmo sirva. Correcto es que la lista salga ordenada por riesgo, y eso insertion sort lo cumple siempre. Viable es que salga dentro de la restricción de tiempo: la ventana de cuatro horas (2:00 a. m. a 6:00 a. m.), que no se mueve porque a las 6 el centro de contacto ya necesita la lista. Esa es la que Tamiza incumple, ya van tres veces en las últimas semanas.

El problema de fondo es que insertion sort no escala: sus comparaciones crecen con el cuadrado del tamaño del lote. Con 20.000 registros aguantaba, pero con 1.200.000 (60 veces más) el costo se multiplicó por unas 3.600. Un servidor del doble de velocidad divide el tiempo entre dos como mucho, y eso casi no cambia nada frente a 3.600. Cuando amplíen el programa otra vez toca comprar otro. Cambiar hardware para tapar un algoritmo malo es botar la plata, lo que toca cambiar es el algoritmo.

Me pasa algo parecido en Nutresa, donde manejo procesos en SAP sobre millones de registros, como la conciliación de movimientos de inventario entre plantas y centros de distribución al cierre del período. El resultado siempre sale correcto, pero tiene que terminar dentro de la ventana de cierre antes de que otros equipos necesiten esos datos, y cuando el volumen crece (más plantas, promociones, fin de mes) empieza a rozar ese límite.

---

## Parte 2. Responsabilidad ambiental y ética de la implementación

Un servidor gasta energía mientras trabaja, así que más tiempo de cómputo es más consumo. Con insertion sort, para 1.200.000 registros la estimación (Parte 4) es de varias horas con el servidor a tope, y eso pasa todas las noches, 365 al año, durante años. Unos minutos de más por noche, multiplicados por miles de noches, son muchos kWh y huella de carbono que nadie ve porque "todo sigue funcionando". Un servidor más grande lo empeora, porque gasta más cada noche, mientras que arreglar el algoritmo baja el tiempo sin agregar consumo.

En lo ético veo dos problemas. El primero es el paciente: si a las 6 a. m. el proceso no terminó, el centro de contacto trabaja con una lista mocha, y un paciente de riesgo alto que quedó de último puede no salir en las llamadas del día. Ese costo lo asume el paciente. El segundo es el operador del centro de contacto: abre la lista, confía en ella y llama sin saber que está incompleta, y si hay un reclamo le echan la culpa a él cuando el problema es un algoritmo mal dimensionado. Paga los platos rotos.

Como el orden decide a quién se llama primero, no basta con que el proceso termine: la lista tiene que salir completa y bien ordenada, porque si falla, falla en los primeros puestos, que son los pacientes más graves.

---

## Parte 3. Peor caso, mejor caso y caso promedio, demostrados en Python

Código de esta parte: [algoritmos.py](algoritmos.py) (`insertion_sort`), [datos.py](datos.py) (generadores de escenarios) y [parte3_casos.py](parte3_casos.py) (el experimento).

### 3.1 Explicación

Fijo un tamaño de entrada `n` y miro todas las formas en que pueden llegar esos `n` registros (todas las permutaciones). Sobre ese conjunto:

- **Peor caso:** el máximo de comparaciones o tiempo, la entrada que más sufrir hace al algoritmo.
- **Mejor caso:** el mínimo, la entrada más favorable.
- **Caso promedio:** el promedio del costo sobre todas esas entradas, asumiendo que cualquier orden es igual de probable.

Para decidir si entra a producción miraría el peor caso: la ventana no se negocia, y con el promedio el día que llegue un lote malo (como el C) el proceso no termina, que es lo que ya pasó tres veces.

Mi predicción antes de medir: el C (inverso) es el peor caso porque cada elemento recorre todo lo anterior, el B (casi ordenado) es el mejor porque casi no hay que mover nada, y el A (aleatorio) queda cerca del promedio.

### 3.2 Demostración experimental

![Comparaciones vs. tamaño de entrada](graficas/parte3_comparaciones.png)

![Tiempo vs. tamaño de entrada](graficas/parte3_tiempo.png)

Medí siete tamaños (100, 200, 400, 800, 1600, 3200 y 6400) y cada tiempo es la mediana de 3 corridas. Con `n = 6400`:

| Escenario | Comparaciones | Tiempo (s) |
|---|---|---|
| A. Aleatorio | 10.276.753 | 1.0718 |
| B. Casi ordenado | 10.649 | 0.0012 |
| C. Orden inverso | 20.476.800 | 2.1268 |

El C es el peor caso y el B el mejor, como predije. El A hace casi la mitad de comparaciones que el C en todos los tamaños, o sea que se parece al promedio. Además las 20.476.800 del C son exactamente `n(n-1)/2`.

Un detalle: el mejor caso real (lista ya en el orden final) haría `n - 1` = 6.399 comparaciones. El B tiene 10.649 por el 2 % desordenado del final, pero igual queda muy cerca.

---

## Parte 4. Complejidad de merge sort e insertion sort: cálculo y validación

Código de esta parte: [algoritmos.py](algoritmos.py) (`merge_sort`) y [parte4_complejidad.py](parte4_complejidad.py) (el experimento comparativo).

### 4.1 Cálculo teórico

La recurrencia de merge sort es `T(n) = 2T(n/2) + Θ(n)`. El 2 sale de que cada llamada se parte en dos subproblemas (mitad izquierda y mitad derecha). El `T(n/2)` es porque cada uno tiene la mitad del tamaño. Y el `Θ(n)` es el costo de combinar: mezclar las dos mitades ya ordenadas recorre los `n` elementos una sola vez, con una comparación por cada elemento que entra a la lista final.

La resuelvo con árbol de recursión:

```
Nivel 0:                    n                              costo: c*n
                            / \
Nivel 1:               n/2      n/2                        costo: 2 * c*(n/2)     = c*n
                       /  \      /  \
Nivel 2:            n/4  n/4  n/4  n/4                      costo: 4 * c*(n/4)     = c*n
                     ...                ...
Nivel i:        (2^i subproblemas de tamaño n/2^i)          costo: 2^i * c*(n/2^i) = c*n
                     ...                ...
Nivel log2(n):  (n subproblemas de tamaño 1)                costo: n * c*(1)       = c*n
```

Cada nivel cuesta `c*n`: al bajar un nivel hay el doble de subproblemas pero cada uno es la mitad de grande, y eso se compensa. La recursión termina cuando el tamaño llega a 1, o sea cuando `n / 2^i = 1`, es decir `i = log2(n)`. Con el nivel 0 son `log2(n) + 1` niveles.

Costo total = costo por nivel × número de niveles = `c*n × (log2(n) + 1) = c*n*log2(n) + c*n`. Manda el término `c*n*log2(n)`, así que T(n) = Θ(n log n).

Para insertion sort lo hago línea por línea con mi implementación de [algoritmos.py](algoritmos.py). Llamo `tᵢ` al número de veces que se evalúa la condición del while para acomodar el elemento `i`, o sea cuántos puestos se devuelve:

| Línea | Costo | Veces que se ejecuta |
|---|---|---|
| `for i in range(1, n):` | c₁ | n |
| `clave = resultado[i]` | c₂ | n − 1 |
| `j = i - 1` | c₃ | n − 1 |
| `while j >= 0:` (control) | c₄ | Σ tᵢ |
| `if resultado[j] < clave:` (comparación) | c₅ | Σ tᵢ |
| `resultado[j+1] = resultado[j]; j -= 1` | c₆ | Σ (tᵢ − 1) |
| `resultado[j+1] = clave` | c₇ | n − 1 |

El cuello de botella son las sumatorias, o sea el while.

- **Mejor caso** (ya viene en el orden final): el while se evalúa una sola vez por elemento y falla de una (tᵢ = 1), sin desplazamientos. Sumando todo queda una expresión lineal, `c₁n + (c₂+c₃+c₄+c₅+c₇)(n-1)`, que es Θ(n).
- **Peor caso** (viene al revés): cada elemento se devuelve hasta el principio (tᵢ = i). Σ tᵢ es la suma de los primeros n números, `n(n-1)/2`, y como n se multiplica por n queda un término cuadrático: Θ(n²).
- **Caso promedio** (al azar): cada elemento se devuelve más o menos la mitad (tᵢ ≈ i/2). La suma sigue dando algo proporcional a n², con una constante más chica: Θ(n²).

| Algoritmo | Mejor caso | Caso promedio | Peor caso |
|---|---|---|---|
| Insertion sort | Θ(n) | Θ(n²) | Θ(n²) |
| Merge sort | Θ(n log n) | Θ(n log n) | Θ(n log n) |

### 4.2 Validación experimental

![Insertion sort vs. merge sort](graficas/parte4_tiempo.png)

Tiempos sobre el escenario A (mediana de 3 corridas), con los mismos siete tamaños de la Parte 3. Aquí van tres:

| n | Insertion sort (s) | Merge sort (s) |
|---|---|---|
| 100 | 0.000251 | 0.000167 |
| 1.600 | 0.066490 | 0.003904 |
| 6.400 | 1.070307 | 0.017794 |

La curva de insertion sort se dispara: con n 64 veces mayor (de 100 a 6.400) el tiempo se multiplica por casi 4.300, cerca de 64² = 4.096. La de merge sort casi no se despega del eje: solo se multiplica por unas 107, que va con n log n. Desde n ≈ 800 la brecha ya se ve a simple vista. Para Tamiza es mejor merge sort.

Coincide con 4.1 (Θ(n²) contra Θ(n log n)). Lo raro es que merge sort suele arrancar más lento con tamaños chicos por las llamadas recursivas y las listas nuevas, y aquí ya gana desde n = 100. Creo que es porque insertion sort ya hace 2.542 comparaciones ahí y su costo cuadrático supera ese costo fijo desde muy temprano.

### 4.3 Concepto técnico a la Secretaría de Salud

Para el equipo de ingeniería de la Plataforma Tamiza:

Recomiendo reemplazar insertion sort por merge sort en todo el proceso nocturno, sin importar el canal de origen.

Como el canal puede cambiar sin aviso y no conviene mantener tres implementaciones, escogí el algoritmo cuyo tiempo no depende de cómo llegue el lote. Insertion sort solo es rápido con datos casi ordenados (escenario B); si cambia el flujo de reproceso o el sistema legado manda todo al revés (C), el proceso se cae. Merge sort hace Θ(n log n) llegue como llegue el lote: en mis pruebas ordenó 6.400 registros aleatorios en 0,0178 s. Además con una sola implementación el equipo mantiene y prueba un solo código, en vez de tres ramas según el canal y de tener que detectar cuál está llegando.

¿Cabe en las cuatro horas con 1.200.000 registros? Es una estimación, no una medición: no corrí el algoritmo con ese volumen, extrapolo desde n = 6.400 con la forma de cada curva de la gráfica de la Parte 4. Con n multiplicado por 187,5:

- Insertion sort es cuadrático, el tiempo se multiplica por 187,5² ≈ 35.156. Desde el peor caso medido (2,1268 s en C) da unas 20,8 horas, y desde el aleatorio (1,0718 s) unas 10,5. Ambas pasan de las 4 horas, lo que cuadra con las tres veces que el proceso no terminó.
- Merge sort es n log n, el tiempo se multiplica por 187,5 × (log2(1.200.000)/log2(6.400)) ≈ 299. Desde 0,0178 s da unos 5,3 segundos. Aunque en la realidad fuera 10 veces peor por memoria y hardware, sería cerca de un minuto.

Sobre el servidor del doble de velocidad: no lo compraría. Como mucho divide el tiempo entre dos, y las 20,8 horas quedarían en unas 10,4, más del doble de la ventana. En la gráfica de la Parte 4, con n = 6.400, insertion sort tarda 1,07 s y merge sort 0,018 s en la misma máquina, unas 60 veces menos sin comprar nada.

Aparte del tiempo, merge sort usa memoria extra, del orden de Θ(n), por las listas temporales de la mezcla; con 1.200.000 enteros es una cantidad razonable y predecible, mucho más barata que fallar la ventana. Los dos son estables, así que los pacientes con el mismo índice de riesgo mantienen el orden en que llegaron. Y insertion sort solo sirve mientras el reproceso siga entregando lotes casi ordenados, dependencia que se quita migrando a merge sort.
