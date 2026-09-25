# Taller de refuerzo · Hilos, GIL y procesos — Sesiones 1 y 2

Práctica de refuerzo sobre lo visto en las clases: concurrencia vs. paralelismo, ciclo de vida del hilo, `join()`, el GIL, hilos por herencia, daemon, excepciones en hilos, `multiprocessing`.

- **Regla de trabajo:** en las Partes B y C, **primero escribir la predicción en papel y después ejecutar**. Quien ejecuta primero no practica nada.
- Todo el código está probado en Python 3.14 sobre Linux. Los tiempos cambian por máquina; lo que se compara es la relación entre ellos.

| Parte | Contenido |
| --- | --- |
| A. Conceptos | 8 preguntas cortas |
| B. Predecir la salida | 6 fragmentos |
| C. Encontrar el error | 4 fragmentos que fallan |
| D. ¿Hilos o procesos? | 6 escenarios |
| E. Programar | 2 ejercicios |

---

## Parte A — Conceptos

Responder en una o dos líneas.

1. Un programa atiende dos tareas alternando en un solo núcleo. ¿Es concurrencia, paralelismo o ambas?
R/=Es concurrencia ya que tiene la capacidad de gestionar y progresar en varias tareas al mismo tiempo.
El paralelismo requiere ejecucion simultanea y fisica de dos o mas instrucciones.


2. Nombrar dos diferencias entre un proceso y un hilo *(memoria, costo, fallo)*.
Memoria.
Proceso.tiene su propio espacio y es independiente
Hilo:Comprte la memoria y los recursos, cmomo codigo, datos y archivos.
Costo.
Proceso:Es de alto costo, y crear o cambiar de contexto se vuelve lento y pesado.
Hilos:Es de bajo costo, y el cambio de contexto entre hilos es mucho mas rapido.
Fallo.
Proceso:Ofrece alta tolerancia a fallos,si un proceso falla o tiene un error muere de forma aislada sin afectar la ejecucion.
Hilo:Ofrece baja tolerancia a fallos,si un hilo realiza una operacion No valida que cause un fallo de memoria,
todo el proceso padre colapsa finalizando todos los hilos asociados.


3. ¿En qué estado del ciclo de vida está un hilo que ejecuta `time.sleep(2)`? ¿Qué devuelve `is_alive()`?
R/:Un hilo que ejecuta time.sleep(2), blocked o en espera durante 2seg el hilo sede voluntaria mente el uso de la CPUy no esta realizando ninguntrabajo activo, is_alive() devuelve un True y evalua si el hilo a iniciado su ejecucion y aun no ha terminado, el hilo sigue en la memoria y su estado es gestionado por el entorno de ejecucion, por lo que responde true hasta que finalice.


4. ¿Qué protege el GIL? ¿Evita las condiciones de carrera en los datos del programa?
R/:El GIL protege los datos internos del propio interprete de CPphyton, preveniendo que multiples hilos manipulen simultaneamente la estructura de datos del lenguaje.
Aunque Gil garantice que un solo hilo ejecute bytecode de python a la vez, el interprete puede suspender un hilo y cambiar a otro medio de cualquier operacion de python.


5. ¿Por qué 4 hilos que duermen 1 s cada uno tardan ~1 s en total y no ~0,25 s?
R/:Debido a que la funcion time.sleep(1) suspende la ejecucion del hilo durante el tiempo real osea (1seg de reloj), no durante un coste de procesamiento que se reparta entre hilos. 


6. Al crear un hilo por herencia, ¿qué método se sobrescribe y cuál nunca? ¿Por qué?
run:el metodo run()representa el punto de entrada y el cuerpo de trabajo del hilo.

start:El metodo start() contiene la parte logica interna del sistema para la gestion de hilos.su funcion es solicitar al sistema operativo la creacion de un hilo de ejecucion nativo.


7. ¿Qué pasa con un hilo daemon cuando termina el hilo principal? ¿Qué **no** se ejecuta?
R/:Cuando el hilo principal y todos los demas hilos no-deamon terminan, la maquina virtual finaliza el programa de forma abruta e inmediata, interrumpiendo y destuyendo todos los hilos deamon en el estado en que se encuentren.

¿Que no se ejecuta?

-Cualquier instrucción que estuviera pendiente dentro del método run() del hilo daemon jamás se ejecutará.
-En Python, los bloques try ... finally no tienen garantía de ejecutarse en un hilo daemon si el proceso principal muere durante la ejecución del bloque try.
-Los métodos de salida (__exit__) que garantizan la liberación de recursos no se invocan.
-: Si el hilo estaba escribiendo en un archivo o enviando datos por la red, las operaciones pendientes en el búfer de memoria no se guardarán en el disco ni se transmitirán, lo que puede causar corrupción de datos.


8. Completar la regla del curso: *hilos para , procesos para*.
R/:En Python, mientras un hilo espera I/O, libera el GIL, lo que permite que otros hilos aprovechen el tiempo de procesador. Dado que los hilos comparten memoria y tienen un bajo costo de creación, son la mejor opción para manejar múltiples conexiones o esperas simultáneas.
-En tareas intensivas en uso de procesador algoritmos matemáticos, procesamiento de imágenes, redes neuronales, el GIL de Python impide que varios hilos ejecuten bytecode en paralelo dentro del mismo núcleo.


