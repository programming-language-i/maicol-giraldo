### B6. Estado por instancia y estado de clase

##python
import threading


class Contador(threading.Thread):
    
    def __init__(self, nombre):
        super().__init__(name=nombre)
        self.total = 0
        self.eventos = []##Movemos la lista aqui para que cada instancia tenga su propia lista de eventos

    def run(self):
        for _ in range(3):
            self.total += 1
            self.eventos.append(self.name)


a, b = Contador("a"), Contador("b")
for h in (a, b):
    h.start()
for h in (a, b):
    h.join()
print(a.total, b.total, len(a.eventos), len(b.eventos))##Imprimimos la longitud de la lista de eventos de cada instancia para ver que son independientes

##La salida total sin correcion es de 3, 3, 6.
##el estado eventos = [] Está declarado a nivel de clase (fuera del __init__).
## Esto significa que todas las instancias de la clase Contador (a y b) comparten la misma y única lista en memoria.
##Cuando el hilo a corre, añade su nombre 3 veces ("a", "a", "a").
## Cuando el hilo b corre, añade su nombre 3 veces ("b", "b", "b").

##el estado por instancia self,total Está inicializado dentro del constructor (__init__) usando self.
## Esto significa que cada objeto tiene su propia copia independiente de la variable.
##El hilo a modifica únicamente el total del objeto a (llegando a 3).
##El hilo b modifica únicamente el total del objeto b (llegando a 3).
##Como no comparten esta variable, no interfieren entre ellos. Por eso a.total es 3 y b.total es 3.
##Dando una salida final de 3, 3, 3, 3.
