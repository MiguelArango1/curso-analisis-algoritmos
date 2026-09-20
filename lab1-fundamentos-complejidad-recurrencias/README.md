# Laboratorio evaluativo 01 — Fundamentos, complejidad y recurrencias

**Autor:** Miguel Arango — miguelarangop36@gmail.com

## Instrucciones para reproducir el experimento

Desde la raíz del repositorio (`curso-analisis-algoritmos/`):

```bash
# 1. Activar el entorno virtual (PowerShell)
.\venv\Scripts\Activate.ps1

# 2. Verificar que matplotlib está instalado (ya está en requirements.txt)
pip install -r requirements.txt

# 3. Entrar a la carpeta del laboratorio
cd lab1-fundamentos-complejidad-recurrencias
```

Para correr cada parte práctica:

```bash
# Parte 3: peor caso, mejor caso, caso promedio de insertion sort
python parte3_casos.py

# Parte 4: insertion sort vs. merge sort
python parte4_complejidad.py
```

Cada script imprime en consola el tiempo y las comparaciones por tamaño de entrada, y regenera las gráficas en `graficas/`.

---

## Parte 1 — Analizar el algoritmo antes de comprar hardware

Que Tamiza lleve ocho años entregando el resultado correcto no dice nada sobre si cabe en la ventana que tiene para entregarlo. Son dos preguntas distintas. La **corrección** responde si, dado un lote de registros, el algoritmo produce la lista ordenada por índice de riesgo que se espera: eso insertion sort lo cumple siempre, sin importar el tamaño del lote. La **eficiencia** responde algo distinto: si ese resultado correcto llega a tiempo, dentro de la restricción de recursos que el sistema tiene — aquí, una ventana de cuatro horas, entre las 2:00 a. m. y las 6:00 a. m., no negociable porque a esa hora el centro de contacto ya necesita la lista para empezar a llamar. Un algoritmo puede ser perfectamente correcto y, al mismo tiempo, incumplir esa restricción de tiempo. Eso es lo que le pasa a Tamiza: la restricción concreta que incumple es la ventana nocturna de cuatro horas, y ya la incumplió tres veces en las últimas semanas.

La razón de fondo es que insertion sort no escala linealmente con el volumen de datos: el número de comparaciones que hace crece con el cuadrado del tamaño del lote. Con 20.000 registros ese costo cuadrático era manejable. Con 1.200.000 — sesenta veces más volumen —, el costo no creció sesenta veces: creció aproximadamente sesenta al cuadrado, unas 3.600 veces. Duplicar la velocidad del servidor, en el mejor de los casos, divide ese tiempo entre dos. Frente a un costo multiplicado por 3.600, una mejora de 2x no resuelve nada de fondo: alivia el síntoma un tiempo corto, hasta la próxima ampliación del programa, y entonces la Secretaría vuelve a la misma decisión, comprando servidores cada vez más caros para compensar un algoritmo cuyo costo crece más rápido que cualquier mejora de hardware razonable. El problema no es la velocidad del procesador; es cómo crece el costo del algoritmo con el tamaño de la entrada, y eso solo se corrige cambiando el algoritmo.

<!-- EDITAR: el siguiente es un ejemplo de referencia; reemplácelo por un caso realmente suyo antes de entregar, siguiendo el mismo nivel de detalle (qué se procesa, cuántos datos, qué restricción se incumple). -->
Un segundo ejemplo, distinto de Tamiza: un script propio para cruzar y depurar listas de asistencia de un evento universitario, exportadas en CSV desde varios formularios. Comparaba cada fila contra todas las demás para detectar inscripciones duplicadas (doble bucle anidado), sobre unos 15.000 registros acumulados en el semestre. El resultado siempre era correcto: detectaba todas las duplicidades. El problema fue el tiempo: el script debía correr cada vez que se actualizaba la pantalla de verificación en la entrada, con un margen práctico de un par de minutos, y al crecer el CSV el cruce terminó tardando más que ese margen. Ahí también un algoritmo correcto —nunca dejó pasar un duplicado— se volvió inviable frente al tiempo real del proceso que lo usaba.

---

## Parte 2 — Responsabilidad ambiental y ética de la implementación

