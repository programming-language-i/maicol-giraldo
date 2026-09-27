
## Parte C — Encontrar el error

##Cada fragmento falla o no hace lo que su autor cree. Para cada uno:
##**(1)** qué pasa al ejecutarlo
##**(2)** por qué
##**(3)** la corrección mínima.


#python
import threading


class Descarga(threading.Thread):
    def __init__(self, archivo):
        super().__init__()##(3) este es el cambio que se debe hacer para que funcione correctamente
        self.archivo = archivo

    def run(self):
        print("descargando", self.archivo)


Descarga("a.zip").start()

##(1) Al ejecutarlo, se lanza un error de tipo `TypeError: super(type, obj): obj must be an instance or subtype of type`.
##(2)Cuando creas una clase que hereda de threading.Thread, estás sobrescribiendo el constructor (__init__).
##Como tu __init__ personalizado no incluye una llamada a la clase padre (super().__init__()),
##el hilo nunca inicializa sus estructuras internas de control (como los estados de vida del hilo)
##Cuando intentas llamar a .start(), 
##se detecta que el hilo no fue inicializado correctamente y detiene la ejecución con un RuntimeError.