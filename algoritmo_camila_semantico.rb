# ==========================================================
# PRUEBA DE ANÁLISIS SEMÁNTICO
# Reglas 1 y 4
# ==========================================================

puts "=== Inicio del programa ==="

# ----------------------------------------------------------
# Declaraciones correctas
# ----------------------------------------------------------

a = 10
b = 20
c = a + b

puts c

# ----------------------------------------------------------
# REGLA 1
# Variable redeclarada
# ----------------------------------------------------------

x = 100
y = 50

x = 200

puts x

# ----------------------------------------------------------
# Función correcta
# ----------------------------------------------------------

def multiplicar(num1, num2)

    resultado = num1 * num2

    return resultado

end

multiplicar(5,4)

# ----------------------------------------------------------
# REGLA 4
# Parámetros duplicados
# ----------------------------------------------------------

def promedio(valor1, valor2, valor1)

    suma = valor1 + valor2

    return suma / 2

end

puts "=== Fin del programa ==="