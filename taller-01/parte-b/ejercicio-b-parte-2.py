```python
import threading
import time


def guardar():
    try:
        
        print("Saving file...")##Corregimos quitando el time.slieep de arriba y lo ponemos abajo.
        time.sleep(2)
        print("file saved")##creamos un print para que se vea que el archivo se guardo correctamente.
    finally:
        print("file closed")

        hilo_guardado = threading.Thread(target=guardar)##creamos este hilo para que se ejecute la funcion guardar.
        hilo_guardado.start()##iniciamos el hilo para que se ejecute la funcion guardar.
        time.sleep(1)##ponemos un sleep para que el hilo principal espere a que el hilo de guardado termine.
        hilo_guardado.join()##ponemos un join para que el hilo principal espere a que el hilo de guardado termine.

        print(" End ")##ponemos un print para que se vea que el hilo principal termino correctamente.



##La salida exacta es:
##fin
##archivo cerrado
##Pero en el codigo el mensaje de guardado no se imprime, ya que el hilo principal termina antes de que el hilo daemon pueda completar su tarea.
## Para evitar esto, se puede usar un hilo no daemon o usar join() para esperar a que el hilo termine antes de que el hilo principal termine.