**Dimensión ambiental.** El servidor que corre Tamiza consume energía en proporción al tiempo que el procesador está activo: más tiempo de cómputo, en el mismo hardware, es más potencia sostenida durante más horas. Con insertion sort, ese tiempo deja de ser una franja corta de la madrugada: como muestro en la Parte 4, para 1.200.000 registros el proceso se estima en el orden de varias horas, con el servidor a carga alta durante buena parte —o la totalidad— de la ventana nocturna, y a veces desbordándose hacia el horario diurno. Ese consumo no es un evento aislado: el proceso corre todas las madrugadas, 365 noches al año, durante los años que la plataforma siga en producción. Una diferencia de minutos por noche, multiplicada por miles de noches, se traduce en un consumo eléctrico acumulado —y una huella de carbono acumulada, según la matriz energética de ese centro de datos— que crece silenciosamente mientras "todo sigue funcionando". Comprar un servidor más grande no revierte esa tendencia: la sube, porque ese hardware más potente consume más cada una de esas 365 noches, de forma permanente, mientras que corregir el algoritmo reduce directamente el producto tiempo × potencia sin agregar consumo adicional.

**Dimensión ética.** Identifico dos perjuicios concretos:

1. **El paciente de alto riesgo que queda fuera de la lista de llamadas del día.** Cuando el proceso no termina antes de las 6:00 a. m., el centro de contacto trabaja con una lista parcial y sin ordenar por riesgo. Un paciente con un índice de riesgo altísimo, cuyo registro llegó tarde en el lote o quedó del lado del corte, puede no ser contactado ese día, retrasando una valoración cardiovascular que se supone prioritaria. Quien asume el costo de ese error es, directamente, **el paciente**: un riesgo que el sistema ya detectó, pero que no se tradujo en una llamada a tiempo.
2. **El operador del centro de contacto.** A las 6:00 a. m. esa persona abre una lista que puede venir incompleta o sin el orden correcto, sin saber que así es. Llama en un orden que ya no prioriza correctamente, y cuando alguien pregunta por qué un paciente crítico no fue contactado, la explicación —o el reclamo— cae sobre el centro de contacto, no sobre la causa real, que es un algoritmo mal dimensionado. Quien asume ese costo es **el operador**: trabaja con una herramienta que le falló sin que él tuviera forma de saberlo o corregirlo, y carga con la responsabilidad de un error que no le pertenece.

**Una tensión propia de este caso.** El orden de la lista no es un detalle estético: decide literalmente a quién se llama primero. Eso impone una obligación que va más allá de terminar a tiempo: el ordenamiento tiene que ser *correcto en el orden relativo de los primeros lugares*, no solo "completo eventualmente". Un algoritmo que, presionado por el tiempo, se corta a la mitad y entrega una lista parcial no ordenada no falla de forma neutral: falla concentrando el error exactamente donde más importa, en la cabeza de la lista, que es la que se usa primero. Por eso la solución no puede ser únicamente "que el proceso termine dentro de la ventana": tiene que terminar dentro de la ventana *produciendo* una lista íntegramente ordenada por riesgo, porque una lista a medias no es una versión aceptable del resultado en un sistema donde el orden decide quién recibe atención primero.

---

## Parte 3 — Peor caso, mejor caso y caso promedio, demostrados en Python

Código de esta parte: [`algoritmos.py`](algoritmos.py) (implementación de `insertion_sort`), [`datos.py`](datos.py) (generadores de escenarios) y [`parte3_casos.py`](parte3_casos.py) (experimento).

### 3.1 — Explicación

- **Peor caso:** sobre el conjunto de *todas* las entradas posibles de un tamaño fijo `n`, es el **máximo** número de comparaciones (o tiempo) que el algoritmo puede necesitar. Es una cota que ninguna entrada de ese tamaño supera.
- **Mejor caso:** sobre ese mismo conjunto de entradas de tamaño `n`, es el **mínimo** número de comparaciones (o tiempo) que el algoritmo puede necesitar.
- **Caso promedio:** sobre ese mismo conjunto de entradas de tamaño `n`, es el **promedio** de comparaciones (o tiempo), asumiendo una distribución de probabilidad sobre las entradas (típicamente, que cada arreglo de entrada es igual de probable).

