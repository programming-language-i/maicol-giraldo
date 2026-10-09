import json

mensaje ={
    "emisor": "Juan",
    "contenido": "hola, clase",
    "etiquetas":("a","b")
}

texto = json.dumps(mensaje, ensure_ascii=False)##ensure desactiva caracteres expeciales, como acentos,
##para que se muestren correctamente en la salida.


copia = json.loads(texto)
print(f"Texto cargado: {copia}")

print("\n")
print(f"son iguales: {mensaje == copia}")##esta direccion sirve para comparar si los dos diccionarios son iguales,
##devolviendo True o False.

