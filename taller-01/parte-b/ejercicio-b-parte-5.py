
### B5. Procesos y una lista global

  ##python
from multiprocessing import manager, process


def calcular(n, lista_compartida):##Modificamos la lista compartida.
    lista_compartida.append(n * n)


if __name__ == "__main__":
    with manager.Manager() as manager:
     
     result = manager.list()##Creamos una lista administrada que se puede compartir entre procesos.
     procesos = [
        process.Process(target=calcular, args=(i, result)) for i in range(4)
     ]

     for p in procesos:
        p.start()
        for p in procesos:
            p.join()

            print(list(result))##Imprimimos la lista compartida convertida a una lista normal.
       
##La salida exactadel programa es []
##se usa multiprocesamiento para calcular los cuadrados de los números del 0 al 3 y almacenarlos en una lista compartida. 
##Sin embargo, debido a la forma en que se manejan los procesos y la sincronización,
## la lista compartida puede no reflejar los resultados esperados si no se maneja correctamente el inicio
## y la unión de los procesos.