Los tres se definen sobre un tamaño de entrada fijo `n` y varían sobre el conjunto de entradas posibles de ese tamaño — no son "un caso malo" al azar, sino un máximo, un mínimo y un promedio bien definidos sobre ese conjunto.

**¿Cuál caso usar para decidir si el algoritmo entra en producción?** El **peor caso**. La ventana de Tamiza es estricta y no negociable: a las 6:00 a. m. el centro de contacto abre, pase lo que pase con el proceso nocturno. Si la decisión se basara en el caso promedio, el sistema quedaría expuesto a que, el día en que llegue una entrada desfavorable (por ejemplo, una migración que entregue los datos en orden inverso, como el escenario C), el proceso no termine — que es exactamente lo que ya ocurrió tres veces. Solo garantizar el peor caso dentro de la ventana asegura que el proceso *siempre* quepa, sin importar cómo llegue el lote ese día.

**Predicción, antes de medir:** insertion sort ordena comparando cada elemento nuevo contra los ya ordenados y desplazándolo hasta su posición. Predigo que el **escenario C (orden inverso)** es el peor caso, porque cada elemento nuevo tiene que compararse y desplazarse contra *todos* los anteriores. Predigo que el **escenario B (casi ordenado)** es el mejor caso, porque el 98 % del lote ya viene en el orden que el algoritmo produce y casi no requiere desplazamientos. El **escenario A (aleatorio)** debería aproximarse al caso promedio, al no tener ninguna estructura particular.

### 3.2 — Demostración experimental

![Comparaciones vs. tamaño de entrada](graficas/parte3_comparaciones.png)

![Tiempo vs. tamaño de entrada](graficas/parte3_tiempo.png)

Resultados medidos para `n = 6400` (mediana de 3 corridas):

| Escenario | Comparaciones | Tiempo (s) |
|---|---|---|
| A — Aleatorio | 10.276.753 | 1.0718 |
| B — Casi ordenado | 10.649 | 0.0012 |
| C — Orden inverso | 20.476.800 | 2.1268 |

El escenario **C resultó ser el peor caso** y el escenario **B el mejor caso**, tal como predije. El escenario **A se aproxima al caso promedio**: sus comparaciones quedan cerca de la mitad de las del escenario C en cada tamaño (10.276.753 frente a 20.476.800 en `n = 6400`), consistente con que, en promedio, un elemento aleatorio se desplaza hasta la mitad del prefijo ya ordenado en vez de hasta el inicio. Como verificación adicional: el valor medido en el escenario C, 20.476.800, coincide exactamente con `n(n-1)/2 = 6400 × 6399 / 2`, la fórmula cerrada del peor caso de insertion sort.

La predicción se confirma, con un matiz en el escenario B: el mejor caso *teórico* de insertion sort es una entrada ya completamente ordenada en el sentido que el algoritmo produce, que exige exactamente `n - 1` comparaciones. El escenario B no es ese caso exacto —tiene 10.649 comparaciones en `n = 6400`, no 6.399—, porque el 2 % final sí está desordenado y exige desplazamientos. Aun así, se aproxima mucho más al mejor caso que A o C, precisamente porque solo esa fracción pequeña del lote requiere trabajo real; el resto del recorrido es una sola comparación por elemento, igual que en el mejor caso absoluto.

---

## Parte 4 — Complejidad de merge sort e insertion sort: cálculo y validación

Código de esta parte: [`algoritmos.py`](algoritmos.py) (implementación de `merge_sort`) y [`parte4_complejidad.py`](parte4_complejidad.py) (experimento comparativo).

### 4.1 — Cálculo teórico

**Recurrencia de merge sort.** `T(n) = 2T(n/2) + Θ(n)`. Cada término sale de dividir el problema en dos mitades y combinarlas:

- `2`: cada llamada a merge sort sobre un lote de tamaño `n` genera **dos** subproblemas (la mitad izquierda y la mitad derecha).
- `T(n/2)`: cada subproblema tiene, cada uno, tamaño **n/2** (se parte el lote exactamente a la mitad).
- `Θ(n)`: el costo de **combinar** — la mezcla de las dos mitades ya ordenadas en una sola lista ordenada — recorre una sola vez, en total, los `n` elementos: por cada elemento que entra a la lista mezclada se hace, como mucho, una comparación entre el frente de las dos sublistas.

