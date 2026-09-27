from concurrent.futures import ProcessPoolExecutor
import time


def es_primo(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


def buscar_primos(rango):
    inicio, fin = rango
    return [n for n in range(inicio, fin) if es_primo(n)]


if __name__ == "__main__":
    limite = 100000
    chunk = limite // 4
    rangos = [(i * chunk + 1, (i + 1) * chunk + 1) for i in range(4)]

    print(f"Buscando números primos hasta {limite} usando procesos...")
    inicio_tiempo = time.perf_counter()

    with ProcessPoolExecutor(max_workers=4) as pool:
        resultados = list(pool.map(buscar_primos, rangos))

    primos_totales = [primo for sublista in resultados for primo in sublista]
    duracion = time.perf_counter() - inicio_tiempo

    print(f"Se encontraron {len(primos_totales)} números primos en {duracion:.4f} segundos.")


     
       
        