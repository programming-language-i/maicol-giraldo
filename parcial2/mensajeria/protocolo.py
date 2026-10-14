"""
PARCIAL 2 - Nivel 1 (20 pts) · Framing

TCP es un flujo de bytes, no de mensajes. Cada mensaje viaja así:

    4 bytes con la longitud del cuerpo (big-endian)  +  el cuerpo en UTF-8

Complete los TODO. No cambie los nombres ni las firmas: las pruebas, el
servidor y los clientes importan estas tres funciones.

Requisitos:
  1. El prefijo es struct.pack("!I", n), donde n es la longitud EN BYTES del
     cuerpo ya codificado.
  2. recibir_exacto llama a recv() EN BUCLE hasta completar los n bytes.
  3. UTF-8 explícito al codificar y al decodificar.
  4. Si recv() devuelve bytes vacíos, la conexión se cerró: se devuelve None.

Se comprueba con:   python3 prueba_n1.py   (desde la carpeta parcial2/)
"""

import socket
import struct


def recibir_exacto(sock: socket.socket, n: int) -> bytes | None:
    """Lee exactamente n bytes. Devuelve None si la conexión se cerró antes."""
    
    # Reivisar 1: recv(n) puede devolver MENOS de n bytes. Acumule en un buffer lo
    #         que vaya llegando y pida cada vez solo lo que falta, hasta tener n.
    #         Si recv() devuelve b"", el otro extremo cerró: devuelva None.
    
    
    bufer = bytearray()##creamos un bufer de tipo bytearray para almacenar los bytes recibidos
    while len(bufer) < n:#mientras la longitud del bufer sea menor a n, seguimos recibiendo datos
        recibido = sock.recv(n - len(bufer))##aqui recibimos los datos del socket, pidiendo solo la cantidad de bytes que faltan
        #         para completar n
        if not recibido:
            return None
        bufer.extend(recibido)##en este bufer.extend esta agregando los bytes recibidos al bufer
    return bytes(bufer)




def enviar_mensaje(sock: socket.socket, texto: str) -> None:
    """Envía texto en UTF-8 precedido de su longitud en 4 bytes big-endian."""
    # Reivisar 2: codifique el texto, arme el prefijo con la longitud de los BYTES
    #         y envíe prefijo + cuerpo con sendall().
    
    body = texto.encode("utf-8")##aqui estamos codificando el texto a bytes usando UTF-8
    prefix = struct.pack("!I", len(body))##en esta linea estamos creando el prefijo con la longitud de los bytes del cuerpo
    ##usando struct.pack con formato big-endian
    sock.sendall(prefix + body)###aqui estamos enviando el prefijo y el cuerpo concatenados usando sendall() 
    ##para asegurarnos de que se envíen todos los bytes


def recibir_mensaje(sock: socket.socket) -> str | None:
    """Lee un mensaje completo. Devuelve None si el otro extremo cerró."""
    # Reivisar 3: lea los 4 bytes del prefijo con recibir_exacto y saque la longitud
    #         con struct.unpack. Lea esa cantidad de bytes y devuélvalos
    #         decodificados. Si cualquiera de las dos lecturas da None, devuelva None.
    
    prefijo = recibir_exacto(sock, 4)##aqui estamos recibiendo los 4 bytes del prefijo usando la funcion recibir_exacto
    if prefijo is None:
        return None
    longitud = struct.unpack("!I", prefijo)[0]##aqui estamos desempaquetando el prefijo para obtener la longitud del cuerpo
    ##en bytes
    cuerpo = recibir_exacto(sock, longitud)##aqui estamos recibiendo el cuerpo del mensaje usando la funcion recibir_exacto 
    ##con la longitud obtenida del prefijo
    if cuerpo is None:
        return None
    return cuerpo.decode("utf-8")##aqui estamos decodificando el cuerpo de bytes a string usando UTF-8 y devolviendo
     ##el mensaje completo