**Resolución por árbol de recursión.**

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

En cada nivel el costo total es `c*n`, independientemente del nivel: al bajar un nivel, el número de subproblemas se duplica y el tamaño de cada uno se reduce a la mitad, y esos dos efectos se cancelan. La recursión llega al caso base (tamaño 1) cuando `n / 2^i = 1`, es decir quede `i = log2(n)`. Contando el nivel 0, hay `log2(n) + 1` niveles.

Costo total = (costo por nivel) × (número de niveles) = `c*n × (log2(n) + 1) = c*n*log2(n) + c*n`.

El término dominante es `c*n*log2(n)`, así que **T(n) = Θ(n log n)**.

**Cota de insertion sort, línea a línea.** Con la implementación de [`algoritmos.py`](algoritmos.py) (versión descendente), y `tᵢ` como el número de veces que se evalúa la condición del `while` para la posición `i` (equivalente al número de elementos que hay que revisar/desplazar antes de insertar la clave):

| Línea | Costo por ejecución | Veces que se ejecuta |
|---|---|---|
| `for i in range(1, n):` | c₁ | n |
| `clave = resultado[i]` | c₂ | n − 1 |
| `j = i - 1` | c₃ | n − 1 |
| `while j >= 0:` | — | n − 1 (control, sin comparar elementos) |
| `comparaciones += 1` / `if resultado[j] < clave:` | c₄ | Σᵢ tᵢ |
| `resultado[j+1] = resultado[j]; j -= 1` | c₅ | Σᵢ (tᵢ − 1) cuando hay desplazamiento |
| `resultado[j+1] = clave` | c₆ | n − 1 |

**Mejor caso** (entrada ya en el orden que produce el algoritmo): para cada `i`, la condición del `while` se evalúa una sola vez y es falsa de inmediato (`tᵢ = 1`, sin desplazamientos). Sumando: `T(n) = c₁n + (c₂+c₃+c₄+c₆)(n-1)`, una función **lineal** en `n` → **Θ(n)**.

**Peor caso** (entrada en orden exactamente contrario): para cada `i`, la clave debe compararse y desplazarse contra los `i` elementos anteriores (`tᵢ = i`). La suma `Σᵢ₌₁ⁿ⁻¹ i = n(n-1)/2` domina el resultado: `T(n) = c₁n + (c₂+c₃+c₆)(n-1) + c₄·(n(n-1)/2 + (n-1)) + c₅·n(n-1)/2`, una función **cuadrática** en `n` → **Θ(n²)**.

**Caso promedio:** para una entrada aleatoria, en promedio la clave se desplaza hasta la mitad del prefijo ya ordenado (`tᵢ ≈ i/2`), así que la suma sigue siendo del orden de `n²`, con una constante menor que en el peor caso → también **Θ(n²)**.

**Tabla de complejidades esperadas:**

| Algoritmo | Mejor caso | Caso promedio | Peor caso |
|---|---|---|---|
| Insertion sort | Θ(n) | Θ(n²) | Θ(n²) |
| Merge sort | Θ(n log n) | Θ(n log n) | Θ(n log n) |

### 4.2 — Validación experimental

![Insertion sort vs. merge sort](graficas/parte4_tiempo.png)

Tiempos medidos sobre el escenario A (mediana de 3 corridas):

| n | Insertion sort (s) | Merge sort (s) |
|---|---|---|
| 100 | 0.000251 | 0.000167 |
| 1.600 | 0.066490 | 0.003904 |
| 6.400 | 1.070307 | 0.017794 |

La curva de insertion sort crece de forma claramente cuadrática: al multiplicar `n` por 64 (de 100 a 6.400), su tiempo se multiplica por casi 4.300 (`0.000251 → 1.070307`), muy cerca de `64² = 4.096`. La curva de merge sort, en cambio, crece mucho más suavemente: para el mismo salto de `n`, su tiempo se multiplica solo por ~107 (`0.000167 → 0.017794`), consistente con el crecimiento `n log n` esperado (`64 × log2(6400)/log2(100) ≈ 64 × 1,9 ≈ 122`, del mismo orden de magnitud). A partir de `n ≈ 800` la separación entre las dos curvas ya es visualmente evidente en la gráfica, y sigue abriéndose con cada tamaño siguiente.

