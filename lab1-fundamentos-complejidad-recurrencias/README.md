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

Que Tamiza lleve ocho años sacando la lista bien no quiere decir que el algoritmo sirva. Son dos cosas distintas. Que sea correcto significa que la lista sale ordenada por índice de riesgo, y eso insertion sort lo cumple siempre, con 20.000 registros o con 1.200.000. Que sea viable es otra historia: la lista tiene que estar lista dentro de la restricción de tiempo que tiene el sistema, que es la ventana de cuatro horas, de 2:00 a. m. a 6:00 a. m. No se puede mover porque a las 6 el centro de contacto ya necesita la lista para empezar a llamar. Eso es lo que Tamiza incumple: ya van tres veces en las últimas semanas que el proceso no alcanzó a terminar.

El problema de fondo es que insertion sort no escala casi nada. El número de comparaciones crece con el cuadrado del tamaño del lote. Con 20.000 registros aguantaba, pero con 1.200.000, que son 60 veces más datos, el costo no se multiplicó por 60 sino por unas 3.600. Si la Secretaría compra un servidor del doble de velocidad, en el mejor de los casos el tiempo se divide entre dos, y eso frente a un costo que se multiplicó por 3.600 casi no cambia nada. Alivia un rato y cuando amplíen el programa otra vez toca comprar otro servidor. Cambiar hardware para tapar un algoritmo malo es botar la plata: el problema no es qué tan rápido es el procesador sino cómo crece el costo con el tamaño de la entrada, y eso solo se arregla cambiando el algoritmo.

Me pasa algo parecido en mi trabajo en Nutresa. Allá manejo procesos en SAP que corren sobre millones de registros, por ejemplo la conciliación de movimientos de inventario entre plantas y centros de distribución al cierre del período. El resultado siempre sale correcto, cada movimiento queda cuadrado, pero el proceso tiene que terminar dentro de la ventana de cierre, unas horas antes de que otros equipos necesiten esos datos para sus reportes. Cuando el volumen crece (más plantas, más referencias, promociones, fin de mes) el proceso empieza a rozar el límite de esa ventana. Es el mismo caso: el resultado es correcto pero no llega a tiempo.

---

## Parte 2. Responsabilidad ambiental y ética de la implementación

Un servidor gasta energía mientras el procesador trabaja, así que más tiempo de cómputo es más consumo. Con insertion sort el proceso de Tamiza ya no es un ratico en la madrugada: como muestro en la Parte 4, con 1.200.000 registros la estimación es de varias horas con el servidor a tope, y a veces se pasa de la ventana y sigue corriendo cuando el centro de contacto ya abrió. Eso no pasa una sola vez. El proceso corre todas las noches, 365 al año, durante los años que la plataforma siga en producción. Unos minutos de más por noche, multiplicados por miles de noches, son un montón de kWh y de huella de carbono (dependiendo de qué tan limpia sea la energía de ese centro de datos) que nadie ve porque "todo sigue funcionando". Comprar un servidor más grande tampoco arregla eso, lo empeora: una máquina más potente gasta más cada noche, todos los días, mientras que arreglar el algoritmo baja el tiempo de ejecución sin agregar consumo.

En lo ético veo dos problemas. El primero es el paciente. Si a las 6 a. m. el proceso no ha terminado, el centro de contacto trabaja con una lista mocha y sin ordenar por riesgo, y un paciente con riesgo alto que quedó de último por la demora puede no salir en las llamadas de ese día. El que asume el costo de ese error es el paciente, porque el sistema ya había detectado que estaba en peligro y aun así nadie lo llamó a tiempo. El segundo afectado es el operador del centro de contacto. Esa persona llega, abre la lista, confía en el orden que le aparece y empieza a llamar sin saber que está incompleta. Si después hay un reclamo por un paciente crítico que no fue contactado, le echan la culpa a él o al centro de contacto, cuando el problema es un algoritmo mal dimensionado. Ahí el operador paga los platos rotos de algo que no hizo.

Como el orden de la lista es lo que decide a quién se llama primero, no basta con que el proceso termine: la lista tiene que estar bien ordenada desde arriba. Una lista a medias falla justo donde más duele, en los primeros puestos, que son los pacientes más graves y los que se llaman primero. Por eso el ordenamiento tiene que ser correcto y completo, además de entrar en el tiempo.

---

## Parte 3. Peor caso, mejor caso y caso promedio, demostrados en Python

Código de esta parte: [algoritmos.py](algoritmos.py) (`insertion_sort`), [datos.py](datos.py) (generadores de escenarios) y [parte3_casos.py](parte3_casos.py) (el experimento).

### 3.1 Explicación

Se fija un tamaño de entrada `n` y se piensa en todas las formas posibles en que pueden llegar esos `n` registros (todas las permutaciones). Sobre ese conjunto:

- El **peor caso** es el máximo de comparaciones (o de tiempo) que el algoritmo puede gastar, o sea la entrada que más lo hace sufrir. Ninguna entrada de ese tamaño lo supera.
- El **mejor caso** es el mínimo, la entrada más favorable de todas.
- El **caso promedio** es el promedio del costo sobre todas esas entradas, asumiendo que cualquier orden es igual de probable.

Para decidir si el algoritmo entra a producción miraría el peor caso. La ventana de Tamiza no se negocia, a las 6 a. m. el centro de contacto abre pase lo que pase. Si me guío por el promedio, el día que llegue un lote malo (por ejemplo una migración que mande todo al revés, como el escenario C) el proceso no termina, que es justo lo que ya ha pasado tres veces. Solo el peor caso me asegura que siempre cabe, llegue como llegue el lote.

