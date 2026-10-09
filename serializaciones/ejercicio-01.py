import pickle

mensaje ={
    "emisor": "Juan",
    "contenido": "hola, clase",
    "etiquetas":("a","b")
}

datos = pickle.dumps(mensaje)

print(datos)
print("\n")

copia = pickle.loads(datos)
print(copia)
##sirve para realizar peticiones cortas.
##es tamnien una forma de serializar objetos en Python,
# permitiendo convertirlos en un formato que se pueda almacenar o transmitir y luego reconstruirlos.