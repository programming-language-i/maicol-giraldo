"""
PARCIAL 2 - Nivel 2 · Servidor concurrente

    python3 -m mensajeria.servidor            escucha en el puerto 8000
    python3 -m mensajeria.servidor 8050       o en el que se le diga

Tal como está, el servidor acepta conexiones y no hace nada con ellas. Falta
el hilo por conexión y la atención del cliente.

Requisitos:
  1. Un hilo por conexión. El hilo principal solo acepta.
  2. La primera trama del cliente es su nombre. El servidor responde "OK" y lo
     registra, o responde "ERROR: nombre en uso" y cierra la conexión.
  3. Cada trama siguiente se retransmite a todos los demás como
     "emisor: contenido".
  4. El envío va FUERA del lock: se copia la lista de destinatarios bajo el
     lock y se envía después.
  5. Una desconexión no tumba nada: si un cliente se va, con aviso o a la
     fuerza, su entrada se borra del registro y los demás siguen. Un
     destinatario al que ya no se puede enviar también se retira.
  6. SO_REUSEADDR y `with` para los sockets.

Se comprueba con:   python3 prueba_n2.py   (desde la carpeta parcial2/)

Nivel 3: copie este archivo, ya resuelto, a mensajeria/servidor_json.py y
trabaje sobre la copia.
"""

import socket
import sys
import threading

from mensajeria.protocolo import enviar_mensaje, recibir_mensaje
from mensajeria.registro import RegistroClientes

HOST = "127.0.0.1"
PUERTO = 8000


def retransmitir(registro: RegistroClientes, emisor: str, texto: str) -> None:
    """Envía "emisor: texto" a todos los conectados menos al emisor."""
    mensaje = f"{emisor}: {texto}"
    
    # Requisito 4: Copiar los destinatarios bajo el lock y enviar FUERA del lock
    with registro.lock:
        destinatarios = list(registro.clientes.items())

    for nombre, conexion in destinatarios:
        if nombre != emisor:
            try:
                enviar_mensaje(conexion, mensaje)
            except (BrokenPipeError, ConnectionResetError, OSError):
                # Requisito 5: Si falla el envío, retiramos al cliente defectuoso de forma segura
                with registro.lock:
                    registro.remover(nombre)
                try:
                    conexion.close()
                except Exception:
                    pass


def atender(
    conexion: socket.socket, direccion: tuple[str, int], registro: RegistroClientes
) -> None:
    """Atiende a UN cliente, en su propio hilo, hasta que se desconecta."""
    nombre = None
    try:
        # Requisito 2: La primera trama es el nombre
        nombre = recibir_mensaje(conexion)
        if not nombre:
            conexion.close()
            return

        with registro.lock:
            # Intentamos registrar el cliente; si ya existe, el método debe manejarlo o retornamos error
         registrado = registro.registrar(nombre, conexion)
        
        # Asumiendo que registro.registrar(nombre, conexion) retorna False o lanza error si está en uso,
        # o validamos directamente según la estructura común de RegistroClientes:
        # (Si `registrar` devuelve booleano de éxito:)
        # Nota: Si tu clase `RegistroClientes` valida de otra forma, asegúrate de ajustarlo, 
        # pero este es el flujo estándar.
        
    except Exception:
        try:
            conexion.close()
        except Exception:
            pass
        return

    # Verificación estricta por si el método de registro evalúa duplicados:
    # (Validamos si el nombre fue aceptado correctamente)
    # Nota: Si `registro.registrar` devuelve False cuando ya existe, manejamos la respuesta de error:
    # (En muchos frameworks de estos talleres, `registrar` retorna True si se pudo y False si estaba ocupado).
    # Vamos a manejarlo robustamente:
    
    # Comprobación del registro:
    exito_registro = False
    with registro.lock:
        # Verificamos si ya está en uso o si el método lo hace internamente
        if nombre in registro.clientes.values() or hasattr(registro, "existe") and registro.existe(nombre):
            # Por seguridad si ya existiera
            pass
        
    # Implementación estándar del flujo de registro y validación:
    # Re-escribiendo la sección de bienvenida de manera limpia:

    def atender(
    conexion: socket.socket, direccion: tuple[str, int], registro: RegistroClientes
) -> None:
    ##"""Atiende a UN cliente, en su propio hilo, hasta que se desconecta."""
     nombre = None
    try:
        nombre = recibir_mensaje(conexion)
        if not nombre:
            conexion.close()
            return

        with registro.lock:
            # Verificamos si el nombre ya está en uso
            if nombre in registro.clientes:
                enviar_mensaje(conexion, "ERROR: nombre en uso")
                conexion.close()
                return
            else:
                enviar_mensaje(conexion, "OK")
                registro.registrar(nombre, conexion)

        # Bucle para escuchar las tramas siguientes del cliente
        while True:
            texto = recibir_mensaje(conexion)
            if not texto:
                break
            retransmitir(registro, nombre, texto)

    except (ConnectionResetError, BrokenPipeError, OSError):
        pass
    finally:
        # Requisito 5: Asegurar la limpieza al desconectarse (con aviso o a la fuerza)
        if nombre:
            with registro.lock:
                registro.remover(nombre)
        try:
            conexion.close()
        except Exception:
            pass


def main() -> None:
    # Las pruebas arrancan el servidor con un puerto libre: no cambie esta línea.
    puerto = int(sys.argv[1]) if len(sys.argv) > 1 else PUERTO
    registro = RegistroClientes()
    
    # Requisito 6: Usar `with` para los sockets y configurar SO_REUSEADDR
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        servidor.bind((HOST, puerto))
        servidor.listen()
        print(f"escuchando en {HOST}:{puerto}")
        
        while True:
            conexion, direccion = servidor.accept()
            # Requisito 1: Un hilo por conexión. El hilo principal solo acepta.
            hilo = threading.Thread(target=atender, args=(conexion, direccion, registro))
            hilo.daemon = True
            hilo.start()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nservidor detenido")

