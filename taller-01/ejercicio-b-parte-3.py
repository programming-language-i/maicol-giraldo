
### B3. Una excepción en el pool

```python
from concurrent.futures import ThreadPoolExecutor


def dividir(a, b):
    return a / b


with ThreadPoolExecutor() as pool:
    futuro = pool.submit(dividir, 1, 0)

try:## ponemos el try para capturar la excepcion de la division por cero
    resultado = futuro.result()
except ZeroDivisionError: ##ponemos execpt para capturar la excepcion de la division por cero         
    print("Error: No se puede dividir por cero.")## este print se ejecuta si hay una excepcion de division por cero

    print("Operacion realizada.")## y finalizamos el programa con este print


    
##La salida exacta es Listo.
##Pero el primer mandamiento de las matematicas es (Nunca dividiras por cero).
##por lo tanto, el resultado de la division y el codigo tendrian error de logica.