Mi predicción antes de medir: como insertion sort compara cada elemento nuevo con los que ya están ordenados y lo va desplazando, el escenario C (orden inverso) debería ser el peor caso, porque cada elemento tiene que recorrer todo lo anterior. El B (casi ordenado) debería ser el mejor, porque el 98 % ya viene en el orden que sale del algoritmo y casi no hay que mover nada. Y el A (aleatorio) debería quedar cerca del caso promedio, porque no tiene ninguna estructura.

### 3.2 Demostración experimental

![Comparaciones vs. tamaño de entrada](graficas/parte3_comparaciones.png)

![Tiempo vs. tamaño de entrada](graficas/parte3_tiempo.png)

Medí siete tamaños (100, 200, 400, 800, 1600, 3200 y 6400) y cada tiempo es la mediana de 3 corridas. Con `n = 6400`:

| Escenario | Comparaciones | Tiempo (s) |
|---|---|---|
| A. Aleatorio | 10.276.753 | 1.0718 |
| B. Casi ordenado | 10.649 | 0.0012 |
| C. Orden inverso | 20.476.800 | 2.1268 |

El C es el peor caso y el B el mejor, como predije. El A queda cerca del caso promedio: hace casi la mitad de las comparaciones del C en todos los tamaños (10.276.753 contra 20.476.800 en `n = 6400`), lo que tiene sentido porque en promedio cada elemento se devuelve hasta la mitad de lo que ya está ordenado. Además, las 20.476.800 comparaciones del C son exactamente `n(n-1)/2 = 6400 × 6399 / 2`, la fórmula del peor caso.

Un detalle con el B: el mejor caso de verdad es una lista que ya viene en el orden final, y ahí insertion sort hace `n - 1` comparaciones (6.399). El B tiene 10.649 porque el 2 % del final sí viene desordenado y hay que acomodarlo. Igual queda mucho más cerca del mejor caso que el A o el C, porque casi todo el lote no necesita trabajo.

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

La curva de insertion sort se dispara: cuando n se multiplica por 64 (de 100 a 6.400) el tiempo se multiplica por casi 4.300, muy cerca de 64² = 4.096, o sea cuadrático. La de merge sort casi ni se despega del eje: para el mismo salto el tiempo solo se multiplica por unas 107 veces, que va con n log n (64 × log2(6400)/log2(100) ≈ 122). Desde n ≈ 800 ya se ve a simple vista que la brecha se abre, y sigue abriéndose. Para Tamiza el mejor es merge sort sin discusión.

Esto coincide con lo que calculé en 4.1, Θ(n²) contra Θ(n log n). Lo único distinto a lo que uno esperaría es que merge sort suele arrancar más lento en tamaños pequeños, por el costo de crear sublistas y hacer llamadas recursivas, y aquí ya le gana a insertion sort desde n = 100. Creo que es porque incluso ahí insertion sort ya hace 2.542 comparaciones, muy por encima de las de merge sort, y el costo cuadrático le gana al costo fijo de la recursión desde un tamaño bien chico.

### 4.3 Concepto técnico a la Secretaría de Salud

Para el equipo de ingeniería de la Plataforma Tamiza:

Mi recomendación es reemplazar insertion sort por merge sort en todo el proceso nocturno, sin importar de qué canal lleguen los datos.

El canal puede cambiar sin aviso y no conviene mantener tres implementaciones, así que escogí el algoritmo cuyo tiempo no depende de cómo llegue el lote. Insertion sort solo es rápido si los datos vienen casi ordenados (escenario B). Si mañana cambian el flujo de reproceso, o el sistema legado manda todo al revés (escenario C), el proceso se cae. Merge sort hace el mismo trabajo, Θ(n log n), llegue como llegue el lote. En mis pruebas ordenó 6.400 registros aleatorios en 0,0178 s y no hay que adivinar cada noche cómo viene el lote.

¿Cabe en las cuatro horas con 1.200.000 registros? Lo que sigue es una estimación, no una medición: no corrí el algoritmo con 1.200.000 registros, extrapolo desde `n = 6.400` con la forma de cada curva de la gráfica de la Parte 4. Con `n` multiplicado por 187,5:

- Insertion sort es cuadrático, así que el tiempo se multiplica por unas 187,5² ≈ 35.156. Desde el peor caso que medí (2,1268 s en el escenario C) da unas 20,8 horas, y desde el aleatorio (1,0718 s) unas 10,5 horas. Las dos muy por encima de las 4 horas, lo que cuadra con las tres veces que el proceso real no terminó.
- Merge sort es n log n, así que el tiempo se multiplica por 187,5 × (log2(1.200.000) / log2(6.400)) ≈ 299. Desde 0,0178 s da unos 5,3 segundos. Aunque en la realidad fuera 10 veces peor por memoria y hardware, que no puedo ver con `n = 6.400`, sería cerca de un minuto, muy lejos de las 4 horas.

Sobre comprar el servidor del doble de velocidad: no lo haría. En el mejor caso divide el tiempo entre dos, y a las 20,8 horas estimadas para el peor caso de insertion sort le quedarían unas 10,4, todavía más del doble de la ventana. El dato que lo muestra es el `n = 6.400` de la gráfica de la Parte 4: insertion sort se demora 1,07 s y merge sort 0,018 s en la misma máquina, unas 60 veces menos sin comprar nada, y ningún servidor razonable compensa esa diferencia.

Aparte del tiempo, merge sort gasta memoria extra, del orden de Θ(n), por las listas temporales de la mezcla (insertion sort trabaja en el mismo lugar). Con 1.200.000 enteros es una cantidad razonable y predecible. Y otro riesgo que vale la pena tener presente: lo único que le sirve a insertion sort es que el reproceso siga entregando lotes casi ordenados. Si ese flujo cambia, se queda sin su único escenario favorable, así que migrar a merge sort quita esa dependencia.
