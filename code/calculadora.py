def suma(valor1, valor2):
    return valor1 + valor2

def resta(valor1, valor2):
    return valor1 - valor2

def multiplicacion(valor1, valor2):
    return valor1 * valor2

def division(valor1, valor2):
    if valor2 != 0:
        return valor1 / valor2
    else:
        return "Error: Division by zero is not allowed."

resultado_suma = suma(5, 3)
resultado_resta = resta(5, 3)
resultado_multiplicacion = multiplicacion(5, 3)
resultado_division = division(5, 3)

print(f"Resultado de la suma: {resultado_suma}")
print(f"Resultado de la resta: {resultado_resta}")
print(f"Resultado de la multiplicación: {resultado_multiplicacion}")
print(f"Resultado de la división: {resultado_division}")