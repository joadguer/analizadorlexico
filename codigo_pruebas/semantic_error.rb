# ==========================================
# 4. ERROR SEMANTICO
# ==========================================

# Error Semantico 1 (Regla Josue): Reasignacion de constante
PI = 3.14
PI = 3.1416

# Error Semantico 2 (Regla Josue): Uso de variable no declarada
puts variable_fantasma

# Error Semantico 3: Retorno fuera de una funcion
return 100

def procesar_datos(a, b)
    resultado = a + b
    return resultado
end

# Error Semantico 4: Numero incorrecto de argumentos (espera 2, recibe 1)
calculo = procesar_datos(50)