Esto coincide con lo calculado en 4.1: Θ(n²) frente a Θ(n log n) predice exactamente este comportamiento, una curva que se dispara y otra que apenas se despega del eje horizontal. El único detalle que no sigue el patrón típico esperado (donde merge sort suele partir *más lento* que insertion sort en tamaños muy pequeños, por el costo fijo de crear sublistas y llamadas recursivas) es que, en mis mediciones, merge sort ya es más rápido desde `n = 100`. La explicación más probable es que, incluso en `n = 100`, el número de comparaciones de insertion sort en el escenario aleatorio (2.542) ya es un orden de magnitud mayor que el de merge sort, así que el costo cuadrático supera el costo fijo de la recursión desde un tamaño bastante pequeño en esta máquina.

### 4.3 — Concepto técnico a la Secretaría de Salud

**Para:** equipo de ingeniería de la Secretaría de Salud — Plataforma Tamiza
**De:** Miguel Arango
**Asunto:** recomendación de algoritmo de ordenamiento para el proceso nocturno

Recomiendo reemplazar insertion sort por **merge sort** como único algoritmo de ordenamiento del proceso nocturno de Tamiza, para los tres canales de entrada (A, B y C) sin distinción.

El criterio detrás de esta recomendación es el mismo que usé para decidir qué caso mirar en la Parte 3: si el canal de entrada puede cambiar sin aviso, la decisión no se puede apoyar en el comportamiento favorable de un escenario particular (el casi-ordenado B), porque ese comportamiento depende de un supuesto operativo —que el reproceso siga partiendo de la lista de ayer— que no está garantizado hacia el futuro. Insertion sort es rápido en B y catastrófico en C; su desempeño es una lotería según cómo llegaron los datos ese día. Merge sort tiene el mismo costo Θ(n log n) sin importar el orden de entrada: mis mediciones lo confirman, con 0,0178 s en el escenario aleatorio para `n = 6.400`, sin detectar de antemano qué escenario llega ni mantener una implementación por canal.

**¿Cabe en la ventana de cuatro horas con 1.200.000 registros?** Es una **estimación**, no una medición directa —no corrí el algoritmo sobre 1.200.000 registros—, obtenida extrapolando la forma de cada curva de la [gráfica de la Parte 4](graficas/parte4_tiempo.png) desde `n = 6.400`:

- **Insertion sort** es Θ(n²): `n` se multiplica por ≈187,5 y el tiempo por ≈187,5² ≈ 35.156. Desde el peor caso medido (2,1268 s en C), la estimación da **≈ 20,8 horas**; desde el aleatorio (1,0718 s), **≈ 10,5 horas**. Ambos muy por encima de las 4 horas — consistente con las tres veces que el proceso real no terminó a tiempo.
- **Merge sort** es Θ(n log n): el tiempo se multiplica por ≈`187,5 × (log2(1.200.000)/log2(6.400)) ≈ 299,4`. Desde 0,0178 s medidos, la estimación da **≈ 5,3 segundos**. Aun suponiendo un costo real diez veces peor por efectos de memoria y hardware no capturados en `n = 6.400`, seguiría siendo del orden de un minuto, muy por debajo de la ventana.

**Sobre duplicar la velocidad del servidor:** no lo recomiendo como solución de fondo. Duplicar la velocidad de reloj, en el mejor caso, divide el tiempo entre dos. Aplicado al peor caso de insertion sort (20,8 horas), el resultado sería **≈ 10,4 horas** — el doble de la ventana disponible. El dato que sostiene esto es el mismo `n = 6.400` de la Parte 4: insertion sort tarda 1,07 s frente a 0,018 s de merge sort en la misma máquina, sin comprar nada — una diferencia de ~60x que ninguna mejora de hardware razonable iguala.

**Una consideración más allá del tiempo:** merge sort necesita memoria adicional Θ(n) para las sublistas temporales de la mezcla (frente al Θ(1) de insertion sort); con 1.200.000 enteros, esa memoria extra es acotada y previsible. Además, la ventaja de insertion sort en B depende de que el reproceso siga generando lotes casi ordenados; si ese flujo cambia, insertion sort pierde su único escenario favorable y queda expuesto en los tres canales por igual. Migrar a merge sort elimina esa dependencia de raíz.