---

## Parte B — Predecir la salida

Para cada fragmento: escribir la salida exacta *(o el tiempo aproximado, si se pide)*, ejecutar y explicar la diferencia si la hubo.

### B1. ¿Cuánto tarda?

```python
import threading
import time


def tarea(n):
    time.sleep(1)


inicio = time.perf_counter()
for i in range(3):
    hilo = threading.Thread(target=tarea, args=(i,))
    hilo.start()
    hilo.join()
print(f"{time.perf_counter() - inicio:.1f} s")
```

### B2. Daemon con `finally`

```python
import threading
import time


def guardar():
    try:
        time.sleep(2)
        print("guardado")
    finally:
        print("archivo cerrado")


threading.Thread(target=guardar, daemon=True).start()
time.sleep(0.5)
print("fin")
```

### B3. Una excepción en el pool

```python
from concurrent.futures import ThreadPoolExecutor


def dividir(a, b):
    return a / b


with ThreadPoolExecutor() as pool:
    futuro = pool.submit(dividir, 1, 0)
print("listo")
```

### B4. Reiniciar un hilo

```python
import threading

hilo = threading.Thread(target=print, args=("hola",))
hilo.start()
hilo.join()
print(hilo.is_alive())
hilo.start()
```

### B5. Procesos y una lista global

```python
import multiprocessing

resultados = []


def calcular(n):
    resultados.append(n * n)


if __name__ == "__main__":
    procesos = [multiprocessing.Process(target=calcular, args=(n,)) for n in range(4)]
    for p in procesos:
        p.start()
    for p in procesos:
        p.join()
    print(resultados)
```

### B6. Estado por instancia y estado de clase

```python
import threading


class Contador(threading.Thread):
    eventos = []

    def __init__(self, nombre):
        super().__init__(name=nombre)
        self.total = 0

    def run(self):
        for _ in range(3):
            self.total += 1
            self.eventos.append(self.name)


a, b = Contador("a"), Contador("b")
for h in (a, b):
    h.start()
for h in (a, b):
    h.join()
print(a.total, b.total, len(a.eventos))
```

---

## Parte C — Encontrar el error

Cada fragmento falla o no hace lo que su autor cree. Para cada uno:
**(1)** qué pasa al ejecutarlo
**(2)** por qué
**(3)** la corrección mínima.

### C1. Descarga por herencia

```python
import threading


class Descarga(threading.Thread):
    def __init__(self, archivo):
        self.archivo = archivo

    def run(self):
        print("descargando", self.archivo)


Descarga("a.zip").start()
```

### C2. Tres tareas "concurrentes"

```python
import threading
import time


class Tarea(threading.Thread):
    def start(self):
        time.sleep(1)
        print(self.name, "lista")


inicio = time.perf_counter()
tareas = [Tarea(name=f"t{i}") for i in range(3)]
for t in tareas:
    t.start()
print(f"{time.perf_counter() - inicio:.1f} s")
for t in tareas:
    t.join()
```

### C3. Un pool de procesos sin guarda

```python
from concurrent.futures import ProcessPoolExecutor


def cuadrado(n):
    return n * n


with ProcessPoolExecutor(max_workers=2) as pool:
    print(list(pool.map(cuadrado, range(4))))
```

---

## Parte D — ¿Hilos o procesos?

Para cada programa, elegir **hilos** o **procesos** y justificar en una línea *(¿espera o calcula?)*.

1. Consultar el precio de 30 productos en 30 APIs distintas.
2. Contar las palabras palíndromas de 10 libros ya cargados en memoria.
3. Un servidor de chat que atiende 15 clientes conectados.
4. Aplicar un filtro de desenfoque a 200 fotos, píxel por píxel, en Python puro.
5. Leer 50 archivos de log del disco y copiarlos a otra carpeta.
6. Simular 1.000.000 de lanzamientos de dados en 8 lotes y promediar.

---

## Parte E — Programar

Repositorio personal, carpeta `practica-clase/`, con un `README.md` que pegue las salidas obtenidas.

```bash
practica-clase/
├── primos.py
├── consultas.py
└── README.md
```

---

## Autoevaluación

Marcar antes de dar el taller por terminado:

- [ ] Explico con un ejemplo la diferencia entre concurrencia y paralelismo.
- [ ] Sé por qué `start()` y `join()` en el mismo bucle vuelven secuencial el programa.
- [ ] Sé qué hace y qué no hace el GIL.
- [ ] Creo un hilo por herencia con `super().__init__()` y `run()`, con estado por instancia.
- [ ] Sé qué se pierde al usar un hilo daemon.
- [ ] Recupero el resultado y la excepción de un hilo, con herencia y con pool.
- [ ] Sé por qué los procesos no ven la memoria del padre y por qué necesitan la guarda `if __name__ == "__main__":`.
- [ ] Elijo entre hilos y procesos preguntando si el programa espera o calcula.