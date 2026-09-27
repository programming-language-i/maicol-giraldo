### C2. Tres tareas "concurrentes"


import threading
import time


class Tarea(threading.Thread):
    def run(self):##(3)solucion minima sustituir start() por run()
        time.sleep(1)
        print(self.name, "lista")


inicio = time.perf_counter()
tareas = [Tarea(name=f"t{i}") for i in range(3)]
for t in tareas:
    t.start()
print(f"{time.perf_counter() - inicio:.1f} s")
for t in tareas:
    t.join()

##(1) Al ejecutarlo, se imprime el nombre de cada tarea después de un segundo, y se muestra el tiempo total de ejecución.
##tardando 3 segundos en total, ya que las tareas se ejecutan de manera concurrente.
##(2) porque, Se sobrescribió el método start() en lugar del método run().
##En Python, el método start() de la clase threading.
##Thread es el encargado interno de crear el hilo a nivel del sistema operativo y ponerlo a correr en segundo plano.