"""
PARCIAL 2 - Nivel 2 (20 pts) · Registro de clientes

Quién está conectado: un dict con el nombre como clave, protegido con UN
threading.Lock. Lo usan a la vez todos los hilos del servidor.

Aquí solo están las firmas: escriba el cuerpo de los cinco métodos.

Requisitos:
  1. insertar devuelve False si el nombre ya está en uso. Verificar e insertar
     ocurren bajo el MISMO lock.
  2. buscar devuelve la conexión de ese nombre, o None si no está.
  3. borrar quita la entrada. Borrar un nombre que ya no está no es un error.
  4. destinatarios devuelve UNA COPIA, hecha dentro del lock: la lista de
     (nombre, conexion) de todos menos `excepto`.
"""

import socket
import threading


class RegistroClientes:
    def __init__(self) -> None:##aqui estamos inicializando la clase RegistroClientes,
        ##creando un lock para proteger el acceso al diccionario de clientes y un diccionario vacío para almacenar los clientes
        # conectados
        self._lock = threading.Lock()
        self._clientes: dict[str, socket.socket] = {}


def insertar(self, nombre: str, conexion: socket.socket) -> bool:##aqui estamos definiendo el método insertar
    #3que recibe un nombre y una conexión de socket, y devuelve un booleano indicando si la inserción fue exitosa o no
        with self._lock:
            if nombre in self._clientes:
                return False
            self._clientes[nombre] = conexion
            return True




def buscar(self, nombre: str) -> socket.socket | None:##aqui estamos definiendo el método buscar que recibe un nombre
    ##y devuelve la conexión de socket correspondiente si el nombre está en el registro, o None si no lo está
   
    with self._lock:
        return self._clientes.get(nombre)
        


      

def borrar(self, nombre: str) -> None:##aqui estamos definiendo el método borrar que recibe un nombre y elimina la entrada
    ##correspondiente del registro de clientes
       with self._lock:
        self._clientes.pop(nombre, None)
        

def destinatarios(self, excepto: str) -> list[tuple[str, socket.socket]]:##aqui estamos definiendo el método destinatarios que
    ##recibe un nombre y devuelve una lista de tuplas
    ##con los nombres y conexiones de todos los clientes conectados, excepto el cliente especificado
        with self._lock:
            return [(nombre, conexion) for nombre, conexion in self._clientes.items() if nombre != excepto]##aqui se realiza el
        ##retorno de las funciones
    