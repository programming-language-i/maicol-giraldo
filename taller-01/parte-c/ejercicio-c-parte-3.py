
### C3. Un pool de procesos sin guarda

from concurrent.futures import ProcessPoolExecutor


def cuadrado(n):
    return n * n

if __name__ == "__main__":##(3)esta es la corrección mínima para evitar el bucle infinito
 with ProcessPoolExecutor(max_workers=2) as pool:
    print(list(pool.map(cuadrado, range(4))))

##(1)cuando se ejecuta se crea un bucle infinito que se queda congelado, 
##(2)esto se debe a que el código no está protegido por un bloque if __name__ == "__main__":, 
##(3)la corrección mínima es agregar el bloque if __name__ == "__main__": antes de la ejecución del código.