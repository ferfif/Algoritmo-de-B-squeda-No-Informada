# Algoritmos de Búsqueda: Informada vs No Informada

Aplicación de escritorio que resuelve el **puzzle de 15 (tablero 4x4)** con algoritmos de búsqueda y permite ver la solución animada paso a paso. Permite elegir entre búsqueda **no informada** (`BFS`, `DFS`) e **informada** (`A*`, `Greedy`) para comparar sus diferencias, y un script de benchmark que las compara por consola.

El usuario puede mezclar el tablero, elegir el tipo de búsqueda y el algoritmo, y ver el resultado (cantidad de movimientos, nodos expandidos y tiempo). No hay límite de nodos: cada algoritmo corre hasta encontrar la solución.

## Ejecución

```bash
pip install -r requirements.txt
python app/app.py
```

Para el benchmark por consola:

```bash
python app/benchmark.py --type all --trials 10 --scramble-moves 20
```

`--type` acepta `uninformed`, `informed` o `all`. Todos los algoritmos resuelven los mismos tableros para que la comparación sea justa.

## Estructura del proyecto

| Ruta | Para qué sirve |
|------|----------------|
| `app/` | Código fuente de la aplicación (detallado abajo). |
| `resources/` | Recursos gráficos; contiene `puzzle.jpg`, la imagen que la interfaz corta en fichas. |
| `requirements.txt` | Dependencias de Python (Pillow, para manejar la imagen). |
| `.venv/` | Entorno virtual local con las dependencias instaladas. No forma parte del código. |
| `.gitignore` | Archivos y carpetas que Git ignora (entorno virtual, cachés, etc.). |

## Archivos de `app/`

### `app.py`
Punto de entrada. Solo importa y ejecuta `main()` de `gui.py`.

### `puzzle.py`
Modelo del puzzle. Un estado es una tupla de 16 valores (el `0` es el hueco) y el estado meta es `1..15, 0`. Contiene:
- Cálculo de movimientos válidos (`UP`, `DOWN`, `LEFT`, `RIGHT`) y aplicación de un movimiento para obtener un nuevo estado.
- `get_neighbors`: genera los estados vecinos, que es lo que recorren los algoritmos.
- `is_goal`: comprueba si se llegó a la meta.
- `manhattan_distance` y tablas precalculadas de vecinos y distancias: la heurística de los algoritmos informados y aceleradores para todos.
- `is_solvable`: verifica que una configuración tenga solución.
- `generate_scrambled_state`: mezcla el tablero haciendo movimientos aleatorios desde la meta (siempre queda resoluble y evita deshacer el movimiento anterior).

### `bfs.py` (no informada)
`BFS` bidireccional: crece un árbol de anchura desde el estado inicial y otro desde la meta, expandiendo siempre la frontera más pequeña, hasta que se encuentran. Sigue siendo una búsqueda no informada y devuelve la solución con menos movimientos, pero expande muchísimos menos nodos que un BFS normal.

### `dfs.py` (no informada)
`DFS` con profundización iterativa: repite una búsqueda en profundidad con un límite de profundidad creciente. No guarda estados visitados (usa muy poca memoria), no se pierde en ramas infinitas y también encuentra la solución óptima, aunque a costa de revisitar nodos, por lo que es el más lento.

### `astar.py` (informada)
`A*`: expande primero el estado con menor `costo recorrido + distancia Manhattan`. Encuentra la solución óptima expandiendo muy pocos nodos.

### `greedy.py` (informada)
Búsqueda voraz: expande el estado que parece más cercano a la meta según Manhattan, sin considerar el costo recorrido. Es muy rápida, pero la solución no es necesariamente la más corta.

### `solver.py`
Capa que une la interfaz con los algoritmos. `solve(estado, algoritmo)` ejecuta el algoritmo elegido, verifica que el tablero tenga solución, mide el tiempo y añade `time` y `algorithm` al resultado. Expone `SEARCH_TYPES` (qué algoritmos hay en cada tipo de búsqueda), que usan la interfaz y el benchmark.

### `gui.py`
Interfaz gráfica hecha con Tkinter y Pillow. Se encarga de:

- Cargar `resources/puzzle.jpg` y dividirlo en las 15 fichas.
- Dibujar el tablero y mostrar los controles (tipo de búsqueda, algoritmo, velocidad de animación, nuevo puzzle, reiniciar, resolver).
- Ejecutar el solver en un hilo aparte para no congelar la ventana.
- Animar el deslizamiento de las fichas con la solución encontrada y mostrar las estadísticas o los errores.

### `benchmark.py`
Script de consola para comparar los algoritmos. Genera varios tableros mezclados, los resuelve con cada algoritmo del tipo elegido y muestra el promedio de nodos expandidos, tiempo y movimientos. Acepta `--type`, `--trials` y `--scramble-moves`.
