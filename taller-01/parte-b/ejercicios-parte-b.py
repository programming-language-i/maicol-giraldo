
## Parte B — Predecir la salida

##Para cada fragmento: escribir la salida exacta *(o el tiempo aproximado, si se pide)*, ejecutar y explicar la diferencia si la hubo.

### B1. ¿Cuánto tarda?

##```python
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



## El codigo presenta un error conceptual en las lineas 21 (hilo.join()).
## ya que le dice al hilo principal que espere a que el hilo termine antes de continuar con la siguiente iteración del bucle.
## Esto significa que los hilos se ejecutan de manera secuencial, no concurrente.
## Por lo tanto, el tiempo total será aproximadamente 3 segundos ( en ves de 1 segundo por cada hilo).
